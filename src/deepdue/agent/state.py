import operator
from typing import TypedDict, Annotated
from deepdue import models
from pydantic import BaseModel, Field

class InputState(BaseModel):
    target_company_number: str
    target_company_name: str = ""
    max_depth: int = Field(default=3)

class InvestigationState(TypedDict):
    target_company_number: str
    target_company_name: str

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