
from deepdue.agent.state import InvestigationState

def node(state: InvestigationState):
    visited_ids = {e.id for e in state["entities_visited"]}
    next_entity = next(e for e in state["entities_to_investigate"] if e.id not in visited_ids)
    
    return {"target_company_number": next_entity.id}