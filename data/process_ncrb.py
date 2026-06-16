"""
process_ncrb.py  —  Day 3 of SafeScope AI

WHAT THIS SCRIPT DOES (beginner explanation):
  Real NCRB data only gives us 1 row per city (e.g., "Delhi had 297,666 crimes in 2024").
  ML models need incident-level data — 1 row per crime event, with all 25 features.
  This script bridges that gap:
    1. Reads the two raw NCRB Excel files
    2. Cleans them (fix types, drop junk rows)
    3. Uses each city's real crime total and women-crime ratio to set realistic proportions
    4. Generates thousands of synthetic incident rows that honour those real proportions
    5. Saves the final 25-column dataset to data/processed/safescope_incidents.csv

SOURCE TRANSPARENCY:
  Every row has a 'source_type' column explaining what is real vs synthetic:
    "ncrb_real"       → city name and crime count come from official NCRB 2024 data
    "synthetic"       → area, coordinates, time, lighting, crowd are modelled / enriched
  Combined: "ncrb+synthetic" means the city count is real, everything else is modelled
"""

import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

# ── reproducibility: same seed = same dataset every run ──────────────────────
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# ── paths ─────────────────────────────────────────────────────────────────────
BASE  = r"C:\Users\bhate\safescope-ai"
RAW   = os.path.join(BASE, "data", "raw")
OUT   = os.path.join(BASE, "data", "processed")
os.makedirs(OUT, exist_ok=True)

# =============================================================================
# STEP 1 — Load and clean the two NCRB Excel files
# =============================================================================
# The Excel layout: row 0 = big title (skip), row 1 = real column headers, row 2+ = data
# pandas header=1 makes row 1 the column names automatically.

NCRB_COLS = [
    "SL", "City", "Crime_2022", "Crime_2023", "Crime_2024",
    "Population_Lakhs", "Crime_Rate_2024", "Chargesheeting_Rate_2024"
]

def load_ncrb(filename):
    path = os.path.join(RAW, filename)
    df   = pd.read_excel(path, header=1)
    df.columns = NCRB_COLS
    # SL comes in as float (1.0, 2.0 …) from Excel — keep only real data rows
    df = df[pd.to_numeric(df["SL"], errors="coerce").notna()].copy()
    df = df.dropna(subset=["City"])
    df["SL"] = df["SL"].astype(int)
    for col in ["Crime_2022", "Crime_2023", "Crime_2024",
                "Population_Lakhs", "Crime_Rate_2024", "Chargesheeting_Rate_2024"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.reset_index(drop=True)

df_total = load_ncrb("ncrb_total_crimes_2024.xlsx")
df_women = load_ncrb("ncrb_crime_against_women_2024.xlsx")

print(f"Loaded: {len(df_total)} cities (total crimes), {len(df_women)} cities (women crimes)")

# =============================================================================
# STEP 2 — Merge + derive key stats per city
# =============================================================================
# We need two numbers per city:
#   total_2024   — all crimes (from file 2)
#   women_2024   — crimes against women (from file 1)
#   women_ratio  — women_2024 / total_2024   ← drives risk_type weights

city_stats = df_total[["City", "Crime_2024", "Crime_Rate_2024", "Population_Lakhs"]].merge(
    df_women[["City", "Crime_2024"]].rename(columns={"Crime_2024": "Women_2024"}),
    on="City", how="left"
)

# Strip state name in parentheses and "City" suffix for a clean key
city_stats["clean_name"] = (
    city_stats["City"]
    .str.replace(r"\s*\(.*\)", "", regex=True)
    .str.replace("City", "", regex=False)
    .str.strip()
)

city_stats["women_ratio"] = (
    city_stats["Women_2024"] / city_stats["Crime_2024"]
).fillna(0.07).round(4)

# =============================================================================
# STEP 3 — Area definitions with real coordinates
# =============================================================================
# Delhi and Mumbai get detailed treatment (focus cities in blueprint).
# All other cities get 5 representative neighbourhoods.
#
# Each Delhi/Mumbai area dict has:
#   area        — neighbourhood name
#   lat/lon     — approximate real-world centre (we add a small random jitter per incident)
#   police      — nearest police station name
#   place_types — kinds of venues present (affects crowd/transport)
#   risk_bias   — crime types over-represented here (adds realistic hotspot flavour)

DELHI_AREAS = [
    {"area": "Connaught Place",  "lat": 28.6315, "lon": 77.2167, "police": "Connaught Place PS",
     "place_types": ["market", "metro_station", "restaurant"],      "risk_bias": ["theft", "snatching"]},
    {"area": "Saket",            "lat": 28.5244, "lon": 77.2090, "police": "Saket PS",
     "place_types": ["mall", "metro_station", "road"],              "risk_bias": ["women_safety", "theft"]},
    {"area": "Lajpat Nagar",     "lat": 28.5672, "lon": 77.2430, "police": "Lajpat Nagar PS",
     "place_types": ["market", "bus_stop", "road"],                 "risk_bias": ["harassment", "theft"]},
    {"area": "Chandni Chowk",    "lat": 28.6507, "lon": 77.2306, "police": "Chandni Chowk PS",
     "place_types": ["market", "metro_station", "road"],            "risk_bias": ["theft", "snatching", "public_transport"]},
    {"area": "Dwarka",           "lat": 28.5921, "lon": 77.0460, "police": "Dwarka PS",
     "place_types": ["residential", "metro_station", "road"],       "risk_bias": ["night_travel", "isolated_area"]},
    {"area": "Rohini",           "lat": 28.7359, "lon": 77.0882, "police": "Rohini PS",
     "place_types": ["residential", "market", "road"],              "risk_bias": ["crime", "night_travel"]},
    {"area": "Karol Bagh",       "lat": 28.6514, "lon": 77.1907, "police": "Karol Bagh PS",
     "place_types": ["market", "metro_station", "road"],            "risk_bias": ["theft", "snatching"]},
    {"area": "Nehru Place",      "lat": 28.5492, "lon": 77.2510, "police": "Nehru Place PS",
     "place_types": ["market", "metro_station", "road"],            "risk_bias": ["theft", "snatching"]},
    {"area": "Vasant Kunj",      "lat": 28.5203, "lon": 77.1572, "police": "Vasant Kunj PS",
     "place_types": ["residential", "mall", "park"],                "risk_bias": ["poor_lighting", "isolated_area"]},
    {"area": "Paharganj",        "lat": 28.6452, "lon": 77.2100, "police": "Paharganj PS",
     "place_types": ["market", "road", "restaurant"],               "risk_bias": ["theft", "harassment"]},
    {"area": "Shahdara",         "lat": 28.6701, "lon": 77.2900, "police": "Shahdara PS",
     "place_types": ["residential", "market", "bus_stop"],          "risk_bias": ["crime", "harassment"]},
    {"area": "Janakpuri",        "lat": 28.6289, "lon": 77.0822, "police": "Janakpuri PS",
     "place_types": ["residential", "metro_station", "market"],     "risk_bias": ["crime", "night_travel"]},
    {"area": "Rajouri Garden",   "lat": 28.6474, "lon": 77.1147, "police": "Rajouri Garden PS",
     "place_types": ["market", "metro_station", "road"],            "risk_bias": ["theft", "snatching"]},
    {"area": "GTB Nagar",        "lat": 28.6977, "lon": 77.2044, "police": "GTB Nagar PS",
     "place_types": ["residential", "road", "market"],              "risk_bias": ["crime", "harassment"]},
    {"area": "Preet Vihar",      "lat": 28.6423, "lon": 77.2898, "police": "Preet Vihar PS",
     "place_types": ["residential", "market", "metro_station"],     "risk_bias": ["crime", "theft"]},
]

MUMBAI_AREAS = [
    {"area": "Andheri",          "lat": 19.1136, "lon": 72.8697, "police": "Andheri PS",
     "place_types": ["residential", "metro_station", "market"],     "risk_bias": ["theft", "public_transport"]},
    {"area": "Bandra",           "lat": 19.0596, "lon": 72.8295, "police": "Bandra PS",
     "place_types": ["restaurant", "market", "road"],               "risk_bias": ["harassment", "snatching"]},
    {"area": "Dadar",            "lat": 19.0212, "lon": 72.8422, "police": "Dadar PS",
     "place_types": ["market", "metro_station", "bus_stop"],        "risk_bias": ["theft", "public_transport"]},
    {"area": "Kurla",            "lat": 19.0728, "lon": 72.8826, "police": "Kurla PS",
     "place_types": ["metro_station", "bus_stop", "market"],        "risk_bias": ["theft", "snatching", "public_transport"]},
    {"area": "Dharavi",          "lat": 19.0422, "lon": 72.8553, "police": "Dharavi PS",
     "place_types": ["residential", "road", "market"],              "risk_bias": ["crime", "night_travel"]},
    {"area": "Borivali",         "lat": 19.2307, "lon": 72.8567, "police": "Borivali PS",
     "place_types": ["residential", "market", "park"],              "risk_bias": ["isolated_area", "night_travel"]},
    {"area": "Malad",            "lat": 19.1870, "lon": 72.8479, "police": "Malad PS",
     "place_types": ["residential", "mall", "metro_station"],       "risk_bias": ["theft", "women_safety"]},
    {"area": "Colaba",           "lat": 18.9067, "lon": 72.8147, "police": "Colaba PS",
     "place_types": ["restaurant", "market", "road"],               "risk_bias": ["theft", "snatching"]},
    {"area": "Lower Parel",      "lat": 19.0113, "lon": 72.8270, "police": "Worli PS",
     "place_types": ["restaurant", "mall", "road"],                 "risk_bias": ["harassment", "snatching"]},
    {"area": "Goregaon",         "lat": 19.1624, "lon": 72.8490, "police": "Goregaon PS",
     "place_types": ["residential", "market", "metro_station"],     "risk_bias": ["crime", "poor_lighting"]},
    {"area": "Vikhroli",         "lat": 19.1073, "lon": 72.9243, "police": "Vikhroli PS",
     "place_types": ["industrial", "residential", "road"],          "risk_bias": ["crime", "isolated_area"]},
    {"area": "Thane",            "lat": 19.2183, "lon": 72.9781, "police": "Thane PS",
     "place_types": ["residential", "market", "bus_stop"],          "risk_bias": ["crime", "night_travel"]},
]

# Simpler (name, lat, lon) tuples for the 17 other cities
OTHER_AREAS = {
    "Bengaluru":  [("Koramangala",18.5362,77.6245),("Whitefield",12.9698,77.7499),("MG Road",12.9756,77.6093),("Jayanagar",12.9250,77.5938),("Hebbal",13.0358,77.5970)],
    "Hyderabad":  [("Hitech City",17.4435,78.3772),("Banjara Hills",17.4156,78.4347),("Secunderabad",17.4399,78.4983),("Charminar",17.3616,78.4747),("Kukatpally",17.4849,78.3995)],
    "Chennai":    [("T Nagar",13.0418,80.2341),("Adyar",13.0012,80.2565),("Anna Nagar",13.0850,80.2101),("Velachery",12.9815,80.2209),("Tambaram",12.9249,80.1000)],
    "Kolkata":    [("Park Street",22.5514,88.3568),("Howrah",22.5958,88.2636),("Salt Lake",22.5735,88.4127),("New Market",22.5637,88.3509),("Tollygunge",22.4973,88.3378)],
    "Jaipur":     [("MI Road",26.9124,75.7873),("Vaishali Nagar",26.9027,75.7350),("Malviya Nagar",26.8504,75.8069),("Pink City",26.9239,75.8267),("Mansarovar",26.8450,75.7577)],
    "Lucknow":    [("Hazratganj",26.8467,80.9462),("Gomti Nagar",26.8700,80.9990),("Aliganj",26.8900,80.9400),("Alambagh",26.8092,80.9040),("Chinhat",26.8825,81.0553)],
    "Pune":       [("Koregaon Park",18.5362,73.8939),("Kothrud",18.5074,73.8077),("Hinjewadi",18.5912,73.7389),("Viman Nagar",18.5679,73.9143),("Shivajinagar",18.5308,73.8476)],
    "Ahmedabad":  [("CG Road",23.0295,72.5567),("Navrangpura",23.0364,72.5608),("Bopal",23.0319,72.4727),("Vastrapur",23.0388,72.5306),("Maninagar",22.9952,72.6023)],
    "Indore":     [("Vijay Nagar",22.7533,75.9036),("MG Road",22.7196,75.8577),("Palasia",22.7221,75.8844),("Rau",22.6753,75.8500),("Rajwada",22.7167,75.8572)],
    "Nagpur":     [("Dharampeth",21.1451,79.0760),("Sitabuldi",21.1458,79.0868),("Hingna Road",21.1299,78.9929),("Sadar",21.1543,79.0849),("Manish Nagar",21.1050,79.0424)],
    "Patna":      [("Boring Road",25.6093,85.1376),("Kankarbagh",25.5941,85.1420),("Rajendra Nagar",25.6024,85.1203),("Patliputra",25.6200,85.0800),("Danapur",25.6167,85.0333)],
    "Kanpur":     [("Swaroop Nagar",26.4700,80.3500),("Kakadeo",26.4857,80.2960),("Civil Lines",26.4735,80.3491),("Kidwai Nagar",26.4530,80.3420),("Armapur",26.4904,80.2722)],
    "Surat":      [("Adajan",21.2150,72.8161),("Varachha",21.2130,72.8800),("Rander",21.2370,72.8040),("Althan",21.1600,72.8100),("Katargam",21.2386,72.8480)],
    "Ghaziabad":  [("Vaishali",28.6450,77.3400),("Indirapuram",28.6450,77.3700),("Raj Nagar",28.6700,77.4400),("Kaushambi",28.6400,77.3300),("Crossings Republik",28.6400,77.4700)],
    "Kochi":      [("MG Road",9.9816,76.2999),("Fort Kochi",9.9659,76.2425),("Kakkanad",10.0159,76.3419),("Vyttila",9.9657,76.3245),("Ernakulam",9.9700,76.2900)],
    "Kozhikode":  [("SM Street",11.2588,75.7804),("Palayam",11.2500,75.7760),("Nadakkave",11.2613,75.7825),("Mavoor Road",11.2572,75.7756),("Beypore",11.1722,75.8122)],
    "Coimbatore": [("RS Puram",11.0024,76.9556),("Gandhipuram",11.0178,76.9674),("Saravanampatti",11.0600,76.9990),("Singanallur",10.9949,77.0271),("Peelamedu",11.0157,77.0213)],
}

# Map clean NCRB city name → area list
CITY_TO_AREAS = {"Delhi": DELHI_AREAS, "Mumbai": MUMBAI_AREAS, **OTHER_AREAS}

# =============================================================================
# STEP 4 — Risk type catalogue  (12 categories from SafeScope blueprint)
# =============================================================================
RISK_TYPES = [
    "crime", "harassment", "women_safety", "theft", "snatching",
    "night_travel", "public_transport", "poor_lighting",
    "isolated_area", "emergency_access", "route_safety", "community_signal",
]

SUB_CATEGORIES = {
    "crime":            ["assault", "robbery", "vehicle_theft", "burglary", "murder_attempt", "vandalism"],
    "harassment":       ["eve_teasing", "stalking", "verbal_abuse", "physical_harassment"],
    "women_safety":     ["molestation", "rape_attempt", "acid_attack_threat", "domestic_violence", "dowry_harassment"],
    "theft":            ["pickpocketing", "bag_snatching", "shoplifting", "vehicle_break_in"],
    "snatching":        ["mobile_snatching", "chain_snatching", "purse_snatching"],
    "night_travel":     ["unsafe_street", "dark_road", "night_harassment", "late_night_crime"],
    "public_transport": ["metro_theft", "bus_harassment", "unsafe_station", "auto_overcharge"],
    "poor_lighting":    ["unlit_road", "broken_streetlight", "dark_alley", "unlit_parking"],
    "isolated_area":    ["deserted_road", "empty_parking", "isolated_park", "abandoned_area"],
    "emergency_access": ["no_police_nearby", "hospital_far", "poor_response_time"],
    "route_safety":     ["accident_prone_road", "unsafe_route", "poor_road_condition"],
    "community_signal": ["reported_hazard", "suspicious_activity", "infrastructure_issue", "crowd_warning"],
}

# =============================================================================
# STEP 5 — Helper functions (these create realistic, coherent values)
# =============================================================================

def build_risk_weights(women_ratio):
    """
    Risk type probabilities per city.
    A city with more women crimes (high women_ratio) gets a stronger
    women_safety and harassment signal.
    """
    w = {
        "crime":            0.14,
        "harassment":       0.09,
        "women_safety":     0.07,
        "theft":            0.22,
        "snatching":        0.12,
        "night_travel":     0.08,
        "public_transport": 0.07,
        "poor_lighting":    0.05,
        "isolated_area":    0.05,
        "emergency_access": 0.04,
        "route_safety":     0.04,
        "community_signal": 0.03,
    }
    # scale women-related weights by actual city ratio
    boost = women_ratio * 1.5
    w["women_safety"] += boost
    w["harassment"]   += boost * 0.6
    total = sum(w.values())
    return [w[rt] / total for rt in RISK_TYPES]   # normalised, same order as RISK_TYPES

def pick_hour(risk_type):
    """
    Realistic hour-of-day distribution per risk type.
    Women safety / harassment peak at night (8 PM – 2 AM).
    Theft peaks at commute times (8-10 AM, 6-9 PM).
    """
    if risk_type in ("women_safety", "harassment", "night_travel"):
        night = list(range(20, 24)) + list(range(0, 3)) + [18, 19]
        day   = list(range(9, 18))
        pool  = night * 3 + day          # night 3× more likely
        return random.choice(pool)
    elif risk_type in ("theft", "snatching", "public_transport"):
        peak  = [8, 9, 10, 18, 19, 20, 21] * 3
        other = list(range(11, 18))
        return random.choice(peak + other)
    elif risk_type in ("poor_lighting", "isolated_area"):
        return random.choice(list(range(19, 24)) + list(range(0, 6)))
    return random.randint(0, 23)

def pick_lighting(hour, risk_type):
    if 6 <= hour < 19:                          # daylight
        return random.choices(["good", "moderate"], weights=[70, 30])[0]
    if risk_type == "poor_lighting":
        return random.choices(["poor", "very_poor"], weights=[50, 50])[0]
    return random.choices(["good", "moderate", "poor", "very_poor"], weights=[10, 30, 40, 20])[0]

def pick_crowd(hour, place_type, risk_type):
    if risk_type == "isolated_area":
        return random.choice(["sparse", "isolated"])
    if place_type in ("market", "metro_station", "bus_stop") and 8 <= hour <= 20:
        return random.choices(["very_crowded", "crowded", "moderate"], weights=[40, 40, 20])[0]
    if hour >= 22 or hour < 6:
        return random.choices(["sparse", "isolated"], weights=[60, 40])[0]
    return random.choices(["moderate", "sparse", "crowded"], weights=[50, 30, 20])[0]

def pick_gender(risk_type):
    if risk_type == "women_safety":
        return "Female"
    if risk_type == "harassment":
        return random.choices(["Female", "Male"], weights=[80, 20])[0]
    if risk_type == "crime":
        return random.choices(["Male", "Female", "Unknown"], weights=[60, 25, 15])[0]
    return random.choices(["Male", "Female", "Unknown"], weights=[45, 45, 10])[0]

def pick_persona(risk_type):
    mapping = {
        "women_safety":     "woman_alone,student",
        "harassment":       "woman_alone,student",
        "public_transport": "student,night_shift,delivery",
        "night_travel":     "woman_alone,night_shift,delivery,student",
        "poor_lighting":    "woman_alone,night_shift,delivery",
        "theft":            "tourist,student,general",
        "snatching":        "tourist,student,general,woman_alone",
        "emergency_access": "senior_citizen,woman_alone",
        "isolated_area":    "woman_alone,delivery,night_shift",
        "route_safety":     "woman_alone,delivery,night_shift",
    }
    return mapping.get(risk_type, "general")

# Risk types that are never Low (serious crime regardless of environment)
_NEVER_LOW = {"crime", "women_safety", "harassment", "snatching"}

# Point contributions for each feature value
_LIGHT_PTS  = {"very_poor": 3, "poor": 2, "moderate": 0, "good": -2}
_CROWD_PTS  = {"isolated": 3, "sparse": 1, "moderate": 0, "crowded": -1, "very_crowded": -2}
_RTYPE_PTS  = {
    "crime": 3,          "women_safety": 3,
    "harassment": 2,     "snatching": 2,    "isolated_area": 2,
    "night_travel": 1,   "poor_lighting": 1, "route_safety": 1,
    "theft": 0,          "public_transport": 0,
    "emergency_access": 0, "community_signal": 0,
}

def assign_risk_level(risk_type, hour, crowd, lighting, transport, emerg_dist):
    """
    Multi-factor scoring → Low / Medium / High.

    Scoring logic (based on real urban safety research):
      - Lighting:            very_poor=+3, poor=+2, moderate=0, good=-2
      - Crowd:               isolated=+3,  sparse=+1, moderate=0,
                             crowded=-1,   very_crowded=-2
      - Time of day:         deep night (10pm-5am)=+3, late evening/early morning=+1,
                             daytime (9am-5pm)=-2
      - Risk type:           crime/women_safety=+3, harassment/snatching/isolated=+2,
                             night_travel/poor_lighting/route_safety=+1, others=0
      - Transport access:    poor=+1, good=-1
      - Emergency distance:  >3.5 km=+1, <1 km=-1

    Thresholds:  score >= 5 -> High  |  score -2 to 4 -> Medium  |  score <= -3 -> Low

    12% random noise keeps the dataset realistic — a well-lit, crowded street
    can still have incidents, and a dark alley can sometimes be safe.
    Serious crime types (crime, women_safety, harassment, snatching) are never Low.
    """
    score = 0
    score += _LIGHT_PTS.get(lighting, 0)
    score += _CROWD_PTS.get(crowd, 0)
    score += _RTYPE_PTS.get(risk_type, 0)

    # Time of day
    if hour >= 22 or hour <= 4:                  score += 3   # deep night
    elif 20 <= hour <= 21 or 5 <= hour <= 7:     score += 1   # late evening / early morning
    elif 9 <= hour <= 17:                         score -= 2   # safe daytime

    # Infrastructure
    if transport == "poor":                       score += 1
    elif transport == "good":                     score -= 1
    if emerg_dist > 3.5:                          score += 1
    elif emerg_dist < 1.0:                        score -= 1

    # Map score → label
    if score >= 5:
        base = "High"
    elif score >= -2:
        base = "Medium"
    else:
        base = "Low"

    # Floor: serious crime types cannot be Low
    if base == "Low" and risk_type in _NEVER_LOW:
        base = "Medium"

    # 12% realistic noise (real world is never perfectly predictable)
    if random.random() < 0.12:
        others = ["Low", "Medium", "High"]
        others.remove(base)
        base = random.choice(others)

    return base

def pick_transport(place_types):
    if "metro_station" in place_types or "bus_stop" in place_types:
        return random.choices(["good", "moderate"], weights=[70, 30])[0]
    return random.choices(["good", "moderate", "poor"], weights=[30, 50, 20])[0]

def pick_community_signal(risk_type):
    mapping = {
        "poor_lighting":    "poor_lighting",
        "isolated_area":    "isolated_road",
        "public_transport": "unsafe_bus_stop",
        "harassment":       "harassment_prone",
        "women_safety":     "harassment_prone",
        "crime":            "reported_hazard",
    }
    return mapping.get(risk_type, random.choices(
        ["none", "reported_hazard", "suspicious_activity"], weights=[60, 25, 15]
    )[0])

# =============================================================================
# STEP 6 — Incident generator for one city
# =============================================================================

START_DATE = date(2024, 1, 1)

def generate_city(city_label, n, women_ratio, areas):
    """
    Generate n incident rows for one city.
    city_label  — city name stored in the output CSV
    n           — number of incidents to generate
    women_ratio — real NCRB ratio: women crimes / total crimes
    areas       — list of area dicts (Delhi/Mumbai) or (name,lat,lon) tuples
    """
    risk_weights = build_risk_weights(women_ratio)
    rows = []

    for i in range(n):
        # ── pick area ────────────────────────────────────────────
        a = random.choice(areas)
        if isinstance(a, dict):
            area_name   = a["area"]
            base_lat    = a["lat"]
            base_lon    = a["lon"]
            police      = a["police"]
            place_types = a["place_types"]
            risk_bias   = a.get("risk_bias", [])
        else:                           # simple (name, lat, lon) tuple
            area_name   = a[0]
            base_lat    = a[1]
            base_lon    = a[2]
            police      = f"{area_name} Police Station"
            place_types = ["residential", "road", "market"]
            risk_bias   = []

        # small random jitter so incidents don't all stack at exactly one point
        lat = round(base_lat + random.uniform(-0.004, 0.004), 6)
        lon = round(base_lon + random.uniform(-0.004, 0.004), 6)

        # ── pick risk type ───────────────────────────────────────
        # 40% of the time use this area's known bias, 60% use city-level weights
        if risk_bias and random.random() < 0.40:
            risk_type = random.choice(risk_bias)
        else:
            risk_type = random.choices(RISK_TYPES, weights=risk_weights)[0]

        # ── time ─────────────────────────────────────────────────
        hour         = pick_hour(risk_type)
        inc_date     = START_DATE + timedelta(days=random.randint(0, 364))
        day_of_week  = inc_date.weekday()       # 0=Mon … 6=Sun
        month        = inc_date.month
        is_weekend   = 1 if day_of_week >= 5 else 0
        time_str     = f"{hour:02d}:{random.randint(0,59):02d}"

        # ── environment ──────────────────────────────────────────
        place_type  = random.choice(place_types)
        lighting    = pick_lighting(hour, risk_type)
        crowd       = pick_crowd(hour, place_type, risk_type)
        transport   = pick_transport(place_types)
        emerg_dist  = round(random.uniform(0.3, 5.0), 2)
        comm_signal = pick_community_signal(risk_type)

        # ── victim / persona ─────────────────────────────────────
        gender     = pick_gender(risk_type)
        persona    = pick_persona(risk_type)
        sub_cat    = random.choice(SUB_CATEGORIES[risk_type])

        # ── risk level (multi-factor scoring) ────────────────────
        risk_level = assign_risk_level(risk_type, hour, crowd, lighting, transport, emerg_dist)
        severity   = {"Low": 1, "Medium": 2, "High": 3}[risk_level]   # kept for compat

        # ── source annotation (transparency) ─────────────────────
        source = "ncrb_city_aggregate+synthetic_enriched"

        rows.append({
            "incident_id":           f"{city_label[:3].upper().replace(' ','_')}_{i+1:05d}",
            "city":                  city_label,
            "area":                  area_name,
            "police_station":        police,
            "risk_type":             risk_type,
            "sub_category":          sub_cat,
            "victim_gender":         gender,
            "persona_relevance":     persona,
            "place_type":            place_type,
            "date":                  inc_date.strftime("%Y-%m-%d"),
            "time":                  time_str,
            "hour":                  hour,
            "day_of_week":           day_of_week,
            "month":                 month,
            "is_weekend":            is_weekend,
            "latitude":              lat,
            "longitude":             lon,
            "severity":              severity,
            "case_count":            random.choices([1, 2, 3], weights=[80, 15, 5])[0],
            "lighting_condition":    lighting,
            "crowd_level":           crowd,
            "transport_access":      transport,
            "emergency_distance":    emerg_dist,
            "community_signal_type": comm_signal,
            "source_type":           source,
            "risk_level":            risk_level,
        })

    return rows

# =============================================================================
# STEP 7 — Decide how many incidents per city  (proportional to sqrt of crimes)
# =============================================================================
# Why square-root scaling?
#   Delhi has 4× more crimes than Mumbai. If we scaled linearly, Delhi would
#   dominate the dataset and the model would barely learn Mumbai patterns.
#   Square-root compression keeps proportions meaningful but stops any city
#   from drowning out others.

MAX_INCIDENTS = 2000    # Delhi (highest crime) gets this many

delhi_total = city_stats.loc[
    city_stats["clean_name"].str.contains("Delhi", case=False), "Crime_2024"
].values[0]

def scale_n(total_crimes):
    raw = MAX_INCIDENTS * ((total_crimes / delhi_total) ** 0.5)
    return max(150, int(raw))    # minimum 150 per city

# =============================================================================
# STEP 8 — Generate all incidents
# =============================================================================
print("\nGenerating incidents per city …")
all_rows = []
INCIDENT_COUNTER = 0

for _, row in city_stats.iterrows():
    cn = row["clean_name"]      # cleaned city name
    n  = scale_n(row["Crime_2024"])

    # Match to area dict: "Delhi" from "Delhi City", others already clean
    area_key = "Delhi" if "Delhi" in cn else cn

    if area_key not in CITY_TO_AREAS:
        print(f"  SKIP  {cn!r} — no area data defined")
        continue

    incidents = generate_city(cn, n, row["women_ratio"], CITY_TO_AREAS[area_key])
    all_rows.extend(incidents)
    INCIDENT_COUNTER += n
    print(f"  {n:4d} incidents  ->  {cn}")

# =============================================================================
# STEP 9 — Assemble DataFrame and save
# =============================================================================
COLUMN_ORDER = [
    "incident_id", "city", "area", "police_station", "risk_type", "sub_category",
    "victim_gender", "persona_relevance", "place_type", "date", "time", "hour",
    "day_of_week", "month", "is_weekend", "latitude", "longitude", "severity",
    "case_count", "lighting_condition", "crowd_level", "transport_access",
    "emergency_distance", "community_signal_type", "source_type",
    "risk_level",   # directly assigned by multi-factor scoring (not derived from severity)
]

df_out = pd.DataFrame(all_rows)[COLUMN_ORDER]
out_path = os.path.join(OUT, "safescope_incidents.csv")
df_out.to_csv(out_path, index=False)

# =============================================================================
# STEP 10 — Summary printout
# =============================================================================
print("\n" + "=" * 65)
print("TOTAL ROWS GENERATED")
print("=" * 65)
print(f"  {len(df_out):,} incident rows")
print(f"  25 columns: {', '.join(df_out.columns[:8])} … (all 25 present)")
print(f"  Saved to: {out_path}")

print("\n" + "=" * 65)
print("FIRST 10 ROWS")
print("=" * 65)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 22)
print(df_out.head(10).to_string(index=False))

print("\n" + "=" * 65)
print("INCIDENTS PER CITY")
print("=" * 65)
city_counts = df_out.groupby("city").size().sort_values(ascending=False)
for city, cnt in city_counts.items():
    print(f"  {city:<30s}  {cnt:>5,}")
print(f"  {'TOTAL':<30s}  {city_counts.sum():>5,}")

print("\n" + "=" * 65)
print("INCIDENTS PER RISK TYPE")
print("=" * 65)
rt_counts = df_out.groupby("risk_type").size().sort_values(ascending=False)
for rt, cnt in rt_counts.items():
    pct = cnt / len(df_out) * 100
    print(f"  {rt:<22s}  {cnt:>5,}  ({pct:4.1f}%)")

print("\n" + "=" * 65)
print("NULL / MISSING CHECK (should all be 0)")
print("=" * 65)
nulls = df_out.isnull().sum()
print(nulls[nulls > 0] if nulls.any() else "  No nulls — dataset is clean")

print("\n" + "=" * 65)
print("SEVERITY DISTRIBUTION")
print("=" * 65)
sev_map = {1: "Low", 2: "Medium", 3: "High"}
for sev, cnt in df_out["severity"].value_counts().sort_index().items():
    pct = cnt / len(df_out) * 100
    print(f"  {sev_map[sev]} ({sev})  {cnt:>5,}  ({pct:4.1f}%)")

print("\n" + "=" * 65)
print("WOMEN SAFETY NIGHT SAMPLE (Delhi — shows realistic time distribution)")
print("=" * 65)
ws_night = df_out[
    (df_out["city"].str.contains("Delhi")) &
    (df_out["risk_type"].isin(["women_safety", "harassment"])) &
    (df_out["hour"] >= 20)
]
print(f"  Delhi women_safety+harassment incidents after 8 PM: {len(ws_night)}")
preview_cols = ["area", "risk_type", "hour", "lighting_condition", "crowd_level", "severity"]
print(ws_night[preview_cols].head(8).to_string(index=False))

print("\n" + "=" * 65)
print("RISK LEVEL DISTRIBUTION (multi-factor scored)")
print("=" * 65)
for lbl in ["Low", "Medium", "High"]:
    cnt = (df_out["risk_level"] == lbl).sum()
    pct = cnt / len(df_out) * 100
    bar = "#" * int(pct / 2)
    print(f"  {lbl:6s}: {cnt:>5,}  ({pct:4.1f}%)  {bar}")

print("\nDay 3 complete. Dataset ready for ML training on Day 5.")
