from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_officer_extraction_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        company_number = state["current_entity_id"]

        company_officers = await client.GetCompanyOfficers(company_number)

        return {"officers": {company_number: company_officers}}

    return node
