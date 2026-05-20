from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_officer_extraction_node(client: CompaniesHouseClient):
    async def officer_extraction(state: InvestigationState):
        company_number = state["target_company_number"]

        company_officers = await client.GetCompanyOfficers(company_number)

        return {"officers": {company_number: company_officers}}

    return officer_extraction
