import os
from langgraph.graph import StateGraph, START, END
from deepdue.agent.state import InvestigationState
from deepdue.agent.nodes import company_lookup, officer_extraction, psc_extraction, filing_history, entity_enqueue, should_continue, dequeue_next, advance_traversal
from deepdue.data.companies_house import CompaniesHouseClient

# No dep version for local debugging with langgraph dev
def create_graph():
    from dotenv import load_dotenv
    load_dotenv()
    client = CompaniesHouseClient(os.environ["CH_API_KEY"])
    return build_graph(client)

def build_graph(ch_client: CompaniesHouseClient):
    company_lookup_node = company_lookup.make_company_lookup_node(ch_client)
    officer_extraction_node = officer_extraction.make_officer_extraction_node(ch_client)
    pscs_extraction_node = psc_extraction.make_psc_extraction_node(ch_client)
    filing_history_node = filing_history.make_filing_history_extraction_node(ch_client)
    
    should_continue_node = should_continue.node
    entity_enqueue_node = entity_enqueue.node

    builder = StateGraph(InvestigationState)
    builder.add_edge(START, "get_company")
    
    builder.add_node("get_company", company_lookup_node)
    builder.add_edge("get_company", "officer_extraction")
    
    builder.add_node("officer_extraction", officer_extraction_node)
    builder.add_edge("officer_extraction", "filing_history")
    
    builder.add_node("filing_history", filing_history_node)
    builder.add_edge("filing_history", "pscs_extraction")

    builder.add_node("pscs_extraction", pscs_extraction_node)
    builder.add_edge("pscs_extraction", "entity_enqueue")

    builder.add_node("entity_enqueue", entity_enqueue_node)
    builder.add_conditional_edges(
        "entity_enqueue", 
        should_continue_node,
        {
            "advance_traversal":"advance_traversal",
            "end": END
        }
    )

    builder.add_node("advance_traversal", advance_traversal.node)
    builder.add_edge("advance_traversal", "dequeue_next")

    builder.add_node("dequeue_next", dequeue_next.node)
    builder.add_edge("dequeue_next", "get_company")
    
    return builder.compile()