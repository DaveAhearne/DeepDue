from deepdue.agent.state import InvestigationState
from deepdue import models
from deepdue import enums

def node(state: InvestigationState):
    entities_to_investigate = []

    company_entities = [
        models.InvestigationEntity(company_id, enums.InvestigationEntityType.COMPANY, 1) 
        for (company_id, _) 
        in state["companies"].items()
        if company_id != state["target_company_number"]
    ]

    officer_entities = [
        models.InvestigationEntity(officer.links.officer.appointments, enums.InvestigationEntityType.OFFICER, 1)
        for (_,officers) in state["officers"].items() 
        for officer in officers.items
        if officer.links and officer.links.officer and  officer.links.officer.appointments
    ]

    psc_entities = [
        models.InvestigationEntity(psc.identification.registration_number, enums.InvestigationEntityType.PSC_ENTITY, 1)
        for (_,pscs) in state["pscs"].items()
        for psc in pscs.items
        if psc.kind == "corporate-entity" and psc.identification and psc.identification.registration_number
    ]

    entities_to_investigate.extend(company_entities)
    entities_to_investigate.extend(officer_entities)
    entities_to_investigate.extend(psc_entities)

    return {
        "entities_to_investigate": entities_to_investigate,
        "entities_visited": [state["target_company_number"]]
    }

