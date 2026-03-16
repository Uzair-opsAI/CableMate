import streamlit as st
import math

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(page_title="Uzair CableMate", layout="wide")

col1,col2 = st.columns([1,6])

with col1:
    st.image("logo.png", width=110)

with col2:
    st.title("Uzair CableMate – MV Cable Sizing Tool")

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.header("Project Inputs")

col1,col2 = st.columns(2)

with col1:

    feeder_from = st.selectbox(
        "From Equipment",
        ["Switchgear","Transformer","Generator"]
    )

    feeder_to = st.selectbox(
        "To Equipment",
        ["Motor","Transformer","Package","Panel"]
    )

    voltage = st.selectbox(
        "System Voltage (kV)",
        [3.3,6.6,11,33]
    )

    cable_length = st.number_input(
        "Cable Length (m)",
        min_value=1,
        value=450
    )

with col2:

    power = st.number_input(
        "Motor Power (kW) / Transformer kVA",
        value=400
    )

    power_factor = st.number_input(
        "Power Factor",
        value=0.9
    )

    efficiency = st.number_input(
        "Efficiency",
        value=0.95
    )

# --------------------------------------------------
# FAULT DATA
# --------------------------------------------------

st.header("Fault Data")

col3,col4 = st.columns(2)

with col3:

    fault_level = st.number_input(
        "Fault Level (kA)",
        value=40
    )

with col4:

    fault_time = st.number_input(
        "Fault Clearing Time (sec)",
        value=0.4
    )

# --------------------------------------------------
# INSTALLATION CONDITIONS
# --------------------------------------------------

st.header("Installation Conditions")

col5,col6,col7,col8 = st.columns(4)

with col5:

    soil_resistivity = st.selectbox(
        "Soil Resistivity (°C.m/W)",
        [1.0,1.5,2.0]
    )

with col6:

    burial_depth = st.selectbox(
        "Burial Depth (m)",
        [0.8,1.0,1.25]
    )

with col7:

    ground_temp = st.selectbox(
        "Ground Temperature (°C)",
        [20,30,40]
    )

with col8:

    cable_group = st.selectbox(
        "Number of Cables in Group",
        [1,2,3,4]
    )

# --------------------------------------------------
# CABLE DATA (Simplified Oman Catalogue)
# --------------------------------------------------

catalog = {

"sizes":[50,70,95,120,150,185,240,300,400],

"R":{

50:0.387,
70:0.268,
95:0.193,
120:0.153,
150:0.124,
185:0.0991,
240:0.0754,
300:0.0601,
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

},

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

}

}

# --------------------------------------------------
# DERATING FACTOR
# --------------------------------------------------

def derating_factor():

    if soil_resistivity == 1.5:
        k1 = 1
    else:
        k1 = 0.9

    if burial_depth == 1.0:
        k2 = 0.98
    else:
        k2 = 1

    if cable_group == 4:
        k3 = 0.73
    elif cable_group == 3:
        k3 = 0.79
    else:
        k3 = 1

    if ground_temp == 40:
        k4 = 0.85
    else:
        k4 = 1

    return k1 * k2 * k3 * k4

# --------------------------------------------------
# FULL LOAD CURRENT
# --------------------------------------------------

def full_load_current():

    if feeder_to == "Motor":

        I = (power*1000) / (
            math.sqrt(3) *
            voltage*1000 *
            power_factor *
            efficiency
        )

    else:

        I = (power*1000) / (
            math.sqrt(3) *
            voltage*1000
        )

    return I

# --------------------------------------------------
# RUNNING VOLTAGE DROP
# --------------------------------------------------

def running_voltage_drop(I,R,X,runs):

    angle = math.acos(power_factor)

    vd = (
        math.sqrt(3)*I*
        (R*math.cos(angle)+X*math.sin(angle))*
        cable_length
    )/(1000*runs*voltage*1000)

    return vd*100

# --------------------------------------------------
# STARTING VOLTAGE DROP
# --------------------------------------------------

def starting_voltage_drop(R,X,runs):

    Ist = 6 * full_load_current()

    pf_start = 0.25

    angle = math.acos(pf_start)

    vd = (
        math.sqrt(3)*Ist*
        (R*math.cos(angle)+X*math.sin(angle))*
        cable_length
    )/(1000*runs*voltage*1000)

    return vd*100

# --------------------------------------------------
# SHORT CIRCUIT SIZE
# --------------------------------------------------

def short_circuit_size():

    K = 143

    S = (fault_level*1000*math.sqrt(fault_time))/K

    return S*0.95

# --------------------------------------------------
# CALCULATION ENGINE
# --------------------------------------------------

if st.button("Calculate Cable Size"):

    I_load = full_load_current()

    kT = derating_factor()

    S_sc = short_circuit_size()

    solutions=[]

    for runs in range(1,4):

        for size in catalog["sizes"]:

            amp = catalog["ampacity"][size]*kT*runs

            if amp < I_load:
                continue

            if size < S_sc:
                continue

            R=catalog["R"][size]
            X=catalog["X"][size]

            vd = running_voltage_drop(I_load,R,X,runs)

            if vd > 5:
                continue

            if feeder_to=="Motor":

                vd_start=starting_voltage_drop(R,X,runs)

                if vd_start>15:
                    continue

            else:

                vd_start=0

            solutions.append({

                "size":size,
                "runs":runs,
                "vd":vd,
                "vd_start":vd_start,
                "ampacity":amp

            })

    # --------------------------------------------------

    if solutions:

        solutions=sorted(
            solutions,
            key=lambda x:(x["runs"],x["size"])
        )

        best=solutions[0]

        if best["size"]<=240:
            cores="3C"
        else:
            cores="1C"

        st.success("Recommended Cable")

        st.write(
            f"{best['runs']}R x {cores} x {best['size']} sq.mm "
            "(CU/XLPE/SWA/PVC)"
        )

        st.write(
            "Derated Ampacity:",
            round(best["ampacity"],1),
            "A"
        )

        st.write(
            "Running Voltage Drop:",
            round(best["vd"],3),
            "%"
        )

        if feeder_to=="Motor":

            st.write(
                "Starting Voltage Drop:",
                round(best["vd_start"],3),
                "%"
            )

        st.write(
            "Minimum SC Cable Size:",
            round(S_sc,1),
            "sq.mm"
        )

        st.subheader("Alternative Cable Options")

        for s in solutions[1:4]:

            if s["size"]<=240:
                cores="3C"
            else:
                cores="1C"

            st.write(
                f"{s['runs']}R x {cores} x {s['size']} sq.mm "
                f"| VD {round(s['vd'],2)} % "
                f"| Capacity {round(s['ampacity'],1)} A"
            )

    else:

        st.error("No suitable cable found for the given inputs")
