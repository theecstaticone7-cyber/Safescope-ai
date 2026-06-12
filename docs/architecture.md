# System Architecture

## Data Flow
```
User (Hindi or English query)
      ↓
React Frontend — Vercel
      ↓
Node.js / Express Backend — Railway
      ↓
FastAPI AI Service — Hugging Face Spaces
      ↓
LangGraph — 6 Agent Workflow
      ↓
MCP Tool Server — 8 modular tools
      ↓
ML Models + RAG (FAISS) + NCRB Database + Geospatial Engine
      ↓
Final Answer + Risk Scores + Maps + Explanation + Disclaimer
```

## Services
| Service | Tech | Deployed To | Port |
|---|---|---|---|
| Frontend | React + Tailwind | Vercel | 3000 |
| Backend | Node.js + Express | Railway | 5000 |
| AI Service | Python + FastAPI | Hugging Face Spaces | 8000 |
| Database | MongoDB Atlas | Cloud | - |

TODO: Add architecture diagram image (Day 25)
