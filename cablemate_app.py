import streamlit as st
import math
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(page_title="CableMate", layout="wide")

# ------------------------------------------------
# PROFESSIONAL UI FIX
# ------------------------------------------------

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background-color: #f8fafc;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #111827;
}

/* TEXT */
p, label, span {
    color: #374151 !important;
}

/* SUCCESS */
div[data-baseweb="notification"][kind="success"] {
    background-color: #ecfdf5;
    border-left: 6px solid #10b981;
}

/* ERROR */
div[data-baseweb="notification"][kind="error"] {
    background-color: #fef2f2;
    border-left: 6px solid #ef4444;
}

/* BUTTON */
button[kind="primary"] {
    background-color: #2563eb;
    border-radius: 8px;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: white;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# CLOSE TAB WARNING
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

h1,h2 = st.columns([1,6])
with h1:
    st.image("logo.png", width=80)
with h2:
    st.title("CableMate – MV Cable Sizing Tool")
    st.caption("Professional Engineering Cable Selection Tool")

st.divider()

# ------------------------------------------------
# SIDEBAR INPUTS (DOUBLE COLUMN)
# ------------------------------------------------

st.sidebar.header("Project Inputs")

c1,c2 = st.sidebar.columns(2)

with c1:
    feeder_from = st.selectbox("From",["Switchgear","Transformer","Generator"])
    voltage = st.selectbox("Voltage (kV)",[3.3,6.6,11,33])
    length = st.number_input("Length (m)",value=300)

with c2:
    feeder_to = st.selectbox("To",["Motor","Transformer","Panel"])
    laying = st.selectbox("Laying",["Direct Buried","Air","Duct"])
    vd_limit = st.number_input("Allowed VD (%)",value=5.0)

# ------------------------------------------------
# LOAD
# ------------------------------------------------

load_type = st.sidebar.selectbox(
    "Load Type",
    ["Motor","Transformer","Generic Load","Power Load"]
)

if load_type=="Transformer":
    power = st.sidebar.number_input("Load (kVA)",value=500)
elif load_type=="Motor":
    power = st.sidebar.number_input("Load (kW)",value=400)
else:
    power = st.sidebar.number_input("Load",value=300)

pf = st.sidebar.number_input("Power Factor",value=0.9)
eff = st.sidebar.number_input("Efficiency",value=0.95)

# ------------------------------------------------
# FAULT
# ------------------------------------------------

fault = st.sidebar.number_input("Fault Level (kA)",value=25)
fault_time = st.sidebar.number_input("Fault Time (s)",value=0.4)

# ------------------------------------------------
# DERATING (MANUAL + DEFAULT)
# ------------------------------------------------

st.sidebar.subheader("Derating")

def input_with_other(label, options, default):
    choice = st.sidebar.selectbox(label, options + ["Other"])
    if choice == "Other":
        return st.sidebar.number_input(f"{label} (Manual)", value=default)
    return float(choice)

soil = input_with_other("Soil Factor",[1.0,1.5,2],1.5)
depth = input_with_other("Depth Factor",[0.8,1.0],1.0)
group = input_with_other("Grouping Factor",[1,0.85,0.79,0.73],1)
temp = input_with_other("Temp Factor",[1,0.85],1)

kT = soil * depth * group * temp

run = st.sidebar.button("Run CableMate Analysis")

# ------------------------------------------------
# CATALOG
# ------------------------------------------------

catalog = {
"sizes":[50,70,95,120,150,185,240,300],
"ampacity":{50:181,70:220,95:263,120:298,150:332,185:374,240:431,300:482},
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

def voltage_drop(I,R,X):
    ang=math.acos(pf)
    return (math.sqrt(3)*I*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*voltage*1000)*100

def start_drop(I,R,X):
    Ist=6*I
    ang=math.acos(0.25)
    return (math.sqrt(3)*Ist*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*voltage*1000)*100

# ------------------------------------------------
# PDF REPORT
# ------------------------------------------------

def report(best,I,S,vd,vd_start):

    f=tempfile.NamedTemporaryFile(delete=False)
    c=canvas.Canvas(f.name,pagesize=A4)

    y=800
    c.drawString(200,y,"CableMate Report")

    y-=40
    c.drawString(50,y,f"Best Cable: 3C x {best} sq.mm")

    y-=20
    c.drawString(50,y,f"Load Current: {round(I,1)} A")

    y-=20
    c.drawString(50,y,f"Voltage Drop: {round(vd,2)} %")

    y-=20
    c.drawString(50,y,f"Starting Drop: {round(vd_start,2)} %")

    y-=20
    c.drawString(50,y,f"Short Circuit Size: {round(S,1)} mm2")

    y-=30
    c.drawString(50,y,"Checks Passed:")
    y-=20
    c.drawString(60,y,"✔ Ampacity OK")
    y-=20
    c.drawString(60,y,"✔ Voltage Drop OK")
    y-=20
    c.drawString(60,y,"✔ Short Circuit OK")
    y-=20
    c.drawString(60,y,"✔ Starting OK")

    c.save()
    return f.name

# ------------------------------------------------
# ENGINE
# ------------------------------------------------

if run:

    I = load_current()
    S = short_circuit()

    best=None

    for size in catalog["sizes"]:

        if size<S:
            continue

        amp=catalog["ampacity"][size]*kT
        if amp<I:
            continue

        vd=voltage_drop(I,catalog["R"][size],catalog["X"][size])
        if vd>vd_limit:
            continue

        vd_start=start_drop(I,catalog["R"][size],catalog["X"][size])
        if vd_start>15:
            continue

        best=size
        break

    if best:

        st.success(f"Best Fit Cable Suggestion: 3C x {best} sq.mm")

        c1,c2,c3 = st.columns(3)
        c1.metric("Load Current (A)", round(I,1))
        c2.metric("Voltage Drop (%)", round(vd,2))
        c3.metric("Starting Drop (%)", round(vd_start,2))

        pdf=report(best,I,S,vd,vd_start)

        with open(pdf,"rb") as f:
            st.download_button("Download Report",f,"CableMate.pdf")

    else:
        st.error("No suitable cable found")
