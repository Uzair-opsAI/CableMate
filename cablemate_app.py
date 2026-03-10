import streamlit as st
import math

st.title("Uzair's CableMate – MV Cable Sizing Tool")

# ------------------------
# User Inputs
# ------------------------

col1, col2 = st.columns(2)

with col1:

    load_current = st.number_input(
        "Load Current (A)",
        min_value=10,
        max_value=1000,
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
        min_value=10,
        max_value=10000,
        value=1200
    )

with col2:

    fault = st.number_input(
        "Fault Level (kA)",
        min_value=5,
        max_value=50,
        value=25
    )

    vd_limit = st.number_input(
        "Voltage Drop Limit (%)",
        min_value=1,
        max_value=10,
        value=6
    )

    voltage_grade = st.selectbox(
        "Cable Voltage Grade (IEC 60502-2)",
        [
            "3.6/6 (7.2) kV",
            "6/10 (12) kV",
            "8.7/15 (17.5) kV",
            "12/20 (24) kV",
            "18/30 (36) kV"
        ]
    )

    core_type = st.selectbox(
        "Cable Core Type",
        ["3 Core", "Single Core"]
    )

# Convert voltage grade to nominal voltage
voltage_map = {
    "3.6/6 (7.2) kV": 6.6,
    "6/10 (12) kV": 11,
    "8.7/15 (17.5) kV": 15,
    "12/20 (24) kV": 22,
    "18/30 (36) kV": 33
}

voltage = voltage_map[voltage_grade]

# ------------------------
# CableMate Functions
# ------------------------

def derated_current(I_nom, derating):

    I = I_nom
    for d in derating:
        I *= d

    return I


def voltage_drop(I, R, X, pf, length):

    angle = math.acos(pf)

    vd = math.sqrt(3) * I * (
        R * math.cos(angle) +
        X * math.sin(angle)
    ) * length / 1000

    return vd


def sc_withstand(Isc_required, Isc_cable, runs):

    # Slightly conservative current sharing
    return Isc_required <= Isc_cable * (runs ** 0.9)


def cablemate_engine(inputs, catalog):

    max_runs = 4
    solutions = []

    for runs in range(1, max_runs + 1):

        for size in catalog["sizes"]:

            # Core restrictions
            if core_type == "3 Core" and size > 240:
                continue

            if core_type == "Single Core" and size > 630:
                continue

            if size not in catalog["current"]:
                continue

            I_nom = catalog["current"][size]
            R = catalog["R"][size]
            X = catalog["X"][size]
            Isc_cable = catalog["sc"][size]

            I_der = derated_current(I_nom, inputs["derating"])
            total_capacity = I_der * runs

            # Current check
            if total_capacity < inputs["load_current"]:
                continue

            # Short circuit check
            if not sc_withstand(inputs["Isc_required"], Isc_cable, runs):
                continue

            # Voltage drop
            vd_volts = voltage_drop(
                inputs["load_current"],
                R / runs,
                X / runs,
                inputs["pf"],
                inputs["length"]
            )

            vd_percent = (vd_volts / (voltage * 1000)) * 100

            if vd_percent > inputs["vd_limit"]:
                continue

            solutions.append({
                "size": size,
                "runs": runs,
                "vd_percent": vd_percent,
                "capacity": total_capacity
            })

    return solutions


# ------------------------
# Cable Catalog (Example Data)
# ------------------------

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

# ------------------------
# Run Calculation
# ------------------------

if st.button("Calculate Cable Size"):

    inputs = {
        "load_current": load_current,
        "pf": pf,
        "length": length,
        "Isc_required": fault,
        "vd_limit": vd_limit,
        "derating": [0.92,0.95]
    }

    solutions = cablemate_engine(inputs, catalog)

    solutions_sorted = sorted(
        solutions,
        key=lambda x: (
            x["size"] * x["runs"],
            x["vd_percent"]
        )
    )

    if solutions_sorted:

        best = solutions_sorted[0]

        st.subheader("Recommended Cable")

        st.success(
            f"{best['runs']} × {best['size']} mm² cable\n"
            f"Voltage Drop: {round(best['vd_percent'],2)} %\n"
            f"Capacity: {round(best['capacity'],1)} A"
        )

        st.subheader("Other Available Options")

        for s in solutions_sorted[1:5]:

            st.info(
                f"{s['runs']} × {s['size']} mm² cable | "
                f"Voltage Drop: {round(s['vd_percent'],2)} % | "
                f"Capacity: {round(s['capacity'],1)} A"
            )

    else:

        st.error("No suitable cable found for the given inputs.")
