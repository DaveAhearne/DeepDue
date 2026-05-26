from deepdue.agent.state import InvestigationState
from deepdue import models
from deepdue import enums

def node(state: InvestigationState):
    current_entity = next(e for e in state["entities_to_investigate"] if e.id == state["current_entity_id"])

    current_officers = state["officers"].get(state["current_entity_id"])
    current_pscs = state["pscs"].get(state["current_entity_id"])

    officer_entities = [
        models.InvestigationEntity(officer.links.officer.appointments, enums.InvestigationEntityType.OFFICER, current_entity.depth + 1)
        for officer in (current_officers.items if current_officers else [])
        if officer.links and officer.links.officer and officer.links.officer.appointments
    ]

    psc_entities = [
        models.InvestigationEntity(psc.identification.registration_number, enums.InvestigationEntityType.PSC_ENTITY, current_entity.depth + 1)
        for psc in (current_pscs.items if current_pscs else [])
        if psc.kind == "corporate-entity" and psc.identification and psc.identification.registration_number
    ]

    entities_to_investigate = [
        e for e in officer_entities + psc_entities
        if e.depth <= state["max_depth"]
    ]

    return {
        "entities_to_investigate": entities_to_investigate,
        "entities_visited": [current_entity]
    }