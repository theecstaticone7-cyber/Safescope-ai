/*
  QueryLog.js — Mongoose Model
  ─────────────────────────────
  BEGINNER EXPLANATION:
  A Mongoose "model" defines the shape (schema) of one type of document
  stored in MongoDB. Think of it like a table definition in SQL.
  Each field has a type and optional rules (required, default, etc.).

  This model stores every safety query a user makes so we can:
    - Show the user their query history
    - Analyse which areas are queried most
    - Train the AI with real usage patterns
*/

const mongoose = require("mongoose");

const QueryLogSchema = new mongoose.Schema(
  {
    query:         { type: String, required: true },   // raw user query text
    city:          { type: String, required: true },
    area:          { type: String },
    time:          { type: String },                   // e.g. "22:30"
    persona:       { type: String, default: "general" },
    language:      { type: String, enum: ["hindi", "english"], default: "english" },
    riskScore:     { type: Number, min: 0, max: 100 }, // overall risk score returned
    confidence:    { type: String, enum: ["Low", "Medium", "High"] },
    responseTime:  { type: Number },                   // ms taken by AI service
  },
  {
    timestamps: true,  // automatically adds createdAt and updatedAt fields
  }
);

// mongoose.model("QueryLog", schema) creates the model AND links it to the
// "querylogs" collection in MongoDB (Mongoose pluralises the name automatically)
module.exports = mongoose.model("QueryLog", QueryLogSchema);
