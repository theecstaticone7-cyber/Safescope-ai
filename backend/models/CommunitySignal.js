/*
  CommunitySignal.js — Mongoose Model
  ─────────────────────────────────────
  Stores user-submitted safety signals (e.g. "poor lighting on this road").
  Each signal carries a trust score that determines how much weight it gets
  in the ML model's risk calculations.
*/

const mongoose = require("mongoose");

const CommunitySignalSchema = new mongoose.Schema(
  {
    userId:          { type: String },                 // optional — anonymous allowed
    signalType:      {
      type: String,
      required: true,
      enum: [
        "poor_lighting", "isolated_road", "unsafe_bus_stop",
        "harassment_prone", "reported_hazard", "suspicious_activity",
        "infrastructure_issue", "safe_spot",
      ],
    },
    description:     { type: String },                 // free-text detail from the user
    latitude:        { type: Number, required: true },
    longitude:       { type: Number, required: true },
    area:            { type: String, required: true },
    city:            { type: String, required: true },
    trustScore:      { type: Number, min: 0, max: 100, default: 50 },
    confidenceLevel: { type: String, enum: ["Low", "Medium", "High"], default: "Low" },
    verifiedAt:      { type: Date },                   // set when an admin verifies it
    isActive:        { type: Boolean, default: true }, // false = spam / removed
  },
  {
    timestamps: true,
  }
);

// Index on city + area so we can quickly fetch all signals for a neighbourhood
CommunitySignalSchema.index({ city: 1, area: 1 });

// Geospatial index so we can query "signals within 300m of this point"
CommunitySignalSchema.index({ latitude: 1, longitude: 1 });

module.exports = mongoose.model("CommunitySignal", CommunitySignalSchema);
