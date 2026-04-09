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

:root {
  --bg:          #f7f6f2;
  --surface:     #ffffff;
  --surface2:    #f0efe9;
  --border:      #e2dfd6;
  --border-dark: #c8c4b8;
  --accent:      #c0392b;
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
  --radius:      12px;
  --font-head:   'Fraunces', Georgia, serif;
  --font-body:   'DM Sans', sans-serif;
  --font-mono:   'DM Mono', monospace;
}

html, body, .stApp {
  background-color: var(--bg) !important;
  font-family: var(--font-body) !important;
  color: var(--text-hi) !important;
}
.block-container { padding: 0 2.5rem 5rem !important; max-width: 1380px !important; }
#MainMenu, footer, header { visibility: hidden !important; }

section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}

.cm-hero {
  background: var(--surface);
  border-bottom: 3px solid var(--accent);
  padding: 2rem 2.5rem 1.6rem;
  margin: 0 -2.5rem 2.5rem;
  display: flex; align-items: flex-end; justify-content: space-between;
  box-shadow: var(--shadow-sm);
}
.cm-hero-left { display: flex; align-items: center; gap: 1.2rem; }
.cm-logo {
  width: 52px; height: 52px; background: var(--accent); border-radius: 10px;
  display: flex; align-items: center; justify-content: center; font-size: 1.5rem;
  box-shadow: 0 4px 14px rgba(192,57,43,0.35); flex-shrink: 0;
}
.cm-brand-name {
  font-family: var(--font-head) !important; font-size: 2.2rem !important;
  font-weight: 700 !important; color: var(--text-hi) !important;
  letter-spacing: -0.5px; line-height: 1; margin: 0;
}
.cm-brand-sub {
  font-family: var(--font-mono) !important; font-size: 0.68rem !important;
  color: var(--text-lo) !important; letter-spacing: 2px !important;
  text-transform: uppercase !important; margin-top: 5px;
}
.cm-hero-right { display: flex; gap: 10px; align-items: center; }
.cm-pill {
  font-family: var(--font-mono) !important; font-size: 0.62rem !important;
  letter-spacing: 1.5px !important; text-transform: uppercase !important;
  padding: 5px 12px; border-radius: 20px; border: 1px solid var(--border-dark);
  color: var(--text-mid); background: var(--surface2);
}
.cm-pill-red { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }

.cm-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1.8rem 2rem 1.6rem;
  margin-bottom: 1.4rem; box-shadow: var(--shadow-sm);
  position: relative; overflow: hidden;
}
.cm-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--amber));
}
.cm-card-blue::before  { background: linear-gradient(90deg, #1a5276, #2e86c1); }
.cm-card-green::before { background: linear-gradient(90deg, #1a7a4a, #27ae60); }
.cm-card-amber::before { background: linear-gradient(90deg, #d35400, #e67e22); }
.cm-card-slate::before { background: linear-gradient(90deg, #4a4e5a, #7f8492); }

.cm-section-heading { display: flex; align-items: center; gap: 10px; margin-bottom: 1.4rem; }
.cm-section-icon {
  width: 34px; height: 34px; border-radius: 8px;
  background: var(--surface2); border: 1px solid var(--border);
  display: flex; align-items: center; justify-content: center; font-size: 0.9rem;
}
.cm-section-title {
  font-family: var(--font-head) !important; font-size: 1.05rem !important;
  font-weight: 600 !important; color: var(--text-hi) !important; letter-spacing: 0.3px !important;
}
.cm-section-tag {
  margin-left: auto; font-family: var(--font-mono) !important; font-size: 0.6rem !important;
  color: var(--text-lo) !important; letter-spacing: 1.5px !important; text-transform: uppercase !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
  background: var(--surface2) !important; border: 1.5px solid var(--border) !important;
  border-radius: 8px !important; color: var(--text-hi) !important;
  font-family: var(--font-body) !important; font-size: 0.9rem !important;
  transition: all 0.18s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
  border-color: var(--accent) !important; background: var(--surface) !important;
  box-shadow: 0 0 0 3px rgba(192,57,43,0.1) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background: var(--surface2) !important; border: 1.5px solid var(--border) !important;
  border-radius: 8px !important; color: var(--text-hi) !important;
}
label[data-testid="stWidgetLabel"] p {
  font-family: var(--font-mono) !important; font-size: 0.7rem !important;
  font-weight: 500 !important; color: var(--text-mid) !important;
  letter-spacing: 0.5px !important; text-transform: uppercase !important; margin-bottom: 4px !important;
}

div[data-testid="stButton"] > button {
  background: var(--accent) !important; border: none !important;
  border-radius: 8px !important; color: white !important;
  font-family: var(--font-body) !important; font-size: 0.92rem !important;
  font-weight: 600 !important; padding: 0.7rem 2.2rem !important;
  transition: all 0.2s ease !important; box-shadow: 0 3px 14px rgba(192,57,43,0.28) !important;
}
div[data-testid="stButton"] > button:hover {
  background: var(--accent2) !important; transform: translateY(-1px) !important;
  box-shadow: 0 6px 22px rgba(192,57,43,0.38) !important;
}
div[data-testid="stDownloadButton"] > button {
  background: var(--surface) !important; border: 1.5px solid var(--accent) !important;
  border-radius: 8px !important; color: var(--accent) !important;
  font-family: var(--font-body) !important; font-weight: 600 !important; font-size: 0.88rem !important;
}
div[data-testid="stDownloadButton"] > button:hover { background: var(--accent-soft) !important; }

div[data-testid="stMetric"] {
  background: var(--surface) !important; border: 1px solid var(--border) !important;
  border-radius: 10px !important; padding: 1.1rem 1.3rem !important; box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stMetricLabel"] p {
  font-family: var(--font-mono) !important; font-size: 0.68rem !important;
  text-transform: uppercase !important; letter-spacing: 1px !important; color: var(--text-lo) !important;
}
div[data-testid="stMetricValue"] {
  font-family: var(--font-head) !important; font-size: 1.55rem !important;
  color: var(--text-hi) !important; font-weight: 600 !important;
}

div[data-testid="stAlert"] {
  border-radius: 8px !important; font-family: var(--font-body) !important;
  font-size: 0.9rem !important; border-left-width: 3px !important;
}
div[data-testid="stAlert"][class*="success"] {
  background: var(--green-bg) !important; border-color: var(--green) !important; color: #145a38 !important;
}
div[data-testid="stAlert"][class*="error"] {
  background: var(--red-bg) !important; border-color: var(--accent) !important; color: #922b21 !important;
}
div[data-testid="stAlert"][class*="warning"] {
  background: var(--warn-bg) !important; border-color: var(--warn) !important; color: #7d5a17 !important;
}
div[data-testid="stAlert"][class*="info"] {
  background: #eaf3fb !important; border-color: #2e86c1 !important; color: #1a5276 !important;
}

div[data-testid="stCaptionContainer"] p {
  font-family: var(--font-mono) !important; font-size: 0.67rem !important;
  color: var(--text-lo) !important; letter-spacing: 0.3px !important;
}
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
h3 {
  font-family: var(--font-head) !important; font-size: 1rem !important;
  font-weight: 600 !important; color: var(--text-hi) !important;
  margin-top: 1.6rem !important; letter-spacing: 0.2px !important;
}

.cm-result {
  background: linear-gradient(135deg, #edf7f1 0%, #f0faf5 100%);
  border: 1.5px solid #27ae60; border-left: 5px solid var(--green);
  border-radius: var(--radius); padding: 1.4rem 1.8rem; margin: 1.2rem 0;
}
.cm-result-eyebrow {
  font-family: var(--font-mono) !important; font-size: 0.65rem !important;
  color: var(--green) !important; letter-spacing: 2px !important; text-transform: uppercase !important;
}
.cm-result-cable {
  font-family: var(--font-head) !important; font-size: 1.8rem !important;
  font-weight: 700 !important; color: #145a38 !important;
  margin-top: 4px !important; letter-spacing: -0.5px !important;
}

.cm-kt {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1.4rem 2rem; text-align: center; box-shadow: var(--shadow-sm);
}
.cm-kt-label {
  font-family: var(--font-mono) !important; font-size: 0.65rem !important;
  color: var(--text-lo) !important; letter-spacing: 2px !important; text-transform: uppercase !important;
}
.cm-kt-val {
  font-family: var(--font-head) !important; font-size: 2.4rem !important;
  font-weight: 700 !important; color: var(--accent) !important; line-height: 1.1 !important; margin: 4px 0 2px !important;
}

.cm-proj-strip {
  background: var(--text-hi); border-radius: var(--radius);
  padding: 1rem 1.8rem; display: flex; flex-wrap: wrap; gap: 1.5rem;
  align-items: center; margin-bottom: 1.6rem;
}
.cm-proj-item { display: flex; flex-direction: column; gap: 2px; }
.cm-proj-key {
  font-family: var(--font-mono) !important; font-size: 0.58rem !important;
  color: rgba(255,255,255,0.45) !important; letter-spacing: 1.5px !important; text-transform: uppercase !important;
}
.cm-proj-val {
  font-family: var(--font-body) !important; font-size: 0.85rem !important;
  font-weight: 500 !important; color: rgba(255,255,255,0.9) !important;
}
.cm-proj-divider { width: 1px; height: 30px; background: rgba(255,255,255,0.15); }

div[data-testid="stNumberInput"] button {
  background: var(--surface2) !important; border-color: var(--border) !important; color: var(--text-mid) !important;
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
# CARD HELPERS
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
# AUTO-SYNC load_type with feeder_to — user does not need to set this separately
# ─────────────────────────────────────────────────
open_card("⚡", "Load Details", "STEP 03", "amber")

# FIX 1: Auto-derive load_type from feeder_to (with fallback selectbox for Panel)
if feeder_to == "Motor":
    load_type = "Motor"
    st.info("ℹ  Load type auto-set to **Motor** based on feeder destination.")
elif feeder_to == "Transformer":
    load_type = "Transformer"
    st.info("ℹ  Load type auto-set to **Transformer** based on feeder destination.")
else:
    # Panel or other — let user choose
    load_type = st.selectbox("Load Type", ["Motor", "Transformer", "Power"])

col1, col2 = st.columns(2)
with col1:
    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=500)
    else:
        power = st.number_input("Load (kW)", value=400)
with col2:
    pf  = st.number_input("Power Factor", value=0.9, min_value=0.01, max_value=1.0, step=0.01, format="%.2f")
    eff = st.number_input("Efficiency", value=0.97, min_value=0.01, max_value=1.0, step=0.01, format="%.2f")
close_card()

# ─────────────────────────────────────────────────
# ④ CONDUCTOR DETAILS
# FIX 2: Starting multiple visible only for Motor; default = 6.0
# ─────────────────────────────────────────────────
open_card("🧵", "Conductor Details", "STEP 04")

if load_type == "Motor":
    col1, col2, col3 = st.columns(3)
    with col1:
        material = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
    with col2:
        cable_type = st.selectbox("Cable Type", ["1-Core", "3-Core"])
    with col3:
        # FIX: Default motor starting multiple = 6.0 per IEC/industry standard
        starting_multiple = st.number_input(
            "Motor Starting Current Multiple",
            value=6.0, min_value=1.0, max_value=15.0, step=0.5, format="%.1f"
        )
else:
    col1, col2 = st.columns(2)
    with col1:
        material = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
    with col2:
        cable_type = st.selectbox("Cable Type", ["1-Core", "3-Core"])
    # FIX: For Transformer/Power feeder — starting multiple not applicable
    starting_multiple = 1.0  # neutral value, won't be used

if voltage >= 66 and cable_type == "3-Core":
    st.warning("⚠  At 66 kV and above, single-core cables are typically used.")
close_card()

# ─────────────────────────────────────────────────
# ⑤ FAULT CONDITIONS
# ─────────────────────────────────────────────────
open_card("⚠", "Fault Conditions", "STEP 05", "amber")
col1, col2 = st.columns(2)
with col1:
    fault      = st.number_input("Fault Level (kA)", value=25.0, step=0.5, format="%.1f")
with col2:
    fault_time = st.number_input("Fault Duration (s)", value=0.4, step=0.05, format="%.2f")
close_card()

# ─────────────────────────────────────────────────
# ⑥ VOLTAGE DROP LIMITS
# ─────────────────────────────────────────────────
open_card("📉", "Voltage Drop Limits", "STEP 06", "blue")
col1, col2 = st.columns(2)
with col1:
    vd_run_limit = st.number_input("Running Voltage Drop (%)", value=5.0, step=0.5, format="%.1f")
with col2:
    if load_type == "Motor":
        vd_start_limit = st.number_input("Starting Voltage Drop (%)", value=15.0, step=0.5, format="%.1f")
    else:
        vd_start_limit = 999.0  # Not applicable — set very high so check always passes
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
    soil  = input_with_other("Soil Resistance Factor", [1.0, 1.5, 2.0], 1.0)
    group = input_with_other("Grouping Factor", [1.0, 0.85, 0.79, 0.73], 1.0)
with col2:
    depth = input_with_other("Depth Factor", [0.8, 1.0], 1.0)
    temp  = input_with_other("Temperature Factor", [1.0, 0.85], 1.0)

# Laying factor (used in ampacity reference but NOT multiplied into kT here
# since catalog amp values are for the respective base condition)
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
kT_base = soil * depth * group * temp * laying_factor

_, col_kt, _ = st.columns([1, 2, 1])
with col_kt:
    st.markdown(f"""
    <div class="cm-kt">
      <div class="cm-kt-label">Overall Derating Factor (kT)</div>
      <div class="cm-kt-val">{round(kT_base, 4)}</div>
      <div class="cm-kt-label" style="font-size:0.6rem;color:#b8b5ae;">
        Soil × Depth × Group × Temp × Laying &nbsp;·&nbsp; Applied to base ampacity from catalog
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
  <div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Load Type</span>
    <span class="cm-proj-val">{load_type}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# RUN BUTTON
# ─────────────────────────────────────────────────
_, col_run, _ = st.columns([1, 2, 1])
with col_run:
    run_btn = st.button("⚡  Run CableMate Analysis", use_container_width=True)

# ─────────────────────────────────────────────────
# CATALOG
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
    "R":     {50:0.387, 70:0.268, 95:0.247, 120:0.153, 150:0.124, 185:0.129, 240:0.098, 300:0.080},
    "X":     {50:0.111, 70:0.106, 95:0.094, 120:0.091, 150:0.089, 185:0.086, 240:0.083, 300:0.082},
}
catalog = catalog_cu if material == "Copper" else catalog_al

# ─────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────

def load_current():
    """
    Calculates full-load current.
    Motor:       I = P / (√3 × V × PF × η)
    Transformer: I = S / (√3 × V)
    Power/Panel: I = P / (√3 × V × PF)
    """
    if load_type == "Motor":
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf * eff)
    elif load_type == "Transformer":
        return power * 1000 / (math.sqrt(3) * voltage * 1000)
    else:
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf)


def short_circuit():
    """
    IEC 60949 formula: A_min = (I_fault × √t) / k
    where:
      I_fault = fault current in Amperes
      t       = fault clearing time in seconds
      k       = 143 for Copper, 94 for Aluminium (PVC insulation, 90°C initial)

    Fault time selection per IEC / industry:
      - Switchgear outgoing feeders → 0.25 s  (fast protection)
      - Other cases                 → user-entered fault_time

    NOTE: No motor correction factor on fault current.
    The full switchboard fault level reaches the cable — this is the
    conservative and IEC-compliant approach for cable sizing.
    """
    k = 143 if material == "Copper" else 94

    # Per IEC 60909 & industry practice for protection coordination:
    if feeder_from == "Switchgear":
        t = 0.25   # switchgear outgoing feeder — relay clears in 250 ms
    else:
        t = fault_time  # incomer or generator feeder — use user value

    S_min = (fault * 1000 * math.sqrt(t)) / k
    return S_min


def vd(I, R, X, runs):
    """
    Running voltage drop (IEC 60364-5-52):
    VD% = (√3 × I × (R·cosφ + X·sinφ) × L) / (V × runs) × 100
    R and X are in Ω/km, L in km.
    """
    ang = math.acos(pf)
    return (math.sqrt(3) * I * (R * math.cos(ang) + X * math.sin(ang)) * (length / 1000)) / (voltage * 1000 * runs) * 100


def vd_start(I, R, X, runs):
    """
    Starting voltage drop (IEC 60034):
    During starting, PF ≈ 0.2 (locked rotor), current = starting_multiple × I_FL
    """
    Ist = starting_multiple * I
    ang = math.acos(0.2)
    return (math.sqrt(3) * Ist * (R * math.cos(ang) + X * math.sin(ang)) * length) / (1000 * runs * voltage * 1000) * 100


def get_rules(feeder_from, feeder_to):
    """
    Rules governing maximum number of parallel runs.
    Transformer feeders: always single run (current sharing issues with xfmr).
    Generator feeders to motor: single run (generator impedance high).
    Others: up to 4 parallel runs (industry standard max for MV).
    """
    if feeder_from == "Switchgear" and feeder_to == "Transformer":
        return {"max_runs": 1, "allow_multi_run": False}
    elif feeder_from == "Generator" and feeder_to == "Motor":
        return {"max_runs": 1, "allow_multi_run": False}
    else:
        return {"max_runs": 4, "allow_multi_run": True}


def select_optimal_cable(valid_options, feeder_to):
    """
    SELECTION LOGIC — Engineering cost-optimised approach:

    Core principle: Among all passing options, find the one with
    the lowest "effective cost index" = runs × size_mm2.

    Why runs × size?
      - More runs = more labour + more joints + more trenching
      - Larger size = more material cost
      - 2 × 95 (index=190) < 1 × 185 (index=185) → nearly equal,
        but 2×95 has more labour → 1×185 preferred if available
      - 2 × 95 (index=190) vs 1 × 240 (index=240) → 2×95 preferred

    Tie-breaking: if cost indices are equal, prefer fewer runs
    (simpler installation), then smaller size.

    Special rule for Transformer feeder:
      - Single run always → just pick smallest passing size.
    """
    if not valid_options:
        return None

    if feeder_to == "Transformer":
        # Single-run only; smallest passing size wins
        return sorted(valid_options, key=lambda x: x["size"])[0]

    # Cost index = runs × size  (proportional to material + labour)
    # Tie-break: fewer runs first, then smaller size
    return sorted(valid_options, key=lambda x: (x["runs"] * x["size"], x["runs"], x["size"]))[0]


# ─────────────────────────────────────────────────
# PDF REPORT
# ─────────────────────────────────────────────────
def report(best, I, S, v, vs):
    f   = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c   = canvas.Canvas(f.name, pagesize=A4)
    width, height = A4

    if os.path.exists("kent_cover.png"):
        c.drawImage("kent_cover.png", 0, 0, width=width, height=height)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 720, "PROJECT DETAILS")
    c.setFont("Helvetica", 12)
    y = 690
    c.drawString(50, y, f"Client Name      : {client_name}");              y -= 20
    c.drawString(50, y, f"Project Name     : {project_name}");              y -= 20
    c.drawString(50, y, f"Feeder           : {feeder_from} → {feeder_to}"); y -= 20
    c.drawString(50, y, f"Voltage Level    : {voltage} kV");                y -= 20
    c.drawString(50, y, f"Cable Length     : {length} m");                  y -= 20
    c.drawString(50, y, f"Load Type        : {load_type}");                 y -= 20
    c.drawString(50, y, f"Power            : {power} {'kVA' if load_type=='Transformer' else 'kW'}"); y -= 20
    c.drawString(50, y, f"Laying Method    : {laying}")
    c.showPage()

    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, "CableMate Engineering Report")
    y -= 40
    c.setFont("Helvetica", 11)
    core_str_pdf = "3C" if cable_type == "3-Core" else "1C"
    c.drawString(50, y, f"Selected Cable: {best['runs']}R x {core_str_pdf} x {best['size']} sq.mm")

    kT_rep = soil * depth * group * temp * laying_factor
    amp    = catalog["amp"][best["size"]] * kT_rep * best["runs"]

    y -= 25; c.drawString(50, y, "LOAD CURRENT CALCULATION")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60038 / IEC 60909)")
    y -= 15; c.setFont("Helvetica", 11);         c.drawString(50, y, f"I_FL = {round(I, 2)} A")

    y -= 25; c.drawString(50, y, "AMPACITY CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60287)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Catalog Ampacity   = {catalog['amp'][best['size']]} A"); y -= 15
    c.drawString(50, y, f"Derating kT        = {round(kT_rep, 4)}");             y -= 15
    c.drawString(50, y, f"Available Ampacity = {round(amp, 1)} A  (= {catalog['amp'][best['size']]} x {round(kT_rep,3)} x {best['runs']} run)"); y -= 15
    c.drawString(50, y, f"Load Current       = {round(I, 1)} A");                y -= 15
    c.drawString(50, y, f"{round(amp, 1)} >= {round(I, 1)} A  → PASS")

    y -= 25; c.drawString(50, y, "SHORT CIRCUIT CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60949 — A_min = I_fault x √t / k)")
    y -= 15; c.setFont("Helvetica", 11)
    sc_area = best["size"] * best["runs"]
    c.drawString(50, y, f"Required min. area  = {round(S, 2)} mm²");            y -= 15
    c.drawString(50, y, f"Provided total area = {round(sc_area, 2)} mm²  ({best['runs']} x {best['size']} mm²)"); y -= 15
    c.drawString(50, y, f"{round(sc_area, 2)} >= {round(S, 2)}  → PASS")

    y -= 25; c.drawString(50, y, "RUNNING VOLTAGE DROP")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Calculated VD   = {round(v, 2)} %"); y -= 15
    c.drawString(50, y, f"Allowed limit   = {vd_run_limit} %"); y -= 15
    c.drawString(50, y, f"{round(v, 2)} <= {vd_run_limit}  → PASS")

    if load_type == "Motor":
        y -= 25; c.drawString(50, y, "STARTING VOLTAGE DROP")
        y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60034 — starting PF = 0.2)")
        y -= 15; c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Starting current   = {round(starting_multiple, 1)} x I_FL = {round(starting_multiple * I, 1)} A"); y -= 15
        c.drawString(50, y, f"Calculated VD      = {round(vs, 2)} %");    y -= 15
        c.drawString(50, y, f"Allowed limit      = {vd_start_limit} %");  y -= 15
        c.drawString(50, y, f"{round(vs, 2)} <= {vd_start_limit}  → PASS")

    y -= 25; c.drawString(50, y, "DERATING FACTOR SUMMARY")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"kT = Soil({soil}) x Depth({depth}) x Group({group}) x Temp({temp}) x Laying({laying_factor}) = {round(kT_rep, 4)}")

    y -= 30
    if y < 100:
        c.showPage(); y = 750

    c.setFont("Helvetica-Bold", 12); c.drawString(50, y, "FINAL ENGINEERING DECISION")
    y -= 20; c.setFont("Helvetica", 10)
    for ref in [
        "IEC 60364 – Electrical Installations",
        "IEC 60287 – Cable Current Rating",
        "IEC 60949 – Short Circuit Capacity",
        "IEC 60034 – Motor Starting",
        "IEC 60947 – Protection Systems",
        "Cable Data: Oman Cable Catalogue",
    ]:
        c.drawString(50, y, f"• {ref}"); y -= 15

    y -= 20; c.setFont("Helvetica", 11)
    c.drawString(50, y, "All design checks (Ampacity, Short Circuit, Voltage Drop)"); y -= 15
    c.drawString(50, y, "have been successfully satisfied.")
    y -= 20; c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"FINAL SELECTED CABLE: {best['runs']}R x {core_str_pdf} x {best['size']} sq.mm")

    c.save()
    return f.name


# ─────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────
if run_btn:
    I = load_current()
    # Safety margin for transformer feeders (NEC/IEC standard practice: 120%)
    if feeder_to == "Transformer":
        I = I * 1.2

    S     = short_circuit()
    rules = get_rules(feeder_from, feeder_to)

    valid_options = []

    for size in catalog["sizes"]:
        for runs in range(1, rules["max_runs"] + 1):

            # Skip multi-run if not allowed for this feeder type
            if not rules["allow_multi_run"] and runs > 1:
                continue

            # ── CHECK 1: SHORT CIRCUIT ──────────────────────────────
            # Total conductor cross-section must meet the IEC 60949 minimum.
            # For a transformer feeder (single run), compare size alone.
            # For all others, total area = size × runs.
            if feeder_to == "Transformer":
                available_sc_area = size          # single cable governs
            else:
                available_sc_area = size * runs   # parallel conductors share fault current

            if available_sc_area < S:
                continue   # does NOT meet SC requirement → skip

            # ── CHECK 2: AMPACITY ───────────────────────────────────
            # Derated ampacity must exceed full-load current
            kT_local = soil * depth * group * temp * laying_factor
            amp      = catalog["amp"][size] * kT_local * runs

            if amp < I:
                continue   # insufficient current capacity → skip

            # ── CHECK 3: RUNNING VOLTAGE DROP ──────────────────────
            v_temp = vd(I, catalog["R"][size], catalog["X"][size], runs)

            if feeder_to == "Transformer":
                vd_limit_check = 1.0   # transformers: max 1% VD at full load
            else:
                vd_limit_check = vd_run_limit

            if v_temp > vd_limit_check:
                continue   # VD too high → skip

            # ── CHECK 4: STARTING VOLTAGE DROP (Motor only) ────────
            if load_type == "Motor":
                vs_temp = vd_start(I, catalog["R"][size], catalog["X"][size], runs)
                if vs_temp > vd_start_limit:
                    continue   # starting VD too high → skip
            else:
                vs_temp = 0.0

            # All checks passed — store as valid candidate
            valid_options.append({
                "size":  size,
                "runs":  runs,
                "v":     v_temp,
                "vs":    vs_temp,
                "amp":   amp,
            })

    # ── OPTIMAL SELECTION ───────────────────────────────────────
    best = select_optimal_cable(valid_options, feeder_to)

    v  = best["v"]  if best else 0.0
    vs = best["vs"] if best else 0.0

    st.session_state.update({
        "best":       best,
        "v":          v,
        "vs":         vs,
        "calculated": True,
        "I":          I,
        "S":          S,
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

        # ── CALCULATION SHEET ──────────────────────────────────────
        open_card("📄", "Cable Calculation Sheet", "IEC VERIFIED", "green")

        # (I) Current
        st.markdown("### (I) &nbsp; Current Calculation")
        st.caption("IEC 60038 / IEC 60909 — Load Current Calculation")
        c1, c2, c3 = st.columns(3)
        c1.metric("Voltage",            f"{voltage} kV")
        c2.metric("Load",               f"{power} {'kVA' if load_type=='Transformer' else 'kW'}")
        c3.metric("Full-Load Current",  f"{round(I, 2)} A")
        st.divider()

        # (II) Ampacity
        st.markdown("### (II) &nbsp; Ampacity Check")
        st.caption("IEC 60287 — Current Carrying Capacity of Cables")
        kT_calc       = soil * depth * group * temp * laying_factor
        amp_available = catalog["amp"][best["size"]] * kT_calc * best["runs"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Catalog Ampacity",   f"{catalog['amp'][best['size']]} A")
        c2.metric("Derating Factor kT", f"{round(kT_calc, 4)}")
        c3.metric("Available Ampacity", f"{round(amp_available, 1)} A")
        if amp_available >= I:
            st.success(f"✅  Ampacity Check — PASS  ({round(amp_available,1)} A ≥ {round(I,1)} A)")
        else:
            st.error(f"❌  Ampacity Check — FAIL  ({round(amp_available,1)} A < {round(I,1)} A)")
        st.divider()

        # (III) Short Circuit
        st.markdown("### (III) &nbsp; Short Circuit Check")
        st.caption("IEC 60949 — A_min = (I_fault × √t) / k")
        sc_area_best = best["size"] if feeder_to == "Transformer" else best["size"] * best["runs"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Required Min. Area",  f"{round(S, 2)} mm²")
        c2.metric("Provided Total Area", f"{round(sc_area_best, 2)} mm²")
        c3.metric("Configuration",       f"{best['runs']}R × {best['size']} mm²")
        if sc_area_best >= S:
            st.success(f"✅  Short Circuit Check — PASS  ({round(sc_area_best,2)} mm² ≥ {round(S,2)} mm²)")
        else:
            st.error(f"❌  Short Circuit Check — FAIL  ({round(sc_area_best,2)} mm² < {round(S,2)} mm²)")
        st.divider()

        # (IV) Voltage Drop
        st.markdown("### (IV) &nbsp; Voltage Drop Check")
        st.caption("IEC 60364-5-52 — Voltage Drop Limits")
        vd_limit_display = 1.0 if feeder_to == "Transformer" else vd_run_limit
        c1, c2 = st.columns(2)
        c1.metric("Calculated Running VD", f"{round(v, 2)} %")
        c2.metric("Permissible Limit",     f"{vd_limit_display} %")
        if v <= vd_limit_display:
            st.success(f"✅  Running Voltage Drop — PASS  ({round(v,2)}% ≤ {vd_limit_display}%)")
        else:
            st.error(f"❌  Running Voltage Drop — FAIL  ({round(v,2)}% > {vd_limit_display}%)")

        if load_type == "Motor":
            st.caption("IEC 60034 — Motor Starting Performance  (starting PF = 0.2)")
            c1, c2, c3 = st.columns(3)
            c1.metric("Starting Current",  f"{round(starting_multiple * I, 1)} A")
            c2.metric("Starting VD",       f"{round(vs, 2)} %")
            c3.metric("Permissible",       f"{vd_start_limit} %")
            if vs <= vd_start_limit:
                st.success(f"✅  Starting Voltage Drop — PASS  ({round(vs,2)}% ≤ {vd_start_limit}%)")
            else:
                st.error(f"❌  Starting Voltage Drop — FAIL  ({round(vs,2)}% > {vd_start_limit}%)")
        st.divider()

        # (V) Final
        st.markdown("### (V) &nbsp; Final Cable Selection")
        st.caption("Based on IEC Standards + Oman Cable Catalogue")
        final_str = f"{best['runs']}R × {'3C' if cable_type=='3-Core' else '1C'} × {best['size']} mm²"
        st.success(f"✅  Selected Cable →  {final_str}")

        st.markdown("### 🧠 &nbsp; Engineering Statement")
        st.info(
            "All design checks — ampacity, short circuit withstand, running voltage drop"
            + (", and motor starting voltage drop" if load_type == "Motor" else "")
            + " — have been satisfied. The selected cable is safe and suitable for the given application."
        )

        close_card()

        # Metrics summary
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Full-Load Current", f"{round(I, 1)} A")
        m2.metric("Running VD",        f"{round(v, 2)} %")
        m3.metric("SC Min. Area",      f"{round(S, 1)} mm²")
        if load_type == "Motor":
            m4.metric("Starting VD", f"{round(vs, 2)} %")

        # PDF
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_dl, _ = st.columns([1, 2, 1])
        with col_dl:
            pdf = report(best, I, S, v, vs)
            with open(pdf, "rb") as f_pdf:
                st.download_button(
                    "📥  Download Engineering Report (PDF)",
                    f_pdf, "CableMate_Report.pdf",
                    use_container_width=True,
                )
    else:
        st.error("⚠  No suitable cable found for the given parameters. Consider increasing cable runs, relaxing voltage drop limits, or reviewing fault settings.")

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

# ── MANUAL CALC ──────────────────────────────────────
if "calculated" in st.session_state and st.session_state.get("calculate_manual", False):
    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")

    I_now = st.session_state["I"]
    S_now = st.session_state["S"]

    if None not in (manual_size_used, manual_runs_used, manual_type_used):
        kT_local = soil * depth * group * temp * laying_factor
        amp      = catalog["amp"][manual_size_used] * kT_local * manual_runs_used

        v_manual  = vd(I_now, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used)
        vs_manual = vd_start(I_now, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used) if load_type == "Motor" else 0.0

        sc_area_manual = manual_size_used if feeder_to == "Transformer" else manual_size_used * manual_runs_used

        amp_ok = amp      >= I_now
        vd_ok  = v_manual <= vd_run_limit
        sc_ok  = sc_area_manual >= S_now
        vs_ok  = (vs_manual <= vd_start_limit) if load_type == "Motor" else True

        st.session_state.update({
            "v_manual":  v_manual,  "vs_manual": vs_manual,
            "amp_ok":    amp_ok,    "vd_ok":     vd_ok,
            "vs_ok":     vs_ok,     "sc_ok":     sc_ok,
        })

        manual_label = f"{manual_runs_used}R × {'3C' if manual_type_used=='3-Core' else '1C'} × {manual_size_used} mm²"
        st.caption("Showing last applied manual selection")
        st.markdown(f"**Manual Cable →** `{manual_label}`")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ampacity",      "✅ PASS" if amp_ok else "❌ FAIL")
        c2.metric("Running VD",    "✅ PASS" if vd_ok  else "❌ FAIL")
        c3.metric("Short Circuit", "✅ PASS" if sc_ok  else "❌ FAIL")
        if load_type == "Motor":
            c4.metric("Starting VD", "✅ PASS" if vs_ok else "❌ FAIL")

        if not amp_ok: st.warning(f"⚠  Ampacity insufficient — available {round(amp,1)} A vs required {round(I_now,1)} A.")
        if not vd_ok:  st.warning(f"⚠  Running VD exceeds limit — {round(v_manual,2)}% vs allowed {vd_run_limit}%.")
        if not sc_ok:  st.warning(f"⚠  Short circuit area insufficient — {sc_area_manual} mm² vs required {round(S_now,2)} mm².")
        if load_type == "Motor" and not vs_ok:
            st.warning(f"⚠  Starting VD too high — {round(vs_manual,2)}% vs allowed {vd_start_limit}%.")

        st.session_state["calculate_manual"] = False

# ── COMPARISON ────────────────────────────────────────
if "calculated" in st.session_state and "manual_done" in st.session_state:
    best = st.session_state.get("best")
    if not best:
        st.error("No auto-selected cable to compare against.")
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
        st.metric("Voltage Drop Δ (Manual − Optimal)", f"{sign}{diff} %",
                  delta=f"{sign}{diff} %", delta_color="inverse")
    else:
        st.info("Apply manual selection to see comparison.")

    st.markdown("### 🧠 &nbsp; Engineering Reasoning")

    amp_ok_val = st.session_state.get("amp_ok")
    vd_ok_val  = st.session_state.get("vd_ok")
    sc_ok_val  = st.session_state.get("sc_ok")
    vs_ok_val  = st.session_state.get("vs_ok")

    if manual_size_used == best["size"] and manual_runs_used == best["runs"]:
        st.success("✔  Manual cable matches the optimal cable selection — excellent engineering judgement!")
    elif amp_ok_val and vd_ok_val and sc_ok_val and vs_ok_val:
        st.info("ℹ  Manual cable passes all checks but is not the most cost-optimal selection.")
    else:
        if not amp_ok_val:
            st.error("❌  Manual cable fails ampacity check — insufficient current carrying capacity.")
        if not sc_ok_val:
            st.error("❌  Manual cable fails short circuit check — conductor area too small.")
        if not vd_ok_val:
            st.error("❌  Manual cable fails running voltage drop check.")
        if load_type == "Motor" and not vs_ok_val:
            st.error("❌  Manual cable fails starting voltage drop check — motor may not start.")

    close_card()
