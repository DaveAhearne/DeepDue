from deepdue.agent.state import InvestigationState
from deepdue.enums import InvestigationEntityType
from deepdue import models

def node(state: InvestigationState) -> dict:
    current_node = models.InvestigationEntity(
        id=state["current_entity_id"], 
        type=InvestigationEntityType.COMPANY,
        depth=0
    )

    return {"entities_to_investigate" : [current_node]}