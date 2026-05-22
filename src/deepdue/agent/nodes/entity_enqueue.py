from deepdue.agent.state import InvestigationState
from deepdue import models
from deepdue import enums

def node(state: InvestigationState):
    current_entity = next(e for e in state["entities_to_investigate"] if e.id == state["current_entity_id"])

    entities_to_investigate: list[models.InvestigationEntity] = []

    company_entities = [
        models.InvestigationEntity(company_id, enums.InvestigationEntityType.COMPANY, current_entity.depth + 1) 
        for (company_id, _) 
        in state["companies"].items()
        if company_id != state["target_company_number"]
    ]

    officer_entities = [
        models.InvestigationEntity(officer.links.officer.appointments, enums.InvestigationEntityType.OFFICER, current_entity.depth + 1)
        for (_,officers) in state["officers"].items() 
        for officer in officers.items
        if officer.links and officer.links.officer and  officer.links.officer.appointments
    ]

    psc_entities = [
        models.InvestigationEntity(psc.identification.registration_number, enums.InvestigationEntityType.PSC_ENTITY, current_entity.depth + 1)
        for (_,pscs) in state["pscs"].items()
        for psc in pscs.items
        if psc.kind == "corporate-entity" and psc.identification and psc.identification.registration_number
    ]

    entities_to_investigate.extend(company_entities)
    entities_to_investigate.extend(officer_entities)
    entities_to_investigate.extend(psc_entities)

    entities_to_investigate = [
        e for e in entities_to_investigate 
        if e.depth <= state["max_depth"]
    ]

    return {
        "entities_to_investigate": entities_to_investigate,
        "entities_visited": [current_entity]
    }

