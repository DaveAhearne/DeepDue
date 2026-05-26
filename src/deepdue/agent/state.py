import operator
from typing import TypedDict, Annotated
from deepdue import models
from pydantic import BaseModel, Field

from deepdue.enums import InvestigationEntityType

class InputState(BaseModel):
    current_entity_id: str
    current_entity_type: InvestigationEntityType = InvestigationEntityType.COMPANY
    max_depth: int = Field(default=2)

class InvestigationState(TypedDict):
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
    depth: int
    max_depth: int

    flags: Annotated[list[str], operator.add]
    report: str | None