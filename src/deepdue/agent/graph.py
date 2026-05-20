from langgraph.graph import StateGraph, START, END
from deepdue.agent.state import InvestigationState
from deepdue.agent.nodes import company_lookup
from deepdue.data.companies_house import CompaniesHouseClient

def build_graph(ch_client: CompaniesHouseClient):
    company_lookup_node = company_lookup.make_company_lookup_node(ch_client)

    builder = StateGraph(InvestigationState)
    builder.add_edge(START, "get_company")
    builder.add_node("get_company", company_lookup_node)
    builder.add_edge("get_company", END)

    return builder.compile()