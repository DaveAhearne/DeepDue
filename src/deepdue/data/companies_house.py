import httpx
from deepdue import models

class CompaniesHouseClient:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.company-information.service.gov.uk",
            auth=(api_key, ""),
        )
    
    async def GetCompanyProfile(self, company_number: str) -> models.CompanyProfile:
        res = await self.client.get(f"/company/{company_number}")
        return models.CompanyProfile.model_validate(res.json())
    
    async def GetCompanyOfficers(self, company_number: str) -> models.CompanyOfficers:
        res = await self.client.get(f"/company/{company_number}/officers")
        return models.CompanyOfficers.model_validate(res.json())
    
    async def GetCompanyPSCs(self, company_number: str) -> models.CompanyPSCs:
        res = await self.client.get(f"/company/{company_number}/persons-with-significant-control")
        return models.CompanyPSCs.model_validate(res.json())
    
    async def GetCompanyFilingHistory(self, company_number: str) -> models.CompanyFilingHistory:
        res = await self.client.get(f"/company/{company_number}/filing-history")
        return models.CompanyFilingHistory.model_validate(res.json())
    
    async def SearchCompanies(self, term: str) -> models.CompanySearchResults:
        res = await self.client.get(f"/search/companies?q={term}")
        return models.CompanySearchResults.model_validate(res.json())