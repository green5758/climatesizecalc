#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ClimateSizeCalc - Interactive Room BTU, Mini-Split, Dehumidifier & HEPA CADR Calculator
+ Automated Daily Amazon Product Review Publisher
Affiliate StoreID: everythi00099-20
"""

import os
import json
import hashlib
import datetime
import urllib.request
import urllib.parse
import urllib.error

AFFILIATE_TAG = "everythi00099-20"
STATE_FILE = "posts_state.json"
OUTPUT_DIR = "public"
REVIEWS_DIR = os.path.join(OUTPUT_DIR, "reviews")
DAILY_NEW_ARTICLES = 3

# Deteksi otomatis URL GitHub Pages dari environment GitHub Actions
REPO_FULL = os.environ.get("GITHUB_REPOSITORY", "username/climatesizecalc")
REPO_OWNER = os.environ.get("GITHUB_REPOSITORY_OWNER", REPO_FULL.split("/")[0])
REPO_NAME = REPO_FULL.split("/")[-1] if "/" in REPO_FULL else "climatesizecalc"

if REPO_NAME.lower() == f"{REPO_OWNER.lower()}.github.io":
    BASE_URL = f"https://{REPO_OWNER.lower()}.github.io"
else:
    BASE_URL = f"https://{REPO_OWNER.lower()}.github.io/{REPO_NAME}"

INDEXNOW_KEY = hashlib.md5(f"climatesizecalc-{AFFILIATE_TAG}".encode("utf-8")).hexdigest()


def amazon_search_url(query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.amazon.com/s?k={encoded}&tag={AFFILIATE_TAG}"


# ==============================================================================
# MASTER BEST SELLER & COMPARISON CATALOG (10 FLAGSHIP PRODUCTS)
# ==============================================================================
CORE_PRODUCTS = [
    {
        "id": "midea-duo-14000-btu-inverter-ac",
        "name": "Midea Duo 14,000 BTU (12,000 SACC) Smart Inverter Portable AC",
        "brand": "Midea",
        "category": "Portable Air Conditioner",
        "sq_ft": 550,
        "btu_or_cap": "14,000 BTU (ASHRAE)",
        "btu_num": 14000,
        "noise_db": "42 dBA",
        "efficiency": "Variable-Speed Inverter (CEER 10.8)",
        "rating": "4.6",
        "reviews_count": 8420,
        "badge": "#1 Best Selling Portable AC",
        "search_query": "Midea Duo 14000 BTU Smart Inverter Portable Air Conditioner Dual Hose",
        "highlight": "Dual-hose hose-in-hose design prevents negative room pressure, cools up to 550 sq. ft. 2x faster with 40% less energy."
    },
    {
        "id": "senville-let-12000-btu-minisplit",
        "name": "Senville LETO 12,000 BTU Ductless Mini-Split AC & Heat Pump",
        "brand": "Senville",
        "category": "Ductless Mini-Split",
        "sq_ft": 600,
        "btu_or_cap": "12,000 BTU Cooling/Heating",
        "btu_num": 12000,
        "noise_db": "27 dBA",
        "efficiency": "19 SEER2 Inverter + Alexa Wi-Fi",
        "rating": "4.6",
        "reviews_count": 6910,
        "badge": "Best Value Mini-Split",
        "search_query": "Senville LETO 12000 BTU Mini Split Air Conditioner Heat Pump",
        "highlight": "Whisper-quiet 4-in-1 DC inverter heat pump with pre-charged R454B/R410A line set for bedrooms, garages, and sunrooms."
    },
    {
        "id": "lg-10000-btu-dual-inverter-window",
        "name": "LG 10,000 BTU Dual Inverter Smart Wi-Fi Window Air Conditioner",
        "brand": "LG",
        "category": "Window Air Conditioner",
        "sq_ft": 450,
        "btu_or_cap": "10,000 BTU (DOE)",
        "btu_num": 10000,
        "noise_db": "44 dBA",
        "efficiency": "Energy Star Dual Inverter",
        "rating": "4.6",
        "reviews_count": 9850,
        "badge": "Quietest Window AC",
        "search_query": "LG 10000 BTU Dual Inverter Smart Window Air Conditioner",
        "highlight": "Dual-rotor compressor eliminates start-stop vibration, delivering ultra-quiet bedroom cooling for rooms up to 450 sq. ft."
    },
    {
        "id": "pioneer-diamante-18000-btu-minisplit",
        "name": "Pioneer Diamante Ultra 18,000 BTU 230V Ductless Mini-Split Heat Pump",
        "brand": "Pioneer",
        "category": "Ductless Mini-Split",
        "sq_ft": 1000,
        "btu_or_cap": "18,000 BTU (1.5 Ton)",
        "btu_num": 18000,
        "noise_db": "31 dBA",
        "efficiency": "20 SEER2 Energy Star",
        "rating": "4.7",
        "reviews_count": 4380,
        "badge": "Best for Large Open Rooms",
        "search_query": "Pioneer Diamante 18000 BTU 230V Ductless Mini Split Heat Pump",
        "highlight": "Heavy-duty 1.5-ton inverter heat pump capable of heating down to -13°F and cooling open living rooms up to 1,000 sq. ft."
    },
    {
        "id": "homelabs-50-pint-dehumidifier",
        "name": "hOmeLabs 50-Pint (70-Pint 2012 DOE) Energy Star Dehumidifier",
        "brand": "hOmeLabs",
        "category": "Dehumidifier",
        "sq_ft": 4500,
        "btu_or_cap": "50 Pints / Day",
        "btu_num": 14000,
        "noise_db": "48 dBA",
        "efficiency": "Energy Star Most Efficient",
        "rating": "4.6",
        "reviews_count": 48200,
        "badge": "#1 Best Selling Dehumidifier",
        "search_query": "hOmeLabs 50 Pint Energy Star Dehumidifier for Basement",
        "highlight": "Built-in Turbo fan and continuous drain hose outlet extract up to 50 pints of moisture daily from damp basements and crawlspaces."
    },
    {
        "id": "midea-cube-50-pint-smart-dehumidifier",
        "name": "Midea Cube 50-Pint Smart Wi-Fi Dehumidifier with Built-in Pump",
        "brand": "Midea",
        "category": "Dehumidifier",
        "sq_ft": 4500,
        "btu_or_cap": "50 Pints + Vertical Pump",
        "btu_num": 15000,
        "noise_db": "45 dBA",
        "efficiency": "Energy Star + 3x Bucket Lift",
        "rating": "4.6",
        "reviews_count": 12400,
        "badge": "Best Basement Pump Model",
        "search_query": "Midea Cube 50 Pint Dehumidifier with Pump Smart WiFi",
        "highlight": "Nested lift-and-twist design holds 3x more water (4.2 gallons) or pumps water vertically up to 16 feet into a utility sink."
    },
    {
        "id": "coway-airmega-400-hepa-purifier",
        "name": "Coway Airmega 400 Dual-Suction True HEPA Air Purifier",
        "brand": "Coway",
        "category": "HEPA Air Purifier",
        "sq_ft": 1560,
        "btu_or_cap": "350 CFM CADR",
        "btu_num": 16000,
        "noise_db": "22 dBA",
        "efficiency": "Dual Green True HEPA H13",
        "rating": "4.8",
        "reviews_count": 7650,
        "badge": "Top Whole-Floor HEPA",
        "search_query": "Coway Airmega 400 True HEPA Air Purifier 1560 sq ft",
        "highlight": "Dual-sided Max2 activated carbon + True HEPA filters capture 99.999% of nano-sized smoke, pollen, mold spores, and VOCs."
    },
    {
        "id": "levoit-core-600s-smart-hepa",
        "name": "LEVOIT Core 600S Smart True HEPA Air Purifier (410 CFM CADR)",
        "brand": "LEVOIT",
        "category": "HEPA Air Purifier",
        "sq_ft": 1588,
        "btu_or_cap": "410 CFM CADR",
        "btu_num": 14000,
        "noise_db": "26 dBA",
        "efficiency": "VortexAir 3.0 + PM2.5 Laser",
        "rating": "4.8",
        "reviews_count": 19300,
        "badge": "Best CADR-Per-Dollar",
        "search_query": "LEVOIT Core 600S Smart Air Purifier Large Room 410 CADR",
        "highlight": "Delivers 410 CFM Clean Air Delivery Rate to scrub a 635 sq. ft. room 5 times per hour or 1,588 sq. ft. once every 30 minutes."
    },
    {
        "id": "black-decker-8000-btu-portable-ac",
        "name": "BLACK+DECKER 8,000 BTU Portable Air Conditioner with Remote",
        "brand": "BLACK+DECKER",
        "category": "Portable Air Conditioner",
        "sq_ft": 350,
        "btu_or_cap": "8,000 BTU (ASHRAE)",
        "btu_num": 8000,
        "noise_db": "51 dBA",
        "efficiency": "3-in-1 Cool/Dehumidify/Fan",
        "rating": "4.5",
        "reviews_count": 41500,
        "badge": "Best Budget Bedroom AC",
        "search_query": "BLACK+DECKER 8000 BTU Portable Air Conditioner",
        "highlight": "Self-evaporating bucketless operation with slide-out washable filter and 5-minute window kit installation for apartments and dorms."
    },
    {
        "id": "dreo-1500w-smart-infrared-ptc-heater",
        "name": "Dreo Solaris Max 1500W (5,120 BTU) Smart PTC Ceramic Tower Heater",
        "brand": "Dreo",
        "category": "Space Heater",
        "sq_ft": 300,
        "btu_or_cap": "5,120 BTU (1500W)",
        "btu_num": 6000,
        "noise_db": "34 dBA",
        "efficiency": "Hyperamics PTC + Digital Eco Stat",
        "rating": "4.8",
        "reviews_count": 22100,
        "badge": "Best Supplemental Heater",
        "search_query": "Dreo Space Heater 1500W Smart Oscillating PTC Ceramic Tower Heater",
        "highlight": "70-degree wide oscillation, ETL tip-over/overheat protection, and 41-95°F precision thermostat for instant zone heating."
    }
]


# ==============================================================================
# COMBINATORIAL ENGINE FOR 1,800 UNIQUE DAILY PRODUCT REVIEW ARTICLES
# ==============================================================================
BRANDS_MATRIX = [
    ("Midea", "Variable-Speed DC Inverter Compressor & Duo-Air Ducting"),
    ("Senville", "Golden Fin Anti-Corrosive Condenser & Low-Ambient Inverter Heat Pump"),
    ("LG", "Dual Inverter Rotor Compressor & ThinQ Smart Energy Telemetry"),
    ("Pioneer", "Diamante Ultra High-SEER2 DC Inverter & Follow-Me Remote Thermostat"),
    ("hOmeLabs", "High-CFM Centrifugal Moisture Extractor & Auto-Defrost Evaporator Coils"),
    ("Coway", "Airmega Dual-Suction Green True HEPA H13 & Smart Eco Particulate Sensor"),
    ("LEVOIT", "VortexAir 360-Degree Intake & AirSight Plus Laser PM2.5 Scanner"),
    ("Frigidaire", "Effortless Humidity Control & PureAir Allergen Capture Stage"),
    ("Hisense", "Quiet-Mode Twin-Rotary Inverter & Self-Evaporative Condensate Mist"),
    ("Whynter", "ARC-Series Dual-Hose Negative-Pressure Prevention & Activated Carbon Matrix"),
    ("Friedrich", "Kühl Commercial-Grade Steel Chassis & QuietMaster Acoustic Insulation"),
    ("Honeywell", "Thermal Overload Protection & Dual-Stage Electrostatic Pre-Filtration"),
    ("Blueair", "HEPASilent Electrostatic + Mechanical Filtration & Whisper-Low dBA Fan"),
    ("De'Longhi", "Pinguino Eco-Real Feel Humidity/Temp Balancing & BioSilver Tech"),
    ("Cooper&Hunter", "Sophia Hyper-Heat Inverter Architecture & Multi-Zone Whisper Blower"),
]

MODELS_MATRIX = [
    ("8,000 BTU Smart Portable Air Conditioner", 8000, 350, "25 Pints/Day", 210, 46, "Portable Air Conditioner"),
    ("10,000 BTU Dual-Inverter Window AC", 10000, 450, "30 Pints/Day", 260, 43, "Window Air Conditioner"),
    ("12,000 BTU Dual-Hose Inverter Portable AC", 12000, 500, "40 Pints/Day", 310, 42, "Portable Air Conditioner"),
    ("14,000 BTU High-Output Dual-Hose AC", 14000, 600, "48 Pints/Day", 360, 44, "Portable Air Conditioner"),
    ("9,000 BTU 21-SEER2 Ductless Mini-Split Heat Pump", 9000, 425, "28 Pints/Day", 280, 25, "Ductless Mini-Split"),
    ("12,000 BTU 20-SEER2 Inverter Mini-Split System", 12000, 600, "36 Pints/Day", 340, 27, "Ductless Mini-Split"),
    ("18,000 BTU (1.5-Ton) 230V Mini-Split Heat Pump", 18000, 950, "52 Pints/Day", 490, 31, "Ductless Mini-Split"),
    ("24,000 BTU (2-Ton) Whole-Zone Ductless Heat Pump", 24000, 1350, "65 Pints/Day", 620, 34, "Ductless Mini-Split"),
    ("35-Pint Energy Star Basement Dehumidifier", 9500, 2500, "35 Pints/Day", 225, 46, "Dehumidifier"),
    ("50-Pint Continuous-Pump Smart Dehumidifier", 14000, 4500, "50 Pints/Day", 320, 45, "Dehumidifier"),
    ("320 CFM CADR True HEPA H13 Air Purifier", 10000, 1250, "N/A (HEPA)", 320, 24, "HEPA Air Purifier"),
    ("420 CFM CADR Extra-Large Room HEPA + Carbon Purifier", 15000, 1650, "N/A (HEPA)", 420, 26, "HEPA Air Purifier"),
]

APPLICATIONS_MATRIX = [
    ("Master Bedroom & Light-Sleeper Acoustic Comfort", "maintains ultra-low decibel levels below 44 dBA while eliminating overnight humidity spikes"),
    ("South-Facing Living Room with High Solar Heat Gain", "compensates for intense afternoon window irradiance without compressor short-cycling"),
    ("Damp Basement, Crawlspace & Mold-Prevention Zone", "keeps relative humidity strictly between 45% and 50% RH to halt mildew and musty odors"),
    ("Home Office, Server Closet & Studio Electronics Cooling", "removes continuous sensible heat output from workstations while keeping microphone noise floor low"),
    ("Two-Car Garage Workshop & Home Gym Climate Control", "overcomes uninsulated garage door thermal transfer during peak summer and winter extremes"),
    ("Open-Concept Loft & Vaulted Ceiling Apartment", "circulates high-CFM conditioned airflow across tall 10-foot to 12-foot ceiling volumes"),
    ("Wildfire Smoke, Pet Dander & Seasonal Allergy Defense", "achieves 4.8+ Air Changes Per Hour (ACH) to strip PM2.5 particulates and volatile organic compounds"),
    ("Sunroom, Florida Room & Three-Season Patio Enclosure", "handles surrounded glass thermal loads with variable-speed inverter modulation"),
    ("Nursery, Kids Bedroom & Asthma-Safe Sleeping Environment", "combines draft-free temperature stabilization with medical-grade particulate scrubbing"),
    ("RV, Tiny Home & Accessory Dwelling Unit (ADU) Efficiency", "draws minimal startup amperage on standard household circuits while maximizing BTU per watt"),
]


def get_article_blueprint(index: int) -> dict:
    """Secara deterministik menghasilkan artikel review produk HVAC/Air Quality unik berdasarkan indeks."""
    b_idx = index % len(BRANDS_MATRIX)
    m_idx = (index // len(BRANDS_MATRIX)) % len(MODELS_MATRIX)
    a_idx = (index // (len(BRANDS_MATRIX) * len(MODELS_MATRIX))) % len(APPLICATIONS_MATRIX)

    brand_name, brand_tech = BRANDS_MATRIX[b_idx]
    model_name, btu_equiv, max_sqft, moisture_cap, cfm_rate, noise_dba, category = MODELS_MATRIX[m_idx]
    app_title, app_benefit = APPLICATIONS_MATRIX[a_idx]

    est_watts = round(btu_equiv / 11.2)
    ach_48_sqft = round((cfm_rate * 60) / (8.0 * 4.8))

    slug = f"review-{brand_name.lower().replace('&', '').replace(' ', '-')}-{model_name.lower().replace(',', '').replace('(', '').replace(')', '').replace('/', '').replace(' ', '-')}-{app_title.lower().split()[0]}-{app_title.lower().split()[1]}-{index + 1}"
    slug = "".join(c if c.isalnum() or c == "-" else "" for c in slug)
    while "--" in slug:
        slug = slug.replace("--", "-")

    title = f"{brand_name} {model_name} Review: Tested for {app_title}"
    search_q = f"{brand_name} {model_name}"

    return {
        "index": index,
        "slug": slug,
        "title": title,
        "brand": brand_name,
        "brand_tech": brand_tech,
        "model_name": model_name,
        "category": category,
        "btu_equiv": btu_equiv,
        "max_sqft": max_sqft,
        "moisture_cap": moisture_cap,
        "cfm_rate": cfm_rate,
        "ach_48_sqft": ach_48_sqft,
        "noise_dba": noise_dba,
        "est_watts": est_watts,
        "app_title": app_title,
        "app_benefit": app_benefit,
        "rating": "4.8" if (index % 2 == 0) else "4.7",
        "search_query": search_q,
        "affiliate_url": amazon_search_url(search_q),
    }


def load_and_advance_state() -> tuple[list[dict], list[dict]]:
    """
    Memuat daftar artikel dari posts_state.json dan menambahkan 3 artikel review baru setiap hari.
    """
    today_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {
            "last_run_date": "",
            "next_index": 0,
            "published_articles": []
        }

    newly_added = []
    if len(state["published_articles"]) == 0:
        count_to_add = 6  # Inisialisasi awal 6 artikel
    else:
        count_to_add = DAILY_NEW_ARTICLES  # Tambah 3 artikel berbeda setiap eksekusi harian

    for _ in range(count_to_add):
        idx = state["next_index"]
        bp = get_article_blueprint(idx)
        entry = {
            "index": idx,
            "slug": bp["slug"],
            "date": today_str,
            "title": bp["title"]
        }
        state["published_articles"].append(entry)
        newly_added.append({**bp, "date": today_str})
        state["next_index"] = idx + 1

    state["last_run_date"] = today_str

    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    all_articles = []
    for item in reversed(state["published_articles"]):
        bp = get_article_blueprint(item["index"])
        bp["date"] = item["date"]
        all_articles.append(bp)

    return all_articles, newly_added


# ==============================================================================
# SHARED CSS — INDUSTRIAL ARCHITECTURAL GREY THEME
# ==============================================================================
GLOBAL_CSS = """
:root {
  --bg-page: #cbd5e1;        /* Abu-abu utama (Slate Grey background sesuai instruksi) */
  --bg-section: #e2e8f0;     /* Abu-abu medium untuk kontainer bagian */
  --bg-card: #f1f5f9;        /* Abu-abu terang untuk kartu produk & kalkulator */
  --bg-dark: #1e293b;        /* Abu-abu arang gelap untuk header & tabel */
  --bg-darker: #0f172a;      /* Slate pekat untuk banner & footer */
  --border-grey: #94a3b8;    /* Garis tepi abu-abu tegas */
  --text-main: #0f172a;
  --text-muted: #334155;
  --accent-amazon: #ff9900;
  --accent-blue: #0284c7;
  --accent-green: #15803d;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: var(--bg-page);
  color: var(--text-main);
  line-height: 1.6;
}
a { color: var(--accent-blue); text-decoration: none; }
.container { max-width: 1240px; margin: 0 auto; padding: 0 18px; }

/* TOP PROMOTIONAL BANNER */
.top-promo-banner {
  background: linear-gradient(90deg, #0f172a 0%, #334155 50%, #1e293b 100%);
  color: #ffffff;
  padding: 12px 16px;
  border-bottom: 3px solid var(--accent-amazon);
  text-align: center;
  font-size: 0.94rem;
}
.top-promo-banner .badge-live {
  background: var(--accent-amazon);
  color: #0f172a;
  font-weight: 900;
  padding: 3px 10px;
  border-radius: 4px;
  margin-right: 10px;
  text-transform: uppercase;
  font-size: 0.78rem;
}
.top-promo-banner a.banner-cta {
  display: inline-block;
  margin-left: 12px;
  background: #38bdf8;
  color: #0f172a;
  font-weight: 800;
  padding: 4px 14px;
  border-radius: 5px;
  text-decoration: none;
}
.top-promo-banner a.banner-cta:hover { background: #7dd3fc; }

/* HEADER & NAVIGATION */
header.site-header {
  background-color: var(--bg-dark);
  color: #f8fafc;
  padding: 16px 0;
  box-shadow: 0 3px 10px rgba(0,0,0,0.22);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-flex {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 14px;
}
.brand-logo {
  font-size: 1.55rem;
  font-weight: 900;
  color: #ffffff;
  letter-spacing: -0.5px;
}
.brand-logo span { color: var(--accent-amazon); }
.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  list-style: none;
}
.nav-links a {
  color: #e2e8f0;
  font-weight: 600;
  font-size: 0.92rem;
  padding: 6px 10px;
  border-radius: 5px;
}
.nav-links a:hover { background: #334155; color: var(--accent-amazon); }

/* HERO BANNER */
.hero-banner {
  background: linear-gradient(135deg, #334155 0%, #1e293b 100%);
  color: #f8fafc;
  padding: 34px 26px;
  margin: 24px 0;
  border-radius: 12px;
  border: 2px solid #64748b;
  box-shadow: 0 8px 20px rgba(0,0,0,0.14);
}
.hero-grid {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 24px;
  align-items: center;
}
@media (max-width: 860px) { .hero-grid { grid-template-columns: 1fr; } }
.hero-banner h1 {
  font-size: 2.05rem;
  line-height: 1.22;
  margin-bottom: 12px;
  color: #ffffff;
}
.hero-banner p { color: #cbd5e1; font-size: 1.03rem; margin-bottom: 18px; }
.hero-deal-box {
  background: #0f172a;
  border: 2px solid var(--accent-amazon);
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
.hero-deal-box h3 { color: var(--accent-amazon); margin-bottom: 8px; font-size: 1.18rem; }

/* AMAZON CTA BUTTONS */
.btn-amazon {
  display: inline-block;
  background: linear-gradient(180deg, #ffd814 0%, #ff9900 100%);
  color: #0f172a !important;
  font-weight: 800;
  padding: 11px 18px;
  border-radius: 6px;
  border: 1px solid #d97706;
  text-align: center;
  cursor: pointer;
  text-decoration: none;
  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
}
.btn-amazon:hover { background: linear-gradient(180deg, #f7ca00 0%, #e68a00 100%); }
.btn-outline {
  display: inline-block;
  padding: 9px 14px;
  border: 2px solid #1e293b;
  color: #0f172a;
  font-weight: 700;
  border-radius: 6px;
  font-size: 0.88rem;
}
.btn-outline:hover { background: #1e293b; color: #ffffff; }

/* GREY SECTION WRAPPERS */
.grey-section {
  background-color: var(--bg-section);
  border: 1px solid var(--border-grey);
  border-radius: 12px;
  padding: 26px;
  margin-bottom: 26px;
  box-shadow: 0 3px 8px rgba(0,0,0,0.06);
}
.section-title {
  font-size: 1.55rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 8px;
  border-left: 6px solid var(--accent-amazon);
  padding-left: 12px;
}
.section-sub { color: var(--text-muted); margin-bottom: 20px; font-size: 0.96rem; }

/* INTERACTIVE CALCULATOR */
.calc-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
@media (max-width: 860px) { .calc-grid { grid-template-columns: 1fr; } }
.calc-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  padding: 22px;
  border-radius: 10px;
}
.preset-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.preset-btn {
  background: #cbd5e1;
  border: 1px solid #64748b;
  color: #0f172a;
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 0.83rem;
  font-weight: 700;
  cursor: pointer;
}
.preset-btn:hover { background: #94a3b8; }
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.form-group { margin-bottom: 14px; }
.form-group label {
  display: block;
  font-weight: 700;
  margin-bottom: 5px;
  font-size: 0.9rem;
  color: #1e293b;
}
.form-group input, .form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #64748b;
  border-radius: 6px;
  background: #ffffff;
  font-size: 0.98rem;
  color: #0f172a;
}
.metrics-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.metric-card {
  background: #e2e8f0;
  border: 1px solid #94a3b8;
  padding: 14px;
  border-radius: 8px;
  text-align: center;
}
.metric-card .val {
  font-size: 1.55rem;
  font-weight: 900;
  color: #0f172a;
}
.metric-card .lbl {
  font-size: 0.78rem;
  font-weight: 700;
  color: #334155;
  text-transform: uppercase;
}
.rec-box {
  background: #ffffff;
  border: 2px solid var(--accent-green);
  border-radius: 8px;
  padding: 16px;
  margin-top: 12px;
}
.rec-box h4 { color: var(--accent-green); font-size: 1.04rem; margin-bottom: 6px; }

/* SEARCH & FILTER BAR */
.search-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 18px;
}
.search-input {
  flex: 1;
  min-width: 240px;
  padding: 12px 15px;
  border: 2px solid #475569;
  border-radius: 8px;
  font-size: 1rem;
  background: #ffffff;
}
.filter-select {
  padding: 12px 15px;
  border: 2px solid #475569;
  border-radius: 8px;
  font-size: 0.95rem;
  background: #ffffff;
  font-weight: 700;
}

/* PRODUCT CARDS & DAILY ARTICLES GRID */
.product-grid, .articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 18px;
}
.product-card, .article-card {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.badge-tag {
  display: inline-block;
  background: #1e293b;
  color: var(--accent-amazon);
  font-size: 0.75rem;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 4px;
  margin-bottom: 10px;
  align-self: flex-start;
  text-transform: uppercase;
}
.spec-box {
  list-style: none;
  margin: 10px 0 14px;
  font-size: 0.88rem;
  background: #e2e8f0;
  padding: 10px 12px;
  border-radius: 6px;
}
.spec-box li { margin-bottom: 4px; }

/* COMPARISON TABLE */
.table-wrap { overflow-x: auto; }
table.comp-table {
  width: 100%;
  border-collapse: collapse;
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
}
table.comp-table th {
  background: #1e293b;
  color: #ffffff;
  text-align: left;
  padding: 13px 12px;
  font-size: 0.86rem;
  text-transform: uppercase;
}
table.comp-table td {
  padding: 12px;
  border-bottom: 1px solid #cbd5e1;
  font-size: 0.91rem;
}
table.comp-table tr:nth-child(even) { background: #e2e8f0; }

/* FAQ ACCORDION */
details.faq-item {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  border-radius: 8px;
  padding: 14px 18px;
  margin-bottom: 12px;
}
details.faq-item summary {
  font-weight: 800;
  font-size: 1.02rem;
  cursor: pointer;
  color: #0f172a;
}
details.faq-item p { margin-top: 10px; color: #334155; font-size: 0.95rem; }

/* SITEMAP DIRECTORY LIST */
.sitemap-columns {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
.sitemap-box {
  background: var(--bg-card);
  border: 1px solid var(--border-grey);
  padding: 18px;
  border-radius: 8px;
}
.sitemap-box h3 { margin-bottom: 10px; font-size: 1.1rem; color: #0f172a; }
.sitemap-box ul { padding-left: 18px; font-size: 0.9rem; line-height: 1.8; }

/* FOOTER */
footer.site-footer {
  background: var(--bg-darker);
  color: #cbd5e1;
  padding: 36px 0;
  margin-top: 40px;
  border-top: 4px solid var(--accent-amazon);
  font-size: 0.9rem;
}
.footer-links {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 14px;
}
.footer-links a { color: #f8fafc; font-weight: 600; }
"""


# ==============================================================================
# HTML PAGE GENERATORS
# ==============================================================================
def build_article_page(article: dict, recent_articles: list[dict]) -> str:
    """Membangun halaman HTML artikel review produk harian lengkap dengan kalkulator ruangan & schema SEO."""
    related_links = ""
    for rel in recent_articles[:8]:
        if rel["slug"] == article["slug"]:
            continue
        related_links += f"""
        <li>
          <a href="{BASE_URL}/reviews/{rel['slug']}.html"><strong>{rel['title']}</strong></a>
          <span> ({rel['max_sqft']} sq. ft. / {rel['noise_dba']} — {rel['date']})</span>
        </li>
        """

    room_scenarios = [
        ("Small Bedroom / Home Office (150 sq. ft.)", 150, 8),
        ("Standard Master Bedroom (300 sq. ft.)", 300, 8),
        ("Sunny Living Room (450 sq. ft.)", 450, 9),
        ("Open Studio / Garage Workshop (650 sq. ft.)", 650, 9),
        ("Large Open Floor Plan (950 sq. ft.)", 950, 10),
    ]
    scenario_rows = ""
    for r_name, sqft, ceil in room_scenarios:
        needed_btu = round(sqft * 22 * (ceil / 8.0))
        fit_status = "Optimal Sizing Match" if article["max_sqft"] >= sqft else "Supplemental / Multi-Unit Needed"
        scenario_rows += f"""
        <tr>
          <td><strong>{r_name}</strong></td>
          <td>{sqft} sq. ft. ({sqft * ceil} cu. ft.)</td>
          <td>~{needed_btu:,} BTU/hr</td>
          <td>{fit_status}</td>
        </tr>
        """

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"What room size does the {article['brand']} {article['model_name']} cover?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"The {article['brand']} {article['model_name']} is rated for rooms up to {article['max_sqft']} square feet with an airflow rate of {article['cfm_rate']} CFM and an acoustic profile of {article['noise_dba']}."
                }
            },
            {
                "@type": "Question",
                "name": f"How much electricity does the {article['brand']} {article['model_name']} use?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Under normal variable-load operation, it draws approximately {article['est_watts']}W thanks to {article['brand_tech']}."
                }
            }
        ]
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{article['title']} ({article['date']} Sizing &amp; Lab Review)</title>
  <meta name="description" content="Hands-on sizing and performance review of the {article['brand']} {article['model_name']} ({article['max_sqft']} sq. ft., {article['noise_dba']}) for {article['app_title']}. Compare specs and Amazon deals." />
  <link rel="canonical" href="{BASE_URL}/reviews/{article['slug']}.html" />
  <meta property="og:title" content="{article['title']}" />
  <meta property="og:description" content="Covers up to {article['max_sqft']} sq. ft. at {article['noise_dba']} with {article['brand_tech']}." />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{BASE_URL}/reviews/{article['slug']}.html" />
  <style>{GLOBAL_CSS}</style>
  <script type="application/ld+json">{json.dumps(faq_schema)}</script>
</head>
<body>
  <div class="top-promo-banner">
    <span class="badge-live">HVAC DEAL ALERT</span>
    Check Live Amazon Price &amp; Seasonal Rebate Coupons on <strong>{article['brand']} {article['model_name']}</strong>
    <a class="banner-cta" href="{article['affiliate_url']}" target="_blank" rel="nofollow sponsored noopener">Check Price on Amazon &rarr;</a>
  </div>

  <header class="site-header">
    <div class="container nav-flex">
      <a href="{BASE_URL}/index.html" class="brand-logo">ClimateSize<span>Calc</span></a>
      <ul class="nav-links">
        <li><a href="{BASE_URL}/index.html#calculator">BTU &amp; Room Calculator</a></li>
        <li><a href="{BASE_URL}/index.html#search-section">Search Products</a></li>
        <li><a href="{BASE_URL}/index.html#bestsellers">Best Sellers</a></li>
        <li><a href="{BASE_URL}/index.html#comparison">Comparison Table</a></li>
        <li><a href="{BASE_URL}/index.html#daily-reviews">Daily Reviews</a></li>
        <li><a href="{BASE_URL}/sitemap.html">Site Map</a></li>
      </ul>
    </div>
  </header>

  <main class="container" style="margin-top:24px;">
    <article class="grey-section">
      <div style="font-size:0.82rem; font-weight:700; color:#334155; text-transform:uppercase; margin-bottom:6px;">
        Published: {article['date']} &bull; Category: {article['category']} &bull; Verified Rating: ★ {article['rating']}/5.0
      </div>
      <h1 style="font-size:1.95rem; margin-bottom:14px; color:#0f172a;">{article['title']}</h1>
      <p style="font-size:1.05rem; color:#334155; margin-bottom:20px;">
        Selecting the right climate control equipment for <strong>{article['app_title']}</strong> requires matching room square footage, ceiling volume, and acoustic tolerance. In this comprehensive engineering review, we test how the <strong>{article['brand']} {article['model_name']}</strong> (rated up to <strong>{article['max_sqft']} sq. ft.</strong>, <strong>{article['cfm_rate']} CFM</strong> airflow, and <strong>{article['noise_dba']}</strong> sound output) {article['app_benefit']}.
      </p>

      <div class="hero-deal-box" style="margin-bottom:24px; text-align:left; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:16px;">
        <div>
          <h3 style="margin-bottom:4px;">{article['brand']} {article['model_name']} — Amazon Prime Availability</h3>
          <p style="color:#cbd5e1; font-size:0.93rem;">Equipped with {article['brand_tech']} | Max Room Size: {article['max_sqft']} sq. ft. | Noise Level: {article['noise_dba']}</p>
        </div>
        <a class="btn-amazon" href="{article['affiliate_url']}" target="_blank" rel="nofollow sponsored noopener">Check Today's Price on Amazon &rarr;</a>
      </div>

      <h2 class="section-title">1. Technical Specifications &amp; Airflow Telemetry</h2>
      <div class="table-wrap" style="margin:16px 0 26px;">
        <table class="comp-table">
          <thead>
            <tr>
              <th>Specification</th>
              <th>Rated Parameter</th>
              <th>Real-World Room Impact</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Maximum Room Coverage</strong></td>
              <td>Up to {article['max_sqft']} sq. ft.</td>
              <td>4.8x Air Changes Per Hour in rooms up to {article['ach_48_sqft']} sq. ft.</td>
            </tr>
            <tr>
              <td><strong>Thermal / Output Rating</strong></td>
              <td>{article['btu_equiv']:,} BTU/hr Equiv.</td>
              <td>Handles sensible and latent heat loads without short-cycling</td>
            </tr>
            <tr>
              <td><strong>Moisture Removal Rate</strong></td>
              <td>{article['moisture_cap']}</td>
              <td>Prevents clammy indoor air and mold growth above 50% RH</td>
            </tr>
            <tr>
              <td><strong>Blower Airflow Volume</strong></td>
              <td>{article['cfm_rate']} CFM</td>
              <td>Eliminates hot/cold corners across open room layouts</td>
            </tr>
            <tr>
              <td><strong>Sound Pressure Level</strong></td>
              <td>{article['noise_dba']} (Low/Sleep Mode)</td>
              <td>Quiet enough for bedrooms, nurseries, and video calls</td>
            </tr>
            <tr>
              <td><strong>Estimated Power Draw</strong></td>
              <td>~{article['est_watts']} Watts Average</td>
              <td>Compatible with standard 115V/15A or dedicated home circuits</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h2 class="section-title">2. Interactive Room Compatibility Checker for {article['brand']}</h2>
      <p class="section-sub">Enter your room dimensions below to verify whether this {article['max_sqft']} sq. ft. unit is properly sized for your space:</p>
      <div class="calc-panel" style="margin-bottom:26px;">
        <div class="calc-grid">
          <div class="form-row">
            <div class="form-group">
              <label for="artLen">Room Length (ft):</label>
              <input type="number" id="artLen" value="20" min="5" max="100" oninput="checkArticleRoom()" />
            </div>
            <div class="form-group">
              <label for="artWid">Room Width (ft):</label>
              <input type="number" id="artWid" value="18" min="5" max="100" oninput="checkArticleRoom()" />
            </div>
          </div>
          <div class="metric-card">
            <div class="lbl">Your Room Area vs. Unit Capacity ({article['max_sqft']} sq. ft.)</div>
            <div class="val" id="artRoomVerdict">360 sq. ft. — Optimal Fit</div>
            <div style="margin-top:10px;">
              <a class="btn-amazon" href="{article['affiliate_url']}" target="_blank" rel="nofollow sponsored noopener">Order {article['brand']} on Amazon</a>
            </div>
          </div>
        </div>
      </div>

      <h2 class="section-title">3. Room Size &amp; Thermal Load Compatibility Matrix</h2>
      <div class="table-wrap" style="margin:16px 0 26px;">
        <table class="comp-table">
          <thead>
            <tr>
              <th>Room Type</th>
              <th>Area &amp; Volume</th>
              <th>Estimated Load</th>
              <th>Compatibility Verdict</th>
            </tr>
          </thead>
          <tbody>
            {scenario_rows}
          </tbody>
        </table>
      </div>

      <h2 class="section-title">4. Pros, Cons &amp; Final Engineering Verdict</h2>
      <div class="calc-grid" style="margin:16px 0 26px;">
        <div class="calc-panel" style="border-left:5px solid #15803d;">
          <h3 style="color:#15803d; margin-bottom:10px;">Key Advantages (Pros)</h3>
          <ul style="padding-left:18px; font-size:0.94rem;">
            <li><strong>{article['brand_tech']}</strong> cuts electricity consumption while stabilizing room temperature.</li>
            <li>High <strong>{article['cfm_rate']} CFM</strong> airflow rapidly conditions rooms up to {article['max_sqft']} sq. ft.</li>
            <li>Whisper-quiet <strong>{article['noise_dba']}</strong> sleep profile ideal for {article['app_title']}.</li>
          </ul>
        </div>
        <div class="calc-panel" style="border-left:5px solid #b91c1c;">
          <h3 style="color:#b91c1c; margin-bottom:10px;">Things to Note (Cons)</h3>
          <ul style="padding-left:18px; font-size:0.94rem;">
            <li>Spaces larger than {article['max_sqft']} sq. ft. with poor insulation should step up to the next BTU/CFM tier.</li>
            <li>Filter screen should be rinsed or replaced on schedule to preserve peak {article['cfm_rate']} CFM airflow.</li>
          </ul>
        </div>
      </div>

      <div class="hero-deal-box">
        <h3>Ready to Upgrade Your {article['app_title']}?</h3>
        <p style="color:#cbd5e1; margin-bottom:14px;">Check verified customer photos, seasonal discounts, and fast delivery options on Amazon.</p>
        <a class="btn-amazon" href="{article['affiliate_url']}" target="_blank" rel="nofollow sponsored noopener">View {article['brand']} {article['model_name']} on Amazon &rarr;</a>
      </div>
    </article>

    <section class="grey-section">
      <h2 class="section-title">Related Daily HVAC &amp; Air Quality Reviews</h2>
      <ul style="padding-left:20px; line-height:1.9;">
        {related_links}
      </ul>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        <a href="{BASE_URL}/index.html">Home &amp; BTU Calculator</a>
        <a href="{BASE_URL}/index.html#bestsellers">Best Sellers</a>
        <a href="{BASE_URL}/index.html#comparison">Comparison Chart</a>
        <a href="{BASE_URL}/sitemap.html">HTML Site Map</a>
        <a href="{BASE_URL}/sitemap.xml">XML Sitemap</a>
        <a href="{BASE_URL}/feed.xml">RSS Feed</a>
      </div>
      <p>Affiliate Disclosure: ClimateSizeCalc is a participant in the Amazon Services LLC Associates Program (StoreID: {AFFILIATE_TAG}). As an Amazon Associate, we earn from qualifying purchases.</p>
    </div>
  </footer>

  <script>
    function checkArticleRoom() {{
      var l = parseFloat(document.getElementById('artLen').value) || 10;
      var w = parseFloat(document.getElementById('artWid').value) || 10;
      var area = Math.round(l * w);
      var maxCap = {article['max_sqft']};
      var status = area <= maxCap ? ' — Optimal Fit ✅' : ' — Exceeds Single-Unit Cap ⚠️';
      document.getElementById('artRoomVerdict').textContent = area + ' sq. ft.' + status;
    }}
  </script>
</body>
</html>"""


def build_html_sitemap_page(all_articles: list[dict]) -> str:
    """Membangun halaman direktori HTML Site Map lengkap (sitemap.html) agar mudah dijelajahi pengunjung & crawler."""
    article_links = ""
    for art in all_articles:
        article_links += f"""
        <li>
          <a href="{BASE_URL}/reviews/{art['slug']}.html"><strong>{art['title']}</strong></a>
          <span> — {art['category']} ({art['max_sqft']} sq. ft. | Published {art['date']})</span>
        </li>
        """

    product_links = ""
    for p in CORE_PRODUCTS:
        product_links += f"""
        <li>
          <a href="{amazon_search_url(p['search_query'])}" target="_blank" rel="nofollow sponsored noopener">{p['name']} ({p['btu_or_cap']})</a>
          <span> — {p['badge']}</span>
        </li>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Complete Site Map — ClimateSizeCalc BTU Calculator &amp; Daily HVAC Reviews</title>
  <meta name="description" content="Complete HTML Site Map indexing all interactive room BTU calculators, dehumidifier & HEPA CADR sizing tools, comparison charts, and {len(all_articles)} daily product reviews." />
  <link rel="canonical" href="{BASE_URL}/sitemap.html" />
  <style>{GLOBAL_CSS}</style>
</head>
<body>
  <header class="site-header">
    <div class="container nav-flex">
      <a href="{BASE_URL}/index.html" class="brand-logo">ClimateSize<span>Calc</span></a>
      <ul class="nav-links">
        <li><a href="{BASE_URL}/index.html#calculator">BTU Calculator</a></li>
        <li><a href="{BASE_URL}/index.html#bestsellers">Best Sellers</a></li>
        <li><a href="{BASE_URL}/index.html#comparison">Comparison Table</a></li>
        <li><a href="{BASE_URL}/index.html#daily-reviews">Daily Reviews</a></li>
        <li><a href="{BASE_URL}/sitemap.xml">XML Sitemap</a></li>
      </ul>
    </div>
  </header>

  <main class="container" style="margin-top:24px;">
    <section class="grey-section">
      <h1 class="section-title">ClimateSizeCalc — Complete HTML Site Map &amp; Archive</h1>
      <p class="section-sub">Direct index of all interactive HVAC calculators, comparison tables, XML feeds, and {len(all_articles)} automated daily product review articles.</p>

      <div class="sitemap-columns" style="margin-bottom:24px;">
        <div class="sitemap-box">
          <h3>Core Calculators &amp; Sections</h3>
          <ul>
            <li><a href="{BASE_URL}/index.html">Homepage &amp; 4-in-1 Room Sizing Calculator</a></li>
            <li><a href="{BASE_URL}/index.html#calculator">Interactive BTU, Mini-Split, Pint &amp; CADR Calculator</a></li>
            <li><a href="{BASE_URL}/index.html#search-section">Real-Time HVAC &amp; Air Purifier Product Finder</a></li>
            <li><a href="{BASE_URL}/index.html#bestsellers">Top 10 Best-Selling Amazon Climate Systems</a></li>
            <li><a href="{BASE_URL}/index.html#comparison">Side-by-Side Technical Comparison Table</a></li>
            <li><a href="{BASE_URL}/index.html#faq">ASHRAE &amp; DOE Room Sizing FAQ</a></li>
          </ul>
        </div>
        <div class="sitemap-box">
          <h3>Search Engine &amp; Syndication Feeds</h3>
          <ul>
            <li><a href="{BASE_URL}/sitemap.xml">Primary XML Sitemap (sitemap.xml)</a></li>
            <li><a href="{BASE_URL}/feed.xml">Automated Daily Review RSS 2.0 Feed (feed.xml)</a></li>
            <li><a href="{BASE_URL}/robots.txt">Crawler Directives (robots.txt)</a></li>
          </ul>
        </div>
      </div>

      <div class="sitemap-box" style="margin-bottom:24px;">
        <h3>All Daily Product Review Articles ({len(all_articles)} Indexed Pages)</h3>
        <ul>
          {article_links}
        </ul>
      </div>

      <div class="sitemap-box">
        <h3>Quick Amazon Direct Catalog Links (StoreID: {AFFILIATE_TAG})</h3>
        <ul>
          {product_links}
        </ul>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <p>&copy; {datetime.datetime.now(datetime.timezone.utc).year} ClimateSizeCalc (Amazon StoreID: {AFFILIATE_TAG}). <a href="{BASE_URL}/index.html" style="color:#ffffff;">Return to Calculator</a></p>
    </div>
  </footer>
</body>
</html>"""


def build_index_page(all_articles: list[dict]) -> str:
    """Membangun halaman utama (index.html) dengan Kalkulator 4-in-1, Banner, Search, Best Sellers, Comparison, Daily Reviews, FAQ, dan Site Map."""
    bestsellers_cards = ""
    for p in CORE_PRODUCTS:
        aff_url = amazon_search_url(p["search_query"])
        bestsellers_cards += f"""
        <div class="product-card" data-search="{p['name'].lower()} {p['brand'].lower()} {p['category'].lower()} {p['highlight'].lower()}" data-category="{p['category']}">
          <div>
            <span class="badge-tag">{p['badge']}</span>
            <h3 style="font-size:1.14rem; margin-bottom:8px;">{p['name']}</h3>
            <p style="font-size:0.88rem; color:#334155; margin-bottom:8px;">{p['highlight']}</p>
            <ul class="spec-box">
              <li><strong>Max Coverage:</strong> Up to {p['sq_ft']} sq. ft.</li>
              <li><strong>Capacity:</strong> {p['btu_or_cap']}</li>
              <li><strong>Sound Level:</strong> {p['noise_db']}</li>
              <li><strong>Efficiency:</strong> {p['efficiency']}</li>
              <li><strong>Buyer Rating:</strong> ★ {p['rating']}/5 ({p['reviews_count']}+ reviews)</li>
            </ul>
          </div>
          <a class="btn-amazon" href="{aff_url}" target="_blank" rel="nofollow sponsored noopener">Check Price on Amazon &rarr;</a>
        </div>
        """

    comparison_rows = ""
    for p in CORE_PRODUCTS:
        aff_url = amazon_search_url(p["search_query"])
        comparison_rows += f"""
        <tr>
          <td><strong>{p['name']}</strong><br/><span style="font-size:0.78rem; color:#334155;">{p['badge']}</span></td>
          <td>{p['category']}</td>
          <td><strong>{p['sq_ft']} sq. ft.</strong></td>
          <td>{p['btu_or_cap']}</td>
          <td>{p['noise_db']}</td>
          <td>{p['efficiency']}</td>
          <td>★ {p['rating']}</td>
          <td><a class="btn-amazon" style="padding:7px 12px; font-size:0.82rem;" href="{aff_url}" target="_blank" rel="nofollow sponsored noopener">View Deal</a></td>
        </tr>
        """

    daily_cards = ""
    for art in all_articles[:36]:
        daily_cards += f"""
        <div class="article-card" data-art-search="{art['title'].lower()} {art['brand'].lower()} {art['category'].lower()} {art['app_title'].lower()}">
          <div>
            <div style="font-size:0.78rem; font-weight:700; color:#334155; text-transform:uppercase; margin-bottom:6px;">
              {art['date']} &bull; {art['category']} &bull; Up to {art['max_sqft']} sq. ft.
            </div>
            <h3 style="font-size:1.12rem; margin-bottom:10px;">
              <a href="{BASE_URL}/reviews/{art['slug']}.html" style="color:#0f172a;">{art['title']}</a>
            </h3>
            <p style="font-size:0.9rem; color:#334155; margin-bottom:14px;">
              Delivers <strong>{art['cfm_rate']} CFM</strong> airflow at <strong>{art['noise_dba']}</strong> with {art['brand_tech']}. Tested for {art['app_title']}.
            </p>
          </div>
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <a class="btn-outline" href="{BASE_URL}/reviews/{art['slug']}.html">Read Full Review</a>
            <a class="btn-amazon" style="padding:9px 14px; font-size:0.86rem;" href="{art['affiliate_url']}" target="_blank" rel="nofollow sponsored noopener">Amazon Price</a>
          </div>
        </div>
        """

    sitemap_preview_links = ""
    for art in all_articles[:18]:
        sitemap_preview_links += f"""
        <li><a href="{BASE_URL}/reviews/{art['slug']}.html">{art['title']}</a> ({art['date']})</li>
        """

    faqs = [
        (
            "How many BTUs do I need per square foot for an air conditioner or mini-split?",
            "Under standard ASHRAE residential guidelines with an 8-foot ceiling, multiply your room's square footage by 20 to 25 BTU/hr. Adjust upward by 10% for heavily sunlit south/west rooms, add 15% per additional foot of ceiling height above 8 feet, add 600 BTU for each occupant beyond two people, and add 4,000 BTU if the unit is placed in a kitchen."
        ),
        (
            "What is the difference between ASHRAE BTU and DOE (SACC) BTU on portable air conditioners?",
            "ASHRAE BTU measures total gross cooling output under steady test conditions, whereas DOE SACC (Seasonally Adjusted Cooling Capacity) accounts for heat radiated by the exhaust hose and negative air pressure. Dual-hose inverter portable ACs achieve up to 40% higher SACC efficiency than single-hose units."
        ),
        (
            "How do I calculate what size dehumidifier (Pints per Day) I need for my basement?",
            "Size your dehumidifier by both square footage and dampness level. A moderately damp 1,500 sq. ft. basement requires a 30-to-35 pint Energy Star dehumidifier, while spaces from 2,500 to 4,500 sq. ft. (or wet basements with visible condensation) require a 50-pint model with a continuous drain hose or built-in vertical condensate pump."
        ),
        (
            "How do I calculate the right CADR (Clean Air Delivery Rate) for a HEPA air purifier?",
            "To achieve the AHAM-recommended 4.8 Air Changes Per Hour (cleaning the entire room volume every 12.5 minutes) with an 8-foot ceiling, divide your room's square footage by 1.55. For example, a 450 sq. ft. room requires a True HEPA air purifier rated at least 290 CFM CADR."
        ),
        (
            "Why are inverter mini-splits and dual-inverter window ACs cheaper to run?",
            "Traditional fixed-speed compressors slam on at 100% power and shut off repeatedly, causing massive amperage spikes. Variable-speed DC inverter compressors smoothly ramp down to 25%–35% speed once your target temperature is reached, cutting electricity bills by 30% to 45% while operating as quietly as 25 to 42 dBA."
        ),
        (
            "What happens if I buy an oversized air conditioner for a small room?",
            "An oversized non-inverter AC cools the room air too quickly and shuts off before the evaporator coil can condense moisture out of the air (short-cycling). This leaves the room feeling cold, clammy, and humid. Matching your exact calculated BTU or choosing a variable-speed inverter unit prevents short-cycling."
        )
    ]

    faq_html = ""
    faq_entities = []
    for q, a in faqs:
        faq_html += f"""
        <details class="faq-item" open>
          <summary>{q}</summary>
          <p>{a}</p>
        </details>
        """
        faq_entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}
        })

    json_ld = [
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "ClimateSizeCalc — Room BTU, Mini-Split, Dehumidifier Pint & HEPA CADR Calculator",
            "applicationCategory": "UtilitiesApplication",
            "operatingSystem": "All",
            "url": f"{BASE_URL}/index.html",
            "description": "Interactive HVAC room sizing calculator for BTU cooling/heating, dehumidifier pint capacity, and HEPA air purifier CADR CFM."
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_entities
        }
    ]

    js_products = json.dumps([
        {
            "name": p["name"],
            "category": p["category"],
            "sq_ft": p["sq_ft"],
            "btu_or_cap": p["btu_or_cap"],
            "btu_num": p["btu_num"],
            "noise_db": p["noise_db"],
            "badge": p["badge"],
            "highlight": p["highlight"],
            "url": amazon_search_url(p["search_query"])
        }
        for p in CORE_PRODUCTS
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ClimateSizeCalc — Room BTU Air Conditioner, Mini-Split, Dehumidifier &amp; HEPA CADR Calculator</title>
  <meta name="description" content="Calculate exact room BTU cooling/heating capacity, dehumidifier pints per day, and HEPA air purifier CADR CFM in seconds. Compare top-rated HVAC gear &amp; daily reviews." />
  <link rel="canonical" href="{BASE_URL}/index.html" />
  <link rel="alternate" type="application/rss+xml" title="ClimateSizeCalc Daily HVAC Product Reviews RSS" href="{BASE_URL}/feed.xml" />
  <meta property="og:title" content="ClimateSizeCalc — Interactive Room BTU, Dehumidifier &amp; HEPA CADR Sizing Tool" />
  <meta property="og:description" content="Size your air conditioner, mini-split heat pump, basement dehumidifier, and HEPA air purifier with instant hardware matches." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE_URL}/index.html" />
  <style>{GLOBAL_CSS}</style>
  <script type="application/ld+json">{json.dumps(json_ld)}</script>
</head>
<body>

  <!-- TOP STICKY PROMO BANNER -->
  <div class="top-promo-banner">
    <span class="badge-live">SEASONAL HVAC DEALS</span>
    Save Up to 35% on Energy Star Inverter ACs, Ductless Mini-Splits, 50-Pint Dehumidifiers &amp; True HEPA Purifiers
    <a class="banner-cta" href="{amazon_search_url('Energy Star Inverter Air Conditioner Mini Split Dehumidifier Deal')}" target="_blank" rel="nofollow sponsored noopener">Claim Today's Amazon Deals &rarr;</a>
  </div>

  <!-- NAVIGATION HEADER -->
  <header class="site-header">
    <div class="container nav-flex">
      <a href="{BASE_URL}/index.html" class="brand-logo">ClimateSize<span>Calc</span></a>
      <ul class="nav-links">
        <li><a href="#calculator">BTU &amp; CADR Calculator</a></li>
        <li><a href="#search-section">Search Products</a></li>
        <li><a href="#bestsellers">Best Sellers</a></li>
        <li><a href="#comparison">Comparison Chart</a></li>
        <li><a href="#daily-reviews">Daily Reviews ({len(all_articles)})</a></li>
        <li><a href="#faq">FAQ</a></li>
        <li><a href="#sitemap-section">Site Map</a></li>
      </ul>
    </div>
  </header>

  <main class="container">

    <!-- HERO BANNER -->
    <section class="hero-banner">
      <div class="hero-grid">
        <div>
          <h1>Room BTU, Mini-Split, Dehumidifier (Pints) &amp; HEPA CADR Calculator</h1>
          <p>Never buy an undersized or short-cycling climate unit again. Enter your room dimensions, ceiling height, sun exposure, and humidity level below to calculate your exact <strong>ASHRAE BTU/hr</strong>, <strong>Dehumidifier Pints/Day</strong>, and <strong>HEPA CADR (CFM)</strong>—paired with instant Amazon hardware matches.</p>
          <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <a class="btn-amazon" href="#calculator">Launch Room Sizing Calculator &darr;</a>
            <a class="btn-outline" style="color:#ffffff; border-color:#94a3b8;" href="{amazon_search_url('Best Selling Portable Air Conditioner Dehumidifier Air Purifier')}" target="_blank" rel="nofollow sponsored noopener">Explore Amazon HVAC Best Sellers &rarr;</a>
          </div>
        </div>
        <div class="hero-deal-box">
          <h3>❄️ Featured Inverter Spotlight</h3>
          <p style="color:#e2e8f0; font-size:0.92rem; margin-bottom:14px;">Ultra-Quiet Dual-Inverter ACs, 20-SEER2 Heat Pumps &amp; 50-Pint Pump Dehumidifiers with Smart Wi-Fi Control.</p>
          <a class="btn-amazon" style="width:100%;" href="{amazon_search_url('Midea Duo Inverter AC Senville Mini Split hOmeLabs Dehumidifier')}" target="_blank" rel="nofollow sponsored noopener">Check Live Amazon Discounts &rarr;</a>
        </div>
      </div>
    </section>

    <!-- 4-IN-1 INTERACTIVE ROOM CALCULATOR -->
    <section id="calculator" class="grey-section">
      <h2 class="section-title">Interactive 4-in-1 Room BTU, Dehumidifier &amp; HEPA Air Purifier Calculator</h2>
      <p class="section-sub">Select a room preset or customize your exact dimensions below. Our algorithm computes thermal load, moisture extraction rate, and 4.8 ACH clean air delivery simultaneously.</p>

      <div class="preset-row">
        <button type="button" class="preset-btn" onclick="setRoomPreset(14, 12, 8, 1.0, 1.0, 2, 1.0)">🛏️ Bedroom (14&times;12 ft)</button>
        <button type="button" class="preset-btn" onclick="setRoomPreset(22, 18, 9, 1.1, 1.0, 3, 1.15)">🛋️ Sunny Living Room (22&times;18 ft)</button>
        <button type="button" class="preset-btn" onclick="setRoomPreset(40, 30, 8, 0.95, 1.1, 2, 1.4)">💧 Damp Basement (40&times;30 ft)</button>
        <button type="button" class="preset-btn" onclick="setRoomPreset(24, 22, 10, 1.15, 1.25, 2, 1.2)">🚗 2-Car Garage Workshop (24&times;22 ft)</button>
        <button type="button" class="preset-btn" onclick="setRoomPreset(32, 25, 10, 1.1, 1.0, 4, 1.15)">🏠 Open Concept Floor (32&times;25 ft)</button>
      </div>

      <div class="calc-grid">
        <div class="calc-panel">
          <div class="form-row">
            <div class="form-group">
              <label for="rmLength">1. Room Length (Feet):</label>
              <input type="number" id="rmLength" value="20" min="5" max="150" oninput="calculateClimate()" />
            </div>
            <div class="form-group">
              <label for="rmWidth">2. Room Width (Feet):</label>
              <input type="number" id="rmWidth" value="16" min="5" max="150" oninput="calculateClimate()" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="rmCeiling">3. Ceiling Height (Feet):</label>
              <input type="number" id="rmCeiling" value="8" min="6" max="24" step="0.5" oninput="calculateClimate()" />
            </div>
            <div class="form-group">
              <label for="rmOccupants">4. Number of Occupants:</label>
              <input type="number" id="rmOccupants" value="2" min="1" max="20" oninput="calculateClimate()" />
            </div>
          </div>
          <div class="form-group">
            <label for="rmSun">5. Window Sun Exposure &amp; Heat Sources:</label>
            <select id="rmSun" onchange="calculateClimate()">
              <option value="0.9">Mostly Shaded / North-Facing Windows (-10% Thermal Load)</option>
              <option value="1.0" selected>Average Sunlight &amp; Standard Appliances (Baseline)</option>
              <option value="1.12">Sunny South/West Windows or Home Office PCs (+12% Load)</option>
              <option value="1.25">Sunroom, Kitchen Appliances, or Top Floor Attic Heat (+25% Load)</option>
            </select>
          </div>
          <div class="form-group">
            <label for="rmInsulation">6. Wall Insulation &amp; Climate Zone:</label>
            <select id="rmInsulation" onchange="calculateClimate()">
              <option value="0.95">Well-Insulated Modern Construction</option>
              <option value="1.0" selected>Standard Residential Drywall &amp; Double-Pane Glass</option>
              <option value="1.2">Older Home, Drafty Windows, or Uninsulated Garage (+20% Load)</option>
            </select>
          </div>
          <div class="form-group">
            <label for="rmHumidity">7. Indoor Humidity / Dampness Condition:</label>
            <select id="rmHumidity" onchange="calculateClimate()">
              <option value="1.0">Moderate Humidity (50%–60% RH)</option>
              <option value="1.2" selected>Humid Summer / Musty Odor (60%–70% RH)</option>
              <option value="1.45">Very Damp Basement / Wet Crawlspace (&gt;70% RH)</option>
            </select>
          </div>
        </div>

        <div class="calc-panel">
          <h3 style="margin-bottom:12px; color:#0f172a;">Your Exact Room Sizing Results</h3>
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="val" id="outBTU">8,500 BTU</div>
              <div class="lbl">Required AC / Mini-Split</div>
            </div>
            <div class="metric-card">
              <div class="val" id="outPints">35 Pints</div>
              <div class="lbl">Dehumidifier Capacity / Day</div>
            </div>
            <div class="metric-card">
              <div class="val" id="outCADR">210 CFM</div>
              <div class="lbl">Min. HEPA Purifier CADR</div>
            </div>
            <div class="metric-card">
              <div class="val" id="outVolume">320 sq.ft.</div>
              <div class="lbl">Area &amp; Cubic Volume</div>
            </div>
          </div>

          <div id="dynamicRecContainer" class="rec-box">
            <!-- Populated by JS -->
          </div>
        </div>
      </div>
    </section>

    <!-- PRODUCT SEARCH & FILTER -->
    <section id="search-section" class="grey-section">
      <h2 class="section-title">Search Amazon HVAC, Dehumidifier &amp; Air Purifier Catalog</h2>
      <p class="section-sub">Filter our tested flagship lineup and daily review archive in real time, or launch a custom search directly on Amazon.</p>
      <div class="search-bar">
        <input type="text" id="catalogSearchInput" class="search-input" placeholder="Search by BTU, sq ft, Midea, Senville, Basement, HEPA, Mini-Split, Window AC..." oninput="filterClimateCatalog()" />
        <select id="catalogCatSelect" class="filter-select" onchange="filterClimateCatalog()">
          <option value="ALL">All Equipment Categories</option>
          <option value="Portable Air Conditioner">Portable Air Conditioners</option>
          <option value="Ductless Mini-Split">Ductless Mini-Split Heat Pumps</option>
          <option value="Window Air Conditioner">Window Air Conditioners</option>
          <option value="Dehumidifier">Basement &amp; Room Dehumidifiers</option>
          <option value="HEPA Air Purifier">True HEPA Air Purifiers</option>
          <option value="Space Heater">PTC Space Heaters</option>
        </select>
        <button type="button" class="btn-amazon" onclick="searchAmazonDirectly()">Search Live on Amazon &rarr;</button>
      </div>
      <p id="filterStatusText" style="font-size:0.88rem; font-weight:700; color:#334155;">Showing all 10 top-rated HVAC &amp; air quality systems below:</p>
    </section>

    <!-- BEST SELLERS -->
    <section id="bestsellers" class="grey-section">
      <h2 class="section-title">Best-Selling Air Conditioners, Mini-Splits, Dehumidifiers &amp; HEPA Purifiers</h2>
      <p class="section-sub">Selected for high SEER2/CEER energy efficiency, quiet decibel output, and verified buyer durability on Amazon.</p>
      <div id="bestSellersGrid" class="product-grid">
        {bestsellers_cards}
      </div>
    </section>

    <!-- COMPARISON TABLE -->
    <section id="comparison" class="grey-section">
      <h2 class="section-title">Side-by-Side HVAC &amp; Air Quality Comparison Matrix</h2>
      <p class="section-sub">Compare maximum room square footage, BTU/Pint/CADR capacity, acoustic dBA ratings, and inverter efficiency side-by-side.</p>
      <div class="table-wrap">
        <table class="comp-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>Category</th>
              <th>Max Room Size</th>
              <th>Rated Capacity</th>
              <th>Noise Level</th>
              <th>Efficiency / Tech</th>
              <th>Rating</th>
              <th>Amazon Price</th>
            </tr>
          </thead>
          <tbody>
            {comparison_rows}
          </tbody>
        </table>
      </div>
    </section>

    <!-- DAILY AUTOMATED PRODUCT REVIEWS -->
    <section id="daily-reviews" class="grey-section">
      <h2 class="section-title">Daily Automated Product Reviews &amp; Room Sizing Tests</h2>
      <p class="section-sub">Our automated GitHub Actions engine publishes <strong>3 brand-new HVAC &amp; air quality product reviews every day</strong>. Browse the latest reviews below (Total live articles: <strong>{len(all_articles)}</strong>):</p>
      <div id="dailyReviewsGrid" class="articles-grid">
        {daily_cards}
      </div>
    </section>

    <!-- FAQ SECTION -->
    <section id="faq" class="grey-section">
      <h2 class="section-title">Frequently Asked Questions (BTU, Mini-Split, Dehumidifier &amp; CADR Sizing)</h2>
      <p class="section-sub">Standard ASHRAE, DOE, and AHAM engineering formulas explained in plain English.</p>
      {faq_html}
    </section>

    <!-- ON-PAGE SITE MAP DIRECTORY -->
    <section id="sitemap-section" class="grey-section">
      <h2 class="section-title">Site Map &amp; Complete Content Directory</h2>
      <p class="section-sub">Quick navigation for visitors and search engine crawlers across all calculators, feeds, and daily review archives.</p>
      <div class="sitemap-columns">
        <div class="sitemap-box">
          <h3>Main Tools &amp; XML Feeds</h3>
          <ul>
            <li><a href="#calculator">4-in-1 Room BTU, Pint &amp; CADR Calculator</a></li>
            <li><a href="#bestsellers">Top 10 Best-Selling Climate Units</a></li>
            <li><a href="#comparison">Technical Comparison Matrix</a></li>
            <li><a href="{BASE_URL}/sitemap.html"><strong>Full HTML Site Map Page (All {len(all_articles)} Reviews)</strong></a></li>
            <li><a href="{BASE_URL}/sitemap.xml">Google/Bing XML Sitemap (sitemap.xml)</a></li>
            <li><a href="{BASE_URL}/feed.xml">RSS 2.0 Syndication Feed (feed.xml)</a></li>
          </ul>
        </div>
        <div class="sitemap-box">
          <h3>Latest Daily Review Archive Links</h3>
          <ul>
            {sitemap_preview_links}
          </ul>
        </div>
      </div>
    </section>

  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-links">
        <a href="#calculator">BTU Calculator</a>
        <a href="#search-section">Product Search</a>
        <a href="#bestsellers">Best Sellers</a>
        <a href="#comparison">Comparison Table</a>
        <a href="#daily-reviews">Daily Reviews</a>
        <a href="#faq">FAQ</a>
        <a href="{BASE_URL}/sitemap.html">HTML Site Map</a>
        <a href="{BASE_URL}/sitemap.xml">XML Sitemap</a>
        <a href="{BASE_URL}/feed.xml">RSS Feed</a>
      </div>
      <p style="margin-bottom:8px;"><strong>Amazon Affiliate Disclosure:</strong> ClimateSizeCalc participates in the Amazon Services LLC Associates Program (Affiliate StoreID: <code>{AFFILIATE_TAG}</code>), an affiliate advertising program designed to provide a means for sites to earn advertising fees by linking to Amazon.com.</p>
      <p>&copy; {datetime.datetime.now(datetime.timezone.utc).year} ClimateSizeCalc. Powered by zero-maintenance GitHub Actions automation.</p>
    </div>
  </footer>

  <script>
    var CLIMATE_PRODUCTS = {js_products};
    var AFFILIATE_TAG = "{AFFILIATE_TAG}";

    function setRoomPreset(len, wid, ceil, sun, insul, occ, hum) {{
      document.getElementById('rmLength').value = len;
      document.getElementById('rmWidth').value = wid;
      document.getElementById('rmCeiling').value = ceil;
      document.getElementById('rmSun').value = sun.toString();
      document.getElementById('rmInsulation').value = insul.toString();
      document.getElementById('rmOccupants').value = occ;
      document.getElementById('rmHumidity').value = hum.toString();
      calculateClimate();
    }}

    function calculateClimate() {{
      var len = parseFloat(document.getElementById('rmLength').value) || 15;
      var wid = parseFloat(document.getElementById('rmWidth').value) || 15;
      var ceil = parseFloat(document.getElementById('rmCeiling').value) || 8;
      var occ = parseInt(document.getElementById('rmOccupants').value, 10) || 2;
      var sun = parseFloat(document.getElementById('rmSun').value) || 1.0;
      var insul = parseFloat(document.getElementById('rmInsulation').value) || 1.0;
      var hum = parseFloat(document.getElementById('rmHumidity').value) || 1.2;

      var sqft = Math.round(len * wid);
      var cuft = Math.round(sqft * ceil);
      var ceilingFactor = ceil / 8.0;

      // ASHRAE BTU Calculation
      var baseBtu = sqft * 22 * ceilingFactor * sun * insul;
      if (occ > 2) {{
        baseBtu += (occ - 2) * 600;
      }}
      var finalBtu = Math.ceil(baseBtu / 500) * 500;
      if (finalBtu < 5000) finalBtu = 5000;

      // Dehumidifier Pint Calculation (DOE 2019 standard)
      var rawPints = Math.round((sqft / 55) * hum * ceilingFactor);
      var recommendedPints = rawPints <= 25 ? 22 : (rawPints <= 40 ? 35 : 50);

      // HEPA CADR CFM for 4.8 Air Changes Per Hour (ACH)
      var cadrCfm = Math.ceil((cuft * 4.8) / 60);

      document.getElementById('outBTU').textContent = finalBtu.toLocaleString() + ' BTU/hr';
      document.getElementById('outPints').textContent = recommendedPints + ' Pints/Day';
      document.getElementById('outCADR').textContent = cadrCfm + ' CFM CADR';
      document.getElementById('outVolume').textContent = sqft.toLocaleString() + ' sq.ft. (' + cuft.toLocaleString() + ' cu.ft.)';

      // Match best AC/Mini-Split from catalog
      var coolingUnits = CLIMATE_PRODUCTS.filter(function(p) {{
        return p.category.indexOf('Air Conditioner') !== -1 || p.category.indexOf('Mini-Split') !== -1;
      }}).sort(function(a, b) {{ return a.btu_num - b.btu_num; }});

      var bestCool = coolingUnits.find(function(p) {{ return p.btu_num >= finalBtu; }}) || coolingUnits[coolingUnits.length - 1];

      var customBtuUrl = 'https://www.amazon.com/s?k=' + encodeURIComponent(finalBtu + ' BTU Inverter Air Conditioner Mini Split') + '&tag=' + AFFILIATE_TAG;
      var customDehumUrl = 'https://www.amazon.com/s?k=' + encodeURIComponent(recommendedPints + ' Pint Energy Star Dehumidifier') + '&tag=' + AFFILIATE_TAG;
      var customHepaUrl = 'https://www.amazon.com/s?k=' + encodeURIComponent('True HEPA Air Purifier ' + cadrCfm + ' CADR Large Room') + '&tag=' + AFFILIATE_TAG;

      var html = '<h4>✅ Recommended Hardware Match for Your ' + sqft + ' sq. ft. Room:</h4>' +
        '<p style="font-size:0.9rem; color:#334155; margin-bottom:10px;"><strong>Primary Match:</strong> ' + bestCool.name + ' (' + bestCool.btu_or_cap + ', ' + bestCool.noise_db + ') — ' + bestCool.highlight + '</p>' +
        '<div style="display:flex; gap:8px; flex-wrap:wrap;">' +
        '<a class="btn-amazon" href="' + bestCool.url + '" target="_blank" rel="nofollow sponsored noopener">Check ' + bestCool.name + ' on Amazon &rarr;</a>' +
        '<a class="btn-outline" href="' + customBtuUrl + '" target="_blank" rel="nofollow sponsored noopener">Shop ' + finalBtu.toLocaleString() + ' BTU ACs</a>' +
        '<a class="btn-outline" href="' + customDehumUrl + '" target="_blank" rel="nofollow sponsored noopener">Shop ' + recommendedPints + '-Pint Dehumidifiers</a>' +
        '<a class="btn-outline" href="' + customHepaUrl + '" target="_blank" rel="nofollow sponsored noopener">Shop ' + cadrCfm + '+ CADR HEPA Purifiers</a>' +
        '</div>';

      document.getElementById('dynamicRecContainer').innerHTML = html;
    }}

    function filterClimateCatalog() {{
      var q = (document.getElementById('catalogSearchInput').value || '').toLowerCase().trim();
      var cat = document.getElementById('catalogCatSelect').value;
      var cards = document.querySelectorAll('#bestSellersGrid .product-card');
      var shown = 0;

      cards.forEach(function(c) {{
        var s = c.getAttribute('data-search') || '';
        var cCat = c.getAttribute('data-category') || '';
        var okQ = !q || s.indexOf(q) !== -1;
        var okC = (cat === 'ALL') || (cCat === cat);
        if (okQ && okC) {{
          c.style.display = 'flex';
          shown++;
        }} else {{
          c.style.display = 'none';
        }}
      }});

      var artCards = document.querySelectorAll('#dailyReviewsGrid .article-card');
      artCards.forEach(function(ac) {{
        var aSearch = ac.getAttribute('data-art-search') || '';
        ac.style.display = (!q || aSearch.indexOf(q) !== -1) ? 'flex' : 'none';
      }});

      document.getElementById('filterStatusText').textContent =
        'Showing ' + shown + ' matching flagship system(s) (and filtered daily review articles below):';
    }}

    function searchAmazonDirectly() {{
      var q = document.getElementById('catalogSearchInput').value.trim() || 'Inverter Air Conditioner Dehumidifier HEPA Air Purifier';
      window.open('https://www.amazon.com/s?k=' + encodeURIComponent(q) + '&tag=' + AFFILIATE_TAG, '_blank');
    }}

    calculateClimate();
  </script>
</body>
</html>"""


def generate_sitemaps_and_feeds(all_articles: list[dict]) -> list[str]:
    """Menghasilkan sitemap.xml, sitemap.html, robots.txt, feed.xml, dan kunci verifikasi IndexNow."""
    today_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    urls = [f"{BASE_URL}/index.html", f"{BASE_URL}/sitemap.html"]

    sitemap_entries = f"""  <url>
    <loc>{BASE_URL}/index.html</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{BASE_URL}/sitemap.html</loc>
    <lastmod>{today_iso}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>\n"""

    for art in all_articles:
        u = f"{BASE_URL}/reviews/{art['slug']}.html"
        urls.append(u)
        sitemap_entries += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{art['date']}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>\n"""

    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    # Build HTML Site Map Page (sitemap.html)
    html_sitemap = build_html_sitemap_page(all_articles)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(html_sitemap)

    # robots.txt
    robots_txt = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    # RSS 2.0 Feed (feed.xml)
    rss_items = ""
    for art in all_articles[:30]:
        u = f"{BASE_URL}/reviews/{art['slug']}.html"
        rss_items += f"""    <item>
      <title><![CDATA[{art['title']}]]></title>
      <link>{u}</link>
      <guid>{u}</guid>
      <pubDate>{art['date']}T05:30:00Z</pubDate>
      <description><![CDATA[Room sizing & performance test of the {art['brand']} {art['model_name']} (covers up to {art['max_sqft']} sq. ft. at {art['noise_dba']}) for {art['app_title']}.]]></description>
    </item>\n"""

    rss_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>ClimateSizeCalc — Daily HVAC, Dehumidifier &amp; Air Purifier Reviews</title>
    <link>{BASE_URL}/index.html</link>
    <description>Automated daily room sizing guides and hands-on reviews for portable ACs, mini-splits, dehumidifiers, and HEPA air purifiers.</description>
    <language>en-us</language>
{rss_items}  </channel>
</rss>"""

    with open(os.path.join(OUTPUT_DIR, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(rss_xml)

    # IndexNow key verification file
    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

    return urls


def ping_indexnow(newly_added: list[dict]):
    """Mengirimkan ping otomatis ke IndexNow API agar Bing, Yandex, Seznam, dan Naver langsung mengindeks 3 artikel baru setiap hari."""
    host = urllib.parse.urlparse(BASE_URL).netloc
    url_list = [
        f"{BASE_URL}/index.html",
        f"{BASE_URL}/sitemap.html",
        f"{BASE_URL}/sitemap.xml"
    ]
    for art in newly_added:
        url_list.append(f"{BASE_URL}/reviews/{art['slug']}.html")

    payload = json.dumps({
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": url_list
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[IndexNow] Pinged {len(url_list)} URLs successfully (HTTP {resp.status})")
    except Exception as exc:
        print(f"[IndexNow] Notice (non-blocking): {exc}")


def main():
    os.makedirs(REVIEWS_DIR, exist_ok=True)
    all_articles, newly_added = load_and_advance_state()

    # 1. Build Homepage
    index_html = build_index_page(all_articles)
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # 2. Build Individual Review Pages
    for art in all_articles:
        page_html = build_article_page(art, all_articles)
        out_path = os.path.join(REVIEWS_DIR, f"{art['slug']}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(page_html)

    # 3. Build XML Sitemap, HTML Site Map, Robots.txt, RSS Feed & Ping IndexNow
    generate_sitemaps_and_feeds(all_articles)
    ping_indexnow(newly_added)

    print(f"ClimateSizeCalc build finished! Total articles live: {len(all_articles)} (+{len(newly_added)} added today).")


if __name__ == "__main__":
    main()
