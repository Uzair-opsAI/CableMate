import streamlit as st
import math

st.title("CableMate – MV Cable Sizing Tool")

# ------------------------
# User Inputs
# ------------------------

load_current = st.number_input("Load Current (A)", value=240)
pf = st.number_input("Power Factor", value=0.85)
length = st.number_input("Cable Length (m)", value=1200)
fault = st.number_input("Fault Level (kA)", value=25)
vd_limit = st.number_input("Voltage Drop Limit (%)", value=6)

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
    vd = math.sqrt(3) * I * (R * math.cos(angle) + X * math.sin(angle)) * length / 1000
    return vd


def sc_withstand(Isc_required, Isc_cable, runs):
    return Isc_required <= Isc_cable * runs


def cablemate_engine(inputs, catalog):

    max_runs = 4
    solutions = []

    for runs in range(1, max_runs + 1):

        for size in catalog["sizes"]:

            if size not in catalog["current"]:
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

            vd_percent = (vd_volts / 11000) * 100

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
# Cable Catalog
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

    st.subheader("Cable Options")

    for s in solutions[:5]:

        st.write(
        f"{s['runs']} × {s['size']} sqmm cable | "
        f"Voltage Drop: {round(s['vd_percent'],2)} % | "
        f"Capacity: {round(s['capacity'],1)} A"
        )
