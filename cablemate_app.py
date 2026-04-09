import streamlit as st
import math
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components
import os

# ─────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────
st.set_page_config(page_title="CableMate", layout="wide", page_icon="⚡")

# ─────────────────────────────────────────────────
# GLOBAL CSS  — Light "Luxury EPC" Theme
# ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;0,9..144,700;1,9..144,300&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

/* ── TOKENS ─────────────────────────────────────── */
:root {
  --bg:          #f7f6f2;
  --surface:     #ffffff;
  --surface2:    #f0efe9;
  --border:      #e2dfd6;
  --border-dark: #c8c4b8;
  --accent:      #c0392b;     /* deep engineering red */
  --accent2:     #e74c3c;
  --accent-soft: #fdf1f0;
  --amber:       #d35400;
  --green:       #1a7a4a;
  --green-bg:    #edf7f1;
  --red-bg:      #fdf1f0;
  --warn-bg:     #fef9ec;
  --warn:        #b7791f;
  --text-hi:     #1a1916;
  --text-mid:    #5a574f;
  --text-lo:     #9e9b94;
  --shadow-sm:   0 1px 4px rgba(0,0,0,0.06);
  --shadow-md:   0 4px 20px rgba(0,0,0,0.08);
  --shadow-lg:   0 8px 40px rgba(0,0,0,0.10);
  --radius:      12px;
  --font-head:   'Fraunces', Georgia, serif;
  --font-body:   'DM Sans', sans-serif;
  --font-mono:   'DM Mono', monospace;
}

/* ── BASE ────────────────────────────────────────── */
html, body, .stApp {
  background-color: var(--bg) !important;
  font-family: var(--font-body) !important;
  color: var(--text-hi) !important;
}
.block-container {
  padding: 0 2.5rem 5rem !important;
  max-width: 1380px !important;
}
#MainMenu, footer, header { visibility: hidden !important; }

/* ── SIDEBAR ─────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}

/* ── HERO HEADER ─────────────────────────────────── */
.cm-hero {
  background: var(--surface);
  border-bottom: 3px solid var(--accent);
  padding: 2rem 2.5rem 1.6rem;
  margin: 0 -2.5rem 2.5rem;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  box-shadow: var(--shadow-sm);
}
.cm-hero-left { display: flex; align-items: center; gap: 1.2rem; }
.cm-logo {
  width: 52px; height: 52px;
  background: var(--accent);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem;
  box-shadow: 0 4px 14px rgba(192,57,43,0.35);
  flex-shrink: 0;
}
.cm-brand-name {
  font-family: var(--font-head) !important;
  font-size: 2.2rem !important;
  font-weight: 700 !important;
  color: var(--text-hi) !important;
  letter-spacing: -0.5px;
  line-height: 1;
  margin: 0;
}
.cm-brand-sub {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  color: var(--text-lo) !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  margin-top: 5px;
}
.cm-hero-right {
  display: flex; gap: 10px; align-items: center;
}
.cm-pill {
  font-family: var(--font-mono) !important;
  font-size: 0.62rem !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
  padding: 5px 12px;
  border-radius: 20px;
  border: 1px solid var(--border-dark);
  color: var(--text-mid);
  background: var(--surface2);
}
.cm-pill-red {
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-soft);
}

/* ── SECTION CARD ────────────────────────────────── */
.cm-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.8rem 2rem 1.6rem;
  margin-bottom: 1.4rem;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}
.cm-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--amber));
}
.cm-card-blue::before  { background: linear-gradient(90deg, #1a5276, #2e86c1); }
.cm-card-green::before { background: linear-gradient(90deg, #1a7a4a, #27ae60); }
.cm-card-amber::before { background: linear-gradient(90deg, #d35400, #e67e22); }
.cm-card-slate::before { background: linear-gradient(90deg, #4a4e5a, #7f8492); }

.cm-section-heading {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1.4rem;
}
.cm-section-icon {
  width: 34px; height: 34px;
  border-radius: 8px;
  background: var(--surface2);
  border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
}
.cm-section-title {
  font-family: var(--font-head) !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
  color: var(--text-hi) !important;
  letter-spacing: 0.3px !important;
}
.cm-section-tag {
  margin-left: auto;
  font-family: var(--font-mono) !important;
  font-size: 0.6rem !important;
  color: var(--text-lo) !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
}

/* ── INPUTS ──────────────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-hi) !important;
  font-family: var(--font-body) !important;
  font-size: 0.9rem !important;
  transition: all 0.18s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important;
  background: var(--surface) !important;
  box-shadow: 0 0 0 3px rgba(192,57,43,0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: var(--surface2) !important;
  border: 1.5px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-hi) !important;
}
label[data-testid="stWidgetLabel"] p {
  font-family: var(--font-mono) !important;
  font-size: 0.7rem !important;
  font-weight: 500 !important;
  color: var(--text-mid) !important;
  letter-spacing: 0.5px !important;
  text-transform: uppercase !important;
  margin-bottom: 4px !important;
}

/* ── BUTTONS ─────────────────────────────────────── */
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button {
  background: var(--accent) !important;
  border: none !important;
  border-radius: 8px !important;
  color: white !important;
  font-family: var(--font-body) !important;
  font-size: 0.92rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.3px !important;
  padding: 0.7rem 2.2rem !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 3px 14px rgba(192,57,43,0.28) !important;
}
div[data-testid="stButton"] > button:hover {
  background: var(--accent2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(192,57,43,0.38) !important;
}
div[data-testid="stDownloadButton"] > button {
  background: var(--surface) !important;
  border: 1.5px solid var(--accent) !important;
  border-radius: 8px !important;
  color: var(--accent) !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  transition: all 0.18s !important;
}
div[data-testid="stDownloadButton"] > button:hover {
  background: var(--accent-soft) !important;
}

/* ── METRIC ──────────────────────────────────────── */
div[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 1.1rem 1.3rem !important;
  box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stMetricLabel"] p {
  font-family: var(--font-mono) !important;
  font-size: 0.68rem !important;
  text-transform: uppercase !important;
  letter-spacing: 1px !important;
  color: var(--text-lo) !important;
}
div[data-testid="stMetricValue"] {
  font-family: var(--font-head) !important;
  font-size: 1.55rem !important;
  color: var(--text-hi) !important;
  font-weight: 600 !important;
}

/* ── ALERTS ──────────────────────────────────────── */
div[data-testid="stAlert"] {
  border-radius: 8px !important;
  font-family: var(--font-body) !important;
  font-size: 0.9rem !important;
  border-left-width: 3px !important;
}
div[data-testid="stAlert"][class*="success"] {
  background: var(--green-bg) !important;
  border-color: var(--green) !important;
  color: #145a38 !important;
}
div[data-testid="stAlert"][class*="error"] {
  background: var(--red-bg) !important;
  border-color: var(--accent) !important;
  color: #922b21 !important;
}
div[data-testid="stAlert"][class*="warning"] {
  background: var(--warn-bg) !important;
  border-color: var(--warn) !important;
  color: #7d5a17 !important;
}
div[data-testid="stAlert"][class*="info"] {
  background: #eaf3fb !important;
  border-color: #2e86c1 !important;
  color: #1a5276 !important;
}

/* ── CAPTION ─────────────────────────────────────── */
div[data-testid="stCaptionContainer"] p {
  font-family: var(--font-mono) !important;
  font-size: 0.67rem !important;
  color: var(--text-lo) !important;
  letter-spacing: 0.3px !important;
}

/* ── DIVIDER ─────────────────────────────────────── */
hr {
  border: none !important;
  border-top: 1px solid var(--border) !important;
  margin: 1.5rem 0 !important;
}

/* ── H3 OVERRIDES ────────────────────────────────── */
h3 {
  font-family: var(--font-head) !important;
  font-size: 1rem !important;
  font-weight: 600 !important;
  color: var(--text-hi) !important;
  margin-top: 1.6rem !important;
  letter-spacing: 0.2px !important;
}

/* ── RESULT BANNER ───────────────────────────────── */
.cm-result {
  background: linear-gradient(135deg, #edf7f1 0%, #f0faf5 100%);
  border: 1.5px solid #27ae60;
  border-left: 5px solid var(--green);
  border-radius: var(--radius);
  padding: 1.4rem 1.8rem;
  margin: 1.2rem 0;
}
.cm-result-eyebrow {
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
  color: var(--green) !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
}
.cm-result-cable {
  font-family: var(--font-head) !important;
  font-size: 1.8rem !important;
  font-weight: 700 !important;
  color: #145a38 !important;
  margin-top: 4px !important;
  letter-spacing: -0.5px !important;
}

/* ── KT BOX ──────────────────────────────────────── */
.cm-kt {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.4rem 2rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
}
.cm-kt-label {
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
  color: var(--text-lo) !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
}
.cm-kt-val {
  font-family: var(--font-head) !important;
  font-size: 2.4rem !important;
  font-weight: 700 !important;
  color: var(--accent) !important;
  line-height: 1.1 !important;
  margin: 4px 0 2px !important;
}

/* ── PROJECT STRIP ───────────────────────────────── */
.cm-proj-strip {
  background: var(--text-hi);
  border-radius: var(--radius);
  padding: 1rem 1.8rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  align-items: center;
  margin-bottom: 1.6rem;
}
.cm-proj-item { display: flex; flex-direction: column; gap: 2px; }
.cm-proj-key {
  font-family: var(--font-mono) !important;
  font-size: 0.58rem !important;
  color: rgba(255,255,255,0.45) !important;
  letter-spacing: 1.5px !important;
  text-transform: uppercase !important;
}
.cm-proj-val {
  font-family: var(--font-body) !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
  color: rgba(255,255,255,0.9) !important;
}
.cm-proj-divider {
  width: 1px; height: 30px;
  background: rgba(255,255,255,0.15);
}

/* ── CHECK TABLE ─────────────────────────────────── */
.cm-check {
  display: flex; align-items: center;
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--border);
  gap: 12px;
}
.cm-check:last-child { border-bottom: none; }
.cm-check-label {
  font-family: var(--font-body);
  font-size: 0.88rem;
  color: var(--text-mid);
  flex: 1;
}
.cm-check-val {
  font-family: var(--font-mono);
  font-size: 0.82rem;
  color: var(--text-hi);
}
.cm-pass { color: var(--green) !important; font-weight: 600; font-family: var(--font-mono); font-size: 0.78rem; }
.cm-fail { color: var(--accent) !important; font-weight: 600; font-family: var(--font-mono); font-size: 0.78rem; }

/* ── NUMBER INPUT CONTROLS ───────────────────────── */
div[data-testid="stNumberInput"] button {
  background: var(--surface2) !important;
  border-color: var(--border) !important;
  color: var(--text-mid) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# CLOSE WARNING
# ─────────────────────────────────────────────────
components.html("""
<script>
let changed=false;
document.addEventListener("input",()=>{changed=true;});
window.onbeforeunload=function(e){
if(changed){e.preventDefault();e.returnValue='';}
};
</script>
""", height=0)

# ─────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────
st.markdown("""
<div class="cm-hero">
  <div class="cm-hero-left">
    <div class="cm-logo">⚡</div>
    <div>
      <div class="cm-brand-name">CableMate</div>
      <div class="cm-brand-sub">MV Cable Sizing &amp; Analysis Platform</div>
    </div>
  </div>
  <div class="cm-hero-right">
    <span class="cm-pill">IEC 60287 · 60949 · 60364</span>
    <span class="cm-pill cm-pill-red">v 2.0</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# HELPER: section card opener
# ─────────────────────────────────────────────────
def open_card(icon, title, tag="", color=""):
    cls = f"cm-card cm-card-{color}" if color else "cm-card"
    st.markdown(f"""
    <div class="{cls}">
      <div class="cm-section-heading">
        <div class="cm-section-icon">{icon}</div>
        <div class="cm-section-title">{title}</div>
        <div class="cm-section-tag">{tag}</div>
      </div>
    """, unsafe_allow_html=True)

def close_card():
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# ① PROJECT INFORMATION
# ─────────────────────────────────────────────────
open_card("📁", "Project Information", "STEP 01", "blue")

col1, col2 = st.columns(2)
with col1:
    client_name  = st.text_input("Client Name", "ABC Pvt Ltd")
    feeder_from  = st.selectbox("From Equipment", ["Switchgear", "Transformer", "Generator"])
    from_tag     = st.text_input("From Equipment Tag", placeholder="e.g. TR-01 / SWGR-A1")
    voltage      = st.selectbox("System Voltage (kV)", [3.3, 6.6, 11, 25, 33, 66, 132])
with col2:
    project_name = st.text_input("Project Name", "Electrical Distribution System")
    feeder_to    = st.selectbox("To Equipment", ["Motor", "Transformer", "Panel"])
    to_tag       = st.text_input("To Equipment Tag", placeholder="e.g. MTR-01 / PNL-B2")
    length       = st.number_input("Cable Length (m)", value=300)

close_card()

# ─────────────────────────────────────────────────
# ② INSTALLATION DETAILS
# ─────────────────────────────────────────────────
open_card("🛠", "Installation Details", "STEP 02", "slate")

col1, col2 = st.columns(2)
with col1:
    laying = st.selectbox("Cable Laying Method", ["Direct Buried", "Air", "Duct"])
with col2:
    pass

close_card()

# ─────────────────────────────────────────────────
# ③ LOAD DETAILS
# ─────────────────────────────────────────────────
open_card("⚡", "Load Details", "STEP 03", "amber")

col1, col2 = st.columns(2)
with col1:
    load_type = st.selectbox("Load Type", ["Motor", "Transformer", "Power"])
    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=500)
    else:
        power = st.number_input("Load (kW)", value=400)
with col2:
    pf  = st.number_input("Power Factor", value=0.9)
    eff = st.number_input("Efficiency", value=0.95)

close_card()

# ─────────────────────────────────────────────────
# ④ CONDUCTOR DETAILS
# ─────────────────────────────────────────────────
open_card("🧵", "Conductor Details", "STEP 04")

col1, col2, col3 = st.columns(3)
with col1:
    material = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
with col2:
    cable_type = st.selectbox("Cable Type", ["1-Core", "3-Core"])
with col3:
    starting_multiple = st.number_input("Motor Starting Current Multiple", value=9.5)

if voltage >= 66 and cable_type == "3-Core":
    st.warning("At 66 kV and above, single-core cables are typically used.")

close_card()

# ─────────────────────────────────────────────────
# ⑤ FAULT CONDITIONS
# ─────────────────────────────────────────────────
open_card("⚠", "Fault Conditions", "STEP 05", "amber")

col1, col2 = st.columns(2)
with col1:
    fault      = st.number_input("Fault Level (kA)", value=25)
with col2:
    fault_time = st.number_input("Fault Duration (s)", value=0.4)

close_card()

# ─────────────────────────────────────────────────
# ⑥ VOLTAGE DROP LIMITS
# ─────────────────────────────────────────────────
open_card("📉", "Voltage Drop Limits", "STEP 06", "blue")

col1, col2 = st.columns(2)
with col1:
    vd_run_limit = st.number_input("Running Voltage Drop (%)", value=5.0)
with col2:
    if load_type == "Motor":
        vd_start_limit = st.number_input("Starting Voltage Drop (%)", value=15.0)
    else:
        vd_start_limit = None

close_card()

# ─────────────────────────────────────────────────
# ⑦ DERATING FACTORS
# ─────────────────────────────────────────────────
open_card("🌡", "Derating Factors", "STEP 07", "slate")

def input_with_other(label, options, default):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        choice = st.selectbox(label, options + ["Other"], key=f"{label}_select")
    if choice == "Other":
        with col_b:
            return st.number_input("Manual", value=float(default), step=0.01,
                                   format="%.3f", key=f"{label}_manual")
    return float(choice)

col1, col2 = st.columns(2)
with col1:
    soil  = input_with_other("Soil Resistance Factor", [1.0, 1.5, 2], 1.5)
    group = input_with_other("Grouping Factor", [1, 0.85, 0.79, 0.73], 1.0)
with col2:
    depth = input_with_other("Depth Factor", [0.8, 1.0], 1.0)
    temp  = input_with_other("Temperature Factor", [1, 0.85], 1.0)

# laying factor logic (unchanged)
if laying == "Air":
    laying_factor = 1.0
elif laying == "Duct":
    laying_factor = 0.9
else:
    laying_factor = 0.85

close_card()

# ─────────────────────────────────────────────────
# kT DISPLAY
# ─────────────────────────────────────────────────
kT_base = soil * depth * group * temp

_, col_kt, _ = st.columns([1, 2, 1])
with col_kt:
    st.markdown(f"""
    <div class="cm-kt">
      <div class="cm-kt-label">Overall Derating Factor (kT)</div>
      <div class="cm-kt-val">{round(kT_base, 3)}</div>
      <div class="cm-kt-label" style="font-size:0.6rem;color:#b8b5ae;">
        Soil × Depth × Group × Temp &nbsp;·&nbsp; Grouping factor applied automatically for multiple runs
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# PROJECT SUMMARY STRIP
# ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="cm-proj-strip">
  <div class="cm-proj-item">
    <span class="cm-proj-key">Client</span>
    <span class="cm-proj-val">{client_name}</span>
  </div>
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Project</span>
    <span class="cm-proj-val">{project_name}</span>
  </div>
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Feeder</span>
    <span class="cm-proj-val">{feeder_from} → {feeder_to}</span>
  </div>
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Voltage</span>
    <span class="cm-proj-val">{voltage} kV</span>
  </div>
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Length</span>
    <span class="cm-proj-val">{length} m</span>
  </div>
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Material</span>
    <span class="cm-proj-val">{material}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# RUN BUTTON
# ─────────────────────────────────────────────────
_, col_run, _ = st.columns([1, 2, 1])
with col_run:
    if st.button("⚡  Run CableMate Analysis"):
        st.session_state["run_analysis"] = True

# ─────────────────────────────────────────────────
# CATALOG  (unchanged)
# ─────────────────────────────────────────────────
catalog_cu = {
    "sizes": [50, 70, 95, 120, 150, 185, 240, 300],
    "amp":   {50:181, 70:220, 95:263, 120:298, 150:332, 185:374, 240:431, 300:482},
    "R":     {50:0.387, 70:0.268, 95:0.193, 120:0.153, 150:0.124, 185:0.099, 240:0.075, 300:0.060},
    "X":     {50:0.111, 70:0.106, 95:0.094, 120:0.091, 150:0.089, 185:0.086, 240:0.083, 300:0.082},
}
catalog_al = {
    "sizes": [50, 70, 95, 120, 150, 185, 240, 300],
    "amp":   {50:150, 70:180, 95:215, 120:245, 150:275, 185:310, 240:360, 300:405},
    "R":     {50:0.387, 70:0.268, 95:0.247, 120:0.153, 150:0.124, 185:0.129, 240:0.098, 300:0.080, 400:0.060},
    "X":     {50:0.111, 70:0.106, 95:0.094, 120:0.091, 150:0.089, 185:0.086, 240:0.083, 300:0.082},
}
catalog = catalog_cu if material == "Copper" else catalog_al

# ─────────────────────────────────────────────────
# FUNCTIONS  (unchanged logic)
# ─────────────────────────────────────────────────
def load_current():
    if load_type == "Motor":
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf * eff)
    elif load_type == "Transformer":
        return power * 1000 / (math.sqrt(3) * voltage * 1000)
    else:
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf)

def short_circuit():
    k = 143 if material == "Copper" else 94
    if feeder_from == "Switchgear":
        t = min(fault_time, 0.3)
    else:
        t = fault_time
    if feeder_to == "Motor":
        fault_effective = fault * 0.65   # motor feeder correction
    else:
        fault_effective = fault

    S = (fault_effective * 1000 * math.sqrt(t)) / k
    return S
    
def vd(I, R, X, runs):
    ang = math.acos(pf)
    return (math.sqrt(3) * I * (R * math.cos(ang) + X * math.sin(ang)) * (length / 1000)) / (voltage * 1000 * runs) * 100

def vd_start(I, R, X, runs):
    Ist = starting_multiple * I
    ang = math.acos(0.2)
    return (math.sqrt(3) * Ist * (R * math.cos(ang) + X * math.sin(ang)) * length) / (1000 * runs * voltage * 1000) * 100

def get_rules(feeder_from, feeder_to, load_type):
    if feeder_from == "Switchgear" and feeder_to == "Motor":
        return {"max_runs": 10, "allow_multi_run": True}
    elif feeder_from == "Switchgear" and feeder_to == "Transformer":
        return {"max_runs": 1, "allow_multi_run": False}
    elif feeder_from == "Generator" and feeder_to == "Motor":
        return {"max_runs": 1, "allow_multi_run": False}
    else:
        return {"max_runs": 10, "allow_multi_run": True}

# ─────────────────────────────────────────────────
# PDF REPORT  (unchanged logic)
# ─────────────────────────────────────────────────
def report(best, I, S, v, vs):
    f = tempfile.NamedTemporaryFile(delete=False)
    c = canvas.Canvas(f.name, pagesize=A4)
    width, height = A4

    if os.path.exists("kent_cover.png"):
        c.drawImage("kent_cover.png", 0, 0, width=width, height=height)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 720, "PROJECT DETAILS")
    c.setFont("Helvetica", 12)
    y = 690
    c.drawString(50, y, f"Client Name      : {client_name}");            y -= 20
    c.drawString(50, y, f"Project Name     : {project_name}");            y -= 20
    c.drawString(50, y, f"Feeder           : {feeder_from} → {feeder_to}"); y -= 20
    c.drawString(50, y, f"Voltage Level    : {voltage} kV");               y -= 20
    c.drawString(50, y, f"Cable Length     : {length} m");                 y -= 20
    c.drawString(50, y, f"Load Type        : {load_type}");                y -= 20
    c.drawString(50, y, f"Power            : {power}");                    y -= 20
    c.drawString(50, y, f"Laying Method    : {laying}")
    c.showPage()

    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, "CableMate Engineering Report")
    y -= 40
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Selected Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

    kT_rep = soil * depth * group * temp
    amp    = catalog["amp"][best["size"]] * kT_rep * best["runs"]

    y -= 25; c.drawString(50, y, "LOAD CURRENT CALCULATION")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60038 / IEC 60909)")
    y -= 15; c.setFont("Helvetica", 11);         c.drawString(50, y, f"I = {round(I, 2)} A")

    y -= 25; c.drawString(50, y, "AMPACITY CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60287)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Available Ampacity = {round(amp, 1)} A");  y -= 15
    c.drawString(50, y, f"Load Current       = {round(I, 1)} A");   y -= 15
    c.drawString(50, y, f"{round(amp,1)} ≥ {round(I,1)} → PASS ✔")

    y -= 25; c.drawString(50, y, "SHORT CIRCUIT CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60949 / IEC 60364-5-54)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Required Size = {round(S, 1)} mm²");     y -= 15
    c.drawString(50, y, f"{round(S,1)} < {best['size']} mm²");     y -= 15
    c.drawString(50, y, f"Next Standard Size Selected → {best['size']} mm² ✔")

    y -= 25; c.drawString(50, y, "RUNNING VOLTAGE DROP")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Calculated VD = {round(v, 2)} %");       y -= 15
    c.drawString(50, y, f"Allowed VD    = {vd_run_limit} %");      y -= 15
    c.drawString(50, y, f"{round(v,2)} ≤ {vd_run_limit} → PASS ✔")

    if load_type == "Motor":
        y -= 25; c.drawString(50, y, "STARTING VOLTAGE DROP")
        y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60034)")
        y -= 15; c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Calculated VD = {round(vs, 2)} %");  y -= 15
        c.drawString(50, y, f"Allowed VD    = {vd_start_limit} %"); y -= 15
        c.drawString(50, y, f"{round(vs,2)} ≤ {vd_start_limit} → PASS ✔")

    y -= 25; c.drawString(50, y, "DERATING FACTOR")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11); c.drawString(50, y, f"kT = {round(kT_rep, 2)}")

    y -= 30
    if y < 100:
        c.showPage(); y = 750

    c.setFont("Helvetica-Bold", 12); c.drawString(50, y, "FINAL ENGINEERING DECISION")
    y -= 20; c.setFont("Helvetica", 10)
    c.drawString(50, y, "• IEC 60364 – Electrical Installations");  y -= 15
    c.drawString(50, y, "• IEC 60287 – Cable Current Rating");      y -= 15
    c.drawString(50, y, "• IEC 60949 – Short Circuit Capacity");    y -= 15
    c.drawString(50, y, "• IEC 60034 – Motor Starting");            y -= 15
    c.drawString(50, y, "• IEC 60947 – Protection Systems");        y -= 15
    c.drawString(50, y, "• Cable Data: Oman Cable Catalogue");      y -= 15
    y -= 20; c.setFont("Helvetica", 11)
    if best:
        c.drawString(50, y, "All design checks (Ampacity, Voltage Drop, Short Circuit)"); y -= 15
        c.drawString(50, y, "have been successfully satisfied.")
    else:
        c.drawString(50, y, "No cable satisfies all design criteria.")
    y -= 20; c.setFont("Helvetica-Bold", 11)
    if best:
        c.drawString(50, y, f"FINAL SELECTED CABLE: {best['runs']}R x 3C x {best['size']} sq.mm")
    else:
        c.drawString(50, y, "FINAL SELECTED CABLE: No suitable cable found")
    c.save()
    return f.name

# ─────────────────────────────────────────────────
# ENGINE  (unchanged logic)
# ─────────────────────────────────────────────────

if st.session_state.get("run_analysis", False):
    I = load_current()
    if feeder_to == "Transformer":
        I = I * 1

    S     = short_circuit()
    rules = get_rules(feeder_from, feeder_to, load_type)
    st.write("FINAL S VALUE:", round(S, 2))
    best  = None
    v     = 0
    vs    = 0
    valid_options = []
    
    for size in catalog["sizes"]:
        for runs in range(1, rules["max_runs"] + 1):
            if not rules["allow_multi_run"] and runs > 1:
                continue

            kT_local = soil * depth * group * temp
            debug_data = []

                for size in catalog["sizes"]:
                    for runs in range(1, rules["max_runs"] + 1):

                        debug_data.append({
                            "size": size,
                            "runs": runs,
                            "S_required": round(S, 2),
                            "size>=S": size >= S
                        })

                st.write(debug_data)
            if feeder_to == "Transformer":
                if size <= S:
                    continue
            
            elif feeder_to == "Motor":
            # Each cable must independently withstand fault
                if size < S:
                    continue
            else:
                if (size * runs) < S:
                    continue
            
            amp = catalog["amp"][size] * kT_local * runs
            if amp < I:
                continue

            v_temp = vd(I, catalog["R"][size], catalog["X"][size], runs)
            vd_limit_check = 1.0 if feeder_to == "Transformer" else vd_run_limit
            if v_temp > vd_limit_check:
                continue

            if load_type == "Motor":
                vs_temp = vd_start(I, catalog["R"][size], catalog["X"][size], runs)
                if vs_temp > vd_start_limit:
                    continue
            else:
                vs_temp = 0

            valid_options.append({"size": size, "runs": runs, "v": v_temp, "vs": vs_temp, "amp": amp})

    if valid_options:
        if feeder_to == "Transformer":
            best = sorted(valid_options, key=lambda x: x["size"])[0]
        elif feeder_to == "Motor":
            single_run = [x for x in valid_options if x["runs"] == 1]
            multi_run  = [x for x in valid_options if x["runs"] > 1]
            if single_run:
                best_single    = sorted(single_run, key=lambda x: x["size"])[0]
                min_multi_size = min(x["size"] for x in multi_run) if multi_run else best_single["size"]
                if best_single["size"] <= min_multi_size * 1.5:
                    best = best_single
                else:
                    best = sorted(multi_run, key=lambda x: (x["runs"], x["size"]))[0]
            else:
                best = sorted(multi_run, key=lambda x: (x["runs"], x["size"]))[0]
        else:
            best = sorted(valid_options, key=lambda x: (x["runs"], x["size"]))[0]

        if best:
            v  = best["v"]
            vs = best["vs"]

    st.session_state.update({
        "best": best, "v": v, "vs": vs,
        "calculated": True, "I": I, "S": S,
    })

# ─────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────
if "calculated" in st.session_state:
    best = st.session_state["best"]
    I    = st.session_state["I"]
    S    = st.session_state["S"]
    v    = st.session_state["v"]
    vs   = st.session_state["vs"]

    st.markdown("<br>", unsafe_allow_html=True)

    if best:
        core_str  = "3C" if cable_type == "3-Core" else "1C"
        cable_str = f"{best['runs']}R × {core_str} × {best['size']} mm²"

        st.markdown(f"""
        <div class="cm-result">
          <div class="cm-result-eyebrow">✔ &nbsp; Optimal Cable Selected</div>
          <div class="cm-result-cable">{cable_str}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── CALCULATION SHEET ──────────────────────────
        open_card("📄", "Cable Calculation Sheet", "IEC VERIFIED", "green")

        # (I) Current
        st.markdown("### (I) &nbsp; Current Calculation")
        st.caption("IEC 60038 / IEC 60909 — Load Current Calculation")
        c1, c2, c3 = st.columns(3)
        c1.metric("Voltage", f"{voltage} kV")
        c2.metric("Load", f"{power} {'kVA' if load_type=='Transformer' else 'kW'}")
        c3.metric("Calculated Current", f"{round(I, 2)} A")

        st.divider()

        # (II) Ampacity
        st.markdown("### (II) &nbsp; Ampacity Check")
        st.caption("IEC 60287 — Current Carrying Capacity of Cables")
        kT_calc       = soil * depth * group * temp
        amp_available = catalog["amp"][best["size"]] * kT_calc * best["runs"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Base Ampacity",      f"{catalog['amp'][best['size']]} A")
        c2.metric("Derating Factor kT", f"{round(kT_calc, 3)}")
        c3.metric("Available Ampacity", f"{round(amp_available, 1)} A")
        if amp_available >= I:
            st.success("✅  Ampacity Check — PASS")
        else:
            st.error("❌  Ampacity Check — FAIL")

        st.divider()

        # (III) Short Circuit
        st.markdown("### (III) &nbsp; Short Circuit Check")
        st.caption("IEC 60949 / IEC 60364-5-54 — Short Circuit Withstand Capacity")
        if feeder_to == "Motor":
            sc_area_best = best["size"]   # per cable check
        else:
            sc_area_best = best["size"] * best["runs"]
        c1, c2 = st.columns(2)
        c1.metric("Required Area",  f"{round(S, 2)} mm²")
        c2.metric("Available Area", f"{round(sc_area_best, 2)} mm²")
        if sc_area_best >= S:
            st.success("✅  Short Circuit Check — PASS")
        else:
            st.error("❌  Short Circuit Check — FAIL")

        st.divider()

        # (IV) Voltage Drop
        st.markdown("### (IV) &nbsp; Voltage Drop Check")
        st.caption("IEC 60364-5-52 — Voltage Drop Limits")
        vd_limit_display = 1 if feeder_to == "Transformer" else (5 if feeder_to == "Motor" else vd_run_limit)
        c1, c2 = st.columns(2)
        c1.metric("Calculated VD",  f"{round(v, 2)} %")
        c2.metric("Permissible VD", f"{vd_limit_display} %")
        if v <= vd_limit_display:
            st.success("✅  Running Voltage Drop — PASS")
        else:
            st.error("❌  Running Voltage Drop — FAIL")

        if load_type == "Motor":
            st.caption("IEC 60034 — Motor Starting Performance")
            c1, c2 = st.columns(2)
            c1.metric("Starting VD",  f"{round(vs, 2)} %")
            c2.metric("Permissible",  f"{vd_start_limit} %")
            if vs <= vd_start_limit:
                st.success("✅  Starting Voltage Drop — PASS")
            else:
                st.error("❌  Starting Voltage Drop — FAIL")

        st.divider()

        # (V) Final
        st.markdown("### (V) &nbsp; Final Cable Selection")
        st.caption("Based on IEC Standards + Oman Cable Catalogue")
        final_str = f"{best['runs']}R × {'3C' if cable_type=='3-Core' else '1C'} × {best['size']} mm²"
        st.success(f"✅  Selected Cable →  {final_str}")

        st.markdown("### 🧠 &nbsp; Engineering Statement")
        st.info(
            "All design checks including ampacity, voltage drop, and short circuit "
            "withstand capability have been satisfied. The selected cable is safe "
            "and suitable for the given application."
        )

        close_card()

        # ── METRIC ROW ─────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Load Current",  f"{round(I, 1)} A")
        m2.metric("Running VD",    f"{round(v, 2)} %")
        if load_type == "Motor":
            m3.metric("Starting VD", f"{round(vs, 2)} %")

        # ── DOWNLOAD ────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_dl, _ = st.columns([1, 2, 1])
        with col_dl:
            pdf = report(best, I, S, v, vs)
            with open(pdf, "rb") as f_pdf:
                st.download_button(
                    "📥  Download Engineering Report (PDF)",
                    f_pdf,
                    "CableMate_Report.pdf",
                    use_container_width=True,
                )
    else:
        st.error("⚠  No suitable cable found for the given parameters.")

# ─────────────────────────────────────────────────
# MANUAL CABLE EVALUATION
# ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
open_card("🔧", "Manual Cable Evaluation", "OVERRIDE", "slate")

col1, col2 = st.columns(2)
with col1:
    manual_size = st.selectbox("Select Cable Size (mm²)", catalog["sizes"], key="manual_size_unique")
with col2:
    manual_runs = st.selectbox("Number of Runs", list(range(1, 11)), key="manual_runs_unique")

_, col_m, _ = st.columns([1, 2, 1])
with col_m:
    apply_manual = st.button("🔧  Apply Manual Selection", use_container_width=True)

close_card()

if apply_manual:
    st.session_state.update({
        "manual_done":      True,
        "calculate_manual": True,
        "selected_size":    manual_size,
        "selected_runs":    manual_runs,
        "selected_type":    cable_type,
    })

# ── MANUAL CALC ────────────────────────────────────
if "calculated" in st.session_state and st.session_state.get("calculate_manual", False):
    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")

    if None not in (manual_size_used, manual_runs_used, manual_type_used):
        kT_local       = soil * depth * group * temp
        amp            = catalog["amp"][manual_size_used] * kT_local * manual_runs_used
        v_manual       = vd(I, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used)
        vs_manual      = vd_start(I, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used) if load_type == "Motor" else 0
        if feeder_to == "Motor":
            sc_area_manual = manual_size_used
        else:
            sc_area_manual = manual_size_used * manual_runs_used
        amp_ok = amp >= I
        vd_ok  = v_manual <= vd_run_limit
        sc_ok  = sc_area_manual >= S
        vs_ok  = (vs_manual <= vd_start_limit) if load_type == "Motor" else True

        st.session_state.update({
            "v_manual": v_manual, "vs_manual": vs_manual,
            "amp_ok": amp_ok, "vd_ok": vd_ok, "vs_ok": vs_ok, "sc_ok": sc_ok,
        })

        manual_label = f"{manual_runs_used}R × {'3C' if manual_type_used=='3-Core' else '1C'} × {manual_size_used} mm²"
        st.caption("Showing last applied manual selection")
        st.markdown(f"**Manual Cable →** `{manual_label}`")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ampacity",      "✅ PASS" if amp_ok else "❌ FAIL")
        c2.metric("Voltage Drop",  "✅ PASS" if vd_ok  else "❌ FAIL")
        c3.metric("Short Circuit", "✅ PASS" if sc_ok  else "❌ FAIL")
        if load_type == "Motor":
            c4.metric("Starting VD", "✅ PASS" if vs_ok else "❌ FAIL")

        if not amp_ok: st.warning("⚠  Ampacity insufficient — cable may overheat.")
        if not vd_ok:  st.warning("⚠  Voltage drop exceeds limit — poor performance expected.")
        if not sc_ok:  st.warning("⚠  Short circuit rating inadequate — risk of damage.")
        if load_type == "Motor" and not vs_ok:
            st.warning("⚠  Starting voltage drop too high — motor may fail to start.")

        st.session_state["calculate_manual"] = False

# ── COMPARISON ─────────────────────────────────────
if "calculated" in st.session_state and "manual_done" in st.session_state:
    best = st.session_state.get("best")
    if not best:
        st.error("No suitable cable found.")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    open_card("🔍", "Best vs Manual Comparison", "ANALYSIS", "blue")

    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")
    core_label       = "3C" if manual_type_used == "3-Core" else "1C"

    best_str_c   = f"{best['runs']}R × {core_label} × {best['size']} mm²"
    manual_str_c = f"{manual_runs_used}R × {core_label} × {manual_size_used} mm²"

    c1, c2 = st.columns(2)
    c1.metric("🏆  Optimal Cable", best_str_c)
    c2.metric("🔧  Manual Cable",  manual_str_c)

    v_manual_val = st.session_state.get("v_manual")
    if v_manual_val is not None:
        diff = round(v_manual_val - v, 2)
        sign = "+" if diff > 0 else ""
        st.metric("Voltage Drop Δ", f"{sign}{diff} %", delta=f"{sign}{diff} %", delta_color="inverse")
    else:
        st.info("Apply manual selection to see comparison.")

    st.markdown("### 🧠 &nbsp; Engineering Reasoning")

    amp_ok_val = st.session_state.get("amp_ok")
    vd_ok_val  = st.session_state.get("vd_ok")
    sc_ok_val  = st.session_state.get("sc_ok")
    vs_ok_val  = st.session_state.get("vs_ok")

    if manual_size_used == best["size"] and manual_runs_used == best["runs"]:
        st.success("✔  Manual cable matches the optimal cable selection — excellent engineering judgement!")
    else:
        if amp_ok_val is False:
            st.error("❌  Manual cable fails due to insufficient ampacity.")
        elif vd_ok_val is False:
            st.error("❌  Manual cable causes excessive voltage drop.")
        elif sc_ok_val is False:
            st.error("❌  Manual cable does not meet short circuit requirements.")
        elif load_type == "Motor" and vs_ok_val is False:
            st.error("❌  Manual cable has unacceptably high starting voltage drop.")
        else:
            st.info("ℹ  Manual cable is technically acceptable but not the most optimal selection.")

    close_card()
