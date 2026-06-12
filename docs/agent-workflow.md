# Agent Workflow

## The 6 LangGraph Agents (in sequence)

| # | Agent | File | Day Built | Job |
|---|---|---|---|---|
| 1 | Query Understanding | query_agent.py | Day 14 | Extract city, time, persona; detect Hindi/English |
| 2 | ML Prediction | prediction_agent.py | Day 15 | XGBoost → risk scores 0–100 |
| 3 | Route Safety | route_agent.py | Day 15 | Score + rank routes with persona weights |
| 4 | Community Signal | community_signal_agent.py | Day 16 | Trust-weighted community reports |
| 5 | RAG Explanation | rag_agent.py | Day 16 | FAISS retrieval → evidence-backed explanation |
| 6 | Final Report | report_agent.py | Day 17 | Assemble complete response + disclaimer |

## LangGraph State Schema (Draft)
```python
{
  "query": str,
  "city": str,
  "area": str,
  "hour": int,
  "persona": str,
  "language": str,           # "hindi" or "english"
  "risk_scores": dict,       # from Agent 2
  "routes": list,            # from Agent 3
  "community_signals": dict, # from Agent 4
  "rag_context": list,       # from Agent 5
  "final_report": dict       # from Agent 6
}
```
