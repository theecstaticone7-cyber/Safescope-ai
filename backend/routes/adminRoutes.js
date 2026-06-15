/*
  adminRoutes.js
  ───────────────
  Admin-only endpoints: upload data, trigger model retraining.
  Mounted at /api/admin in server.js.
*/

const express = require("express");
const router  = express.Router();

// GET /api/admin/status
// Returns basic system status for the admin dashboard.
router.get("/status", (req, res) => {
  res.json({
    backend:  "ok",
    mongodb:  require("mongoose").connection.readyState === 1 ? "connected" : "disconnected",
    message:  "Admin panel — more features coming Day 22",
  });
});

// POST /api/admin/train
// Triggers ML model retraining in the Python AI service.
// TODO (Day 22): forward request to AI service /retrain endpoint
router.post("/train", async (req, res) => {
  res.json({ message: "Model retraining — AI service not connected yet (Day 10)" });
});

module.exports = router;
