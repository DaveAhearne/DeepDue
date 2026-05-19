# DeepDue

An agentic corporate fraud investigation system built on the Companies House public API.An agentic corporate fraud investigation system built on the Companies House public API. Given a company name or number, DeepDue autonomously traverses the related entity graph (directors, PSC records, filing history, related companies), identifies known fraud patterns, and surfaces findings for human review.

Built as the companion codebase to a five-part blog series at [blog.daveahearne.com](https://blog.daveahearne.com).

> **Note:** This is an investigation *assistant*, not a verdict machine. All data used is public record. Findings are surfaced for human review. Conclusions are for the investigator to draw.

---

## What it detects

- **Phoenixing**: dissolved companies with successor entities sharing directors or addresses
- **Director network anomalies**: individuals controlling unusually large numbers of companies, particularly dormant or dissolved ones
- **Registered address clustering**: multiple unrelated companies sharing an address, particularly formation agent addresses
- **Filing timeline irregularities**: persistent late filing, overdue accounts preceding dissolution
- **Circular or layered ownership**: PSC chains that resolve to companies rather than natural persons

---

## Stack

| Component | Choice |
|-----------|--------|
| Agent framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM gateway | [LiteLLM](https://github.com/BerriAI/litellm) |
| Vector database | [Qdrant](https://qdrant.tech) |
| Data source | [Companies House REST API](https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference) |
| Backend | [FastAPI](https://fastapi.tiangolo.com) |

---

## Getting started

### Prerequisites

- Python 3.10+
- A free [Companies House API key](https://developer.companieshouse.gov.uk/api/docs/)

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

### Run

```bash
dev
```

---

## Project structure

```
src/deepdue/
    app.py                  # Entrypoint
    models.py               # Shared domain types
    data/
        enums.py            # API enumeration types
        models.py           # Data layer models
        ch.py               # Companies House API client
    agent/                  # LangGraph investigation loop (Part 2+)
    patterns/               # Fraud pattern detection (Part 3+)
```

---

## Blog series

This repo is built part by part alongside a blog series. Each part has a clear deliverable.

| Part | Title | Status |
|------|-------|--------|
| 1 | The Data Landscape | 🚧 In progress |
| 2 | First LangGraph Agent | ⏳ Upcoming |
| 3 | Multi-Entity Traversal | ⏳ Upcoming |
| 4 | LiteLLM and Qdrant | ⏳ Upcoming |
| 5 | FastAPI, Demo, and Honest Evaluation | ⏳ Upcoming |

---

## Disclaimer

DeepDue is a research and educational project. It is not a fraud detection system, compliance tool, or replacement for professional due diligence. All data retrieved is public record via the Companies House API. No data is scraped or harvested beyond what the API provides.