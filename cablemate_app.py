import streamlit as st
import math
import pandas as pd
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit.components.v1 as components

# ------------------------------------------------
# CLOSE TAB WARNING
# ------------------------------------------------

components.html("""
<script>
window.onbeforeunload = function() {
return "Are you sure you want to close CableMate?";
};
</script>
""",height=0)

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(page_title="CableMate",layout="wide")

col1,col2 = st.columns([1,6])

with col1:
    st.image("logo.png",width=100)

with col2:
    st.title("CableMate – MV Cable Sizing Tool")

# ------------------------------------------------
# INPUT SECTION
# ------------------------------------------------

st.header("Project Details")

c1,c2 = st.columns(2)

with c1:

    feeder_from = st.selectbox(
        "From Equipment",
        ["Switchgear","Transformer","Generator"]
    )

    feeder_to = st.selectbox(
        "To Equipment",
        ["Motor","Transformer","Panel","Package"]
    )

    voltage = st.selectbox(
        "System Voltage (kV)",
        [3.3,6.6,11,33]
    )

    length = st.number_input(
        "Cable Length (m)",
        value=450
    )

with c2:

    load_type = st.selectbox(
        "Load Type",
        ["Motor","Transformer","Generic Load"]
    )

    power = st.number_input(
        "Power (kW / kVA)",
        value=400
    )

    pf = st.number_input(
        "Power Factor",
        value=0.9
    )

    efficiency = st.number_input(
        "Efficiency",
        value=0.95
    )

# ------------------------------------------------
# FAULT CONDITIONS
# ------------------------------------------------

st.header("Fault Conditions")

f1,f2 = st.columns(2)

with f1:
    fault = st.number_input("Fault Level (kA)",value=40)

with f2:
    fault_time = st.number_input("Fault Duration (sec)",value=0.4)

# ------------------------------------------------
# INSTALLATION CONDITIONS
# ------------------------------------------------

st.header("Installation Conditions")

d1,d2,d3,d4 = st.columns(4)

with d1:
    soil = st.selectbox("Soil Resistivity",[1.0,1.5,2])

with d2:
    depth = st.selectbox("Burial Depth",[0.8,1.0,1.25])

with d3:
    temp = st.selectbox("Ground Temperature",[20,30,40])

with d4:
    group = st.selectbox("Cable Group",[1,2,3,4])

# ------------------------------------------------
# CABLE CATALOG
# ------------------------------------------------

catalog = {

"sizes":[50,70,95,120,150,185,240,300,400],

"ampacity":{
50:181,
70:220,
95:263,
120:298,
150:332,
185:374,
240:431,
300:482,
400:541
},

"R":{
50:0.387,
70:0.268,
95:0.193,
120:0.153,
150:0.124,
185:0.099,
240:0.075,
300:0.060,
400:0.047
},

"X":{
50:0.111,
70:0.106,
95:0.094,
120:0.091,
150:0.089,
185:0.086,
240:0.083,
300:0.082,
400:0.080
}

}

# ------------------------------------------------
# FUNCTIONS
# ------------------------------------------------

def full_load_current():

    if load_type=="Motor":
        return (power*1000)/(math.sqrt(3)*voltage*1000*pf*efficiency)

    elif load_type=="Transformer":
        return (power*1000)/(math.sqrt(3)*voltage*1000)

    else:
        return (power*1000)/(math.sqrt(3)*voltage*1000*pf)

def derating():

    k1 = 1 if soil==1.5 else 0.9
    k2 = 0.98 if depth==1 else 1
    k3 = {1:1,2:0.85,3:0.79,4:0.73}[group]
    k4 = 0.85 if temp==40 else 1

    return k1*k2*k3*k4

def short_circuit():

    K=143
    return (fault*1000*math.sqrt(fault_time))/K

def voltage_drop(I,R,X,runs):

    ang = math.acos(pf)

    vd=(math.sqrt(3)*I*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*runs*voltage*1000)

    return vd*100

def start_drop(R,X,runs):

    Ist=6*full_load_current()
    pf_s=0.25

    ang=math.acos(pf_s)

    vd=(math.sqrt(3)*Ist*(R*math.cos(ang)+X*math.sin(ang))*length)/(1000*runs*voltage*1000)

    return vd*100

# ------------------------------------------------
# PDF REPORT
# ------------------------------------------------

def generate_pdf(result,I,S,kT):

    temp=tempfile.NamedTemporaryFile(delete=False)

    c=canvas.Canvas(temp.name,pagesize=A4)

    y=800

    c.setFont("Helvetica-Bold",16)
    c.drawString(180,y,"CableMate Engineering Report")

    y-=40
    c.setFont("Helvetica",11)

    c.drawString(50,y,f"Feeder: {feeder_from} → {feeder_to}")

    y-=20
    c.drawString(50,y,f"Voltage: {voltage} kV")

    y-=20
    c.drawString(50,y,f"Load Current: {round(I,1)} A")

    core="3C" if result["size"]<=240 else "1C"

    y-=30
    c.drawString(50,y,f"Selected Cable: {result['runs']}R x {core} x {result['size']} sq.mm")

    y-=20
    c.drawString(50,y,f"Ampacity: {round(result['amp'],1)} A")

    y-=20
    c.drawString(50,y,f"Voltage Drop: {round(result['vd'],2)} %")

    c.save()

    return temp.name

# ------------------------------------------------
# CALCULATION ENGINE
# ------------------------------------------------

if st.button("Calculate Cable Size"):

    I = full_load_current()
    kT = derating()
    S = short_circuit()

    solutions=[]

    for runs in range(1,4):

        for size in catalog["sizes"]:

            if size<S:
                continue

            amp=catalog["ampacity"][size]*kT*runs

            if amp<I:
                continue

            R=catalog["R"][size]
            X=catalog["X"][size]

            vd=voltage_drop(I,R,X,runs)

            if vd>5:
                continue

            if load_type=="Motor":

                vd_start=start_drop(R,X,runs)

                if vd_start>15:
                    continue

            else:

                vd_start=0

            solutions.append({
            "size":size,
            "runs":runs,
            "vd":vd,
            "vd_start":vd_start,
            "amp":amp
            })

    if solutions:

        solutions=sorted(solutions,key=lambda x:(x["runs"],x["size"]))

        budget=solutions[0]
        performance=sorted(solutions,key=lambda x:x["vd"])[0]

        st.header("Cable Recommendations")

        results=[budget,performance]

        df=pd.DataFrame(results)

        st.dataframe(df)

        st.header("Design Summary")

        st.write("Load Current:",round(I,1),"A")
        st.write("Derating Factor:",round(kT,2))
        st.write("Minimum Short Circuit Size:",round(S,1),"mm²")

        pdf_path=generate_pdf(budget,I,S,kT)

        with open(pdf_path,"rb") as f:

            st.download_button(
                "Download Engineering Report",
                f,
                file_name="CableMate_Report.pdf"
            )

    else:

        st.error("No suitable cable found")
