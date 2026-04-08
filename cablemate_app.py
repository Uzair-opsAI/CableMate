import streamlit as st
import math
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components
import os

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="CableMate", layout="wide", page_icon="⚡")

# ------------------------------------------------
# GLOBAL STYLES
# ------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

/* ── ROOT PALETTE ─────────────────────────────── */
:root {
    --bg-deep:      #080c14;
    --bg-panel:     #0d1422;
    --bg-card:      #111827;
    --bg-card2:     #141d2e;
    --border:       #1e2d45;
    --border-glow:  #1e4a7a;
    --accent:       #0ea5e9;
    --accent2:      #38bdf8;
    --accent-dim:   #0c3f5e;
    --success:      #10b981;
    --success-dim:  #064e3b;
    --warning:      #f59e0b;
    --danger:       #ef4444;
    --danger-dim:   #450a0a;
    --text-hi:      #e2e8f0;
    --text-mid:     #94a3b8;
    --text-lo:      #4b6080;
    --mono:         'IBM Plex Mono', monospace;
    --head:         'Rajdhani', sans-serif;
    --body:         'Inter', sans-serif;
}

/* ── GLOBAL RESET ─────────────────────────────── */
html, body, .stApp {
    background-color: var(--bg-deep) !important;
    color: var(--text-hi) !important;
    font-family: var(--body) !important;
}
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1400px !important;
}

/* ── SIDEBAR ──────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: var(--bg-panel) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text-mid) !important; }

/* ── HEADER BAND ──────────────────────────────── */
.cm-header {
    display: flex;
    align-items: center;
    gap: 1.4rem;
    padding: 1.6rem 2rem;
    background: linear-gradient(135deg, #0a1628 0%, #0d1f3c 50%, #081221 100%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 12px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.cm-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(14,165,233,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.cm-logo-ring {
    width: 56px; height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0ea5e9, #0369a1);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem;
    box-shadow: 0 0 20px rgba(14,165,233,0.4);
    flex-shrink: 0;
}
.cm-title {
    font-family: var(--head) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    letter-spacing: 3px !important;
    color: var(--text-hi) !important;
    margin: 0 !important; line-height: 1.1 !important;
}
.cm-subtitle {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--accent) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    margin-top: 3px !important;
}
.cm-badge {
    margin-left: auto;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    color: var(--accent2) !important;
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    padding: 4px 10px;
    border-radius: 20px;
    letter-spacing: 1px;
}

/* ── SECTION HEADERS ──────────────────────────── */
.cm-section {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1.8rem 0 1rem 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.cm-section-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: var(--accent-dim);
    border: 1px solid var(--border-glow);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
}
.cm-section-title {
    font-family: var(--head) !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    color: var(--text-hi) !important;
    text-transform: uppercase !important;
}
.cm-section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border-glow), transparent);
}

/* ── INPUT FIELDS ──────────────────────────────── */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-hi) !important;
    font-family: var(--body) !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.12) !important;
    outline: none !important;
}
label[data-testid="stWidgetLabel"] p {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-mid) !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ────────────────────────────────────── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #0ea5e9, #0369a1) !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-family: var(--head) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.3) !important;
    text-transform: uppercase !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(14,165,233,0.45) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ── METRIC CARDS ──────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
}
div[data-testid="stMetricValue"] {
    font-family: var(--mono) !important;
    color: var(--accent2) !important;
    font-size: 1.5rem !important;
}
div[data-testid="stMetricLabel"] {
    font-family: var(--mono) !important;
    color: var(--text-mid) !important;
    font-size: 0.72rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

/* ── SUCCESS / ERROR / WARNING ─────────────────── */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    font-family: var(--body) !important;
}
div[data-testid="stAlert"][class*="success"] {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid var(--success) !important;
    color: #6ee7b7 !important;
}
div[data-testid="stAlert"][class*="error"] {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid var(--danger) !important;
    color: #fca5a5 !important;
}
div[data-testid="stAlert"][class*="warning"] {
    background: rgba(245,158,11,0.08) !important;
    border: 1px solid var(--warning) !important;
    color: #fcd34d !important;
}
div[data-testid="stAlert"][class*="info"] {
    background: rgba(14,165,233,0.08) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent2) !important;
}

/* ── DIVIDER ───────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.6rem 0 !important;
}

/* ── CAPTION / SMALL TEXT ───────────────────────── */
div[data-testid="stCaptionContainer"] p {
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    color: var(--text-lo) !important;
    letter-spacing: 0.5px !important;
}

/* ── MARKDOWN HEADINGS ─────────────────────────── */
h1, h2, h3, h4 {
    font-family: var(--head) !important;
    letter-spacing: 1.5px !important;
    color: var(--text-hi) !important;
}
h3 { color: var(--accent2) !important; font-size: 1rem !important; }

/* ── CARDS / INFO BOXES ─────────────────────────── */
.cm-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.cm-card-accent {
    border-left: 3px solid var(--accent);
}
.cm-result-banner {
    background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(14,165,233,0.05));
    border: 1px solid var(--success);
    border-left: 4px solid var(--success);
    border-radius: 10px;
    padding: 1.2rem 1.6rem;
    margin: 1rem 0;
}
.cm-result-label {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--success) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
.cm-result-value {
    font-family: var(--head) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #6ee7b7 !important;
    letter-spacing: 2px !important;
}
.cm-check-row {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid var(--border);
    font-family: var(--body);
    font-size: 0.88rem;
}
.cm-check-label { color: var(--text-mid); flex: 1; }
.cm-check-pass { color: var(--success); font-weight: 600; font-family: var(--mono); font-size: 0.8rem; }
.cm-check-fail { color: var(--danger); font-weight: 600; font-family: var(--mono); font-size: 0.8rem; }
.cm-val { color: var(--text-hi); font-family: var(--mono); font-size: 0.82rem; }

/* ── DERATING BOX ─────────────────────────────── */
.cm-derating {
    background: linear-gradient(135deg, #0d1e35, #0a1525);
    border: 1px solid var(--border-glow);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    text-align: center;
}
.cm-derating-val {
    font-family: var(--mono) !important;
    font-size: 2rem !important;
    font-weight: 500 !important;
    color: var(--accent) !important;
}
.cm-derating-label {
    font-family: var(--mono) !important;
    font-size: 0.65rem !important;
    color: var(--text-lo) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

/* ── SELECTBOX DROPDOWN ─────────────────────────── */
div[data-testid="stSelectbox"] * {
    background-color: var(--bg-card2) !important;
    color: var(--text-hi) !important;
}

/* ── DOWNLOAD BUTTON ─────────────────────────── */
div[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0f4c75, #1b262c) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 8px !important;
    color: var(--accent2) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── NUMBER INPUT ARROWS ─────────────────────── */
div[data-testid="stNumberInput"] button {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--accent) !important;
}

/* ── TABLE  ──────────────────────────────────── */
.cm-proj-info {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.4rem;
    font-family: var(--body);
    font-size: 0.88rem;
    color: var(--text-mid);
    line-height: 1.8;
}
.cm-proj-info strong { color: var(--text-hi); font-weight: 500; }

/* Hide default streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* Subheader override */
div[data-testid="stHeadingWithActionElements"] h2 {
    font-family: var(--head) !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    color: var(--text-hi) !important;
    text-transform: uppercase !important;
    padding-bottom: 8px !important;
    border-bottom: 1px solid var(--border) !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HEADER
# ------------------------------------------------
st.markdown("""
<div class="cm-header">
    <div class="cm-logo-ring">⚡</div>
    <div>
        <div class="cm-title">CABLE MATE</div>
        <div class="cm-subtitle">MV Cable Sizing &amp; Analysis Platform</div>
    </div>
    <div class="cm-badge">IEC COMPLIANT · v2.0</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CLOSE WARNING
# ------------------------------------------------
components.html("""
<script>
let changed=false;
document.addEventListener("input",()=>{changed=true;});
window.onbeforeunload=function(e){
if(changed){e.preventDefault();e.returnValue='';}
};
</script>
""", height=0)

# ------------------------------------------------
# SECTION HELPER
# ------------------------------------------------
def section(icon, title):
    st.markdown(f"""
    <div class="cm-section">
        <div class="cm-section-icon">{icon}</div>
        <div class="cm-section-title">{title}</div>
        <div class="cm-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------
# PROJECT INFORMATION
# ------------------------------------------------
section("📁", "Project Information")

col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input("Client Name", "ABC Pvt Ltd")
    feeder_from = st.selectbox("From Equipment", ["Switchgear", "Transformer", "Generator"])
    from_tag = st.text_input("From Equipment Tag", placeholder="e.g. TR-01 / SWGR-A1")
    voltage = st.selectbox("System Voltage (kV)", [3.3, 6.6, 11, 25, 33, 66, 132])

with col2:
    project_name = st.text_input("Project Name", "Electrical Distribution System")
    feeder_to = st.selectbox("To Equipment", ["Motor", "Transformer", "Panel"])
    to_tag = st.text_input("To Equipment Tag", placeholder="e.g. MTR-01 / PNL-B2")
    length = st.number_input("Cable Length (m)", value=300)

st.divider()

# ------------------------------------------------
# INSTALLATION
# ------------------------------------------------
section("🛠", "Installation Details")

col1, col2 = st.columns(2)
with col1:
    laying = st.selectbox("Cable Laying Method", ["Direct Buried", "Air", "Duct"])
with col2:
    pass

st.divider()

# ------------------------------------------------
# LOAD DETAILS
# ------------------------------------------------
section("⚡", "Load Details")

col1, col2 = st.columns(2)

with col1:
    load_type = st.selectbox("Load Type", ["Motor", "Transformer", "Power"])
    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=500)
    else:
        power = st.number_input("Load (kW)", value=400)

with col2:
    pf = st.number_input("Power Factor", value=0.9)
    eff = st.number_input("Efficiency", value=0.95)

st.divider()

# ------------------------------------------------
# CONDUCTOR DETAILS
# ------------------------------------------------
section("🧵", "Conductor Details")

col1, col2, col3 = st.columns(3)
with col1:
    material = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
with col2:
    cable_type = st.selectbox("Cable Type", ["1-Core", "3-Core"])
with col3:
    starting_multiple = st.number_input("Motor Starting Current Multiple", value=9.5)

if voltage >= 66 and cable_type == "3-Core":
    st.warning("⚠  At 66 kV and above, single-core cables are typically used.")

st.divider()

# ------------------------------------------------
# FAULT CONDITIONS
# ------------------------------------------------
section("⚠", "Fault Conditions")

col1, col2 = st.columns(2)
with col1:
    fault = st.number_input("Fault Level (kA)", value=25)
with col2:
    fault_time = st.number_input("Fault Duration (s)", value=0.4)

st.divider()

# ------------------------------------------------
# VOLTAGE DROP LIMITS
# ------------------------------------------------
section("📉", "Voltage Drop Limits")

col1, col2 = st.columns(2)
with col1:
    vd_run_limit = st.number_input("Running Voltage Drop (%)", value=5.0)
with col2:
    if load_type == "Motor":
        vd_start_limit = st.number_input("Starting Voltage Drop (%)", value=15.0)
    else:
        vd_start_limit = None

st.divider()

# ------------------------------------------------
# DERATING FACTORS
# ------------------------------------------------
section("🌡", "Derating Factors")

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

if laying == "Air":
    laying_factor = 1.0
elif laying == "Duct":
    laying_factor = 0.9
else:
    laying_factor = 0.85

# ------------------------------------------------
# OVERALL DERATING DISPLAY
# ------------------------------------------------
kT_base = soil * depth * group * temp

st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(f"""
    <div class="cm-derating">
        <div class="cm-derating-label">Overall Derating Factor (kT)</div>
        <div class="cm-derating-val">{round(kT_base, 3)}</div>
        <div class="cm-derating-label" style="color:#4b6080;margin-top:4px;">
            Soil × Depth × Group × Temp — Note: Grouping factor applied automatically for multiple runs
        </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ------------------------------------------------
# PROJECT SUMMARY CARD
# ------------------------------------------------
st.markdown(f"""
<div class="cm-proj-info">
    <strong>CLIENT</strong> &nbsp;{client_name} &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>PROJECT</strong> &nbsp;{project_name} &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>FEEDER</strong> &nbsp;{feeder_from} → {feeder_to} &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>VOLTAGE</strong> &nbsp;{voltage} kV &nbsp;&nbsp;|&nbsp;&nbsp;
    <strong>LENGTH</strong> &nbsp;{length} m
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ------------------------------------------------
# RUN BUTTON
# ------------------------------------------------
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run_btn = st.button("⚡  RUN CABLEMATE ANALYSIS", use_container_width=True)

# ------------------------------------------------
# CATALOG
# ------------------------------------------------
catalog_cu = {
    "sizes": [50, 70, 95, 120, 150, 185, 240, 300],
    "amp":   {50:181, 70:220, 95:263, 120:298, 150:332, 185:374, 240:431, 300:482},
    "R":     {50:0.387, 70:0.268, 95:0.193, 120:0.153, 150:0.124, 185:0.099, 240:0.075, 300:0.060},
    "X":     {50:0.111, 70:0.106, 95:0.094, 120:0.091, 150:0.089, 185:0.086, 240:0.083, 300:0.082}
}
catalog_al = {
    "sizes": [50, 70, 95, 120, 150, 185, 240, 300],
    "amp":   {50:150, 70:180, 95:215, 120:245, 150:275, 185:310, 240:360, 300:405},
    "R":     {50:0.387, 70:0.268, 95:0.247, 120:0.153, 150:0.124, 185:0.129, 240:0.098, 300:0.080, 400:0.060},
    "X":     {50:0.111, 70:0.106, 95:0.094, 120:0.091, 150:0.089, 185:0.086, 240:0.083, 300:0.082}
}

catalog = catalog_cu if material == "Copper" else catalog_al

# ------------------------------------------------
# FUNCTIONS (UNCHANGED LOGIC)
# ------------------------------------------------
def load_current():
    if load_type == "Motor":
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf * eff)
    elif load_type == "Transformer":
        return power * 1000 / (math.sqrt(3) * voltage * 1000)
    else:
        return power * 1000 / (math.sqrt(3) * voltage * 1000 * pf)

def short_circuit():
    k = 143 if material == "Copper" else 94
    if feeder_from == "Switchgear" and feeder_to in ["Motor", "Transformer"]:
        t = 0.25
    else:
        t = fault_time
    return (fault * 1000 * math.sqrt(t)) / k

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

# ------------------------------------------------
# PDF REPORT (UNCHANGED LOGIC)
# ------------------------------------------------
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
    c.drawString(50, y, f"Client Name      : {client_name}");          y -= 20
    c.drawString(50, y, f"Project Name     : {project_name}");          y -= 20
    c.drawString(50, y, f"Feeder           : {feeder_from} → {feeder_to}"); y -= 20
    c.drawString(50, y, f"Voltage Level    : {voltage} kV");             y -= 20
    c.drawString(50, y, f"Cable Length     : {length} m");               y -= 20
    c.drawString(50, y, f"Load Type        : {load_type}");              y -= 20
    c.drawString(50, y, f"Power            : {power}");                  y -= 20
    c.drawString(50, y, f"Laying Method    : {laying}")
    c.showPage()

    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, "CableMate Engineering Report")
    y -= 40
    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Selected Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

    kT_rep = soil * depth * group * temp
    amp = catalog["amp"][best["size"]] * kT_rep * best["runs"]

    y -= 25; c.drawString(50, y, "LOAD CURRENT CALCULATION")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60038 / IEC 60909)")
    y -= 15; c.setFont("Helvetica", 11);         c.drawString(50, y, f"I = {round(I,2)} A")

    y -= 25; c.drawString(50, y, "AMPACITY CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60287)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Available Ampacity = {round(amp,1)} A");  y -= 15
    c.drawString(50, y, f"Load Current       = {round(I,1)} A");   y -= 15
    c.drawString(50, y, f"{round(amp,1)} ≥ {round(I,1)} → PASS ✔")

    y -= 25; c.drawString(50, y, "SHORT CIRCUIT CHECK")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60949 / IEC 60364-5-54)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Required Size = {round(S,1)} mm²");       y -= 15
    c.drawString(50, y, f"{round(S,1)} < {best['size']} mm²");      y -= 15
    c.drawString(50, y, f"Next Standard Size Selected → {best['size']} mm² ✔")

    y -= 25; c.drawString(50, y, "RUNNING VOLTAGE DROP")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Calculated VD = {round(v,2)} %");         y -= 15
    c.drawString(50, y, f"Allowed VD    = {vd_run_limit} %");       y -= 15
    c.drawString(50, y, f"{round(v,2)} ≤ {vd_run_limit} → PASS ✔")

    if load_type == "Motor":
        y -= 25; c.drawString(50, y, "STARTING VOLTAGE DROP")
        y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60034)")
        y -= 15; c.setFont("Helvetica", 11)
        c.drawString(50, y, f"Calculated VD = {round(vs,2)} %");    y -= 15
        c.drawString(50, y, f"Allowed VD    = {vd_start_limit} %"); y -= 15
        c.drawString(50, y, f"{round(vs,2)} ≤ {vd_start_limit} → PASS ✔")

    y -= 25; c.drawString(50, y, "DERATING FACTOR")
    y -= 15; c.setFont("Helvetica-Oblique", 10); c.drawString(50, y, "(IEC 60364-5-52)")
    y -= 15; c.setFont("Helvetica", 11)
    c.drawString(50, y, f"kT = {round(kT_rep,2)}")

    y -= 30
    if y < 100:
        c.showPage(); y = 750

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "FINAL ENGINEERING DECISION")
    y -= 20; c.setFont("Helvetica", 10)
    c.drawString(50, y, "• IEC 60364 – Electrical Installations");  y -= 15
    c.drawString(50, y, "• IEC 60287 – Cable Current Rating");      y -= 15
    c.drawString(50, y, "• IEC 60949 – Short Circuit Capacity");    y -= 15
    c.drawString(50, y, "• IEC 60034 – Motor Starting");            y -= 15
    c.drawString(50, y, "• IEC 60947 – Protection Systems");        y -= 15
    c.drawString(50, y, "• Cable Data: Oman Cable Catalogue");      y -= 15

    y -= 20; c.setFont("Helvetica", 11)
    if best:
        c.drawString(50, y, "All design checks (Ampacity, Voltage Drop, Short Circuit)")
        y -= 15
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

# ------------------------------------------------
# ENGINE (UNCHANGED LOGIC)
# ------------------------------------------------
if run_btn:
    I = load_current()
    if feeder_to == "Transformer":
        I = I * 1.2

    S = short_circuit()
    rules = get_rules(feeder_from, feeder_to, load_type)

    best = None
    v = 0
    vs = 0
    valid_options = []

    for size in catalog["sizes"]:
        for runs in range(1, rules["max_runs"] + 1):
            if not rules["allow_multi_run"] and runs > 1:
                continue

            kT_local = soil * depth * group * temp

            if feeder_to == "Transformer":
                if size < S:
                    continue
            else:
                if (size * runs) < S:
                    continue

            amp = catalog["amp"][size] * kT_local * runs
            if amp < I:
                continue

            v_temp = vd(I, catalog["R"][size], catalog["X"][size], runs)

            if feeder_to == "Transformer":
                vd_limit_check = 1.0
            elif load_type == "Motor":
                vd_limit_check = vd_run_limit
            else:
                vd_limit_check = vd_run_limit

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
                best_single   = sorted(single_run, key=lambda x: x["size"])[0]
                min_multi_size = min(x["size"] for x in multi_run) if multi_run else best_single["size"]
                if best_single["size"] <= min_multi_size * 1.5:
                    best = best_single
                else:
                    best = sorted(multi_run, key=lambda x: (x["runs"], x["size"]))[0]
            else:
                best = sorted(multi_run, key=lambda x: (x["runs"], x["size"]))[0]

        if best:
            v  = best["v"]
            vs = best["vs"]

    st.session_state["best"]       = best
    st.session_state["v"]          = v
    st.session_state["vs"]         = vs
    st.session_state["calculated"] = True
    st.session_state["I"]          = I
    st.session_state["S"]          = S

# ------------------------------------------------
# RESULTS DISPLAY
# ------------------------------------------------
if "calculated" in st.session_state:
    best = st.session_state["best"]
    I    = st.session_state["I"]
    S    = st.session_state["S"]
    v    = st.session_state["v"]
    vs   = st.session_state["vs"]

    if best:
        cable_str = f"{best['runs']}R × {'3C' if cable_type == '3-Core' else '1C'} × {best['size']} mm²"

        st.markdown(f"""
        <div class="cm-result-banner">
            <div class="cm-result-label">✔  Optimal Cable Selected</div>
            <div class="cm-result-value">{cable_str}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── CALCULATION SHEET ──────────────────────────────
        st.divider()
        section("📄", "Cable Calculation Sheet")

        # (I) CURRENT
        st.markdown("### (I)  Current Calculation")
        st.caption("📘  IEC 60038 / IEC 60909 — Load Current Calculation")
        col1, col2, col3 = st.columns(3)
        col1.metric("Voltage", f"{voltage} kV")
        col2.metric("Load", f"{power} {'kVA' if load_type=='Transformer' else 'kW'}")
        col3.metric("Load Current", f"{round(I,2)} A")

        # (II) AMPACITY
        st.markdown("### (II)  Ampacity Check")
        st.caption("📘  IEC 60287 — Current Carrying Capacity of Cables")
        kT_calc = soil * depth * group * temp
        amp_available = catalog["amp"][best["size"]] * kT_calc * best["runs"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Base Ampacity", f"{catalog['amp'][best['size']]} A")
        col2.metric("Derating Factor", f"{round(kT_calc, 3)}")
        col3.metric("Available Ampacity", f"{round(amp_available, 2)} A")
        if amp_available >= I:
            st.success("✅  Ampacity Check → PASS")
        else:
            st.error("❌  Ampacity Check → FAIL")

        # (III) SHORT CIRCUIT
        st.markdown("### (III)  Short Circuit Check")
        st.caption("📘  IEC 60949 / IEC 60364-5-54 — Short Circuit Withstand Capacity")
        sc_area_best = best["size"] if feeder_to == "Transformer" else best["size"] * best["runs"]
        col1, col2 = st.columns(2)
        col1.metric("Required Area", f"{round(S,2)} mm²")
        col2.metric("Available Area", f"{round(sc_area_best,2)} mm²")
        if sc_area_best >= S:
            st.success("✅  Short Circuit Check → PASS")
        else:
            st.error("❌  Short Circuit Check → FAIL")

        # (IV) VOLTAGE DROP
        st.markdown("### (IV)  Voltage Drop Check")
        st.caption("📘  IEC 60364-5-52 — Voltage Drop Limits")
        vd_limit_display = 1 if feeder_to == "Transformer" else (5 if feeder_to == "Motor" else vd_run_limit)
        col1, col2 = st.columns(2)
        col1.metric("Calculated VD", f"{round(v,2)} %")
        col2.metric("Permissible VD", f"{vd_limit_display} %")
        if v <= vd_limit_display:
            st.success("✅  Running Voltage Drop → PASS")
        else:
            st.error("❌  Running Voltage Drop → FAIL")

        if load_type == "Motor":
            st.caption("📘  IEC 60034 — Motor Starting Performance")
            col1, col2 = st.columns(2)
            col1.metric("Starting VD", f"{round(vs,2)} %")
            col2.metric("Permissible", f"{vd_start_limit} %")
            if vs <= vd_start_limit:
                st.success("✅  Starting Voltage Drop → PASS")
            else:
                st.error("❌  Starting Voltage Drop → FAIL")

        # (V) FINAL SELECTION
        st.markdown("### (V)  Final Cable Selection")
        st.caption("📘  Based on IEC Standards + Oman Cable Catalogue")
        final_str = f"{best['runs']}R × {'3C' if cable_type=='3-Core' else '1C'} × {best['size']} mm²"
        st.success(f"✅  Selected Cable →  {final_str}")

        # ENGINEERING STATEMENT
        st.markdown("### 🧠  Engineering Statement")
        st.info(
            "All design checks including ampacity, voltage drop, and short circuit "
            "withstand capability have been satisfied. The selected cable is safe "
            "and suitable for the given application."
        )

        # METRICS ROW
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Load Current", f"{round(I,1)} A")
        m2.metric("Running VD", f"{round(v,2)} %")
        if load_type == "Motor":
            m3.metric("Starting VD", f"{round(vs,2)} %")

        # PDF DOWNLOAD
        st.markdown("<br>", unsafe_allow_html=True)
        pdf = report(best, I, S, v, vs)
        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            with open(pdf, "rb") as f:
                st.download_button("📥  Download Engineering Report", f,
                                   "CableMate_Report.pdf", use_container_width=True)
    else:
        st.error("⚠  No suitable cable found for the given parameters.")

# ================================================
# MANUAL CABLE EVALUATION
# ================================================
st.divider()
section("🔧", "Manual Cable Evaluation")

col1, col2 = st.columns(2)
with col1:
    manual_size = st.selectbox("Select Cable Size (mm²)", catalog["sizes"], key="manual_size_unique")
with col2:
    manual_runs = st.selectbox("Number of Runs", list(range(1, 11)), key="manual_runs_unique")

col_m1, col_m2, col_m3 = st.columns([1, 2, 1])
with col_m2:
    apply_manual = st.button("🔧  APPLY MANUAL SELECTION", use_container_width=True)

if apply_manual:
    st.session_state["manual_done"]        = True
    st.session_state["calculate_manual"]   = True
    st.session_state["selected_size"]      = manual_size
    st.session_state["selected_runs"]      = manual_runs
    st.session_state["selected_type"]      = cable_type

# ── MANUAL RESULTS ──────────────────────────────────
if "calculated" in st.session_state and st.session_state.get("calculate_manual", False):

    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")

    if manual_size_used is not None and manual_runs_used is not None and manual_type_used is not None:
        kT_local   = soil * depth * group * temp
        amp        = catalog["amp"][manual_size_used] * kT_local * manual_runs_used
        v_manual   = vd(I, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used)
        vs_manual  = vd_start(I, catalog["R"][manual_size_used], catalog["X"][manual_size_used], manual_runs_used) if load_type == "Motor" else 0
        sc_area_manual = manual_size_used if feeder_to == "Transformer" else manual_size_used * manual_runs_used

        amp_ok = amp >= I
        vd_ok  = v_manual <= vd_run_limit
        sc_ok  = sc_area_manual >= S
        vs_ok  = (vs_manual <= vd_start_limit) if load_type == "Motor" else True

        st.session_state.update({
            "v_manual":  v_manual,
            "vs_manual": vs_manual,
            "amp_ok": amp_ok, "vd_ok": vd_ok,
            "vs_ok":  vs_ok,  "sc_ok": sc_ok
        })

        manual_str_display = f"{manual_runs_used}R × {'3C' if manual_type_used == '3-Core' else '1C'} × {manual_size_used} mm²"
        st.markdown(f"<div style='font-family:var(--mono,monospace);font-size:0.75rem;color:#4b6080;margin-bottom:4px;'>MANUAL SELECTION RESULT</div>", unsafe_allow_html=True)
        st.markdown(f"**{manual_str_display}**")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Ampacity",     "✅ PASS" if amp_ok else "❌ FAIL")
        c2.metric("Voltage Drop", "✅ PASS" if vd_ok  else "❌ FAIL")
        c3.metric("Short Circuit","✅ PASS" if sc_ok  else "❌ FAIL")
        if load_type == "Motor":
            c4.metric("Starting VD",  "✅ PASS" if vs_ok  else "❌ FAIL")

        if not amp_ok: st.warning("⚠  Ampacity insufficient — cable may overheat.")
        if not vd_ok:  st.warning("⚠  Voltage drop exceeds limit — poor performance expected.")
        if not sc_ok:  st.warning("⚠  Short circuit rating inadequate — risk of damage.")
        if load_type == "Motor" and not vs_ok:
            st.warning("⚠  Starting voltage drop too high — motor may fail to start.")

        st.session_state["calculate_manual"] = False

# ── COMPARISON + JUSTIFICATION ──────────────────────
if "calculated" in st.session_state and "manual_done" in st.session_state:
    best = st.session_state.get("best")
    if not best:
        st.error("No suitable cable found.")
        st.stop()

    st.divider()
    section("🔍", "Best vs Manual Comparison")

    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")

    best_str_c   = f"{best['runs']}R × {'3C' if manual_type_used == '3-Core' else '1C'} × {best['size']} mm²"
    manual_str_c = f"{manual_runs_used}R × {'3C' if manual_type_used == '3-Core' else '1C'} × {manual_size_used} mm²"

    col1, col2 = st.columns(2)
    col1.metric("🏆  Optimal Cable",  best_str_c)
    col2.metric("🔧  Manual Cable",   manual_str_c)

    v_manual_val = st.session_state.get("v_manual")
    if v_manual_val is not None:
        diff = round(v_manual_val - v, 2)
        sign = "+" if diff > 0 else ""
        st.metric("Voltage Drop Δ", f"{sign}{diff} %",
                  delta=f"{sign}{diff} %",
                  delta_color="inverse")
    else:
        st.info("Apply manual selection to see comparison.")

    # ENGINEERING REASONING
    st.markdown("### 🧠  Engineering Reasoning")

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
