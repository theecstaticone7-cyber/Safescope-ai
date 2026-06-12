# SafeScope AI — Project Context for Claude

## What We're Building
**SafeScope AI: Agentic Urban Safety Decision Engine for Indian Cities**

A FAANG-quality final year project that turns safety data into actionable decisions — not just a map. Targeted at Delhi, Mumbai, and other Indian cities. Supports Hindi + English queries. Quality target: 9.6/10.

**Live one-liner (for interviews):**
> SafeScope AI is the only agentic urban safety platform built specifically for Indian cities — using real NCRB crime data, Hindi natural language queries, 6 LangGraph agents, MCP tool server, RAG-backed explanations, trust-weighted community signals, trained ML models, and publicly deployed on Vercel + Railway.

---

## Student Context
- Complete beginner — explain everything alongside every build step
- Golden rule: **Build → Run → Understand → Explain** before moving to the next day
- Timeline: 25 days × 6 hours/day = 150 hours total

---

## The 6 LangGraph Agents (In Order)

| # | Agent | File | Job |
|---|---|---|---|
| 1 | Query Understanding Agent | `query_agent.py` | Extract city, time, persona; detect Hindi/English |
| 2 | ML Prediction Agent | `prediction_agent.py` | Call XGBoost model → risk scores 0–100 |
| 3 | Route Safety Agent | `route_agent.py` | Score + rank routes by risk, persona, hotspots |
| 4 | Community Signal Agent | `community_signal_agent.py` | Fetch trust-weighted community reports |
| 5 | RAG Explanation Agent | `rag_agent.py` | Retrieve FAISS docs → evidence-backed explanation |
| 6 | Final Report Agent | `report_agent.py` | Assemble scores + map + explanation + disclaimer |

---

## Tech Stack

### Frontend (Vercel)
- React.js + Tailwind CSS
- React Leaflet / Mapbox (maps)
- Chart.js / Recharts (charts)
- Axios

### Backend (Railway/Render)
- Node.js + Express.js
- MongoDB + Mongoose

### AI/ML Service (Hugging Face Spaces)
- Python + FastAPI
- LangGraph (6-agent orchestration)
- MCP (Model Context Protocol — 8 tools)
- Pandas, Scikit-learn, XGBoost

### RAG Layer
- Sentence Transformers (embeddings)
- FAISS (vector database)

### Databases
- MongoDB Atlas — app data, logs, community signals
- SQLite — structured safety analytics (local in AI service)

### Data
- NCRB (ncrb.gov.in) — primary, real government data
- data.gov.in — India open data portal
- Delhi/Mumbai Police open statistics
- Synthetic enrichment only for columns NCRB doesn't provide (lighting, crowd level)

---

## MCP Tool Server (8 Tools)

| Tool | Job |
|---|---|
| `predict_area_risk` | ML model area risk score |
| `score_route_risk` | Score and compare route options |
| `get_safety_hotspots` | Find crime/harassment clusters |
| `get_community_signals` | Fetch trust-weighted community reports |
| `retrieve_rag_context` | Fetch relevant docs from FAISS |
| `find_emergency_resources` | Nearest police, hospital, metro |
| `get_best_time_window` | Safest time window for an area |
| `generate_final_report` | Assemble complete final response |

---

## ML Models (Self-Trained on NCRB Data)

1. **Risk Classifier** (`risk_classifier.pkl`) — Random Forest + XGBoost → Low/Medium/High risk
2. **Incident Count Regressor** (`incident_regressor.pkl`) — Random Forest + XGBoost → expected incident count
3. **Route Risk Scoring** — Formula-based:
   `average area risk + hotspot proximity penalty + night-time multiplier + persona weight + emergency distance penalty + community signal penalty`

---

## 12 Risk Categories (NOT just crime)
Crime, Harassment, Women safety, Theft, Snatching, Night travel, Public transport, Poor lighting, Isolated areas, Emergency access, Route safety, Community signals

## 7 Persona Profiles
Woman alone, Student, Tourist, Night-shift worker, Delivery worker, Senior citizen, General user — each gets different category weights.

## 8 Safety Scores Per Query
Overall, Women Safety, Theft/Snatching, Night Travel, Public Transport, Emergency Access, Community Signal, Confidence Level (Low/Med/High)

---

## 4 Core Frontend Pages
1. **Ask SafeScope** — main query page (English + Hindi, risk cards, RAG explanation, map)
2. **City Safety Twin** — interactive map with toggleable layers
3. **Safer Route** — source + destination + persona → route comparison
4. **Community Signals** — submit trust-scored signal, view signal map

---

## Folder Structure (Key Paths)
```
safescope-ai/
├── frontend/src/pages/       ← Home, AskSafeScope, CitySafetyTwin, SaferRoute, CommunitySignals, Admin
├── frontend/src/components/  ← MapView, RiskCard, RoutePanel, QueryBox, HeatmapLayer, TrustBadge
├── backend/routes/           ← queryRoutes, routeRoutes, communitySignalRoutes, adminRoutes
├── backend/models/           ← QueryLog, CommunitySignal, Feedback
├── ai-service/agents/        ← 6 agent files
├── ai-service/graph/         ← workflow.py (LangGraph orchestration)
├── ai-service/mcp_server/    ← server.py + tools/
├── ai-service/ml/            ← train_model, features, predict, evaluate
├── ai-service/rag/           ← embeddings, vector_store, retriever, context_docs/
├── ai-service/safety/        ← risk_scoring, persona_weights, trust_score, disclaimers
├── data/raw/                 ← Downloaded NCRB data
├── data/processed/           ← Cleaned data
└── models/                   ← .pkl files + FAISS index
```

---

## Deployment (All Free)
| Service | Platform |
|---|---|
| React Frontend | Vercel → safescope-ai.vercel.app |
| Node.js Backend | Railway or Render |
| FastAPI AI Service | Hugging Face Spaces (~30s cold start) |
| MongoDB | MongoDB Atlas (free 512MB) |

---

## 25-Day Phase Plan
- **Days 1–4** (Phase 1): Setup, NCRB data download + cleaning, Express backend skeleton
- **Days 5–10** (Phase 2): Train ML models, wrap in FastAPI
- **Days 11–17** (Phase 3): RAG pipeline, MCP server, all 6 agents
- **Days 18–22** (Phase 4): React frontend + maps + full end-to-end
- **Days 23–25** (Phase 5): Tests, deployment, README, demo video

---

## Dataset Columns (25 Fields)
`incident_id, city, area, police_station, risk_type, sub_category, victim_gender, persona_relevance, place_type, date, time, hour, day_of_week, month, is_weekend, latitude, longitude, severity, case_count, lighting_condition, crowd_level, transport_access, emergency_distance, community_signal_type, source_type`

---

## Trust Score Algorithm
- Repeated reports from same location (boosts trust)
- Duplicate detection (prevents spam)
- Recency decay (older reports matter less)
- Verified/admin user weighting
- Number of similar reports within 300m radius
- Historical accuracy of user's past reports

---

## Responsible AI Disclaimer (Always Include)
```
This analysis is based on NCRB government crime statistics and geospatial enrichment data.
It does not guarantee real-time safety. Crime data may be underreported or regionally biased.
Safety scores are estimates, not guarantees.
Always use official emergency services (112) in real danger.
```

---

## Testing Stack
- **AI Service:** Pytest
- **Backend:** Jest + Supertest
- **Frontend:** React Testing Library
