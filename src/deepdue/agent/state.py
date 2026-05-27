import operator
from typing import TypedDict, Annotated
from deepdue import models
from pydantic import BaseModel, Field

from deepdue.enums import InvestigationEntityType

def merge_flags(existing: list[models.Flag], new: list[models.Flag]) -> list[models.Flag]:
    result = {frozenset(f.entity_ids): f for f in existing}
    
    for flag in new:
        key = frozenset(flag.entity_ids)
        if key in result:
            existing_flag = result[key]
            result[key] = existing_flag.model_copy(update={
                "reasoning": existing_flag.reasoning + flag.reasoning,
                "evidence": existing_flag.evidence | flag.evidence,
                "confidence": max(existing_flag.confidence, flag.confidence),
                "severity": max(existing_flag.severity, flag.severity),
                "scale": max(existing_flag.scale, flag.scale),
            })
        else:
            result[key] = flag
    
    return list(result.values())

class InputState(BaseModel):
    target_company_number: str
    max_depth: int = Field(default=2)

class InvestigationState(TypedDict):
    target_company_number: str

    current_entity_id: str
    current_entity_type: InvestigationEntityType

    companies: Annotated[dict[str, models.CompanyProfile], operator.or_]
    officers: Annotated[dict[str, models.CompanyOfficers], operator.or_]
    appointments: Annotated[dict[str, models.OfficerAppointments], operator.or_]
    pscs: Annotated[dict[str, models.CompanyPSCs], operator.or_]
    psc_statements: Annotated[dict[str, models.CompanyPSCStatements], operator.or_]
    filing_histories: Annotated[dict[str, models.CompanyFilingHistory], operator.or_]

    entities_to_investigate: Annotated[list[models.InvestigationEntity], operator.add]
    entities_visited: Annotated[list[models.InvestigationEntity], operator.add]
    max_depth: int

    flags: Annotated[list[models.Flag], merge_flags]
    report: str | None