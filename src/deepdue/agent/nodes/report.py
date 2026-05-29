import json
import logging

from langsmith import get_current_run_tree
from deepdue.agent.state import InvestigationState
from deepdue.llm import LLMClient

SYSTEM_PROMPT = """
You are a corporate fraud investigator writing a summary of findings from an automated Companies House traversal.

You will be given a JSON array of flags raised during the investigation. Each flag has a pattern type, affected entity IDs, confidence and severity scores, and reasoning.

Write a concise investigation summary using markdown. Use the following structure:

## Overview
One or two sentences stating how many entities were flagged and the dominant pattern types found.

## Findings
A short paragraph for each distinct pattern type found, naming the most significant entities and what the data suggests. Translate confidence and severity scores into plain language — do not repeat the raw numbers.

## Risk Assessment
A closing sentence stating the overall risk level and whether deeper manual investigation is warranted.

Rules:
- Use ## for section headers, plain paragraphs for body text
- Do not use HTML tags
- Do not use bullet points
- Do not invent findings beyond what the flags contain
- If no flags are provided, state that no anomalies were detected in the traversal scope
"""

logger = logging.getLogger(__name__)

def make_report_summary_node(llm: LLMClient):
    async def node(state: InvestigationState):
        flags = state['flags']

        run = get_current_run_tree()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}, 
            {"role": "user", "content": json.dumps([f.model_dump() for f in flags])}
        ]

        response = await llm(messages, 1.0, {"parent_run_id": str(run.id) if run else None})

        return {"report": response}

    return node