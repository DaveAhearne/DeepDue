import os
from langgraph.graph import StateGraph, START, END
from deepdue.agent.state import InputState, InvestigationState
from deepdue.agent.nodes import enqueue_company_details, enqueue_officer_details, init, route_lookup_by_type ,company_lookup, dequeue_next, officer_extraction, psc_extraction, filing_history, should_continue, officer_appointment_extraction, pattern_detection
from deepdue.data.companies_house import CompaniesHouseClient
from deepdue.llm import LLMClients, make_llm_clients
from dotenv import load_dotenv

# No dep version for local debugging with langgraph dev
def create_graph():
    load_dotenv()
    
    llm_clients = make_llm_clients()
    client = CompaniesHouseClient(os.environ["CH_API_KEY"], llm_clients)
    
    return build_graph(client, llm_clients)

def build_graph(ch_client: CompaniesHouseClient, llm_clients: LLMClients):
    
    company_lookup_node = company_lookup.make_company_lookup_node(ch_client)
    officer_extraction_node = officer_extraction.make_officer_extraction_node(ch_client)
    pscs_extraction_node = psc_extraction.make_psc_extraction_node(ch_client)
    filing_history_node = filing_history.make_filing_history_extraction_node(ch_client)
    officer_appointment_extraction_node = officer_appointment_extraction.make_officer_appointment_extraction_node(ch_client)

    pattern_detection_node = pattern_detection.make_pattern_detection_node(llm_clients["reasoning"])

    should_continue_node = should_continue.node
    enqueue_officer_node = enqueue_officer_details.node
    enqueue_company_node = enqueue_company_details.node

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
    builder.add_edge("pscs_extraction", "enqueue_company")

    builder.add_node("enqueue_company", enqueue_company_node)
    builder.add_edge("enqueue_company", "should_continue")

    builder.add_node("get_officer_appointments", officer_appointment_extraction_node)
    builder.add_edge("get_officer_appointments", "enqueue_officer")

    builder.add_node("enqueue_officer", enqueue_officer_node)
    builder.add_edge("enqueue_officer", "should_continue")

    builder.add_node("should_continue", should_continue_node)
    builder.add_conditional_edges(
            "should_continue", 
            should_continue.route,
            {
                "dequeue_next":"dequeue_next",
                "pattern_detection": "pattern_detection"
            }
        )

    builder.add_node("dequeue_next", dequeue_next.node)
    builder.add_edge("dequeue_next", "route_extraction_by_type")

    builder.add_node("pattern_detection", pattern_detection_node)
    builder.add_edge("pattern_detection", END)
    
    return builder.compile()