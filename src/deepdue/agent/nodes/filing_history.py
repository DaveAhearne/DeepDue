from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_filing_history_extraction_node(client: CompaniesHouseClient):
    async def filing_history_extraction(state: InvestigationState):
        company_number = state["target_company_number"]

        filing_history = await client.GetCompanyFilingHistory(company_number)

        return {"filing_histories": {**state["filing_histories"], company_number: filing_history}}

    return filing_history_extraction
