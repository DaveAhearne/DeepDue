
from deepdue.agent.state import InvestigationState

def node(state: InvestigationState):
    visited_ids = {e.id for e in state["entities_visited"]}
    next_entity = next(e for e in state["entities_to_investigate"] if e.id not in visited_ids)
    
    return {
        "current_entity_id": next_entity.id,
        "current_entity_type": next_entity.type
    }