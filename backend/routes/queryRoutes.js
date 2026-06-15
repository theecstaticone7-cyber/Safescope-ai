/*
  queryRoutes.js
  ──────────────
  Handles everything related to safety queries.

  BEGINNER EXPLANATION:
  express.Router() is like a mini Express app.
  We define routes on it, then in server.js we "mount" it at /api/query.
  So a route defined as router.post("/") is actually reachable at POST /api/query
  A route defined as router.get("/history") → GET /api/query/history
*/

const express = require("express");
const router  = express.Router();

// POST /api/query
// Receives the user's safety question, forwards to the Python AI service,
// returns the full risk report (scores + explanation).
// Body: { query: string, city: string, area: string, time: string, persona: string }
// TODO (Day 10): connect to AI service and return real response
router.post("/", async (req, res) => {
  try {
    const { query, city, area, time, persona } = req.body;

    // Basic input validation
    if (!query || !city) {
      return res.status(400).json({ error: "query and city are required" });
    }

    // Placeholder response — will be replaced with real AI call on Day 10
    res.json({
      message:  "Query received — AI service not connected yet (Day 10)",
      received: { query, city, area, time, persona },
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/query/history
// Returns recent query logs stored in MongoDB.
// TODO (Day 10): query the QueryLog model and return real history
router.get("/history", async (req, res) => {
  res.json({ message: "Query history — coming on Day 10", logs: [] });
});

module.exports = router;
