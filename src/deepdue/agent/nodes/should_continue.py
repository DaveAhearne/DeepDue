from langgraph.graph import END
from deepdue.agent.state import InvestigationState

def node(state: InvestigationState):
    visited_ids = {e.id for e in state["entities_visited"]}

    remaining = [
        e for e in state["entities_to_investigate"] 
        if e.id not in visited_ids and e.depth <= state["max_depth"]
    ]

    if remaining:
        return "dequeue_next"
    
    return "end"