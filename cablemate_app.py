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
# UI STYLE (CLEAN PROFESSIONAL)
# ------------------------------------------------

st.markdown("""
<style>
.stApp {background-color:#f4f6f9;}
section[data-testid="stSidebar"] {background-color:#0f172a;}
section[data-testid="stSidebar"] * {color:#e5e7eb !important;}
.block-container {padding-top:1rem;}
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

st.sidebar.header("Project Setup")

client_name = st.sidebar.text_input("Client Name","ABC Pvt Ltd")
project_name = st.sidebar.text_input("Project Name","Electrical System")

st.sidebar.divider()

# Layout split for better UX
left,right = st.sidebar.columns(2)

with left:
    feeder_from = st.selectbox("From",["Switchgear","Transformer","Generator"])
    voltage = st.selectbox("Voltage (kV)",[3.3,6.6,11,33])
    laying = st.selectbox("Laying",["Direct Buried","Air","Duct"])

with right:
    feeder_to = st.selectbox("To",["Motor","Transformer","Panel"])
    length = st.number_input("Length (m)",value=300)

# ------------------------------------------------
# LOAD
# ------------------------------------------------

st.sidebar.subheader("Load")

load_type = st.sidebar.selectbox("Type",["Motor","Transformer","Power"])

if load_type=="Transformer":
    power = st.sidebar.number_input("Load (kVA)",500)
else:
    power = st.sidebar.number_input("Load (kW)",400)

pf = st.sidebar.number_input("PF",0.9)
eff = st.sidebar.number_input("Efficiency",0.95)

# ------------------------------------------------
# FAULT
# ------------------------------------------------

st.sidebar.subheader("Fault")

fault = st.sidebar.number_input("Fault Level (kA)",25)
fault_time = st.sidebar.number_input("Fault Time (s)",0.4)

# ------------------------------------------------
# VD LIMITS
# ------------------------------------------------

st.sidebar.subheader("Voltage Drop")

vd_run_limit = st.sidebar.number_input("Running VD (%)",5.0)
vd_start_limit = st.sidebar.number_input("Starting VD (%)",15.0)

# ------------------------------------------------
# DERATING
# ------------------------------------------------

st.sidebar.subheader("Derating")

def input_with_other(label, options, default):
    val = st.sidebar.selectbox(label, options + ["Other"])
    if val=="Other":
        return st.sidebar.number_input(f"{label} Manual",value=default)
    return float(val)

soil = input_with_other("Soil",[1.0,1.5,2],1.5)
depth = input_with_other("Depth",[0.8,1.0],1.0)
group = input_with_other("Grouping",[1,0.85,0.79,0.73],1)
temp = input_with_other("Temp",[1,0.85],1)

laying_factor = 1.0 if laying=="Air" else 0.9 if laying=="Duct" else 0.85

kT = soil*depth*group*temp*laying_factor

run_btn = st.sidebar.button("Run CableMate")

# ------------------------------------------------
# HEADER
# ------------------------------------------------

c1,c2 = st.columns([1,6])
with c1:
    st.image("logo.png",width=80)
with c2:
    st.title("CableMate – MV Cable Sizing Tool")
    st.caption("Professional Cable Design Assistant")

st.markdown(f"""
### 📁 Project
**Client:** {client_name}  
**Project:** {project_name}
""")

st.divider()

# ------------------------------------------------
# CATALOG
# ------------------------------------------------

catalog={
"sizes":[50,70,95,120,150,185,240,300],
"amp":{50:181,70:220,95:263,120:298,150:332,185:374,240:431,300:482},
"R":{50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.099,240:0.075,300:0.060},
"X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083,300:0.082}
}

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
    return (fault*1000*math.sqrt(fault_time))/143

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
    amp = catalog["amp"][best["size"]] * kT * best["runs"]

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
    c.drawString(50, y, f"kT = {round(kT,2)}")

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
# ENGINE
# ------------------------------------------------

if run_btn:

    I=load_current()
    S=short_circuit()

    best=None
    v=0
    vs=0

    for runs in range(1,4):
        for size in catalog["sizes"]:

            if size<S: continue

            amp=catalog["amp"][size]*kT*runs
            if amp<I: continue

            v=vd(I,catalog["R"][size],catalog["X"][size],runs)
            if v>vd_run_limit: continue

            vs=vd_start(I,catalog["R"][size],catalog["X"][size],runs)
            if vs>vd_start_limit: continue

            best={"size":size,"runs":runs}
            break

        if best: break

    if best:

        st.success(f"Best Fit Cable → {best['runs']}R x 3C x {best['size']} sq.mm")

        m1,m2,m3=st.columns(3)
        m1.metric("Load Current",round(I,1))
        m2.metric("Running VD %",round(v,2))
        m3.metric("Starting VD %",round(vs,2))

        pdf=report(best,I,S,v,vs)

        with open(pdf,"rb") as f:
            st.download_button("Download Report",f,"CableMate_Report.pdf")

    else:
        st.error("No suitable cable found")
