import streamlit as st

st.set_page_config(
    page_title="Blast Furnace Oxygen Balance",
    page_icon="🟡",
    layout="wide"
)

# ---------- Yellow theme ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #fffdf0;
}
[data-testid="stHeader"] {
    background: #fffdf0;
}
.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
.hero {
    background: #ffd43b;
    padding: 28px 32px;
    border-radius: 18px;
    border: 2px solid #e6b800;
    margin-bottom: 24px;
}
.hero h1 {
    color: #3b3000;
    margin: 0;
    font-size: 2.25rem;
}
.hero p {
    color: #574900;
    margin: 8px 0 0;
}
.panel {
    background: #fff8c9;
    border: 1px solid #ead36a;
    border-radius: 16px;
    padding: 24px;
}
.answer {
    background: #fff3a6;
    border-left: 8px solid #f0b900;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 10px 0;
}
.answer h2 {
    margin: 3px 0;
    color: #4a3b00;
}
.flow {
    text-align: center;
    font-size: 1.15rem;
    padding: 15px;
    background: #fff9d9;
    border-radius: 12px;
}
div.stButton > button {
    background: #f2c400;
    color: #2e2600;
    border: 1px solid #c9a500;
    border-radius: 10px;
    font-weight: 800;
}
div.stButton > button:hover {
    background: #ffd83d;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="hero">
    <h1>🟡 Blast Furnace Oxygen Balance</h1>
    <p>Interactive calculation tool · PIFA Metallurgy · Chapter 1, Problem 1.7</p>
</div>
""", unsafe_allow_html=True)

# ---------- Process overview ----------
st.markdown("""
<div class="flow">
    <b>1000 Nm³ dry air</b>
    &nbsp; → &nbsp;
    <b>+ pure O₂</b>
    &nbsp; → &nbsp;
    <b>specified final O₂ concentration</b>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- Inputs ----------
input_col, info_col = st.columns([1, 1.4])

with input_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("🎯 Target condition")

    target = st.number_input(
        "Final O₂ concentration (vol. %)",
        min_value=21.01,
        max_value=99.0,
        value=25.0,
        step=0.5
    )

    calculate = st.button(
        "Calculate oxygen requirement",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with info_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("Given conditions")

    g1, g2 = st.columns(2)
    g1.metric("Dry air", "1000 Nm³")
    g2.metric("O₂ in air", "21 vol.%")

    st.write(
        "The initial oxygen quantity is therefore "
        "**210 Nm³**."
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Calculation ----------
if calculate:
    air = 1000.0
    initial_o2 = 0.21 * air
    y = target / 100.0

    # Oxygen balance:
    # (initial O2 + added O2) / (initial air + added O2) = target fraction
    added_o2 = (air * y - initial_o2) / (1.0 - y)
    added_mass = (added_o2 / 22.414) * 32.0

    final_volume = air + added_o2
    achieved = ((initial_o2 + added_o2) / final_volume) * 100.0

    st.write("")
    st.subheader("📌 Result")

    r1, r2 = st.columns(2)

    with r1:
        st.markdown(f"""
        <div class="answer">
            <div>PURE O₂ TO ADD</div>
            <h2>{added_o2:.2f} Nm³</h2>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="answer">
            <div>MASS OF PURE O₂</div>
            <h2>{added_mass:.2f} kg</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🔎 Balance check")

    c1, c2, c3 = st.columns(3)
    c1.metric("Initial O₂", f"{initial_o2:.2f} Nm³")
    c2.metric("Final gas", f"{final_volume:.2f} Nm³")
    c3.metric("Calculated O₂", f"{achieved:.2f}%")

    with st.expander("View equations"):
        st.markdown("**Oxygen balance**")
        st.latex(r"\frac{210+x}{1000+x}=y")

        st.markdown("**Rearranged equation**")
        st.latex(r"x=\frac{1000y-210}{1-y}")

        st.markdown("**Volume-to-mass conversion**")
        st.latex(r"m_{O_2}=\frac{V_{O_2}}{22.414}\times32")

        st.code(
            f"Target fraction y = {y:.4f}\n"
            f"x = (1000 × {y:.4f} − 210) / (1 − {y:.4f})\n"
            f"x = {added_o2:.2f} Nm³\n\n"
            f"m = ({added_o2:.2f} / 22.414) × 32\n"
            f"m = {added_mass:.2f} kg"
        )

else:
    st.write("")
    st.warning("Choose a target O₂ concentration and press the calculation button.")

# ---------- Reference ----------
with st.expander("📚 Textbook reference"):
    st.write(
        "J. G. Peacey and W. G. Davenport, "
        "The Iron Blast Furnace: Theory and Practice, Pergamon Press, 1979."
    )
    st.write(
        "Chapter 1, Problem 1.7 asks for an interactive program that "
        "calculates the volume (Nm³) and weight (kg) of pure oxygen added "
        "to 1000 Nm³ of dry air to reach a specified O₂ volume percentage."
    )
    st.write(
        "Assumptions used here: dry air contains 21 vol.% O₂; the added "
        "gas is pure O₂; 22.414 Nm³/kmol and 32 kg/kmol are used for "
        "the volume-to-mass conversion."
    )
