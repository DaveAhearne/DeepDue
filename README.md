# DeepDue

An agentic corporate fraud investigation system built on the Companies House public API. Given a company name or number, DeepDue autonomously traverses the related entity graph (directors, PSC records, filing history, related companies), identifies known fraud patterns, and surfaces findings for human review.

Built as the companion codebase to a five-part blog series at [blog.daveahearne.com](https://blog.daveahearne.com).

> **Note:** This is an investigation *assistant*, not a verdict machine. All data used is public record. Findings are surfaced for human review. Conclusions are for the investigator to draw.

## What it detects

- **Phoenixing**: dissolved companies with successor entities sharing directors or addresses
- **Director network anomalies**: individuals controlling unusually large numbers of companies, particularly dormant or dissolved ones
- **Registered address clustering**: multiple unrelated companies sharing an address, particularly formation agent addresses
- **Filing timeline irregularities**: persistent late filing, overdue accounts preceding dissolution
- **Circular or layered ownership**: PSC chains that resolve to companies rather than natural persons

## Stack

| Component | Choice |
|-----------|--------|
| Agent framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM gateway | [LiteLLM](https://github.com/BerriAI/litellm) |
| Vector database | [Qdrant](https://qdrant.tech) |
| Data source | [Companies House REST API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference) |
| Backend | [FastAPI](https://fastapi.tiangolo.com) |

## Getting started

### Prerequisites

- Python 3.10+
- A free [Companies House API key](https://developer.companieshouse.gov.uk/api/docs/)
- A free [LangSmith account](https://smith.langchain.com) (for LangGraph Studio)

### Installation

```bash
git clone https://github.com/daveahearne/deepdue
cd deepdue
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Configuration

```bash
cp .env.example .env
# Add your Companies House API key to .env
```

### Run the FastAPI server

```bash
dev
```

### Run in LangGraph Studio

Studio gives you a visual graph, node-by-node execution tracing, and interactive state inspection during development.

```bash
pip install -U "langgraph-cli[inmem]"

# Standard (Chrome/Firefox only — Safari blocks localhost)
langgraph dev

# With tunnel (works in all browsers, required for Safari)
langgraph dev --tunnel
```

This starts the Agent Server locally and opens Studio automatically. The `--tunnel` flag is recommended — it avoids mixed-content browser blocking by giving the local server a public HTTPS endpoint.

Once running, Studio is accessible at:

```
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

Or via the tunnel URL printed in the terminal output.

## Project structure

```
src/deepdue/
    config.py               # Settings via pydantic-settings
    enums.py                # Shared API enumeration types
    models.py               # Shared domain types
    data/
        companies_house.py  # Companies House API client
    agent/
        graph.py            # LangGraph graph definition
        state.py            # InvestigationState TypedDict
        nodes/
            company_lookup.py       # Fetch company profile
            officer_extraction.py   # Fetch officers
            psc_extraction.py       # Fetch PSC records and statements
            filing_history.py       # Fetch filing history
            entity_enqueue.py       # Queue entities for traversal
    serve/
        api.py              # FastAPI application
        log.py              # Logging and request ID middleware
        schema.py           # Request/response schemas
        templates_env.py    # Jinja2 template setup
        routes/
            health.py       # GET /health
            home.py         # GET / (investigation UI)
            investigation.py # POST /investigation
        templates/
            index.html      # Investigation UI
```

## Companies House API coverage

| Endpoint | Method | Used for |
|----------|--------|----------|
| `/company/{number}` | `GetCompanyProfile` | Status, address, SIC codes, incorporation/cessation dates |
| `/company/{number}/officers` | `GetCompanyOfficers` | Director appointments, resignations, roles |
| `/company/{number}/persons-with-significant-control` | `GetCompanyPSCs` | Beneficial owners, corporate PSCs, control types |
| `/company/{number}/persons-with-significant-control-statements` | `GetCompanyPSCStatements` | PSC statements for companies with no registrable PSC |
| `/company/{number}/filing-history` | `GetCompanyFilingHistory` | Filing categories, types, dates |
| `/search/companies` | `SearchCompanies` | Resolve company name to registration number |
| `/search/officers` | `SearchOfficers` | Find officers by name, surface appointment counts |

## Disclaimer

DeepDue is a research and educational project. It is not a fraud detection system, compliance tool, or replacement for professional due diligence. All data retrieved is public record via the Companies House API. No data is scraped or harvested beyond what the API provides.

---

Running qdrant:
```
docker run -d --name deepdue-qdrant -p 6333:6333 qdrant/qdrant
```