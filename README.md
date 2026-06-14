# SafeScope AI

**Agentic Urban Safety Decision Engine for Indian Cities**

SafeScope AI helps users make safer travel decisions in Indian cities using real NCRB crime data, 6 LangGraph agents, MCP tools, RAG explanations, and trust-weighted community signals. Supports Hindi and English queries.

## Services

| Service | Folder | Deployed To |
|---|---|---|
| React Frontend | `frontend/` | Vercel |
| Node.js Backend | `backend/` | Railway / Render |
| Python AI Service | `ai-service/` | Hugging Face Spaces |

## Quick Start (Development)

```bash
# Backend
cd backend && npm install && npm run dev

# Frontend
cd frontend && npm install && npm start

# AI Service
cd ai-service && pip install -r requirements.txt && uvicorn main:app --reload
```

## Progress

| Day | What Was Built |
|-----|----------------|
| Day 1 | Project scaffold — 3-service architecture (React, Node.js, FastAPI), folder structure, all agent/MCP/RAG placeholders |
| Day 2 | Real NCRB crime data downloaded and inspected (`inspect_ncrb.py`, `process_ncrb.py`) |
| Day 3 | Incident-level dataset built — 12,926 records across 19 cities and 12 risk categories, expanded from NCRB aggregates |

## Data
Real NCRB crime data + geospatial enrichment. See `data/` folder.

## Disclaimer
This platform uses NCRB government crime statistics for demonstration purposes.
It does not guarantee real-time safety. Always use official emergency services (112) in real danger.
