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

st.set_page_config(page_title="CableMate", layout="wide")
# ------------------------------------------------
# HEADER
# ------------------------------------------------

c1,c2 = st.columns([1,6])
with c1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
with c2:
    st.title("CableMate – MV Cable Sizing Tool")
    st.caption("Professional Cable Design Assistant")
# ------------------------------------------------
# UI STYLE (CLEAN PROFESSIONAL)
# ------------------------------------------------

st.markdown("""
<style>
.stApp {background-color:#f4f6f9;}
section[data-testid="stSidebar"] {background-color:#0f172a;}
section[data-testid="stSidebar"] * {color:#e5e7eb !important;}
.block-container {padding-top:4rem;}
.metric-box {
    background-color:white;
    padding:15px;
    border-radius:10px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.1);
}
</style>
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
# SIDEBAR INPUTS
# ------------------------------------------------

# ------------------------------------------------
# USER INPUT UI (PROFESSIONAL + DOUBLE COLUMN)
# ------------------------------------------------

st.subheader("📁 Project Information")

col1, col2 = st.columns(2)

with col1:
    client_name = st.text_input("Client Name", "ABC Pvt Ltd")
    
    feeder_from = st.selectbox(
        "From Equipment",
        ["Switchgear","Transformer","Generator"]
    )
    
    from_tag = st.text_input(
        "From Equipment Tag",
        placeholder="e.g. TR-01 / SWGR-A1"
    )

    voltage = st.selectbox("System Voltage (kV)", [3.3,6.6,11,25,33,66,132])

with col2:
    project_name = st.text_input("Project Name", "Electrical Distribution System")
    
    feeder_to = st.selectbox(
        "To Equipment",
        ["Motor","Transformer","Panel"]
    )
    
    to_tag = st.text_input(
        "To Equipment Tag",
        placeholder="e.g. MTR-01 / PNL-B2"
    )

    length = st.number_input("Cable Length (m)", value=300)

st.divider()

# ------------------------------------------------
# INSTALLATION
# ------------------------------------------------

st.subheader("🛠 Installation Details")

col1, col2 = st.columns(2)

with col1:
    laying = st.selectbox("Cable Laying Method", ["Direct Buried","Air","Duct"])

with col2:
    pass  # future expansion

st.divider()

# ------------------------------------------------
# LOAD DETAILS
# ------------------------------------------------

st.subheader("⚡ Load Details")

col1, col2 = st.columns(2)

with col1:
    load_type = st.selectbox("Load Type", ["Motor","Transformer","Power"])

    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=500)
    else:
        power = st.number_input("Load (kW)", value=400)

with col2:
    pf = st.number_input("Power Factor", value=0.9)
    eff = st.number_input("Efficiency", value=0.95)
st.divider()
st.subheader("🧵 Conductor Details")

material = st.selectbox("Conductor Material", ["Copper", "Aluminium"])
cable_type = st.selectbox("Cable Type", ["1-Core", "3-Core"])
if voltage >= 66 and cable_type == "3-Core":
    st.warning("At 66 kV and above, single-core cables are typically used.")
st.divider()

# ------------------------------------------------
# FAULT CONDITIONS
# ------------------------------------------------

st.subheader("⚠ Fault Conditions")

col1, col2 = st.columns(2)

with col1:
    fault = st.number_input("Fault Level (kA)", value=25)

with col2:
    fault_time = st.number_input("Fault Duration (s)", value=0.4)

st.divider()

# ------------------------------------------------
# VOLTAGE DROP LIMITS
# ------------------------------------------------

st.subheader("📉 Voltage Drop Limits")

col1, col2 = st.columns(2)

with col1:
    vd_run_limit = st.number_input("Running Voltage Drop (%)", value=5.0)

if load_type == "Motor":
    with col2:
        vd_start_limit = st.number_input("Starting Voltage Drop (%)", value=15.0)
else:
    vd_start_limit = 100  # dummy high value so it never fails

st.divider()

# ------------------------------------------------
# DERATING FACTORS
# ------------------------------------------------

st.subheader("🌡 Derating Factors")

def input_with_other(label, options, default):
    col_a, col_b = st.columns([2,1])

    with col_a:
        choice = st.selectbox(label, options + ["Other"], key=f"{label}_select")

    if choice == "Other":
        with col_b:
            return st.number_input(
                "Manual",
                value=float(default),
                step=0.01,
                format="%.3f",
                key=f"{label}_manual"
            )
    return float(choice)

col1, col2 = st.columns(2)

with col1:
    soil = input_with_other("Soil Resistance Factor",[1.0,1.5,2],1.5)
    group = input_with_other("Grouping Factor",[1,0.85,0.79,0.73],1.0)

with col2:
    depth = input_with_other("Depth Factor",[0.8,1.0],1.0)
    temp = input_with_other("Temperature Factor",[1,0.85],1.0)

# Laying factor logic (unchanged)
if laying == "Air":
    laying_factor = 1.0
elif laying == "Duct":
    laying_factor = 0.9
else:
    laying_factor = 0.85


# ------------------------------------------------
# OVERALL DERATING DISPLAY
# ------------------------------------------------

st.markdown("### 📊 Overall Derating Factor")

kT_base = soil * depth * temp
st.success(f"Base Derating Factor (kT) = {round(kT_base, 3)}")
st.caption("Note: Grouping factor applied automatically for multiple runs")
st.divider()

st.markdown(f"""
### 📁 Project
**Client:** {client_name}  
**Project:** {project_name}
""")

st.divider()

# ------------------------------------------------
# RUN BUTTON
# ------------------------------------------------

run_btn = st.button("🚀 Run CableMate Analysis")
# ------------------------------------------------
# CATALOG
# ------------------------------------------------

catalog_cu={
"sizes":[50,70,95,120,150,185,240,300],
"amp":{50:181,70:220,95:263,120:298,150:332,185:374,240:431,300:482},
"R":{50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.099,240:0.075,300:0.060},
"X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083,300:0.082}
}

catalog_al={
"sizes":[50,70,95,120,150,185,240,300],
"amp":{50:150,70:180,95:215,120:245,150:275,185:310,240:360,300:405},
"R":{50:0.641,70:0.443,95:0.320,120:0.253,150:0.206,185:0.164,240:0.125,300:0.100},
"X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083,300:0.082}
}

if material == "Copper":
    catalog = catalog_cu
else:
    catalog = catalog_al
# ------------------------------------------------
# FUNCTIONS (UNCHANGED LOGIC)
# ------------------------------------------------

def load_current():
    if load_type=="Motor":
        return power*1000/(math.sqrt(3)*voltage*1000*pf*eff)
    elif load_type=="Transformer":
        return power*1000/(math.sqrt(3)*voltage*1000)
    else:
        return power*1000/(math.sqrt(3)*voltage*1000*pf)

def short_circuit():
    if material == "Copper":
        k = 143
    else:
        k = 94
    return (fault*1000*math.sqrt(fault_time))/k
    
def vd(I,R,X,runs):
    ang=math.acos(pf)
    return (math.sqrt(3)*I*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*runs*voltage*1000)*100

def vd_start(I,R,X,runs):
    Ist=6*I
    ang=math.acos(0.25)
    return (math.sqrt(3)*Ist*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*runs*voltage*1000)*100

# ------------------------------------------------
# PDF REPORT (UNCHANGED LOGIC)
# ------------------------------------------------

def report(best, I, S, v, vs):

    f = tempfile.NamedTemporaryFile(delete=False)
    c = canvas.Canvas(f.name, pagesize=A4)

    width, height = A4

    # ================================
    # PAGE 1 → COVER
    # ================================

    if os.path.exists("kent_cover.png"):
        c.drawImage("kent_cover.png", 0, 0, width=width, height=height)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 720, "PROJECT DETAILS")

    c.setFont("Helvetica", 12)
    y = 690

    c.drawString(50, y, f"Client Name      : {client_name}"); y -= 20
    c.drawString(50, y, f"Project Name     : {project_name}"); y -= 20
    c.drawString(50, y, f"Feeder           : {feeder_from} → {feeder_to}"); y -= 20
    c.drawString(50, y, f"Voltage Level    : {voltage} kV"); y -= 20
    c.drawString(50, y, f"Cable Length     : {length} m"); y -= 20
    c.drawString(50, y, f"Load Type        : {load_type}"); y -= 20
    c.drawString(50, y, f"Power            : {power}"); y -= 20
    c.drawString(50, y, f"Laying Method    : {laying}")

    c.showPage()

    # ================================
    # PAGE 2 → ENGINEERING REPORT
    # ================================

    y = 800
    c.setFont("Helvetica-Bold", 16)
    c.drawString(140, y, "CableMate Engineering Report")

    y -= 40
    c.setFont("Helvetica", 11)

    # --------------------------------
    # SELECTED CABLE
    # --------------------------------
    c.drawString(50, y, f"Selected Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

    # --------------------------------
    # LOAD CURRENT
    # --------------------------------
    y -= 25
    c.drawString(50, y, "LOAD CURRENT CALCULATION")
    y -= 15
    c.drawString(50, y, f"I = {round(I,2)} A")

    # --------------------------------
    # AMPACITY CHECK
    # --------------------------------
    if best["runs"] == 1:
        kT_rep = soil * depth * temp
    else:
        kT_rep = soil * depth * group * temp

    amp = catalog["amp"][best["size"]] * kT_rep * best["runs"]
    y -= 25
    c.drawString(50, y, "AMPACITY CHECK")
    y -= 15
    c.drawString(50, y, f"Available Ampacity = {round(amp,1)} A")
    y -= 15
    c.drawString(50, y, f"Load Current       = {round(I,1)} A")
    y -= 15
    c.drawString(50, y, f"{round(amp,1)} ≥ {round(I,1)} → PASS ✔")

    # --------------------------------
    # SHORT CIRCUIT CHECK
    # --------------------------------
    y -= 25
    c.drawString(50, y, "SHORT CIRCUIT CHECK")
    y -= 15
    c.drawString(50, y, f"Required Size = {round(S,1)} mm²")
    y -= 15
    c.drawString(50, y, f"{round(S,1)} < {best['size']} mm²")
    y -= 15
    c.drawString(50, y, f"Next Standard Size Selected → {best['size']} mm² ✔")

    # --------------------------------
    # RUNNING VOLTAGE DROP
    # --------------------------------
    y -= 25
    c.drawString(50, y, "RUNNING VOLTAGE DROP")
    y -= 15
    c.drawString(50, y, f"Calculated VD = {round(v,2)} %")
    y -= 15
    c.drawString(50, y, f"Allowed VD    = {vd_run_limit} %")
    y -= 15
    c.drawString(50, y, f"{round(v,2)} ≤ {vd_run_limit} → PASS ✔")

    # --------------------------------
    # STARTING VOLTAGE DROP
    # --------------------------------
    y -= 25
    c.drawString(50, y, "STARTING VOLTAGE DROP")
    y -= 15
    c.drawString(50, y, f"Calculated VD = {round(vs,2)} %")
    y -= 15
    c.drawString(50, y, f"Allowed VD    = {vd_start_limit} %")
    y -= 15
    c.drawString(50, y, f"{round(vs,2)} ≤ {vd_start_limit} → PASS ✔")

    # --------------------------------
    # DERATING FACTOR
    # --------------------------------
    y -= 25
    c.drawString(50, y, "DERATING FACTOR")
    y -= 15
    if best["runs"] == 1:
        kT_rep = soil * depth * temp
    else:
        kT_rep = soil * depth * group * temp

    c.drawString(50, y, f"kT = {round(kT_rep,2)}")

    # --------------------------------
    # FINAL STATEMENT
    # --------------------------------
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "FINAL ENGINEERING DECISION")

    y -= 20
    c.setFont("Helvetica", 11)

    c.drawString(50, y, "All design checks (Ampacity, Voltage Drop, Short Circuit)")
    y -= 15
    c.drawString(50, y, "have been successfully satisfied.")

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(
        50,
        y,
        f"FINAL SELECTED CABLE: {best['runs']}R x 3C x {best['size']} sq.mm"
    )

    c.save()
    return f.name
# ------------------------------------------------
# ENGINE (FINAL FIXED)
# ------------------------------------------------

# RUN BUTTON LOGIC (FINAL CLEAN ENGINE)
if run_btn:

    I = load_current()
    S = short_circuit()

    valid_options = []

    for runs in range(1,4):
        for size in catalog["sizes"]:

            # DERATING
            if runs == 1:
                kT_local = soil * depth * temp
            else:
                kT_local = soil * depth * group * temp

            # SHORT CIRCUIT (FINAL FIX)
            if size * runs < S:
                continue

            # AMPACITY
            amp = catalog["amp"][size] * kT_local * runs
            if amp < I:
                continue

            # VOLTAGE DROP
            v_temp = vd(I, catalog["R"][size], catalog["X"][size], runs)
            if v_temp > vd_run_limit:
                continue

            vs_temp = vd_start(I, catalog["R"][size], catalog["X"][size], runs)
            if vs_temp > vd_start_limit:
                continue

            # STORE VALID OPTION
            valid_options.append({
                "size": size,
                "runs": runs,
                "v": v_temp,
                "vs": vs_temp
            })

    # ----------------------------------------
    # SELECT BEST OPTION
    # ----------------------------------------
    best = None
    v = 0
    vs = 0

    if valid_options:
        # BASIC SORT (can improve later)
        valid_options.sort(key=lambda x: (x["runs"], x["size"]))

        best = valid_options[0]

        v = best["v"]
        vs = best["vs"]

    # ----------------------------------------
    # STORE IN SESSION
    # ----------------------------------------
    st.session_state["best"] = best
    st.session_state["v"] = v
    st.session_state["vs"] = vs
    st.session_state["calculated"] = True
    st.session_state["I"] = I
    st.session_state["S"] = S
# ----------------------------------------
# SHOW BEST CABLE (PERSISTENT)
# ----------------------------------------

if "calculated" in st.session_state:

    best = st.session_state["best"]
    I = st.session_state["I"]
    S = st.session_state["S"]
    v = st.session_state["v"]
    vs = st.session_state["vs"]

    if best:

        if cable_type == "3-Core":
            cable_str = f"{best['runs']}R x 3C x {best['size']} sq.mm"
        else:
            cable_str = f"{best['runs']}R x 1C x {best['size']} sq.mm"

        st.success(f"Best Fit Cable → {cable_str}")
        # ============================================
        # 📄 CALCULATION SHEET VIEW (LIKE PDF)
        # ============================================

        st.divider()
        st.subheader("📄 Cable Calculation Sheet")

        # -------------------------------
        # (I) CURRENT CALCULATION
        # -------------------------------
        st.markdown("### (I) Current Calculation")

        st.write(f"Voltage → {voltage} kV")
        st.write(f"Load → {power} {'kVA' if load_type=='Transformer' else 'kW'}")
        st.write(f"Power Factor → {pf}")
        
        st.success(f"Calculated Load Current → {round(I,2)} A")

# -------------------------------
# (II) AMPACITY CHECK
# -------------------------------
        st.markdown("### (II) Ampacity Check")

        if best["runs"] == 1:
            kT_calc = soil * depth * temp
        else:
            kT_calc = soil * depth * group * temp

        amp_available = catalog["amp"][best["size"]] * kT_calc * best["runs"]

        st.write(f"Base Ampacity → {catalog['amp'][best['size']]} A")
        st.write(f"Derating Factor → {round(kT_calc,3)}")
        st.write(f"Available Ampacity → {round(amp_available,2)} A")

        if amp_available >= I:
            st.success("Ampacity Check → PASS ✅")
        else:
            st.error("Ampacity Check → FAIL ❌")

# -------------------------------
# (III) SHORT CIRCUIT CHECK
# -------------------------------
        st.markdown("### (III) Short Circuit Check")

        if cable_type == "3-Core":
            S_check = S / 2
        else:
            S_check = S

        st.write(f"Required Area → {round(S_check,2)} sq.mm")
        st.write(f"Selected Cable Size → {best['size']} sq.mm")

        if best["size"] >= S_check:
            st.success("Short Circuit Check → PASS ✅")
        else:
            st.error("Short Circuit Check → FAIL ❌")

# -------------------------------
# (IV) VOLTAGE DROP
# -------------------------------
        st.markdown("### (IV) Voltage Drop Check")

        st.write(f"Calculated VD → {round(v,2)} %")
        st.write(f"Permissible VD → {vd_run_limit} %")

        if v <= vd_run_limit:
            st.success("Running Voltage Drop → PASS ✅")
        else:
            st.error("Running Voltage Drop → FAIL ❌")

        if load_type == "Motor":
            st.write(f"Starting VD → {round(vs,2)} %")
            st.write(f"Permissible → {vd_start_limit} %")

            if vs <= vd_start_limit:
                st.success("Starting Voltage Drop → PASS ✅")
            else:
                st.error("Starting Voltage Drop → FAIL ❌")

# -------------------------------
# (V) FINAL SELECTION
# -------------------------------
        st.markdown("### (V) Final Cable Selection")

        if cable_type == "3-Core":
            final_str = f"{best['runs']}R x 3C x {best['size']} sq.mm"
        else:
             final_str = f"{best['runs']}R x 1C x {best['size']} sq.mm"

        st.success(f"Selected Cable → {final_str}")

# -------------------------------
# ENGINEERING STATEMENT
# -------------------------------
        st.markdown("### 🧠 Engineering Statement")

        st.write(
            "All design checks including ampacity, voltage drop, and short circuit "
            "withstand capability have been satisfied. The selected cable is safe "
             "and suitable for the given application."
        )
        # METRICS
        m1, m2, m3 = st.columns(3)
        m1.metric("Load Current", round(I,1))
        m2.metric("Running VD %", round(v,2))

        if load_type == "Motor":
            m3.metric("Starting VD %", round(vs,2))

        # PDF
        pdf = report(best,I,S,v,vs)
        with open(pdf,"rb") as f:
            st.download_button("Download Report",f,"CableMate_Report.pdf")

    else:
        st.error("No suitable cable found")


# ============================================
# MANUAL SECTION (ONLY ONE PLACE)
# ============================================

st.divider()
st.subheader("🔧 Manual Cable Evaluation")

col1, col2 = st.columns(2)

with col1:
    manual_size = st.selectbox(
        "Select Cable Size (sq.mm)",
        catalog["sizes"],
        key="manual_size_unique"
    )

with col2:
    manual_runs = st.selectbox(
        "Number of Runs",
        [1,2,3],
        key="manual_runs_unique"
    )
apply_manual = st.button("Apply Manual Selection")

if apply_manual:
    st.session_state["manual_done"] = True
    st.session_state["calculate_manual"] = True
    # STORE CURRENT SELECTION
    st.session_state["selected_size"] = manual_size
    st.session_state["selected_runs"] = manual_runs
    st.session_state["selected_type"] = cable_type
# ============================================
# MANUAL CALCULATION (STABLE VERSION - FIXED)
# ============================================

if "calculated" in st.session_state and st.session_state.get("calculate_manual", False):

    # USE STORED VALUES (NOT LIVE DROPDOWN)
    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")
    manual_type_used = st.session_state.get("selected_type")  # ✅ NEW

    if manual_size_used is not None and manual_runs_used is not None and manual_type_used is not None:

        # ------------------------------------
        # DERATING
        # ------------------------------------
        if manual_runs_used == 1:
            kT_manual = soil * depth * temp
        else:
            kT_manual = soil * depth * group * temp

        # ------------------------------------
        # CALCULATIONS
        # ------------------------------------
        amp = catalog["amp"][manual_size_used] * kT_manual * manual_runs_used

        v_manual = vd(
            I,
            catalog["R"][manual_size_used],
            catalog["X"][manual_size_used],
            manual_runs_used
        )

        vs_manual = vd_start(
            I,
            catalog["R"][manual_size_used],
            catalog["X"][manual_size_used],
            manual_runs_used
        )

        # ------------------------------------
        # SHORT CIRCUIT FIX (IMPORTANT)
        # ------------------------------------
        if manual_type_used == "3-Core":
            sc_ok = manual_size_used >= (S / 2)
        else:
            sc_ok = manual_size_used >= S

        # ------------------------------------
        # CHECKS
        # ------------------------------------
        amp_ok = amp >= I
        vd_ok = v_manual <= vd_run_limit
        vs_ok = vs_manual <= vd_start_limit

        # ------------------------------------
        # STORE VALUES
        # ------------------------------------
        st.session_state["v_manual"] = v_manual
        st.session_state["vs_manual"] = vs_manual
        st.session_state["amp_ok"] = amp_ok
        st.session_state["vd_ok"] = vd_ok
        st.session_state["vs_ok"] = vs_ok
        st.session_state["sc_ok"] = sc_ok

        # ------------------------------------
        # SAFE FETCH
        # ------------------------------------
        amp_ok_val = st.session_state.get("amp_ok")
        vd_ok_val = st.session_state.get("vd_ok")
        vs_ok_val = st.session_state.get("vs_ok")
        sc_ok_val = st.session_state.get("sc_ok")

        # ------------------------------------
        # DISPLAY RESULT
        # ------------------------------------
        st.caption("Showing last applied manual selection")

        st.markdown("### 📊 Manual Cable Result")

        if manual_type_used == "3-Core":
            manual_str = f"{manual_runs_used}R x 3C x {manual_size_used} sq.mm"
        else:
            manual_str = f"{manual_runs_used}R x 1C x {manual_size_used} sq.mm"

        if manual_type_used == "3-Core":
            manual_str = f"{manual_runs_used}R x 3C x {manual_size_used} sq.mm"
        else:
            manual_str = f"{manual_runs_used}R x 1C x {manual_size_used} sq.mm"

        st.write(f"Manual Cable → {manual_str}")

        st.write(f"Ampacity → {'✅ PASS' if amp_ok_val else '❌ FAIL'}")
        st.write(f"Voltage Drop → {'✅ PASS' if vd_ok_val else '❌ FAIL'}")

        if load_type == "Motor":
            st.write(f"Starting VD → {'✅ PASS' if vs_ok_val else '❌ FAIL'}")

        st.write(f"Short Circuit → {'✅ PASS' if sc_ok_val else '❌ FAIL'}")

        # ------------------------------------
        # WARNINGS
        # ------------------------------------
        if amp_ok_val is False:
            st.warning("⚠ Ampacity is insufficient → Cable may overheat")

        if vd_ok_val is False:
            st.warning("⚠ Voltage drop exceeds limit → Poor performance")

        if sc_ok_val is False:
            st.warning("⚠ Short circuit rating inadequate → Risk of damage")

        if load_type == "Motor" and vs_ok_val is False:
            st.warning("⚠ Starting voltage drop too high → Motor may fail to start")

        # ------------------------------------
        # RESET FLAG
        # ------------------------------------
        st.session_state["calculate_manual"] = False

# ============================================
# COMPARISON + JUSTIFICATION (FINAL CLEAN)
# ============================================

if "calculated" in st.session_state and "manual_done" in st.session_state:

    best = st.session_state.get("best")
    if not best:
        st.error("No suitable cable found")
        st.stop()
        
    st.markdown("### 🔍 Best vs Manual Comparison")

    # USE STORED VALUES (NOT LIVE DROPDOWN)
    manual_size_used = st.session_state.get("selected_size")
    manual_runs_used = st.session_state.get("selected_runs")

    if cable_type == "3-Core":
        best_str = f"{best['runs']}R x 3C x {best['size']} sq.mm"
    else:
        best_str = f"{best['runs']}R x 1C x {best['size']} sq.mm"

    st.write(f"Best Cable → {best_str}")
    st.write(f"Manual Cable → {manual_runs_used}R x {manual_size_used} sq.mm")

    # SAFE FETCH
    v_manual_val = st.session_state.get("v_manual")

    if v_manual_val is not None:
        st.write(f"Voltage Drop Difference → {round(v_manual_val - v, 2)} %")
    else:
        st.info("Apply manual selection to see comparison")

    # ============================================
    # ENGINEERING JUSTIFICATION
    # ============================================

    st.markdown("### 🧠 Engineering Reasoning")

    amp_ok_val = st.session_state.get("amp_ok")
    vd_ok_val = st.session_state.get("vd_ok")
    vs_ok_val = st.session_state.get("vs_ok")
    sc_ok_val = st.session_state.get("sc_ok")

    if amp_ok_val is False:
        st.write("Manual cable fails due to insufficient ampacity.")

    if vd_ok_val is False:
        st.write("Manual cable causes excessive voltage drop.")

    if load_type == "Motor" and vs_ok_val is False:
        st.write("Manual cable has high starting voltage drop.")

  # ------------------------------------
# CHECK IF MANUAL == BEST (IMPORTANT)
# ------------------------------------
manual_size_used = st.session_state.get("selected_size")
manual_runs_used = st.session_state.get("selected_runs")
manual_type_used = st.session_state.get("selected_type")

best_type = st.session_state.get("selected_type")  # ✅ FIXED

if (
    manual_size_used == best["size"]
    and manual_runs_used == best["runs"]
    and manual_type_used == best_type
):
    st.success("✔ Manual cable matches the optimal cable selection")

else:
    # ------------------------------------
    # FAILURE CONDITIONS (PRIORITY)
    # ------------------------------------
    if amp_ok_val is False:
        st.error("Manual cable fails due to insufficient ampacity.")

    elif vd_ok_val is False:
        st.error("Manual cable causes excessive voltage drop.")

    elif sc_ok_val is False:
        st.error("Manual cable does not meet short circuit requirements.")

    elif load_type == "Motor" and vs_ok_val is False:
        st.error("Manual cable has high starting voltage drop.")

    # ------------------------------------
    # IF ALL PASS BUT NOT BEST
    # ------------------------------------
    else:
        st.info("Manual cable is technically acceptable but not optimal compared to selected cable.")

    # ----------------------------------------
    # IF NO CABLE FOUND
    # ----------------------------------------
