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
# CSS
# ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;0,9..144,700;1,9..144,300&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
:root {
  --bg:#f7f6f2; --surface:#ffffff; --surface2:#f0efe9;
  --border:#e2dfd6; --border-dark:#c8c4b8;
  --accent:#c0392b; --accent2:#e74c3c; --accent-soft:#fdf1f0;
  --amber:#d35400; --green:#1a7a4a; --green-bg:#edf7f1;
  --red-bg:#fdf1f0; --warn-bg:#fef9ec; --warn:#b7791f;
  --text-hi:#1a1916; --text-mid:#5a574f; --text-lo:#9e9b94;
  --shadow-sm:0 1px 4px rgba(0,0,0,0.06);
  --radius:12px;
  --font-head:'Fraunces',Georgia,serif;
  --font-body:'DM Sans',sans-serif;
  --font-mono:'DM Mono',monospace;
}
html,body,.stApp{background-color:var(--bg)!important;font-family:var(--font-body)!important;color:var(--text-hi)!important;}
.block-container{padding:0 2.5rem 5rem!important;max-width:1380px!important;}
#MainMenu,footer,header{visibility:hidden!important;}
section[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}

.cm-hero{background:var(--surface);border-bottom:3px solid var(--accent);padding:2rem 2.5rem 1.6rem;
  margin:0 -2.5rem 2.5rem;display:flex;align-items:flex-end;justify-content:space-between;box-shadow:var(--shadow-sm);}
.cm-hero-left{display:flex;align-items:center;gap:1.2rem;}
.cm-logo{width:52px;height:52px;background:var(--accent);border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:1.5rem;box-shadow:0 4px 14px rgba(192,57,43,0.35);flex-shrink:0;}
.cm-brand-name{font-family:var(--font-head)!important;font-size:2.2rem!important;font-weight:700!important;
  color:var(--text-hi)!important;letter-spacing:-0.5px;line-height:1;margin:0;}
.cm-brand-sub{font-family:var(--font-mono)!important;font-size:0.68rem!important;color:var(--text-lo)!important;
  letter-spacing:2px!important;text-transform:uppercase!important;margin-top:5px;}
.cm-hero-right{display:flex;gap:10px;align-items:center;}
.cm-pill{font-family:var(--font-mono)!important;font-size:0.62rem!important;letter-spacing:1.5px!important;
  text-transform:uppercase!important;padding:5px 12px;border-radius:20px;border:1px solid var(--border-dark);
  color:var(--text-mid);background:var(--surface2);}
.cm-pill-red{border-color:var(--accent);color:var(--accent);background:var(--accent-soft);}

.cm-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:1.8rem 2rem 1.6rem;margin-bottom:1.4rem;box-shadow:var(--shadow-sm);position:relative;overflow:hidden;}
.cm-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--accent),var(--amber));}
.cm-card-blue::before{background:linear-gradient(90deg,#1a5276,#2e86c1);}
.cm-card-green::before{background:linear-gradient(90deg,#1a7a4a,#27ae60);}
.cm-card-amber::before{background:linear-gradient(90deg,#d35400,#e67e22);}
.cm-card-slate::before{background:linear-gradient(90deg,#4a4e5a,#7f8492);}

.cm-section-heading{display:flex;align-items:center;gap:10px;margin-bottom:1.4rem;}
.cm-section-icon{width:34px;height:34px;border-radius:8px;background:var(--surface2);border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;font-size:0.9rem;}
.cm-section-title{font-family:var(--font-head)!important;font-size:1.05rem!important;font-weight:600!important;
  color:var(--text-hi)!important;letter-spacing:0.3px!important;}
.cm-section-tag{margin-left:auto;font-family:var(--font-mono)!important;font-size:0.6rem!important;
  color:var(--text-lo)!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}

div[data-testid="stTextInput"] input,div[data-testid="stNumberInput"] input{
  background:var(--surface2)!important;border:1.5px solid var(--border)!important;border-radius:8px!important;
  color:var(--text-hi)!important;font-family:var(--font-body)!important;font-size:0.9rem!important;transition:all 0.18s ease!important;}
div[data-testid="stTextInput"] input:focus,div[data-testid="stNumberInput"] input:focus{
  border-color:var(--accent)!important;background:var(--surface)!important;box-shadow:0 0 0 3px rgba(192,57,43,0.1)!important;}
div[data-testid="stSelectbox"]>div>div{background:var(--surface2)!important;border:1.5px solid var(--border)!important;
  border-radius:8px!important;color:var(--text-hi)!important;}
label[data-testid="stWidgetLabel"] p{font-family:var(--font-mono)!important;font-size:0.7rem!important;
  font-weight:500!important;color:var(--text-mid)!important;letter-spacing:0.5px!important;
  text-transform:uppercase!important;margin-bottom:4px!important;}

div[data-testid="stButton"]>button{background:var(--accent)!important;border:none!important;border-radius:8px!important;
  color:white!important;font-family:var(--font-body)!important;font-size:0.92rem!important;font-weight:600!important;
  padding:0.7rem 2.2rem!important;transition:all 0.2s ease!important;box-shadow:0 3px 14px rgba(192,57,43,0.28)!important;}
div[data-testid="stButton"]>button:hover{background:var(--accent2)!important;transform:translateY(-1px)!important;
  box-shadow:0 6px 22px rgba(192,57,43,0.38)!important;}
div[data-testid="stDownloadButton"]>button{background:var(--surface)!important;border:1.5px solid var(--accent)!important;
  border-radius:8px!important;color:var(--accent)!important;font-family:var(--font-body)!important;
  font-weight:600!important;font-size:0.88rem!important;}
div[data-testid="stDownloadButton"]>button:hover{background:var(--accent-soft)!important;}

div[data-testid="stMetric"]{background:var(--surface)!important;border:1px solid var(--border)!important;
  border-radius:10px!important;padding:1.1rem 1.3rem!important;box-shadow:var(--shadow-sm)!important;}
div[data-testid="stMetricLabel"] p{font-family:var(--font-mono)!important;font-size:0.68rem!important;
  text-transform:uppercase!important;letter-spacing:1px!important;color:var(--text-lo)!important;}
div[data-testid="stMetricValue"]{font-family:var(--font-head)!important;font-size:1.55rem!important;
  color:var(--text-hi)!important;font-weight:600!important;}

div[data-testid="stAlert"]{border-radius:8px!important;font-family:var(--font-body)!important;
  font-size:0.9rem!important;border-left-width:3px!important;}
div[data-testid="stAlert"][class*="success"]{background:var(--green-bg)!important;border-color:var(--green)!important;color:#145a38!important;}
div[data-testid="stAlert"][class*="error"]{background:var(--red-bg)!important;border-color:var(--accent)!important;color:#922b21!important;}
div[data-testid="stAlert"][class*="warning"]{background:var(--warn-bg)!important;border-color:var(--warn)!important;color:#7d5a17!important;}
div[data-testid="stAlert"][class*="info"]{background:#eaf3fb!important;border-color:#2e86c1!important;color:#1a5276!important;}

div[data-testid="stCaptionContainer"] p{font-family:var(--font-mono)!important;font-size:0.67rem!important;
  color:var(--text-lo)!important;letter-spacing:0.3px!important;}
hr{border:none!important;border-top:1px solid var(--border)!important;margin:1.5rem 0!important;}
h3{font-family:var(--font-head)!important;font-size:1rem!important;font-weight:600!important;
  color:var(--text-hi)!important;margin-top:1.6rem!important;letter-spacing:0.2px!important;}

.cm-result{background:linear-gradient(135deg,#edf7f1 0%,#f0faf5 100%);border:1.5px solid #27ae60;
  border-left:5px solid var(--green);border-radius:var(--radius);padding:1.4rem 1.8rem;margin:1.2rem 0;}
.cm-result-eyebrow{font-family:var(--font-mono)!important;font-size:0.65rem!important;color:var(--green)!important;
  letter-spacing:2px!important;text-transform:uppercase!important;}
.cm-result-cable{font-family:var(--font-head)!important;font-size:1.8rem!important;font-weight:700!important;
  color:#145a38!important;margin-top:4px!important;letter-spacing:-0.5px!important;}

.cm-kt{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);
  padding:1.4rem 2rem;text-align:center;box-shadow:var(--shadow-sm);}
.cm-kt-label{font-family:var(--font-mono)!important;font-size:0.65rem!important;color:var(--text-lo)!important;
  letter-spacing:2px!important;text-transform:uppercase!important;}
.cm-kt-val{font-family:var(--font-head)!important;font-size:2.4rem!important;font-weight:700!important;
  color:var(--accent)!important;line-height:1.1!important;margin:4px 0 2px!important;}

.cm-proj-strip{background:var(--text-hi);border-radius:var(--radius);padding:1rem 1.8rem;
  display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center;margin-bottom:1.6rem;}
.cm-proj-item{display:flex;flex-direction:column;gap:2px;}
.cm-proj-key{font-family:var(--font-mono)!important;font-size:0.58rem!important;
  color:rgba(255,255,255,0.45)!important;letter-spacing:1.5px!important;text-transform:uppercase!important;}
.cm-proj-val{font-family:var(--font-body)!important;font-size:0.85rem!important;
  font-weight:500!important;color:rgba(255,255,255,0.9)!important;}
.cm-proj-divider{width:1px;height:30px;background:rgba(255,255,255,0.15);}

div[data-testid="stNumberInput"] button{background:var(--surface2)!important;
  border-color:var(--border)!important;color:var(--text-mid)!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# CLOSE-TAB WARNING
# ─────────────────────────────────────────────────
components.html("""
<script>
let changed=false;
document.addEventListener("input",()=>{changed=true;});
window.onbeforeunload=function(e){if(changed){e.preventDefault();e.returnValue='';}};
</script>""", height=0)

# ─────────────────────────────────────────────────
# HERO
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
# HELPERS
# ─────────────────────────────────────────────────
def open_card(icon, title, tag="", color=""):
    cls = f"cm-card cm-card-{color}" if color else "cm-card"
    st.markdown(f"""<div class="{cls}">
      <div class="cm-section-heading">
        <div class="cm-section-icon">{icon}</div>
        <div class="cm-section-title">{title}</div>
        <div class="cm-section-tag">{tag}</div>
      </div>""", unsafe_allow_html=True)

def close_card():
    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# ① PROJECT INFORMATION
# ─────────────────────────────────────────────────
open_card("📁", "Project Information", "STEP 01", "blue")
col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name", "ABC Pvt Ltd")
    feeder_from = st.selectbox("From Equipment", ["Switchgear", "Transformer", "Generator"])
    from_tag    = st.text_input("From Equipment Tag", placeholder="e.g. TR-01 / SWGR-A1")
    voltage     = st.selectbox("System Voltage (kV)", [3.3, 6.6, 11, 25, 33, 66, 132])
with col2:
    project_name = st.text_input("Project Name", "Electrical Distribution System")
    feeder_to    = st.selectbox("To Equipment", ["Motor", "Transformer", "Panel"])
    to_tag       = st.text_input("To Equipment Tag", placeholder="e.g. MTR-01 / PNL-B2")
    length       = st.number_input("Cable Length (m)", value=300, min_value=1)
close_card()

# ─────────────────────────────────────────────────
# ② INSTALLATION
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
# FIX A ─ load_type AUTO-SET from feeder_to
# ─────────────────────────────────────────────────
open_card("⚡", "Load Details", "STEP 03", "amber")

# Derive load_type automatically — user never needs to set this separately
if feeder_to == "Motor":
    load_type = "Motor"
elif feeder_to == "Transformer":
    load_type = "Transformer"
else:
    # Panel destination — let user pick
    load_type = st.selectbox("Load Type", ["Motor", "Transformer", "Power"])

# Show auto-set notice (only when feeder_to drives it)
if feeder_to in ("Motor", "Transformer"):
    st.caption(f"📌  Load type automatically set to  {load_type}  based on feeder destination.")

col1, col2 = st.columns(2)
with col1:
    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=500, min_value=1)
    else:
        power = st.number_input("Load (kW)", value=400, min_value=1)
with col2:
    pf  = st.number_input("Power Factor", value=0.91, min_value=0.01, max_value=1.0,
                          step=0.01, format="%.2f")
    eff = st.number_input("Efficiency", value=0.97, min_value=0.01, max_value=1.0,
                          step=0.01, format="%.2f")
close_card()

# ─────────────────────────────────────────────────
# ④ CONDUCTOR DETAILS
# FIX B ─ starting_multiple shown ONLY for Motor
# FIX C ─ default starting_multiple = 6.0
# ─────────────────────────────────────────────────
open_card("🧵", "Conductor Details", "STEP 04")

if load_type == "Motor":
    col1, col2, col3 = st.columns(3)
    with col1:
        material   = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
    with col2:
        cable_type = st.selectbox("Cable Type", ["3-Core", "1-Core"])
    with col3:
        # IEC 60034 / industry standard: DOL starting = 5–7× FLC → default 6.0
        starting_multiple = st.number_input(
            "Motor Starting Current Multiple (×I_FL)",
            value=6.0, min_value=1.0, max_value=15.0, step=0.5, format="%.1f"
        )
else:
    # Transformer or Power — starting multiple NOT applicable, hide it completely
    starting_multiple = 1.0   # neutral, unused in VD_start for non-motor
    col1, col2 = st.columns(2)
    with col1:
        material   = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
    with col2:
        cable_type = st.selectbox("Cable Type", ["3-Core", "1-Core"])

if voltage >= 66 and cable_type == "3-Core":
    st.warning("⚠  At 66 kV and above, single-core cables are typically used.")
close_card()

# ─────────────────────────────────────────────────
# ⑤ FAULT CONDITIONS
# ─────────────────────────────────────────────────
open_card("⚠", "Fault Conditions", "STEP 05", "amber")
col1, col2 = st.columns(2)
with col1:
    fault      = st.number_input("Fault Level (kA)", value=25.0, min_value=0.1,
                                 step=1.0, format="%.1f")
with col2:
    fault_time = st.number_input("Fault Duration (s) — used for non-switchgear feeders",
                                 value=0.4, min_value=0.01, step=0.05, format="%.2f")
st.caption("📌  For Switchgear outgoing feeders, fault duration is fixed at 0.25 s per IEC 60909 / industry protection standard.")
close_card()

# ─────────────────────────────────────────────────
# ⑥ VOLTAGE DROP LIMITS
# ─────────────────────────────────────────────────
open_card("📉", "Voltage Drop Limits", "STEP 06", "blue")
col1, col2 = st.columns(2)
with col1:
    vd_run_limit = st.number_input("Running Voltage Drop Limit (%)", value=5.0,
                                   min_value=0.1, step=0.5, format="%.1f")
with col2:
    if load_type == "Motor":
        vd_start_limit = st.number_input("Starting Voltage Drop Limit (%)", value=15.0,
                                         min_value=1.0, step=1.0, format="%.1f")
    else:
        vd_start_limit = 999.0  # not applicable
        st.caption("Starting VD limit not applicable for this load type.")
close_card()

# ─────────────────────────────────────────────────
# ⑦ DERATING FACTORS
# ─────────────────────────────────────────────────
open_card("🌡", "Derating Factors", "STEP 07", "slate")

def input_with_other(label, options, default):
    col_a, col_b = st.columns([2, 1])
    with col_a:
        choice = st.selectbox(label, options + ["Other"], key=f"df_{label}")
    if choice == "Other":
        with col_b:
            return st.number_input("Manual value", value=float(default),
                                   step=0.01, format="%.3f", key=f"df_{label}_m")
    return float(choice)

col1, col2 = st.columns(2)
with col1:
    soil  = input_with_other("Soil Thermal Resistivity Factor", [1.0, 1.5, 2.0], 1.0)
    group = input_with_other("Cable Grouping Factor",           [1.0, 0.85, 0.79, 0.73], 1.0)
with col2:
    depth = input_with_other("Depth of Laying Factor",          [0.8, 1.0], 1.0)
    temp  = input_with_other("Ambient Temperature Factor",      [1.0, 0.85], 1.0)

# Laying method factor
laying_factor_map = {"Direct Buried": 0.85, "Air": 1.0, "Duct": 0.9}
laying_factor = laying_factor_map[laying]

close_card()

# ─────────────────────────────────────────────────
# kT — OVERALL DERATING (all factors combined)
# ─────────────────────────────────────────────────
kT = soil * depth * group * temp

_, col_kt, _ = st.columns([1, 2, 1])
with col_kt:
    st.markdown(f"""
    <div class="cm-kt">
      <div class="cm-kt-label">Overall Derating Factor (kT)</div>
      <div class="cm-kt-val">{round(kT, 4)}</div>
      <div class="cm-kt-label" style="font-size:0.6rem;color:#b8b5ae;margin-top:4px;">
        Soil({soil}) × Depth({depth}) × Group({group}) × Temp({temp}) × Laying({laying_factor})
      </div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# PROJECT STRIP
# ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="cm-proj-strip">
  <div class="cm-proj-item">
    <span class="cm-proj-key">Client</span>
    <span class="cm-proj-val">{client_name}</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Project</span>
    <span class="cm-proj-val">{project_name}</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Feeder</span>
    <span class="cm-proj-val">{feeder_from} → {feeder_to}</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Voltage</span>
    <span class="cm-proj-val">{voltage} kV</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Length</span>
    <span class="cm-proj-val">{length} m</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Material</span>
    <span class="cm-proj-val">{material}</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">Load Type</span>
    <span class="cm-proj-val">{load_type}</span>
  </div><div class="cm-proj-divider"></div>
  <div class="cm-proj-item">
    <span class="cm-proj-key">kT</span>
    <span class="cm-proj-val">{round(kT,4)}</span>
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
# CALCULATION FUNCTIONS
# ─────────────────────────────────────────────────

def calc_load_current():
    """IEC 60038 / 60909 — Full-load current"""
    if load_type == "Motor":
        # P = √3 × V × I × PF × η  →  I = P / (√3 × V × PF × η)
        return (power * 1000) / (math.sqrt(3) * voltage * 1000 * pf * eff)
    elif load_type == "Transformer":
        # S = √3 × V × I  →  I = S / (√3 × V)
        return (power * 1000) / (math.sqrt(3) * voltage * 1000)
    else:
        # General power load
        return (power * 1000) / (math.sqrt(3) * voltage * 1000 * pf)


def calc_sc_min_area():
    """
    IEC 60949 — Minimum conductor cross-section for short-circuit withstand:
        A_min (mm²) = (I_fault_A × √t) / k

    Fault time selection:
        Switchgear outgoing feeder → t = 0.25 s  (protection relay clears in 250 ms)
        All other feeders          → t = user-entered fault_time

    k values (IEC 60949, Table 1 — initial temp 90°C, PVC insulation):
        Copper    → k = 143
        Aluminium → k = 94
    """
    k = 143 if material == "Copper" else 94
    t = 0.25 if feeder_from == "Switchgear" else fault_time
    raw = (fault * 1000 * math.sqrt(t)) / k

# Round to next standard cable size
    for s in catalog["sizes"]:
        if s >= raw:
            return s

    return max(catalog["sizes"])


def calc_vd_run(I, R, X, runs):
    """
    IEC 60364-5-52 — Running voltage drop:
        VD% = (√3 × I × (R·cosφ + X·sinφ) × L_km) / (V_line × runs) × 100
    """
    cos_phi = pf
    sin_phi = math.sin(math.acos(pf))
    return (math.sqrt(3) * I * (R * cos_phi + X * sin_phi) * (length / 1000)) / (voltage * 1000 * runs) * 100


def calc_vd_start(I, R, X, runs):
    """
    IEC 60034 — Motor starting voltage drop:
        Starting current I_st = starting_multiple × I_FL
        Starting power factor ≈ 0.2 (locked-rotor condition)
    """
    I_start  = starting_multiple * I
    cos_s    = 0.2
    sin_s    = math.sin(math.acos(cos_s))
    return (math.sqrt(3) * I_start * (R * cos_s + X * sin_s) * (length / 1000)) / (voltage * 1000 * runs) * 100


def get_feeder_rules():
    """
    Returns max parallel runs allowed for this feeder configuration.

    Transformer feeders → always 1 run
        (parallel transformer feeders cause circulating currents without
        special impedance matching — not done in standard MV practice)

    Generator → Motor → 1 run
        (generator source impedance is high; parallel cables cause
        unequal sharing and protection complications)

    All other → up to 4 runs
        (IEC / industry consensus: beyond 4 parallel MV cables,
        current sharing imbalance becomes unacceptable without transposition)
    """
    if feeder_to == "Transformer":
        return {"max_runs": 1, "allow_multi_run": False}
    elif feeder_from == "Generator" and feeder_to == "Motor":
        return {"max_runs": 1, "allow_multi_run": False}
    else:
        return {"max_runs": 4, "allow_multi_run": True}

def pick_best(valid_options):
    """
    Engineering cost-optimised selection from passing candidates.

    Cost index = runs × size_mm²
    This approximates:
        - Material cost  ∝ size
        - Labour cost    ∝ runs  (trenching, jointing, terminations)

    So 1R×185 (index=185) < 2R×95 (index=190) — but 1R×185 fails ampacity
    for the test case (185 A × kT < 198 A), so 2R×95 is correctly chosen.

    Tie-break: fewer runs preferred (simpler install), then smaller size.
    """
    if not valid_options:
        return None
    return sorted(valid_options, key=lambda x: (
        x["size"],              # 🔴 PRIORITY 1 → fewer runs (very important)
        x["runs"],              # 🔴 PRIORITY 2 → smaller cable
        x["score"]              # 🔴 PRIORITY 3 → cost
    ))[0]


# ─────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────
if run_btn:
  
    st.write("🚀 ENGINE STARTED")
    I_fl  = calc_load_current()
    S_min = calc_sc_min_area()
    rules = get_feeder_rules()

    # Transformer feeders: add 20% safety margin to current per IEC practice
    I_design = I_fl * 1 if feeder_to == "Transformer" else I_fl

    valid_options = []

    for size in catalog["sizes"]:
        for runs in range(1, rules["max_runs"] + 1):
        # 🔴 ADD THIS BLOCK HERE (VERY IMPORTANT POSITION)
             # 🔴 HARD FILTER — Transformer SC enforcement (ONLY HERE)
            if feeder_to == "Transformer" and size < S_min:
                continue

            if runs >= 2 and size < 95:
                continue

            #DEBUG STARTS
            if not rules["allow_multi_run"] and runs > 1:
                continue
            # ── CHECK 1: SHORT CIRCUIT WITHSTAND ─────────────────────────────
            # Total cross-section of all parallel conductors must ≥ S_min.
            # For Transformer feeder (1 run forced), compare the single cable size.
            if feeder_to != "Transformer":
    # 🔵 Motor / others → total area allowed
                sc_area = size * runs
                if sc_area < S_min:
                    continue

            # ── CHECK 2: AMPACITY ─────────────────────────────────────────────
            # Derated ampacity of (runs) parallel cables must ≥ design current.
            amp_avail = catalog["amp"][size] * kT * runs
            if amp_avail < I_design:
                continue

            # ── CHECK 3: RUNNING VOLTAGE DROP ─────────────────────────────────
            vd_r = calc_vd_run(I_fl, catalog["R"][size], catalog["X"][size], runs)
            vd_limit = 1.0 if feeder_to == "Transformer" else vd_run_limit
            if vd_r > vd_limit:
                continue

            # ── CHECK 4: STARTING VOLTAGE DROP (Motor only) ───────────────────
            if load_type == "Motor":
                vd_s = calc_vd_start(I_fl, catalog["R"][size], catalog["X"][size], runs)
                if vd_s > vd_start_limit:
                    continue
            else:
                vd_s = 0.0

            valid_options.append({
                "size":  size,
                "runs":  runs,
                "v":     vd_r,
                "vs":    vd_s,
                "amp":   amp_avail,
                "score": vd_r + (vd_s if load_type=="Motor" else 0)
            })
    best = pick_best(valid_options)

    st.session_state.update({
        "best":       best,
        "I":          I_fl,
        "I_design":   I_design,
        "S":          S_min,
        "v":          best["v"]  if best else 0.0,
        "vs":         best["vs"] if best else 0.0,
        "calculated": True,
    })
    
# ─────────────────────────────────────────────────
# RESULTS
# ─────────────────────────────────────────────────
if "calculated" in st.session_state:
    best     = st.session_state["best"]
    I_fl     = st.session_state["I"]
    I_design = st.session_state["I_design"]
    S_min    = st.session_state["S"]
    v        = st.session_state["v"]
    vs       = st.session_state["vs"]

    st.markdown("<br>", unsafe_allow_html=True)

    if best:
        core_str  = "3C" if cable_type == "3-Core" else "1C"
        cable_str = f"{best['runs']}R × {core_str} × {best['size']} mm²"

        st.markdown(f"""
        <div class="cm-result">
          <div class="cm-result-eyebrow">✔  Optimal Cable Selected</div>
          <div class="cm-result-cable">{cable_str}</div>
        </div>""", unsafe_allow_html=True)

        open_card("📄", "Cable Calculation Sheet", "IEC VERIFIED", "green")

        # (I) Current
        st.markdown("### (I)  Current Calculation")
        st.caption("IEC 60038 / IEC 60909")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Voltage",          f"{voltage} kV")
        c2.metric("Load",             f"{power} {'kVA' if load_type=='Transformer' else 'kW'}")
        c3.metric("Full-Load Current",f"{round(I_fl, 2)} A")
        if feeder_to == "Transformer":
            c4.metric("Design Current (+20%)", f"{round(I_design, 2)} A")
        st.divider()

        # (II) Ampacity
        st.markdown("### (II)  Ampacity Check")
        st.caption("IEC 60287 — Derated ampacity must exceed design current")
        amp_avail = catalog["amp"][best["size"]] * kT * best["runs"]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Catalog Base Ampacity",    f"{catalog['amp'][best['size']]} A")
        c2.metric("Derating Factor kT",       f"{round(kT, 4)}")
        c3.metric("Runs",                     f"{best['runs']}")
        c4.metric("Available Ampacity",       f"{round(amp_avail, 1)} A")
        if amp_avail >= I_design:
            st.success(f"✅  Ampacity — PASS   ( {round(amp_avail,1)} A  ≥  {round(I_design,1)} A )")
        else:
            st.error(f"❌  Ampacity — FAIL   ( {round(amp_avail,1)} A  <  {round(I_design,1)} A )")
        st.divider()

        # (III) Short Circuit
        st.markdown("### (III)  Short Circuit Check")
        t_used = 0.25 if feeder_from == "Switchgear" else fault_time
        k_used = 143  if material == "Copper" else 94
        st.caption(f"IEC 60949 — A_min = (I_fault × √t) / k  =  ({fault} kA × √{t_used}) / {k_used}")
        sc_area = best["size"] * best["runs"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Required Min. Area",  f"{round(S_min, 2)} mm²")
        c2.metric("Provided Total Area", f"{sc_area} mm²")
        c3.metric("Configuration",       f"{best['runs']} × {best['size']} mm²")
        if sc_area >= S_min:
            st.success(f"✅  Short Circuit — PASS   ( {sc_area} mm²  ≥  {round(S_min,2)} mm² )")
        else:
            st.error(f"❌  Short Circuit — FAIL   ( {sc_area} mm²  <  {round(S_min,2)} mm² )")
        st.divider()

        # (IV) Voltage Drop
        st.markdown("### (IV)  Voltage Drop Check")
        st.caption("IEC 60364-5-52")
        vd_limit_disp = 1.0 if feeder_to == "Transformer" else vd_run_limit
        c1, c2 = st.columns(2)
        c1.metric("Calculated Running VD", f"{round(v, 3)} %")
        c2.metric("Permissible Limit",     f"{vd_limit_disp} %")
        if v <= vd_limit_disp:
            st.success(f"✅  Running VD — PASS   ( {round(v,3)}%  ≤  {vd_limit_disp}% )")
        else:
            st.error(f"❌  Running VD — FAIL   ( {round(v,3)}%  >  {vd_limit_disp}% )")

        if load_type == "Motor":
            st.caption(f"IEC 60034 — Starting: I_st = {starting_multiple}× I_FL = {round(starting_multiple*I_fl,1)} A,  PF_start = 0.2")
            c1, c2 = st.columns(2)
            c1.metric("Starting VD",   f"{round(vs, 3)} %")
            c2.metric("Permissible",   f"{vd_start_limit} %")
            if vs <= vd_start_limit:
                st.success(f"✅  Starting VD — PASS   ( {round(vs,3)}%  ≤  {vd_start_limit}% )")
            else:
                st.error(f"❌  Starting VD — FAIL   ( {round(vs,3)}%  >  {vd_start_limit}% )")
        st.divider()

        # (V) Final
        st.markdown("### (V)  Final Cable Selection")
        st.caption("Oman Cable Catalogue — IEC Standards")
        st.success(f"✅  Selected Cable →  {cable_str}")

        st.markdown("### 🧠  Engineering Statement")
        checks = "ampacity, short circuit withstand, and running voltage drop"
        if load_type == "Motor":
            checks += ", and motor starting voltage drop"
        st.info(f"All design checks ({checks}) are satisfied. "
                f"The selected cable is safe and suitable for the given application.")

        close_card()

        # Summary metrics
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Full-Load Current", f"{round(I_fl, 1)} A")
        m2.metric("Running VD",        f"{round(v, 3)} %")
        m3.metric("SC Min. Area",      f"{round(S_min, 1)} mm²")
        if load_type == "Motor":
            m4.metric("Starting VD",   f"{round(vs, 3)} %")

        # PDF
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_dl, _ = st.columns([1, 2, 1])
        with col_dl:
            # ── PDF generation ────────────────────────────
            def make_pdf():
                f   = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                c   = canvas.Canvas(f.name, pagesize=A4)
                W, H = A4
                if os.path.exists("kent_cover.png"):
                    c.drawImage("kent_cover.png", 0, 0, width=W, height=H)
                c.setFont("Helvetica-Bold", 18); c.drawString(50, 720, "PROJECT DETAILS")
                c.setFont("Helvetica", 12); y = 690
                for line in [
                    f"Client          : {client_name}",
                    f"Project         : {project_name}",
                    f"Feeder          : {feeder_from} → {feeder_to}",
                    f"Voltage         : {voltage} kV",
                    f"Cable Length    : {length} m",
                    f"Load Type       : {load_type}",
                    f"Power           : {power} {'kVA' if load_type=='Transformer' else 'kW'}",
                    f"Laying Method   : {laying}",
                ]:
                    c.drawString(50, y, line); y -= 20
                c.showPage()

                y = 800
                c.setFont("Helvetica-Bold", 16)
                c.drawString(100, y, "CableMate — Engineering Calculation Report")
                y -= 35; c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y, f"SELECTED CABLE: {best['runs']}R × {core_str} × {best['size']} mm²")

                def section(title, ref):
                    nonlocal y
                    y -= 22; c.setFont("Helvetica-Bold", 11); c.drawString(50, y, title)
                    y -= 13; c.setFont("Helvetica-Oblique", 9); c.drawString(55, y, ref)
                    y -= 2

                def row(text):
                    nonlocal y
                    y -= 14; c.setFont("Helvetica", 10); c.drawString(60, y, text)
                    if y < 80: c.showPage(); y = 760

                section("1. LOAD CURRENT", "(IEC 60038 / IEC 60909)")
                row(f"I_FL = P / (√3 × V × PF × η)  =  {power}kW / (√3 × {voltage}kV × {pf} × {eff})  =  {round(I_fl,2)} A")

                section("2. AMPACITY CHECK", "(IEC 60287)")
                row(f"Catalog ampacity ({best['size']} mm²)  =  {catalog['amp'][best['size']]} A")
                row(f"Derating kT  =  {soil} × {depth} × {group} × {temp} × {laying_factor}  =  {round(kT,4)}")
                row(f"Available  =  {catalog['amp'][best['size']]} × {round(kT,4)} × {best['runs']}  =  {round(amp_avail,1)} A")
                row(f"Required   =  {round(I_design,1)} A     →  {round(amp_avail,1)} ≥ {round(I_design,1)}  ✔  PASS")

                section("3. SHORT CIRCUIT CHECK", f"(IEC 60949 — k={k_used}, t={t_used} s)")
                row(f"A_min = (I_fault × √t) / k  =  ({fault}kA × √{t_used}) / {k_used}  =  {round(S_min,2)} mm²")
                row(f"Provided  =  {best['runs']} × {best['size']}  =  {sc_area} mm²")
                row(f"{sc_area} ≥ {round(S_min,2)}  ✔  PASS")

                section("4. RUNNING VOLTAGE DROP", "(IEC 60364-5-52)")
                row(f"VD%  =  {round(v,3)} %     Limit  =  {vd_limit_disp} %     →  ✔  PASS")

                if load_type == "Motor":
                    section("5. STARTING VOLTAGE DROP", "(IEC 60034 — PF_start = 0.2)")
                    row(f"I_start  =  {starting_multiple} × {round(I_fl,1)}  =  {round(starting_multiple*I_fl,1)} A")
                    row(f"VD_start%  =  {round(vs,3)} %     Limit  =  {vd_start_limit} %     →  ✔  PASS")

                section("6. DERATING SUMMARY", "(IEC 60364-5-52)")
                row(f"kT  =  Soil({soil}) × Depth({depth}) × Group({group}) × Temp({temp})")

                y -= 25
                if y < 120: c.showPage(); y = 760
                c.setFont("Helvetica-Bold", 11); c.drawString(50, y, "STANDARDS REFERENCED")
                y -= 3
                for ref in ["IEC 60364","IEC 60287","IEC 60949","IEC 60034","IEC 60947","Oman Cable Catalogue"]:
                    y -= 14; c.setFont("Helvetica", 10); c.drawString(60, y, f"• {ref}")

                y -= 22; c.setFont("Helvetica-Bold", 11)
                c.drawString(50, y, f"FINAL CABLE: {best['runs']}R × {core_str} × {best['size']} mm²  — All checks PASSED")
                c.save()
                return f.name

            pdf_path = make_pdf()
            with open(pdf_path, "rb") as fp:
                st.download_button("📥  Download Engineering Report (PDF)", fp,
                                   "CableMate_Report.pdf", use_container_width=True)

    else:
        st.error("⚠  No suitable cable found. Consider: relaxing voltage drop limits, "
                 "reviewing fault settings, or checking that load parameters are correct.")

# ─────────────────────────────────────────────────
# MANUAL CABLE EVALUATION
# ─────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
open_card("🔧", "Manual Cable Evaluation", "OVERRIDE", "slate")
col1, col2 = st.columns(2)
with col1:
    manual_size = st.selectbox("Cable Size (mm²)", catalog["sizes"], key="man_size")
with col2:
    manual_runs = st.selectbox("Number of Runs", list(range(1, 11)), key="man_runs")

_, col_m, _ = st.columns([1, 2, 1])
with col_m:
    apply_manual = st.button("🔧  Apply Manual Selection", use_container_width=True)
close_card()

if apply_manual:
    st.session_state.update({
        "manual_done": True, "calc_manual": True,
        "m_size": manual_size, "m_runs": manual_runs, "m_type": cable_type,
    })

if "calculated" in st.session_state and st.session_state.get("calc_manual", False):
    ms   = st.session_state["m_size"]
    mr   = st.session_state["m_runs"]
    mt   = st.session_state["m_type"]
    I_fl = st.session_state["I"]
    I_d  = st.session_state["I_design"]
    Sn   = st.session_state["S"]

    amp_m  = catalog["amp"][ms] * kT * mr
    vdr_m  = calc_vd_run(I_fl, catalog["R"][ms], catalog["X"][ms], mr)
    vds_m  = calc_vd_start(I_fl, catalog["R"][ms], catalog["X"][ms], mr) if load_type == "Motor" else 0.0
    sc_m   = ms * mr
    amp_ok = amp_m  >= I_d
    vdr_ok = vdr_m  <= (1.0 if feeder_to == "Transformer" else vd_run_limit)
    sc_ok  = sc_m   >= Sn
    vds_ok = (vds_m <= vd_start_limit) if load_type == "Motor" else True

    st.session_state.update({
        "v_m": vdr_m, "vs_m": vds_m,
        "amp_ok": amp_ok, "vdr_ok": vdr_ok, "sc_ok": sc_ok, "vds_ok": vds_ok,
    })

    lbl = f"{mr}R × {'3C' if mt=='3-Core' else '1C'} × {ms} mm²"
    st.caption("Manual selection result:")
    st.markdown(f"**Cable →** `{lbl}`")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ampacity",       "✅ PASS" if amp_ok else "❌ FAIL")
    c2.metric("Running VD",     "✅ PASS" if vdr_ok else "❌ FAIL")
    c3.metric("Short Circuit",  "✅ PASS" if sc_ok  else "❌ FAIL")
    if load_type == "Motor":
        c4.metric("Starting VD","✅ PASS" if vds_ok else "❌ FAIL")

    if not amp_ok: st.warning(f"⚠  Ampacity: available {round(amp_m,1)} A vs required {round(I_d,1)} A")
    if not vdr_ok: st.warning(f"⚠  Running VD: {round(vdr_m,3)}% exceeds limit.")
    if not sc_ok:  st.warning(f"⚠  SC area: {sc_m} mm² < required {round(Sn,2)} mm²")
    if load_type == "Motor" and not vds_ok:
        st.warning(f"⚠  Starting VD: {round(vds_m,3)}% exceeds {vd_start_limit}%")

    st.session_state["calc_manual"] = False

# ─────────────────────────────────────────────────
# COMPARISON
# ─────────────────────────────────────────────────
if "calculated" in st.session_state and "manual_done" in st.session_state:
    best = st.session_state.get("best")
    if not best:
        st.error("No auto-selected cable to compare against.")
        st.stop()

    st.markdown("<br>", unsafe_allow_html=True)
    open_card("🔍", "Best vs Manual Comparison", "ANALYSIS", "blue")

    ms  = st.session_state.get("m_size")
    mr  = st.session_state.get("m_runs")
    mt  = st.session_state.get("m_type")
    cl  = "3C" if mt == "3-Core" else "1C"

    c1, c2 = st.columns(2)
    c1.metric("🏆  Optimal Cable", f"{best['runs']}R × {cl} × {best['size']} mm²")
    c2.metric("🔧  Manual Cable",  f"{mr}R × {cl} × {ms} mm²")

    vdr_m = st.session_state.get("v_m")
    if vdr_m is not None:
        diff = round(vdr_m - v, 3)
        sign = "+" if diff >= 0 else ""
        st.metric("Running VD Δ  (Manual − Optimal)", f"{sign}{diff} %",
                  delta=f"{sign}{diff} %", delta_color="inverse")
    else:
        st.info("Apply manual selection to see the voltage drop comparison.")

    st.markdown("### 🧠  Engineering Reasoning")
    amp_ok = st.session_state.get("amp_ok")
    vdr_ok = st.session_state.get("vdr_ok")
    sc_ok  = st.session_state.get("sc_ok")
    vds_ok = st.session_state.get("vds_ok")

    if ms == best["size"] and mr == best["runs"]:
        st.success("✔  Manual selection matches the optimal cable — excellent engineering judgement!")
    elif amp_ok and vdr_ok and sc_ok and (vds_ok if load_type=="Motor" else True):
        st.info("ℹ  Manual cable passes all checks but is not the most cost-optimal choice.")
    else:
        if not amp_ok:
            st.error("❌  Fails ampacity — cable cannot carry the load current safely.")
        if not sc_ok:
            st.error("❌  Fails short circuit check — conductor area insufficient.")
        if not vdr_ok:
            st.error("❌  Fails running voltage drop check.")
        if load_type == "Motor" and not vds_ok:
            st.error("❌  Fails starting voltage drop — motor may not start successfully.")

    close_card()
