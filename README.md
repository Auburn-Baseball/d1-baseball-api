# D1 Baseball API (FastAPI)

A minimal FastAPI service built and maintained by **Auburn University Baseball**.  
Deployed on Render and managed with Poetry.

## Live API

- **Base URL:** https://d1-baseball-api-c79q.onrender.com/
- **Interactive docs (Swagger UI):** https://d1-baseball-api-c79q.onrender.com/docs

## Quickstart

### Prerequisites
- Python (3.10+ recommended)
- [Poetry](https://python-poetry.org/)

### Installation
```bash
poetry install
```

### Run
```bash
poetry run uvicorn d1_baseball_api.main:app --reload
```

### Once Running
- Local API: http://127.0.0.1:8000
- Local docs: http://127.0.0.1:8000/docs

### Testing
```bash
poetry run pytest
```

War Eagle! ⚾
