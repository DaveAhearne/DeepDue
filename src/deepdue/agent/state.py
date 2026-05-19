from typing import TypedDict
from deepdue import models

class InvestigationState(TypedDict):
    target_company_number: str
    target_company_name: str

    companies: dict[str, models.CompanyProfile]
    officers: dict[str, models.CompanyOfficers]
    pscs: dict[str, models.CompanyPSCs]
    filing_histories: dict[str, models.CompanyFilingHistory]

    entities_to_investigate: list[str]
    entities_visited: list[str]
    depth: int
    max_depth: int

    flags: list[str]
    report: str | None