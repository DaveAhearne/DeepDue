import httpx
from deepdue import models

class CompaniesHouseClient:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(
            base_url="https://api.company-information.service.gov.uk",
            auth=(api_key, ""),
        )
    
    async def GetCompanyProfile(self, company_number: str) -> models.CompanyProfile:
        """Fetch the full profile for a company by its registration number.
        Returns status, address, SIC codes, incorporation and cessation dates,
        and filing overdue flags."""
        res = await self.client.get(f"/company/{company_number}")
        res.raise_for_status()
        return models.CompanyProfile.model_validate(res.json())
    
    async def GetCompanyOfficers(self, company_number: str) -> models.CompanyOfficers:
        """Fetch the list of current and resigned officers for a company.
        Returns appointment and resignation dates, roles, and links to each
        officer's full appointments list for graph traversal."""
        res = await self.client.get(f"/company/{company_number}/officers")
        res.raise_for_status()
        return models.CompanyOfficers.model_validate(res.json())
    
    async def GetCompanyPSCs(self, company_number: str) -> models.CompanyPSCs:
        """Fetch the persons with significant control for a company.
        Returns natural persons and corporate entities, natures of control,
        and identification details for corporate PSCs to enable ownership
        chain traversal."""
        res = await self.client.get(f"/company/{company_number}/persons-with-significant-control")
        res.raise_for_status()
        return models.CompanyPSCs.model_validate(res.json())
    
    async def GetCompanyPSCStatements(self, company_number: str) -> models.CompanyPSCStatements:
        """Fetch the PSC statements for a company.
        Returned instead of or alongside PSC records when no registrable person
        with significant control has been identified. Each statement carries a
        coded reason from the Companies House enumeration — for example, that
        steps to find a PSC are not yet complete, or that a PSC exists but has
        not been confirmed. Presence of statements is itself a weak signal for
        layered or obscured ownership."""
        res = await self.client.get(f"/company/{company_number}/persons-with-significant-control-statements")
        res.raise_for_status()
        return models.CompanyPSCStatements.model_validate(res.json())
    
    async def GetCompanyFilingHistory(self, company_number: str) -> models.CompanyFilingHistory:
        """Fetch the filing history for a company.
        Returns filed document categories, types, and dates. Useful for
        detecting timeline irregularities such as overdue accounts, dissolution
        filings, and gazette notices."""
        res = await self.client.get(f"/company/{company_number}/filing-history")
        res.raise_for_status()
        return models.CompanyFilingHistory.model_validate(res.json())
    
    async def SearchCompanies(self, term: str) -> models.CompanySearchResults:
        """Search for companies by name or number.
        Returns a ranked list of matching companies with status, type, and
        dates. Primarily used to resolve a company name to a registration
        number before structured traversal."""
        res = await self.client.get(f"/search/companies?q={term}")
        res.raise_for_status()
        return models.CompanySearchResults.model_validate(res.json())
    
    async def SearchOfficers(self, term: str) -> models.OfficerSearchResults:
        """Search for officers by name.
        Returns matching officers with appointment counts and date of birth.
        Appointment count provides an early signal for director network
        anomalies before any further traversal."""
        res = await self.client.get(f"/search/officers?q={term}")
        res.raise_for_status()
        return models.OfficerSearchResults.model_validate(res.json())