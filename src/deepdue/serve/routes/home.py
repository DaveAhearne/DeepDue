import logging
from fastapi import APIRouter, Request

from deepdue.serve.templates_env import templates

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_predict(request: Request):
    logger.info("HIT: GET / - serving UI")
    return templates.TemplateResponse(request, "index.html")