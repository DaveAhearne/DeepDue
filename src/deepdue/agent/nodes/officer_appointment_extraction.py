from deepdue.agent.state import InvestigationState
from deepdue.data.companies_house import CompaniesHouseClient

def make_officer_appointment_extraction_node(client: CompaniesHouseClient):
    async def node(state: InvestigationState):
        appointments_path = state["current_entity_id"]
        appointments = await client.GetOfficerAppointments(appointments_path)
        return {"appointments": {appointments_path: appointments}}
    return node
