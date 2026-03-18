import streamlit as st
import math
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components

st.set_page_config(page_title="CableMate", layout="wide")

# ------------------------------------------------
# UI STYLE
# ------------------------------------------------

st.markdown("""
<style>
.stApp {background-color:#f4f6f9;}
section[data-testid="stSidebar"] {background-color:#0f172a;}
section[data-testid="stSidebar"] * {color:#e5e7eb !important;}
h1,h2,h3 {color:#111827;}
.block-container {padding-top:1rem;}
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
# HEADER
# ------------------------------------------------

c1,c2 = st.columns([1,6])
with c1:
    st.image("logo.png", width=80)
with c2:
    st.title("CableMate – MV Cable Sizing Tool")
    st.caption("Professional Cable Design Assistant")

st.divider()

# ------------------------------------------------
# SIDEBAR INPUTS
# ------------------------------------------------

st.sidebar.header("Project Inputs")

feeder_from = st.sidebar.selectbox("From",["Switchgear","Transformer","Generator"])
feeder_to = st.sidebar.selectbox("To",["Motor","Transformer","Panel"])

voltage = st.sidebar.selectbox("Voltage (kV)",[3.3,6.6,11,33])
length = st.sidebar.number_input("Cable Length (m)",value=300)

laying = st.sidebar.selectbox("Cable Laying",["Direct Buried","Air","Duct"])

# ------------------------------------------------
# LOAD
# ------------------------------------------------

st.sidebar.subheader("Load Details")

load_type = st.sidebar.selectbox("Load Type",["Motor","Transformer","Power"])

if load_type=="Transformer":
    power = st.sidebar.number_input("Load (kVA)",value=500)
else:
    power = st.sidebar.number_input("Load (kW)",value=400)

pf = st.sidebar.number_input("Power Factor",value=0.9)
eff = st.sidebar.number_input("Efficiency",value=0.95)

# ------------------------------------------------
# FAULT
# ------------------------------------------------

st.sidebar.subheader("Fault Conditions")

fault = st.sidebar.number_input("Fault Level (kA)",value=25)
fault_time = st.sidebar.number_input("Fault Time (s)",value=0.4)

# ------------------------------------------------
# VOLTAGE DROP LIMITS
# ------------------------------------------------

st.sidebar.subheader("Voltage Drop Limits")

vd_run_limit = st.sidebar.number_input("Running VD (%)",value=5.0)
vd_start_limit = st.sidebar.number_input("Starting VD (%)",value=15.0)

# ------------------------------------------------
# DERATING
# ------------------------------------------------

st.sidebar.subheader("Derating Factors")

def input_with_other(label, options, default):
    choice = st.sidebar.selectbox(label, options + ["Other"])
    if choice == "Other":
        return st.sidebar.number_input(f"{label} (Manual)", value=default)
    return float(choice)

soil = input_with_other("Soil Factor",[1.0,1.5,2],1.5)
depth = input_with_other("Depth Factor",[0.8,1.0],1.0)
group = input_with_other("Grouping Factor",[1,0.85,0.79,0.73],1)
temp = input_with_other("Temperature Factor",[1,0.85],1)

# LAYING FACTOR
if laying == "Air":
    laying_factor = 1.0
elif laying == "Duct":
    laying_factor = 0.9
else:
    laying_factor = 0.85

kT = soil * depth * group * temp * laying_factor

run_btn = st.sidebar.button("Run CableMate")

# ------------------------------------------------
# CATALOG
# ------------------------------------------------

catalog = {
"sizes":[50,70,95,120,150,185,240,300],
"amp":{50:181,70:220,95:263,120:298,150:332,185:374,240:431,300:482},
"R":{50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.099,240:0.075,300:0.060},
"X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083,300:0.082}
}

# ------------------------------------------------
# FUNCTIONS
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
# PDF REPORT
# ------------------------------------------------

def report(best,I,S,v,vs):

    f=tempfile.NamedTemporaryFile(delete=False)
    c=canvas.Canvas(f.name,pagesize=A4)

    y=800
    c.drawString(180,y,"CableMate Engineering Report")

    y-=30
    c.drawString(50,y,f"Feeder: {feeder_from} → {feeder_to}")

    y-=20
    c.drawString(50,y,f"Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

    y-=25
    c.drawString(50,y,"LOAD CURRENT")
    y-=15
    c.drawString(50,y,f"I = {round(I,2)} A")

    y-=25
    c.drawString(50,y,"SHORT CIRCUIT")
    y-=15
    c.drawString(50,y,f"{round(S,1)} < {best['size']} → next size selected ✔")

    y-=25
    c.drawString(50,y,"VOLTAGE DROP")
    y-=15
    c.drawString(50,y=f"Running: {round(v,2)} % ≤ {vd_run_limit}")
    y-=15
    c.drawString(50,y=f"Starting: {round(vs,2)} % ≤ {vd_start_limit}")

    y-=25
    c.drawString(50,y,"DERATING")
    y-=15
    c.drawString(50,y=f"kT = {round(kT,2)}")

    y-=25
    c.drawString(50,y,"JUSTIFICATION")
    y-=15
    c.drawString(50,y,"Cable satisfies ampacity, VD and SC criteria.")

    c.save()
    return f.name

# ------------------------------------------------
# ENGINE
# ------------------------------------------------

if run_btn:

    I = load_current()
    S = short_circuit()

    best=None

    for runs in range(1,4):
        for size in catalog["sizes"]:

            if size < S:
                continue

            amp = catalog["amp"][size]*kT*runs
            if amp < I:
                continue

            v = vd(I,catalog["R"][size],catalog["X"][size],runs)
            if v > vd_run_limit:
                continue

            vs = vd_start(I,catalog["R"][size],catalog["X"][size],runs)
            if vs > vd_start_limit:
                continue

            best={"size":size,"runs":runs}
            break

        if best:
            break

    if best:

        st.success(f"Best Fit Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

        col1,col2,col3 = st.columns(3)
        col1.metric("Load Current",round(I,1))
        col2.metric("Running VD %",round(v,2))
        col3.metric("Starting VD %",round(vs,2))

        pdf = report(best,I,S,v,vs)

        with open(pdf,"rb") as f:
            st.download_button("Download Report",f,"CableMate_Report.pdf")

    else:
        st.error("No suitable cable found")
