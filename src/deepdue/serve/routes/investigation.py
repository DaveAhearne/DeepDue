import logging
from fastapi import APIRouter, HTTPException, Request

from deepdue.serve.schema import InvestigationRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/investigation")
async def request_investigation(request: Request, payload: InvestigationRequest):
    logger.info("HIT: /investigation")
    
    graph = request.app.state.investigation_graph
    
    try:
        result = await graph.ainvoke({
            "target_company_number": payload.company_number,
            "target_company_name": "",
            "companies": {},
            "officers": {},
            "pscs": {},
            "psc_statements": {},
            "filing_histories": {},
            "entities_to_investigate": [],
            "entities_visited": set(),
            "depth": 0,
            "max_depth": 3,
            "flags": [],
            "report": None
        })

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )