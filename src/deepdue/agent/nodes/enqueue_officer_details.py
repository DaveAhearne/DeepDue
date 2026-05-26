from deepdue.agent.state import InvestigationState
from deepdue import models
from deepdue import enums
from langsmith import get_current_run_tree

def node(state: InvestigationState):
    current_entity = next(e for e in state["entities_to_investigate"] if e.id == state["current_entity_id"])

    current_appointments = state["appointments"].get(state["current_entity_id"])

    company_entities = [
        models.InvestigationEntity(
            appointment.appointed_to.company_number,
            enums.InvestigationEntityType.COMPANY,
            current_entity.depth + 1
        )
        for appointment in (current_appointments.items if current_appointments else [])
        if appointment.appointed_to and appointment.appointed_to.company_number
    ]

    entities_to_investigate = [
        e for e in company_entities
        if e.depth <= state["max_depth"]
    ]

    run = get_current_run_tree()
    if run:
        run.metadata.update({
            "companies_visited": len(state["companies"]),
            "officers_visited": len(state["officers"]),
            "appointments_visited": len(state["appointments"]),
            "entities_queued": len(state["entities_to_investigate"]),
            "entities_visited": len(state["entities_visited"]),
            "depth": current_entity.depth,
        })

    return {
        "entities_to_investigate": entities_to_investigate,
        "entities_visited": [current_entity]
    }