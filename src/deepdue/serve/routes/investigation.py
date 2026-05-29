import time
import logging
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse

from deepdue.serve.templates_env import templates

logger = logging.getLogger(__name__)

router = APIRouter()

_SKIP_NODES = {"LangGraph", "__start__", "should_continue", "route_extraction_by_type", "dequeue_next", "route"}

NODE_LABELS = {
    "init": "init",
    "get_company": "company_lookup",
    "officer_extraction": "officer_extraction",
    "filing_history": "filing_history",
    "pscs_extraction": "psc_extraction",
    "enqueue_company": "enqueue_company",
    "get_officer_appointments": "officer_appointments",
    "enqueue_officer": "enqueue_officer",
    "pattern_detection": "pattern_detection",
    "report_summary": "report_summary",
}


def _get_message(node: str, input_state) -> str:
    if hasattr(input_state, "model_dump"):
        input_state = input_state.model_dump()
    if not isinstance(input_state, dict):
        return "started"

    entity_id = input_state.get("current_entity_id") or ""
    target = input_state.get("target_company_number") or ""
    to_investigate = input_state.get("entities_to_investigate") or []
    visited = input_state.get("entities_visited") or []

    short_id = entity_id.split("/")[-1] if entity_id else ""

    visited_ids = set()
    for e in visited:
        visited_ids.add(e.id if hasattr(e, "id") else e.get("id", ""))

    remaining = sum(
        1 for e in to_investigate
        if (e.id if hasattr(e, "id") else e.get("id", "")) not in visited_ids
    )

    return {
        "init": f"seeding traversal from {target}",
        "get_company": f"fetching profile → {entity_id or target}",
        "officer_extraction": f"extracting officers → {entity_id or target}",
        "filing_history": f"fetching filing history → {entity_id or target}",
        "pscs_extraction": f"fetching PSCs → {entity_id or target}",
        "enqueue_company": f"{remaining} entities queued for traversal",
        "get_officer_appointments": f"fetching appointments → {short_id}",
        "enqueue_officer": f"{remaining} entities queued for traversal",
        "pattern_detection": f"analysing {len(to_investigate)} collected entities",
        "report_summary": "generating investigation summary",
    }.get(node, "started")


@router.get("/investigation/init", response_class=HTMLResponse)
async def investigation_init(request: Request, company_number: str):
    return templates.TemplateResponse(
        request,
        "partials/_investigation_panel.html",
        {"company_number": company_number},
    )


@router.get("/investigation/stream")
async def investigation_stream(request: Request, company_number: str):
    graph = request.app.state.investigation_graph
    start_time = time.time()

    async def event_generator():
        try:
            async for event in graph.astream_events(
                {"target_company_number": company_number, "max_depth": 1},
                config={"recursion_limit": 200},
                version="v2",
            ):
                if await request.is_disconnected():
                    break

                kind = event["event"]
                node = event.get("name", "")

                if kind == "on_chain_start" and node not in _SKIP_NODES:
                    logger.debug("SSE node: %r", node)
                    input_state = event.get("data", {}).get("input") or {}
                    elapsed = round(time.time() - start_time, 1)
                    html = templates.env.get_template("partials/_log_line.html").render(
                        node_label=NODE_LABELS.get(node, node),
                        message=_get_message(node, input_state),
                        timestamp=elapsed,
                    )
                    yield {"event": "status", "data": html}

                elif kind == "on_chain_end" and node == "LangGraph":
                    output = event["data"].get("output", {})
                    elapsed = round(time.time() - start_time, 1)
                    html = templates.env.get_template("partials/_result.html").render(
                        flags=output.get("flags") or [],
                        entities_visited=output.get("entities_visited") or [],
                        depth=output.get("depth", 0),
                        elapsed=elapsed,
                        company_number=company_number,
                    )
                    yield {"event": "result", "data": html}

                    if not output.get("report"):
                        elapsed = round(time.time() - start_time, 1)
                        complete_html = templates.env.get_template("partials/_complete.html").render(
                            company_number=company_number,
                            elapsed=elapsed,
                        )
                        yield {"event": "complete", "data": complete_html}
                        yield {"event": "done", "data": ""}

                elif kind == "on_chain_end" and node == "report_summary":
                    output = event["data"].get("output", {})
                    elapsed = round(time.time() - start_time, 1)
                    html = templates.env.get_template("partials/_report.html").render(
                        report=output.get("report", ""),
                    )
                    yield {"event": "report", "data": html}

                    complete_html = templates.env.get_template("partials/_complete.html").render(
                        company_number=company_number,
                        elapsed=elapsed,
                    )
                    yield {"event": "complete", "data": complete_html}
                    yield {"event": "done", "data": ""}

        except Exception as e:
            logger.exception("SSE investigation error")
            html = templates.env.get_template("partials/_error.html").render(message=str(e))
            yield {"event": "error", "data": html}
            error_html = templates.env.get_template("partials/_complete.html").render(
                company_number=company_number,
                elapsed=round(time.time() - start_time, 1),
                error=True,
            )
            yield {"event": "complete", "data": error_html}
            yield {"event": "done", "data": ""}

    return EventSourceResponse(event_generator())