from pydantic import BaseModel

class InvestigationRequest(BaseModel):
    company_number: str