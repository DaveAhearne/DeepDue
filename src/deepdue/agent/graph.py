import os
from langgraph.graph import StateGraph, START, END
from deepdue.agent.state import InputState, InvestigationState
from deepdue.agent.nodes import init, route_lookup_by_type ,company_lookup, dequeue_next, officer_extraction, psc_extraction, filing_history, entity_enqueue, route_entity_lookups, should_continue, officer_appointment_extraction
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
    officer_appointment_extraction_node = officer_appointment_extraction.make_officer_appointment_extraction_node(ch_client)

    should_continue_node = should_continue.node
    entity_enqueue_node = entity_enqueue.node

    builder = StateGraph(InvestigationState, input=InputState)

    builder.add_edge(START, "init")
    builder.add_node("init", init.node)
    builder.add_edge("init", "route_extraction_by_type")
    
    builder.add_node("route_extraction_by_type", route_lookup_by_type.node)
    builder.add_conditional_edges(
        "route_extraction_by_type",
        route_lookup_by_type.route,
        {
            "get_company": "get_company",
            "get_officer_appointments": "get_officer_appointments",
        }
    )
    
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
            "dequeue_next":"dequeue_next",
            "end": END
        }
    )

    builder.add_node("get_officer_appointments", officer_appointment_extraction_node)
    builder.add_edge("get_officer_appointments", "entity_enqueue")

    builder.add_node("dequeue_next", dequeue_next.node)
    builder.add_edge("dequeue_next", "route_extraction_by_type")
    
    return builder.compile()