from langgraph.graph import END
from deepdue.agent.state import InvestigationState
from deepdue.enums import InvestigationEntityType 

def node(state: InvestigationState):
    next_entity = next(e for e in state["entities_to_investigate"] if e.id == state["current_entity_id"])

    match next_entity.type:
        case InvestigationEntityType.COMPANY:
            return "get_company"
        case InvestigationEntityType.OFFICER:
            return "get_officer_appointments"
        case InvestigationEntityType.PSC_ENTITY:
            return "get_company"
        case _:
            return END