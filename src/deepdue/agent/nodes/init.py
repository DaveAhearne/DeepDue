from deepdue.agent.state import InputState, InvestigationState
from deepdue.enums import InvestigationEntityType
from deepdue import models

def node(state: InputState) -> dict:
    current_node = models.InvestigationEntity(
        id=state.target_company_number, 
        type=InvestigationEntityType.COMPANY,
        depth=0
    )

    return {
        "target_company_number": state.target_company_number,
        "current_entity_id": state.target_company_number, 
        "current_entity_type": InvestigationEntityType.COMPANY,
        "entities_to_investigate": [current_node],
        "max_depth": state.max_depth,
    }