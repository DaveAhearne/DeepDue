import os
import uvicorn
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from deepdue.agent import graph
from deepdue.data.companies_house import CompaniesHouseClient
from deepdue.serve import log
from deepdue.config import settings
from deepdue.serve.routes.health import router as health_router
from deepdue.serve.routes.home import router as home_router
from deepdue.serve.routes.investigation import router as investigation_router

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.configure_logging()

    os.environ["LANGSMITH_TRACING"] = settings.langsmith_tracing
    os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
    os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project

    ch_client = CompaniesHouseClient(settings.ch_api_key)
    app.state.investigation_graph = graph.build_graph(ch_client)
    
    yield
    
app = FastAPI(
    title="DeepDue",
    description="Agentic UK corporate fraud investigator built on the Companies House public API.",
    version="1.0.0",
    docs_url="/docs",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(home_router)
app.include_router(investigation_router)

app.add_middleware(log.RequestIdMiddleware)

def main() -> None:
    host = os.getenv("HOST", settings.host)
    port = int(os.getenv("PORT", settings.port))
    workers = int(os.getenv("WORKERS", settings.workers))

    uvicorn.run(
        "deepdue.serve.api:app",
        host=host,
        port=port,
        workers=workers,
        log_config=None
    )