import json

from langsmith import get_current_run_tree
from deepdue import models
from deepdue.agent.state import InvestigationState
from deepdue.llm import LLMClient

SYSTEM_PROMPT = """
You are a corporate fraud investigator analysing Companies House data.

You will be given a JSON object mapping officer appointment identifiers to their total number of company appointments across the UK register.

Identify any officers whose appointment count is anomalously high. Most legitimate directors hold between 1 and 5 appointments. Counts above 10 are worth examining. Counts above 25 are unusual and warrant scrutiny. Counts above 50 are strongly anomalous and may indicate a nominee director, a shell company network, or systematic fraud. Only flag officers where the count is genuinely suspicious in context — do not flag every officer above the minimum threshold.

You must respond with a raw JSON array only. No explanation, no preamble, no markdown, no code fences. If no anomalies are found return an empty array.

Each flag in the array must follow this exact structure:
{
    "pattern_type": "director-network-anomaly",
    "entity_ids": ["<appointment_identifier>"],
    "confidence": 0.0,
    "severity": 0.0,
    "scale": 0.0,
    "reasoning": ["<your reasoning as a single string inside an array>"],
    "evidence": { "appointment_count": 0 }
}

confidence: how certain you are this is genuinely anomalous, not just a prolific legitimate director
severity: how serious this pattern would be if confirmed as fraudulent
scale: proportion of the overall network implicated, 0.0 to 1.0
reasoning: a single string explaining specifically why this count is suspicious in context
"""

MIN_APPOINTMENTS = 10

def make_pattern_detection_node(llm: LLMClient):
    async def node(state: InvestigationState):
        officers = state['officers']
        appointments = state['appointments']

        if not appointments:
            return {"flags": []}

        officer_appointment_links = [o.links.officer.appointments for (_, co) in officers.items() 
         for o in co.items 
         if o.links and o.links.officer and o.links.officer.appointments]

        officer_appointments = {
            ol: appointments[ol].total_results 
            for ol in officer_appointment_links 
            if ol in appointments 
            and appointments[ol].total_results is not None
            and appointments[ol].total_results >= MIN_APPOINTMENTS
        }

        run = get_current_run_tree()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}, 
            {"role": "user", "content": f"{json.dumps(officer_appointments)}"}
        ]

        response = await llm(messages, 1.0, {"parent_run_id": str(run.id) if run else None})

        try:
            response = response[response.index("["):response.rindex("]") + 1]

            parsed = json.loads(response)
        except json.JSONDecodeError as e:
            run = get_current_run_tree()
            if run:
                run.metadata["raw_llm_response"] = response
                run.patch()
            raise

        for f in parsed:
            if isinstance(f.get("reasoning"), str):
                f["reasoning"] = [f["reasoning"]]

        return {"flags": [models.Flag.model_validate(f) for f in parsed]}

    return node