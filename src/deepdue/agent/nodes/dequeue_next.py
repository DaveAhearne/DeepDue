from langgraph.graph import END
from deepdue.agent.state import InvestigationState
from deepdue.enums import InvestigationEntityType 

def node(state: InvestigationState):
    visited_ids = {e for e in state["entities_visited"]}
    next_entity = next(e for e in state["entities_to_investigate"] if e.id not in visited_ids)

    match next_entity.type:
        case InvestigationEntityType.COMPANY:
            return "get_company"
        case InvestigationEntityType.OFFICER:
            return "get_appointments"
        case InvestigationEntityType.PSC_ENTITY:
            return "get_company"
        case _:
            return END

    return {"target_company_number": next_entity.id}