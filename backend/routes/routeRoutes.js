/*
  routeRoutes.js
  ──────────────
  Handles safer-route comparisons.
  Mounted at /api/route in server.js.
*/

const express = require("express");
const router  = express.Router();

// POST /api/route
// Body: { source: string, destination: string, time: string, persona: string, city: string }
// Returns ranked route options with safety scores from the AI service.
// TODO (Day 10): forward to AI service route-scoring pipeline
router.post("/", async (req, res) => {
  try {
    const { source, destination, time, persona, city } = req.body;

    if (!source || !destination || !city) {
      return res.status(400).json({ error: "source, destination, and city are required" });
    }

    // Placeholder — real route scoring added Day 10
    res.json({
      message:  "Route comparison — AI service not connected yet (Day 10)",
      received: { source, destination, time, persona, city },
      routes:   [],
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
