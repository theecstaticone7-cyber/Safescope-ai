/*
  server.js — SafeScope AI Backend Entry Point
  ─────────────────────────────────────────────
  BEGINNER EXPLANATION:

  What is Express?
    Express is a small library that lets you build a web server in Node.js
    easily. Without Express you'd have to write a lot of low-level code.
    With Express you just say "when someone visits /api/health, run THIS
    function" — that's it.

  What is a "route"?
    A route is a URL + HTTP method pair that your server responds to.
    Example:  GET  /api/health  →  return { status: "ok" }
              POST /api/query   →  run the AI safety query
    Think of routes like pages on a website, but instead of HTML they
    return JSON data that the React frontend can use.

  What is middleware?
    Middleware runs BEFORE your routes, on every request. We use:
      cors()     — allows the React frontend (on a different port) to call us
      express.json() — automatically reads JSON from request body
      dotenv     — loads .env file so we can use process.env.MONGODB_URI

  What is Mongoose?
    Mongoose is a library that connects Node.js to MongoDB and lets you
    define the shape (schema) of documents you store.

  Flow of every request:
    Browser/Frontend
      → HTTP request arrives at Express
        → CORS middleware checks it's allowed
          → JSON middleware parses the body
            → Correct route runs
              → Response sent back
*/

const express  = require("express");   // the web framework
const mongoose = require("mongoose");  // MongoDB connection library
const cors     = require("cors");      // allows cross-origin requests (React → Express)
const dotenv   = require("dotenv");    // loads .env file into process.env

// ── 1. Load environment variables from .env file ─────────────────────────────
// Must be called before anything else reads process.env
dotenv.config();

// ── 2. Create the Express application ────────────────────────────────────────
// `app` is the object we attach routes and middleware to
const app = express();

// ── 3. Middleware (runs on EVERY request before routes) ──────────────────────

// cors() — without this the browser blocks requests from localhost:3000 → :5000
app.use(cors());

// express.json() — lets us read JSON from request body (needed for POST routes)
app.use(express.json());

// Log every incoming request to the terminal (helpful for debugging)
app.use((req, _res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
  next(); // IMPORTANT: always call next() in middleware or the request hangs
});

// ── 4. Import route files ─────────────────────────────────────────────────────
// Each route file handles a group of related endpoints.
// We mount them at a prefix so all their URLs automatically start with that prefix.
const queryRoutes           = require("./routes/queryRoutes");
const routeRoutes           = require("./routes/routeRoutes");
const communitySignalRoutes = require("./routes/communitySignalRoutes");
const adminRoutes           = require("./routes/adminRoutes");

// ── 5. Health-check route ─────────────────────────────────────────────────────
// This is a simple GET route defined directly on `app` (not in a separate file).
// Purpose: verify the server is running and MongoDB is connected.
// Test it: open http://localhost:5000/api/health in your browser
app.get("/api/health", (req, res) => {
  // res.json() sends a JSON response with status code 200 (OK)
  res.json({
    status:   "ok",
    service:  "SafeScope backend",
    mongodb:  mongoose.connection.readyState === 1 ? "connected" : "disconnected",
    uptime:   `${Math.floor(process.uptime())}s`,
    timestamp: new Date().toISOString(),
  });
});

// ── 6. Mount route files at their URL prefixes ───────────────────────────────
// All routes inside queryRoutes.js will start with /api/query
// All routes inside communitySignalRoutes.js will start with /api/signals
// etc.
app.use("/api/query",    queryRoutes);
app.use("/api/route",    routeRoutes);
app.use("/api/signals",  communitySignalRoutes);
app.use("/api/admin",    adminRoutes);

// ── 7. 404 handler — catches any URL that didn't match a route above ─────────
app.use((req, res) => {
  res.status(404).json({
    error:   "Route not found",
    path:    req.path,
    method:  req.method,
    hint:    "Check /api/health to confirm the server is running",
  });
});

// ── 8. Global error handler — catches unhandled errors in any route ──────────
// Express calls this automatically when you call next(error) in a route
app.use((err, req, res, _next) => {
  console.error("Unhandled error:", err.message);
  res.status(500).json({ error: "Internal server error", details: err.message });
});

// ── 9. Connect to MongoDB, then start the server ─────────────────────────────
// We connect to MongoDB FIRST, and only start listening after it succeeds.
// If MongoDB isn't available we still start (so /api/health works), but warn.

const PORT        = process.env.PORT        || 5000;
const MONGODB_URI = process.env.MONGODB_URI || "mongodb://localhost:27017/safescope";

mongoose
  .connect(MONGODB_URI)
  .then(() => {
    console.log("MongoDB connected:", MONGODB_URI.split("@").pop()); // hide credentials
  })
  .catch((err) => {
    // Don't crash the server — MongoDB might come online later
    console.warn("MongoDB connection failed (server will still start):", err.message);
    console.warn("Health check will show mongodb: disconnected until DB is available.");
  });

// Start listening for HTTP requests
app.listen(PORT, () => {
  console.log("─────────────────────────────────────────");
  console.log(`SafeScope backend running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/api/health`);
  console.log("─────────────────────────────────────────");
});

// Export app for Jest / Supertest tests (so tests can call routes without
// starting a real HTTP server)
module.exports = app;
