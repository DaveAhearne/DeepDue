from datetime import datetime
from pydantic import BaseModel, Field
from deepdue import enums

class CompanyProfilePreviousCompanyNames(BaseModel):
    ceased_on: datetime | None = None
    effective_from: datetime | None = None
    name: str | None = None

class CompanyProfileLinks(BaseModel):
    charges: str | None = None
    exemptions: str | None = None
    filing_history: str | None = None
    insolvency: str | None = None
    officers: str | None = None
    overseas: str | None = None
    persons_with_significant_control: str | None = None
    persons_with_significant_control_statements: str | None = None
    registers: str | None = None
    self: str | None = None
    uk_establishments: str | None = Field(None, alias="uk-establishments")

class CompanyProfileConfirmationStatement(BaseModel):
    last_made_up_to: datetime | None = None
    next_due: datetime | None = None
    next_made_up_to: datetime | None = None
    overdue: bool | None = None

class CompanyProfileRegisteredOfficeAddress(BaseModel):
    address_line_1: str | None = None
    address_line_2: str | None = None
    care_of: str | None = None
    country: str | None = None
    locality: str | None = None
    po_box: str | None = None
    postal_code: str | None = None
    premises: str | None = None
    region: str | None = None

class CompanyProfileLastAccounts(BaseModel):
    made_up_to: datetime | None = None
    period_end_on: datetime | None = None
    period_start_on: datetime | None = None
    type: enums.CompanyProfileAccountFilingType | None = None

class CompanyProfileAccounts(BaseModel):
    last_accounts: CompanyProfileLastAccounts | None = None

class CompanyProfile(BaseModel):
    company_number:str
    company_name:str
    company_status:enums.CompanyStatusType | None = None
    company_status_detail:enums.CompanyStatusDetailType | None = None
    type:enums.CompanyProfileType | None = None
    date_of_creation:datetime | None = None
    date_of_cessation:datetime | None = None
    registered_office_address:CompanyProfileRegisteredOfficeAddress | None = None
    accounts: CompanyProfileAccounts | None = None
    confirmation_statement :CompanyProfileConfirmationStatement | None = None
    previous_company_names: list[CompanyProfilePreviousCompanyNames] | None = None
    sic_codes: list[str] | None = None
    links: CompanyProfileLinks | None = None
