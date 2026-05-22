from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_psc_extraction_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        result = {}

        company_number = state["current_entity_id"]
        company_profile = state["companies"][company_number]
        
        if(company_profile.links and company_profile.links.persons_with_significant_control):
            pscs = await client.GetCompanyPSCs(company_number)
            result["pscs"] = {company_number: pscs}

        if(company_profile.links and company_profile.links.persons_with_significant_control_statements):
            psc_statements = await client.GetCompanyPSCStatements(company_number)
            result["psc_statements"] = {company_number: psc_statements}

        return result

    return node
