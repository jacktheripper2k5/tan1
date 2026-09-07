import streamlit as st

st.set_page_config(
    page_title="Oxygen Enrichment",
    page_icon="🟡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #101114;
    color: #f5f5f5;
}
[data-testid="stHeader"] {
    background-color: #101114;
}
.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
}
h1, h2, h3 {
    color: #ffd21f !important;
}
.subtitle {
    color: #b9b9b9;
    font-size: 1.05rem;
}
.card {
    background: #191b20;
    border: 1px solid #3b3d43;
    border-radius: 16px;
    padding: 24px;
}
.yellow-card {
    background: #26230d;
    border: 1px solid #8f7b00;
    border-radius: 16px;
    padding: 22px;
}
.big-number {
    color: #ffd21f;
    font-size: 2rem;
    font-weight: 800;
}
.label {
    color: #aaa;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.stButton > button {
    background: #ffd21f;
    color: #111;
    border: none;
    border-radius: 9px;
    font-weight: 800;
}
.stButton > button:hover {
    background: #ffe45e;
    color: #111;
}
div[data-testid="stMetric"] {
    background: #191b20;
    border: 1px solid #3b3d43;
    padding: 15px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] {
    color: #ffd21f;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <div class="label">PROCESS CALCULATOR</div>
    <h1>🟡 Oxygen Enrichment</h1>
    <div class="subtitle">
        Calculate the pure oxygen required to enrich a dry-air blast.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

input_col, preview_col = st.columns([1, 1])

with input_col:
    st.markdown('<div class="yellow-card">', unsafe_allow_html=True)
    st.subheader("Set target")

    target_pct = st.slider(
        "Final O₂ concentration",
        min_value=21.1,
        max_value=50.0,
        value=25.0,
        step=0.1
    )

    st.markdown(
        f'<div class="big-number">{target_pct:.1f}% O₂</div>',
        unsafe_allow_html=True
    )

    calculate = st.button(
        "RUN CALCULATION",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with preview_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Starting gas")

    a, b = st.columns(2)
    a.metric("Dry air", "1000 Nm³")
    b.metric("Air O₂", "21 vol.%")

    st.markdown(
        "Initial oxygen available: **210 Nm³**"
    )
    st.caption("The added gas is treated as pure O₂.")
    st.markdown('</div>', unsafe_allow_html=True)

if calculate:
    air = 1000.0
    air_o2 = 0.21
    target = target_pct / 100.0

    initial_o2 = air * air_o2

    # Oxygen balance:
    # (initial O2 + added O2) / (initial air + added O2) = target
    added_volume = (air * target - initial_o2) / (1 - target)
    added_mass = added_volume / 22.414 * 32.0

    final_volume = air + added_volume
    checked = (initial_o2 + added_volume) / final_volume * 100

    st.write("")
    st.subheader("Results")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Pure oxygen volume</div>
                <div class="big-number">{added_volume:.2f} Nm³</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">Pure oxygen mass</div>
                <div class="big-number">{added_mass:.2f} kg</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.subheader("Verification")

    v1, v2, v3 = st.columns(3)
    v1.metric("Initial O₂", f"{initial_o2:.2f} Nm³")
    v2.metric("Final gas volume", f"{final_volume:.2f} Nm³")
    v3.metric("Verified O₂", f"{checked:.2f}%")

    with st.expander("Show calculation"):
        st.markdown("#### Oxygen balance")
        st.latex(r"\frac{210+x}{1000+x}=y")

        st.markdown("#### Added oxygen")
        st.latex(r"x=\frac{1000y-210}{1-y}")

        st.code(
            f"y = {target:.4f}\n"
            f"x = (1000 × {target:.4f} − 210) / (1 − {target:.4f})\n"
            f"x = {added_volume:.2f} Nm³"
        )

        st.markdown("#### Oxygen mass")
        st.latex(r"m=\frac{V}{22.414}\times32")

        st.code(
            f"m = ({added_volume:.2f} / 22.414) × 32\n"
            f"m = {added_mass:.2f} kg"
        )

    st.success(
        f"Result: add {added_volume:.2f} Nm³ of pure O₂ "
        f"({added_mass:.2f} kg)."
    )

with st.expander("Assumptions"):
    st.write(
        "Dry air = 21 vol.% O₂. Added gas = pure O₂. "
        "For volume-to-mass conversion, 22.414 Nm³/kmol and "
        "32 kg/kmol are used."
    )
