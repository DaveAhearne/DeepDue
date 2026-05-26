from deepdue.agent.state import InvestigationState
from deepdue.enums import InvestigationEntityType
from deepdue import models

def node(state: InvestigationState) -> dict:
    current_node = models.InvestigationEntity(
        id=state["target_company_number"], 
        type=InvestigationEntityType.COMPANY,
        depth=0
    )

    return {
        "current_entity_id": state["target_company_number"], 
        "entities_to_investigate" : [current_node],
        "current_entity_type": InvestigationEntityType.COMPANY,
        "depth": 0
    }