from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_officer_appointment_extraction_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        company_number = state["current_entity_id"]
        officers_data = state["officers"].get(company_number)

        appointment_paths = [
            o.links.officer.appointments 
            for o in officers_data.items 
            if o.links and o.links.officer and o.links.officer.appointments
        ]

        appointments = {a: await client.GetOfficerAppointments(a) for a in appointment_paths}

        return {"appointments": appointments}

    return node
