from langgraph.graph import END
from deepdue.agent.state import InvestigationState
from deepdue.enums import InvestigationEntityType 

def node(state: InvestigationState):
    current_entity_type = state["current_entity_type"]

    match current_entity_type:
        case InvestigationEntityType.COMPANY:
            return "get_company"
        case InvestigationEntityType.OFFICER:
            return "get_officer_appointments"
        case _:
            return END