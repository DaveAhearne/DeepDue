from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_filing_history_extraction_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        company_number = state["current_entity_id"]

        filing_history = await client.GetCompanyFilingHistory(company_number)

        return {"filing_histories": {company_number: filing_history}}

    return node
