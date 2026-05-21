from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_company_lookup_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        company_number = state["target_company_number"]

        company_profile = await client.GetCompanyProfile(company_number)

        return {"companies": {company_number: company_profile}}

    return node
