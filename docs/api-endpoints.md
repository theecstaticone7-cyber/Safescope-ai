# API Endpoints

## Backend (Node.js) — localhost:5000

| Method | Endpoint | What It Does |
|---|---|---|
| GET | /health | Health check — returns { status: "ok" } |
| POST | /api/query | Submit a safety query → returns risk scores + explanation |
| POST | /api/route | Get safer route comparison |
| GET | /api/signals | Get community signals for an area |
| POST | /api/signals | Submit a new community signal |
| POST | /api/admin/upload | Upload new NCRB CSV data |
| POST | /api/admin/train | Trigger ML model retraining |

## AI Service (FastAPI) — localhost:8000

| Method | Endpoint | What It Does |
|---|---|---|
| GET | / | Health check |
| POST | /analyze | Run full 6-agent pipeline → returns final report |
| POST | /predict | Direct ML prediction (bypasses agents) |
| POST | /route | Score and rank routes |
| POST | /rag | Direct RAG retrieval (for testing) |

TODO: Add request/response JSON schemas after Day 10.
