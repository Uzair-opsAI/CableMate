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
.stApp {background-color:#f8fafc;}
section[data-testid="stSidebar"] {background-color:#0f172a;}
section[data-testid="stSidebar"] * {color:#e5e7eb !important;}
h1,h2,h3 {color:#111827;}
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

st.divider()

# ------------------------------------------------
# SIDEBAR INPUTS
# ------------------------------------------------

st.sidebar.header("Inputs")

voltage = st.sidebar.selectbox("Voltage (kV)",[3.3,6.6,11,33])
length = st.sidebar.number_input("Length (m)",value=300)

load_type = st.sidebar.selectbox(
    "Load Type",
    ["Motor","Transformer","Power"]
)

if load_type=="Transformer":
    power = st.sidebar.number_input("Load (kVA)",value=500)
else:
    power = st.sidebar.number_input("Load (kW)",value=400)

pf = st.sidebar.number_input("Power Factor",value=0.9)
eff = st.sidebar.number_input("Efficiency",value=0.95)

fault = st.sidebar.number_input("Fault Level (kA)",value=25)
fault_time = st.sidebar.number_input("Fault Time (s)",value=0.4)

vd_run_limit = st.sidebar.number_input("Allowed VD Running (%)",value=5.0)
vd_start_limit = st.sidebar.number_input("Allowed VD Starting (%)",value=15.0)

run = st.sidebar.button("Run CableMate")

# ------------------------------------------------
# CATALOG
# ------------------------------------------------

catalog = {
"sizes":[50,70,95,120,150,185,240],
"amp":{50:181,70:220,95:263,120:298,150:332,185:374,240:431},
"R":{50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.099,240:0.075},
"X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083}
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
# PDF
# ------------------------------------------------

def report(best,I,S,vd_run,vd_st):

    f=tempfile.NamedTemporaryFile(delete=False)
    c=canvas.Canvas(f.name,pagesize=A4)

    y=800
    c.drawString(180,y,"CableMate Engineering Report")

    y-=40
    c.drawString(50,y,f"Selected Cable = {best['runs']}R x 3C x {best['size']} sq.mm")

    y-=30
    c.drawString(50,y,"SHORT CIRCUIT CHECK")
    y-=20
    c.drawString(50,y,f"Required S = {round(S,1)} mm²")
    y-=15
    c.drawString(50,y,f"Selected Size = {best['size']} mm²")
    y-=15
    c.drawString(50,y,f"{round(S,1)} < {best['size']} → Next standard size selected ✔")

    y-=30
    c.drawString(50,y,"RUNNING VOLTAGE DROP")
    y-=20
    c.drawString(50,y,f"VD = {round(vd_run,2)} % ≤ {vd_run_limit} % ✔")

    y-=30
    c.drawString(50,y,"STARTING VOLTAGE DROP")
    y-=20
    c.drawString(50,y,f"VD(start) = {round(vd_st,2)} % ≤ {vd_start_limit} % ✔")

    y-=30
    c.drawString(50,y,"ENGINEERING JUSTIFICATION")
    y-=20
    c.drawString(50,y,"Cable satisfies ampacity, voltage drop,")
    y-=15
    c.drawString(50,y,"short circuit and starting conditions.")

    c.save()
    return f.name

# ------------------------------------------------
# ENGINE
# ------------------------------------------------

if run:

    I=load_current()
    S=short_circuit()

    best=None

    for runs in range(1,4):
        for size in catalog["sizes"]:

            if size<S:
                continue

            if catalog["amp"][size]*runs<I:
                continue

            v=vd(I,catalog["R"][size],catalog["X"][size],runs)
            if v>vd_run_limit:
                continue

            vs=vd_start(I,catalog["R"][size],catalog["X"][size],runs)
            if vs>vd_start_limit:
                continue

            best={"size":size,"runs":runs}
            break

        if best:
            break

    if best:

        st.success(f"Best Fit Cable: {best['runs']}R x 3C x {best['size']} sq.mm")

        c1,c2,c3 = st.columns(3)
        c1.metric("Load Current",round(I,1))
        c2.metric("VD Running %",round(v,2))
        c3.metric("VD Starting %",round(vs,2))

        pdf=report(best,I,S,v,vs)

        with open(pdf,"rb") as f:
            st.download_button("Download Report",f,"CableMate_Report.pdf")

    else:
        st.error("No suitable cable found")
