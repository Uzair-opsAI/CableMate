
import streamlit as st
import math
import os
import streamlit.components.v1 as components

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="CableMate", layout="wide")

c1,c2 = st.columns([1,6])
with c1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
with c2:
    st.title("CableMate – MV Cable Sizing Tool (IEC Standards)")
    st.caption("Standards: IEC 60364 | Oman Cable Catalogue")

# ------------------------------------------------
# INPUTS
# ------------------------------------------------
st.subheader("📁 Project Information")
col1, col2 = st.columns(2)

with col1:
    voltage = st.selectbox("System Voltage (kV)", [3.3,6.6,11,25,33])
    length = st.number_input("Cable Length (m)", value=500)

with col2:
    load_type = st.selectbox("Load Type", ["Motor","Transformer","Power"])

st.subheader("⚡ Load Details")

col1, col2 = st.columns(2)

with col1:
    if load_type == "Transformer":
        power = st.number_input("Load (kVA)", value=400)
    else:
        power = st.number_input("Load (kW)", value=1000)

with col2:
    pf = st.number_input("Power Factor", value=0.9)
    eff = st.number_input("Efficiency", value=0.97)

st.subheader("🛠 Installation")

col1, col2 = st.columns(2)

with col1:
    laying = st.selectbox("Laying Method", ["Direct Buried","Duct","Tray"])

with col2:
    material = st.selectbox("Material", ["Copper","Aluminium"])

st.subheader("🌡 Derating")

col1, col2 = st.columns(2)

with col1:
    group = st.number_input("Grouping", value=0.85)
    soil = st.number_input("Soil", value=0.9)

with col2:
    temp = st.number_input("Temperature", value=0.9)
    depth = st.number_input("Depth", value=1.0)

k_total = group * soil * temp * depth
st.success(f"Total Derating = {round(k_total,3)}")

st.subheader("⚠ Fault Data")

col1, col2 = st.columns(2)

with col1:
    fault = st.number_input("Fault Level (kA)", value=25)

with col2:
    fault_time = st.number_input("Fault Time (s)", value=1.0)

st.subheader("📉 Voltage Drop Limits")

col1, col2 = st.columns(2)

with col1:
    vd_run_limit = st.number_input("Running VD %", value=5.0)

with col2:
    vd_start_limit = st.number_input("Starting VD %", value=20.0)

# ------------------------------------------------
# CATALOG (UPDATED 90°C VALUES)
# ------------------------------------------------
catalog = {
    "sizes":[50,70,95,120,150,185,240,300,400],
    "R":{50:0.387,70:0.268,95:0.193,120:0.153,150:0.124,185:0.129,240:0.098,300:0.080,400:0.060},
    "X":{50:0.111,70:0.106,95:0.094,120:0.091,150:0.089,185:0.086,240:0.083,300:0.082,400:0.080},
    "amp":{
        50:170,70:205,95:245,120:280,150:315,
        185:355,240:410,300:460,400:520
    }
}

# ------------------------------------------------
# FUNCTIONS
# ------------------------------------------------
def load_current():
    if load_type == "Transformer":
        return power*1000/(math.sqrt(3)*voltage*1000)
    else:
        return power*1000/(math.sqrt(3)*voltage*1000*pf*eff)

def short_circuit():
    k = 226 if material == "Copper" else 148
    return (fault*1000*math.sqrt(fault_time))/k

def voltage_drop(I,R,X,runs):
    cos_phi = pf
    sin_phi = math.sqrt(1-pf**2)
    return (math.sqrt(3)*I*(R*cos_phi+X*sin_phi)*length)/(1000*runs*voltage*1000)*100

def voltage_drop_start(I,R,X,runs):
    Ist = 6*I
    cos_phi = 0.2
    sin_phi = math.sqrt(1-cos_phi**2)
    return (math.sqrt(3)*Ist*(R*cos_phi+X*sin_phi)*length)/(1000*runs*voltage*1000)*100

def get_equivalent_size(area):
    for s in catalog["sizes"]:
        if s >= area:
            return s
    return max(catalog["sizes"])

# ------------------------------------------------
# RUN
# ------------------------------------------------
if st.button("🚀 Run Cable Sizing"):

    I = load_current()
    S = short_circuit()

    st.info(f"Load Current = {round(I,2)} A")
    st.info(f"Required SC Area = {round(S,2)} mm²")

    valid = []

    for runs in range(1,4):
        for size in catalog["sizes"]:

            amp = catalog["amp"][size]*k_total*runs
            if amp < I:
                continue

            equiv = get_equivalent_size(size*runs)
            if equiv < S:
                continue

            vd = voltage_drop(I,catalog["R"][size],catalog["X"][size],runs)
            if vd > vd_run_limit:
                continue

            vd_s = voltage_drop_start(I,catalog["R"][size],catalog["X"][size],runs)
            if load_type=="Motor" and vd_s > vd_start_limit:
                continue

            valid.append({
                "size":size,
                "runs":runs,
                "vd":vd,
                "amp":amp
            })

    if valid:
        valid.sort(key=lambda x:(x["runs"],x["size"],x["vd"]))
        best = valid[0]

        st.success(f"✅ Selected Cable → {best['runs']}R x 3C x {best['size']} sq.mm")

        st.metric("Load Current", round(I,2))
        st.metric("Voltage Drop", round(best["vd"],3))
        st.metric("Ampacity", round(best["amp"],1))

    else:
        st.error("❌ No suitable cable found")
```
