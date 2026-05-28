import asyncio

import httpx
from deepdue import models
from deepdue.data.cache import QdrantCHCache
from deepdue.enums import CacheEntityType

class CompaniesHouseClient:
    def __init__(self, api_key: str, cache: QdrantCHCache, calls_per_second: float = 2):
        self.client = httpx.AsyncClient(
            base_url="https://api.company-information.service.gov.uk",
            auth=(api_key, ""),
        )
        self.cache = cache
        self._delay = 1.0 / calls_per_second
    
    async def _get(self, path: str):
        await asyncio.sleep(self._delay)
        res = await self.client.get(path)
        res.raise_for_status()
        return res
    
    async def GetCompanyProfile(self, company_number: str) -> models.CompanyProfile:
        """Fetch the full profile for a company by its registration number.
        Returns status, address, SIC codes, incorporation and cessation dates,
        and filing overdue flags."""
        
        cache_res = self.cache.get(company_number, CacheEntityType.COMPANY)
        if cache_res is not None:
            return models.CompanyProfile.model_validate(cache_res)

        res = await self._get(f"/company/{company_number}")
        valid_res = models.CompanyProfile.model_validate(res.json())

        self.cache.set(company_number, CacheEntityType.COMPANY, res.json())
        return valid_res
    
    async def GetCompanyOfficers(self, company_number: str) -> models.CompanyOfficers:
        """Fetch the list of current and resigned officers for a company.
        Returns appointment and resignation dates, roles, and links to each
        officer's full appointments list for graph traversal."""
        cache_res = self.cache.get(company_number, CacheEntityType.OFFICER)
        if cache_res is not None:
            return models.CompanyOfficers.model_validate(cache_res)

        res = await self._get(f"/company/{company_number}/officers")
        valid_res = models.CompanyOfficers.model_validate(res.json())

        self.cache.set(company_number, CacheEntityType.OFFICER, res.json())
        return valid_res

    async def GetOfficerAppointments(self, appointments_path: str) -> models.OfficerAppointments:
        """Fetch all company appointments for an officer.
        The appointments_path comes from officer.links.officer.appointments
        (e.g. /officers/abc123/appointments). Returns each company the officer
        is or was appointed to — the primary mechanism for graph traversal
        from a director node outward to related companies."""
        cache_res = self.cache.get(appointments_path, CacheEntityType.OFFICER)
        if cache_res is not None:
            return models.OfficerAppointments.model_validate(cache_res)
        res = await self._get(appointments_path)
        self.cache.set(appointments_path, CacheEntityType.OFFICER, res.json())
        return models.OfficerAppointments.model_validate(res.json())

    async def GetCompanyPSCs(self, company_number: str) -> models.CompanyPSCs:
        """Fetch the persons with significant control for a company.
        Returns natural persons and corporate entities, natures of control,
        and identification details for corporate PSCs to enable ownership
        chain traversal."""
        cache_res = self.cache.get(company_number, CacheEntityType.PSC)
        if cache_res is not None:
            return models.CompanyPSCs.model_validate(cache_res)
        res = await self._get(f"/company/{company_number}/persons-with-significant-control")
        self.cache.set(company_number, CacheEntityType.PSC, res.json())
        return models.CompanyPSCs.model_validate(res.json())

    async def GetCompanyPSCStatements(self, company_number: str) -> models.CompanyPSCStatements:
        """Fetch the PSC statements for a company.
        Returned instead of or alongside PSC records when no registrable person
        with significant control has been identified. Each statement carries a
        coded reason from the Companies House enumeration — for example, that
        steps to find a PSC are not yet complete, or that a PSC exists but has
        not been confirmed. Presence of statements is itself a weak signal for
        layered or obscured ownership."""
        cache_res = self.cache.get(company_number, CacheEntityType.PSC_STATEMENT)
        if cache_res is not None:
            return models.CompanyPSCStatements.model_validate(cache_res)
        res = await self._get(f"/company/{company_number}/persons-with-significant-control-statements")
        self.cache.set(company_number, CacheEntityType.PSC_STATEMENT, res.json())
        return models.CompanyPSCStatements.model_validate(res.json())

    async def GetCompanyFilingHistory(self, company_number: str) -> models.CompanyFilingHistory:
        """Fetch the filing history for a company.
        Returns filed document categories, types, and dates. Useful for
        detecting timeline irregularities such as overdue accounts, dissolution
        filings, and gazette notices."""
        cache_res = self.cache.get(company_number, CacheEntityType.FILING_HISTORY)
        if cache_res is not None:
            return models.CompanyFilingHistory.model_validate(cache_res)
        res = await self._get(f"/company/{company_number}/filing-history")
        self.cache.set(company_number, CacheEntityType.FILING_HISTORY, res.json())
        return models.CompanyFilingHistory.model_validate(res.json())
    
    async def SearchCompanies(self, term: str) -> models.CompanySearchResults:
        """Search for companies by name or number.
        Returns a ranked list of matching companies with status, type, and
        dates. Primarily used to resolve a company name to a registration
        number before structured traversal."""
        res = await self._get(f"/search/companies?q={term}")
        return models.CompanySearchResults.model_validate(res.json())
    
    async def SearchOfficers(self, term: str) -> models.OfficerSearchResults:
        """Search for officers by name.
        Returns matching officers with appointment counts and date of birth.
        Appointment count provides an early signal for director network
        anomalies before any further traversal."""
        res = await self._get(f"/search/officers?q={term}")
        return models.OfficerSearchResults.model_validate(res.json())