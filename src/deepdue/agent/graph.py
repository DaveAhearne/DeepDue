from langgraph.graph import StateGraph, START, END
from deepdue.agent.state import InvestigationState
from deepdue.agent.nodes import company_lookup, officer_extraction, psc_extraction, filing_history
from deepdue.data.companies_house import CompaniesHouseClient

def build_graph(ch_client: CompaniesHouseClient):
    company_lookup_node = company_lookup.make_company_lookup_node(ch_client)
    officer_extraction_node = officer_extraction.make_officer_extraction_node(ch_client)
    pscs_extraction_node = psc_extraction.make_psc_extraction_node(ch_client)
    filing_history_node = filing_history.make_filing_history_extraction_node(ch_client)

    builder = StateGraph(InvestigationState)
    builder.add_edge(START, "get_company")
    
    builder.add_node("get_company", company_lookup_node)
    builder.add_edge("get_company", "officer_extraction")
    
    builder.add_node("officer_extraction", officer_extraction_node)
    builder.add_edge("officer_extraction", "filing_history")
    
    builder.add_node("filing_history", filing_history_node)
    builder.add_edge("filing_history", "pscs_extraction")

    builder.add_node("pscs_extraction", pscs_extraction_node)
    builder.add_edge("pscs_extraction", END)

    return builder.compile()