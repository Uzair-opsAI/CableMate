import streamlit as st
import math

st.title("Uzair's CableMate – MV Cable Sizing Tool")

# -----------------------------
# INPUT SECTION
# -----------------------------

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

    fault = st.number_input(
        "Fault Level (kA)",
        min_value=5,
        max_value=63,
        value=25
    )

with col2:

    vd_limit = st.number_input(
        "Voltage Drop Limit (%)",
        min_value=1,
        max_value=10,
        value=6
    )

    voltage_grade = st.selectbox(
        "Voltage Grade (IEC 60502-2)",
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
        [
            "1 Core",
            "2 Core",
            "3 Core",
            "3.5 Core",
            "4 Core",
            "5 Core"
        ]
    )

    installation = st.selectbox(
        "Installation Method",
        [
            "Direct Buried",
            "Cable Tray",
            "Air",
            "Underground Duct",
            "Tunnel"
        ]
    )

# -----------------------------
# VOLTAGE MAPPING
# -----------------------------

voltage_map = {
    "3.6/6 (7.2) kV": 6.6,
    "6/10 (12) kV": 11,
    "8.7/15 (17.5) kV": 15,
    "12/20 (24) kV": 22,
    "18/30 (36) kV": 33
}

voltage = voltage_map[voltage_grade]

# -----------------------------
# DERATING FACTORS
# -----------------------------

ambient_factor = st.slider(
    "Ambient Temperature Derating",
    0.7,
    1.0,
    0.9
)

grouping_factor = st.slider(
    "Cable Grouping Derating",
    0.5,
    1.0,
    0.95
)

installation_factor_map = {
    "Direct Buried": 0.9,
    "Cable Tray": 0.95,
    "Air": 1.0,
    "Underground Duct": 0.85,
    "Tunnel": 0.9
}

installation_factor = installation_factor_map[installation]

derating_factors = [
    ambient_factor,
    grouping_factor,
    installation_factor
]

# -----------------------------
# CATALOG TABLES
# -----------------------------

catalog_tables = {

"6/10 (12) kV":{

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

},

"18/30 (36) kV":{

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
95:0.129,
120:0.124,
150:0.120,
185:0.116,
240:0.112,
300:0.108,
400:0.105,
500:0.102,
630:0.100
},

"current":{
95:190,
120:220,
150:240,
185:270,
240:300,
300:340,
400:420,
500:480,
630:540
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

}

# automatically choose catalog table
catalog = catalog_tables.get(voltage_grade, catalog_tables["6/10 (12) kV"])

# -----------------------------
# ENGINEERING FUNCTIONS
# -----------------------------

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

    return Isc_required <= Isc_cable * (runs ** 0.9)


def cablemate_engine(inputs, catalog):

    max_runs = 4
    solutions = []

    for runs in range(1, max_runs + 1):

        for size in catalog["sizes"]:

            if core_type == "3 Core" and size > 240:
                continue

            if core_type == "1 Core" and size > 1000:
                continue

            I_nom = catalog["current"][size]
            R = catalog["R"][size]
            X = catalog["X"][size]
            Isc_cable = catalog["sc"][size]

            I_der = derated_current(I_nom, inputs["derating"])
            total_capacity = I_der * runs

            if total_capacity < inputs["load_current"]:
                continue

            if not sc_withstand(inputs["Isc_required"], Isc_cable, runs):
                continue

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


# -----------------------------
# RUN CALCULATION
# -----------------------------

if st.button("Calculate Cable Size"):

    inputs = {
        "load_current": load_current,
        "pf": pf,
        "length": length,
        "Isc_required": fault,
        "vd_limit": vd_limit,
        "derating": derating_factors
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

        st.subheader("Alternative Options")

        for s in solutions_sorted[1:5]:

            st.info(
                f"{s['runs']} × {s['size']} mm² cable | "
                f"Voltage Drop: {round(s['vd_percent'],2)} % | "
                f"Capacity: {round(s['capacity'],1)} A"
            )

        st.subheader("Design Summary")

        st.write(f"Voltage Grade : {voltage_grade}")
        st.write(f"Core Type : {core_type}")
        st.write(f"Installation : {installation}")
        st.write(f"Load Current : {load_current} A")
        st.write(f"Cable Length : {length} m")
        st.write(f"Fault Level : {fault} kA")

    else:

        st.error("No suitable cable found for the given inputs.")
