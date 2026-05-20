from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_psc_extraction_node(client: CompaniesHouseClient):
    async def psc_extraction(state: InvestigationState):
        updated_pscs = state["pscs"]
        updated_psc_statements = state["psc_statements"]
        
        company_number = state["target_company_number"]
        company_profile = state["companies"][company_number]
        
        if(company_profile.links and company_profile.links.persons_with_significant_control):
            pscs = await client.GetCompanyPSCs(company_number)
            updated_pscs = {**state["pscs"], company_number: pscs}

        if(company_profile.links and company_profile.links.persons_with_significant_control_statements):
            psc_statements = await client.GetCompanyPSCStatements(company_number)
            updated_psc_statements = {**state["psc_statements"], company_number: psc_statements}

        return {"pscs": updated_pscs, "psc_statements": updated_psc_statements}

    return psc_extraction
