/*
  Feedback.js — Mongoose Model
  ─────────────────────────────
  Stores user feedback on AI responses (was the risk assessment helpful/accurate?).
  This data can be used to retrain and improve the models over time.
*/

const mongoose = require("mongoose");

const FeedbackSchema = new mongoose.Schema(
  {
    queryId:     { type: mongoose.Schema.Types.ObjectId, ref: "QueryLog" },
    rating:      { type: Number, min: 1, max: 5, required: true },  // 1=bad 5=perfect
    wasHelpful:  { type: Boolean },
    comment:     { type: String },                                   // optional free text
    city:        { type: String },
    area:        { type: String },
    riskType:    { type: String },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("Feedback", FeedbackSchema);
