import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import datetime

# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Uzair's CableMate",
    page_icon="logo.png",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

col_logo, col_title = st.columns([1,6])

with col_logo:
    st.image("logo.png", width=110)

with col_title:
    st.title("Uzair's CableMate – MV Cable Sizing Tool")
    st.caption("Engineering Cable Sizing Utility | IEC 60502")

st.markdown("---")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.image("logo.png", width=150)
st.sidebar.title("CableMate")
st.sidebar.write("MV Cable Engineering Utility")
st.sidebar.markdown("---")

# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.header("Project Information")

colA, colB = st.columns(2)

with colA:
    project = st.text_input("Project Name")
    engineer = st.text_input("Engineer")

with colB:
    location = st.text_input("Location")
    date = datetime.date.today()

# --------------------------------------------------
# ELECTRICAL PARAMETERS
# --------------------------------------------------

st.header("Electrical Parameters")

col1, col2 = st.columns(2)

with col1:

    load_current = st.number_input(
        "Load Current (A)",
        min_value=10,
        max_value=2000,
        value=240
    )

    pf = st.number_input(
        "Power Factor",
        min_value=0.7,
        max_value=1.0,
        value=0.85
    )

    length = st.number_input(
        "Cable Length (m)",
        min_value=1,
        max_value=20000,
        value=1200
    )

with col2:

    fault = st.number_input(
        "Fault Level (kA)",
        min_value=5,
        max_value=63,
        value=25
    )

    voltage_grade = st.selectbox(
        "Voltage Grade",
        ["6/10 (12) kV","18/30 (36) kV"]
    )

    core_type = st.selectbox(
        "Cable Core Type",
        ["1 Core","2 Core","2.5 Core","3 Core","3.5 Core","4 Core","5 Core"]
    )

# --------------------------------------------------
# INSTALLATION CONDITIONS
# --------------------------------------------------

st.header("Installation Conditions")

installation = st.selectbox(
    "Installation Method",
    ["Direct Buried","Cable Tray","Air","Underground Duct","Tunnel"]
)

vd_limit = st.number_input(
    "Voltage Drop Limit (%)",
    min_value=1,
    max_value=10,
    value=6
)

# --------------------------------------------------
# DERATING FACTORS
# --------------------------------------------------

st.header("Project Specific Derating Factors")

derating = []

col5, col6, col7 = st.columns(3)

with col5:

    if st.checkbox("Ambient Temperature"):
        ambient = st.number_input("Ambient Factor",0.5,1.2,0.9)
        derating.append(ambient)

    if st.checkbox("Cable Grouping"):
        grouping = st.number_input("Grouping Factor",0.5,1.2,0.95)
        derating.append(grouping)

with col6:

    if st.checkbox("Soil Thermal Resistivity"):
        soil = st.number_input("Soil Factor",0.5,1.2,1.0)
        derating.append(soil)

    if st.checkbox("Depth of Laying"):
        depth = st.number_input("Depth Factor",0.5,1.2,1.0)
        derating.append(depth)

with col7:

    if st.checkbox("Installation Factor"):

        inst_map = {
        "Direct Buried":0.9,
        "Cable Tray":0.95,
        "Air":1.0,
        "Underground Duct":0.85,
        "Tunnel":0.9
        }

        inst_factor = inst_map[installation]

        st.write("Installation Factor =",inst_factor)

        derating.append(inst_factor)

    if st.checkbox("Manual Factors"):

        manual = st.text_input("Manual factors (comma separated)","1")

        try:
            extra = [float(x.strip()) for x in manual.split(",")]
            derating.extend(extra)
        except:
            st.warning("Check manual factor format")

if len(derating)==0:
    derating=[1.0]

# --------------------------------------------------
# VOLTAGE MAP
# --------------------------------------------------

voltage_map = {
"6/10 (12) kV":11,
"18/30 (36) kV":33
}

voltage = voltage_map[voltage_grade]

# --------------------------------------------------
# CATALOG DATA
# --------------------------------------------------

catalog = {

"sizes":[95,120,150,185,240,300,400,500,630],

"R":{
95:0.193,
120:0.153,
150:0.124,
185:0.099,
240:0.075,
300:0.060,
400:0.047,
500:0.036,
630:0.029
},

"X":{
95:0.106,
120:0.103,
150:0.100,
185:0.097,
240:0.094,
300:0.090,
400:0.087,
500:0.084,
630:0.082
},

"current":{
95:210,
120:240,
150:260,
185:290,
240:320,
300:360,
400:455,
500:520,
630:590
},

"sc":{
95:8.4,
120:10.1,
150:12.3,
185:14.5,
240:18,
300:20.2,
400:22,
500:28,
630:32
}

}

# --------------------------------------------------
# ENGINE FUNCTIONS
# --------------------------------------------------

def derated_current(I_nom,derating):

    I = I_nom

    for d in derating:
        I*=d

    return I


def voltage_drop(I,R,X,pf,length):

    angle = math.acos(pf)

    vd = math.sqrt(3)*I*(R*math.cos(angle)+X*math.sin(angle))*length/1000

    return vd


def sc_withstand(Isc,Isc_cable,runs):

    return Isc <= Isc_cable*(runs**0.9)

# --------------------------------------------------
# CABLE ENGINE
# --------------------------------------------------

def cable_engine():

    solutions=[]

    for runs in range(1,5):

        for size in catalog["sizes"]:

            if core_type=="3 Core" and size>240:
                continue

            I_nom = catalog["current"][size]

            R = catalog["R"][size]

            X = catalog["X"][size]

            Isc_cable = catalog["sc"][size]

            I_der = derated_current(I_nom,derating)

            capacity = I_der*runs

            if capacity < load_current:
                continue

            if not sc_withstand(fault,Isc_cable,runs):
                continue

            vd_volts = voltage_drop(
                load_current,
                R/runs,
                X/runs,
                pf,
                length
            )

            vd_percent = (vd_volts/(voltage*1000))*100

            if vd_percent > vd_limit:
                continue

            solutions.append({
                "Runs":runs,
                "Size mm2":size,
                "Capacity A":round(capacity,1),
                "Voltage Drop %":round(vd_percent,2)
            })

    return solutions

# --------------------------------------------------
# RUN CALCULATION
# --------------------------------------------------

if st.button("Calculate Cable Size"):

    solutions = cable_engine()

    if solutions:

        df = pd.DataFrame(solutions)

        df["Copper"] = df["Runs"] * df["Size mm2"]

        df = df.sort_values(["Copper","Voltage Drop %"])

        best = df.iloc[0]

        st.header("Recommended Cable")

        st.success(
        f"{best['Runs']} × {best['Size mm2']} mm² cable\n"
        f"Voltage Drop: {best['Voltage Drop %']} %"
        )

        st.header("Cable Comparison")

        st.dataframe(df)

        st.header("Voltage Drop Graph")

        fig,ax = plt.subplots()

        ax.plot(df["Size mm2"],df["Voltage Drop %"])

        ax.set_xlabel("Cable Size (mm²)")
        ax.set_ylabel("Voltage Drop (%)")

        st.pyplot(fig)

        report_lines=[
        f"Project: {project}",
        f"Engineer: {engineer}",
        f"Location: {location}",
        f"Voltage Grade: {voltage_grade}",
        f"Core Type: {core_type}",
        f"Installation: {installation}",
        f"Load Current: {load_current} A",
        f"Fault Level: {fault} kA",
        f"Recommended Cable: {best['Runs']} x {best['Size mm2']} mm2",
        f"Voltage Drop: {best['Voltage Drop %']} %",
        ]

        tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".pdf")

        c=canvas.Canvas(tmp.name,pagesize=A4)

        y=800

        for line in report_lines:
            c.drawString(50,y,line)
            y-=20

        c.save()

        with open(tmp.name,"rb") as f:

            st.download_button(
            "Download Engineering Report",
            f,
            "CableMate_Report.pdf"
            )

    else:

        st.error("No suitable cable found")
