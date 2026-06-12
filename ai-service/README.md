# AI Service — Python FastAPI

Deployed to **Hugging Face Spaces** (free). Expect ~30s cold start on first request.

## Stack
- FastAPI (REST API server)
- LangGraph (6-agent workflow orchestration)
- MCP (Model Context Protocol — 8 modular tools)
- XGBoost + Scikit-learn (ML models)
- FAISS + Sentence Transformers (RAG vector search)
- Pandas (data processing)

## The 6 Agents (agents/)
| File | Agent | Job |
|---|---|---|
| query_agent.py | Agent 1 — Query Understanding | Extract city, time, persona; detect Hindi/English |
| prediction_agent.py | Agent 2 — ML Prediction | Run XGBoost → risk scores 0–100 |
| route_agent.py | Agent 3 — Route Safety | Score + rank route options with persona weights |
| community_signal_agent.py | Agent 4 — Community Signal | Fetch trust-weighted community reports |
| rag_agent.py | Agent 5 — RAG Explanation | Retrieve FAISS docs → evidence-backed explanation |
| report_agent.py | Agent 6 — Final Report | Assemble scores + map data + explanation + disclaimer |

## MCP Tools (mcp_server/tools/)
| File | Tools Inside |
|---|---|
| risk_tools.py | predict_area_risk |
| route_tools.py | score_route_risk, get_safety_hotspots, get_best_time_window |
| rag_tools.py | retrieve_rag_context |
| community_tools.py | get_community_signals |
| emergency_tools.py | find_emergency_resources, generate_final_report |

## Other Modules
- `ml/` — model training, feature engineering, prediction, evaluation
- `rag/` — embeddings, FAISS vector store, retriever
- `geospatial/` — hotspot clustering, route risk geometry
- `database/` — SQLite connection + SQL queries
- `safety/` — risk scoring formulas, persona weights, trust score, disclaimers

## Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
pytest tests/    # run all tests
```
