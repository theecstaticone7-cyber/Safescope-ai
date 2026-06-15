/*
  communitySignalRoutes.js
  ─────────────────────────
  Handles community safety signals (user-submitted reports).
  Mounted at /api/signals in server.js.
*/

const express = require("express");
const router  = express.Router();

// GET /api/signals
// Returns community signals for an area.
// Query params: ?city=Delhi&area=Saket&radius=500
// TODO (Day 16): query CommunitySignal model with trust score filtering
router.get("/", async (req, res) => {
  const { city, area } = req.query;
  res.json({
    message: "Community signals — model not connected yet (Day 16)",
    filters: { city, area },
    signals: [],
  });
});

// POST /api/signals
// Submits a new community safety signal.
// Body: { signalType, description, lat, lng, area, city, userId }
// TODO (Day 16): save to MongoDB CommunitySignal model, compute trust score
router.post("/", async (req, res) => {
  try {
    const { signalType, description, lat, lng, area, city } = req.body;

    if (!signalType || !area || !city) {
      return res.status(400).json({ error: "signalType, area, and city are required" });
    }

    // Placeholder — real save + trust score calculation added Day 16
    res.status(201).json({
      message:  "Signal received — will be saved to MongoDB on Day 16",
      received: { signalType, description, lat, lng, area, city },
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
