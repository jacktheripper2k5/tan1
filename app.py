import streamlit as st

st.set_page_config(
    page_title="Oxygen Enrichment Calculator",
    page_icon="🟡",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #fffef2; }
.block-container { max-width: 1100px; padding-top: 2rem; }
.hero {
    background: linear-gradient(135deg, #ffd92f, #ffe873);
    padding: 30px;
    border-radius: 20px;
    border: 2px solid #d6ad00;
    margin-bottom: 24px;
}
.hero h1 { color: #352b00; margin: 0; }
.hero p { color: #5d4d00; margin: 7px 0 0; }
.box {
    background: #fff8c7;
    border: 1px solid #e5cc55;
    border-radius: 16px;
    padding: 22px;
}
.output {
    background: #fff1a8;
    border: 2px solid #e0b900;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}
.output h2 { color: #463900; margin: 4px 0 0; }
div.stButton > button {
    background: #f0c400;
    color: #302600;
    border: 1px solid #b99800;
    font-weight: 800;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🟡 Oxygen Enrichment Calculator</h1>
    <p>Blast Furnace Process Calculation</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.6])

with left:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("Input")
    target_pct = st.number_input(
        "Desired oxygen concentration",
        min_value=21.01,
        max_value=99.0,
        value=25.0,
        step=0.5,
        format="%.2f"
    )
    st.caption("Unit: volume percent O₂")
    calculate = st.button("Calculate", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.subheader("Initial conditions")
    a, b = st.columns(2)
    a.metric("Dry air", "1000 Nm³")
    b.metric("O₂ in air", "21%")
    st.write("Initial oxygen quantity: **210 Nm³**")
    st.markdown('</div>', unsafe_allow_html=True)

if calculate:
    air_volume = 1000.0
    air_o2_fraction = 0.21
    desired_fraction = target_pct / 100.0

    initial_o2 = air_volume * air_o2_fraction

    # Oxygen balance:
    # (initial O2 + added O2) / (initial air + added O2)
    # = desired oxygen fraction
    added_o2 = (
        air_volume * desired_fraction - initial_o2
    ) / (1.0 - desired_fraction)

    added_mass = added_o2 / 22.414 * 32.0

    final_volume = air_volume + added_o2
    verified_pct = (
        (initial_o2 + added_o2) / final_volume
    ) * 100.0

    st.write("")
    st.subheader("Calculated output")

    x, y = st.columns(2)

    with x:
        st.markdown(
            f'<div class="output"><div>O₂ VOLUME TO ADD</div>'
            f'<h2>{added_o2:.2f} Nm³</h2></div>',
            unsafe_allow_html=True
        )

    with y:
        st.markdown(
            f'<div class="output"><div>O₂ MASS TO ADD</div>'
            f'<h2>{added_mass:.2f} kg</h2></div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.subheader("Process check")

    p1, p2, p3 = st.columns(3)
    p1.metric("Initial O₂", f"{initial_o2:.2f} Nm³")
    p2.metric("Final gas volume", f"{final_volume:.2f} Nm³")
    p3.metric("Verified concentration", f"{verified_pct:.2f}%")

    with st.expander("Calculation details"):
        st.markdown("**Oxygen balance**")
        st.latex(r"\frac{210+x}{1000+x}=y")

        st.markdown("**Solving for added oxygen**")
        st.latex(r"x=\frac{1000y-210}{1-y}")

        st.write(f"Target fraction: **y = {desired_fraction:.4f}**")

        st.code(
            f"x = (1000 × {desired_fraction:.4f} − 210) "
            f"/ (1 − {desired_fraction:.4f})\n"
            f"x = {added_o2:.2f} Nm³"
        )

        st.markdown("**Convert volume to mass**")
        st.latex(r"m=\frac{V}{22.414}\times32")

        st.code(
            f"m = ({added_o2:.2f} / 22.414) × 32\n"
            f"m = {added_mass:.2f} kg"
        )

    st.success(
        f"Add {added_o2:.2f} Nm³ of pure O₂, corresponding to "
        f"{added_mass:.2f} kg."
    )

with st.expander("Assumptions"):
    st.write(
        "Dry air is taken as 21 vol.% O₂. The added gas is pure O₂. "
        "The conversion uses 22.414 Nm³/kmol and 32 kg/kmol."
    )
