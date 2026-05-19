import httpx
from deepdue import models

class CompaniesHouseClient:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.company-information.service.gov.uk",
            auth=(api_key, ""),
        )
    
    async def GetCompanyProfile(self, company_number: str):
        res = await self.client.get(f"/company/{company_number}")
        return models.CompanyProfile.model_validate(res.json())