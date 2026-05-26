import logging
from fastapi import APIRouter, HTTPException, Request

from deepdue.enums import InvestigationEntityType
from deepdue.serve.schema import InvestigationRequest

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/investigation")
async def request_investigation(request: Request, payload: InvestigationRequest):
    logger.info("HIT: /investigation")
    
    graph = request.app.state.investigation_graph
    
    try:
        result = await graph.ainvoke({
            "current_entity_id": payload.company_number,
            "current_entity_type": InvestigationEntityType.COMPANY,
            "max_depth": 2,
        })

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )