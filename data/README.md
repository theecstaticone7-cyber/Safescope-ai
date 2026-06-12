# Data

## raw/
Downloaded directly from NCRB (ncrb.gov.in), data.gov.in, and Delhi/Mumbai Police.
Do NOT modify these files. Keep originals as-is.

## processed/
Cleaned and enriched versions of the raw data.
Added columns: lighting_condition, crowd_level, transport_access, emergency_distance (synthetic enrichment).
Final file: `processed/safescope_dataset.csv` (25 columns, ready for ML training).

## context_docs/
Plain-text safety documents used by the RAG pipeline.
These get embedded into FAISS vectors and retrieved to explain AI responses.
Examples: area safety summaries, risk category guides, public safety guidelines.

## Dataset Columns (25 fields)
incident_id, city, area, police_station, risk_type, sub_category,
victim_gender, persona_relevance, place_type, date, time, hour,
day_of_week, month, is_weekend, latitude, longitude, severity,
case_count, lighting_condition, crowd_level, transport_access,
emergency_distance, community_signal_type, source_type

## Sources
- NCRB (National Crime Records Bureau) — ncrb.gov.in
- data.gov.in — India open data portal
- Delhi Police / Mumbai Police open statistics
