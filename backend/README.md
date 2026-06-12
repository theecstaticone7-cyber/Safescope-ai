# Backend — Node.js / Express API

Deployed to **Railway** (or Render) on free tier.

## Stack
- Node.js + Express.js
- MongoDB Atlas + Mongoose
- Forwards AI queries to the FastAPI ai-service

## Routes (routes/)
| File | Prefix | What It Handles |
|---|---|---|
| queryRoutes.js | /api/query | Receives user query → forwards to ai-service → returns results |
| routeRoutes.js | /api/route | Safer route comparisons |
| communitySignalRoutes.js | /api/signals | Submit + fetch community safety signals |
| adminRoutes.js | /api/admin | Data upload, model training trigger |

## Models (models/)
| File | Collection | What It Stores |
|---|---|---|
| QueryLog.js | query_logs | Every query made (city, time, persona, result) |
| CommunitySignal.js | community_signals | User-submitted safety reports + trust scores |
| Feedback.js | feedback | User feedback on AI responses |

## Run
```bash
npm install
npm run dev     # nodemon dev server on localhost:5000
npm test        # Jest + Supertest
```

## Environment
Copy `.env.example` to `.env` and fill in MONGODB_URI and AI_SERVICE_URL.
