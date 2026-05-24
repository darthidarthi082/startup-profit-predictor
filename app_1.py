import streamlit as st
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Startup Profit Predictor",
    page_icon="📈",
    layout="centered"
)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("📈 Startup Profit Predictor")
st.markdown("Predict your startup's profit using **Multiple Linear Regression** trained on the 50 Startups dataset.")
st.markdown("---")

# ── Model coefficients (from your notebook) ───────────────────────────────────
# regressor.coef_  = [7.90838939e-01, 3.01972395e-02, 3.10155570e-02, 4.62827681e+02, 3.04737841e+02]
# regressor.intercept_ = 42403.73
INTERCEPT   = 42403.7318072
COEF_RD     = 0.790838939   # R&D Spend
COEF_ADMIN  = 0.0301972395  # Administration
COEF_MKT    = 0.0310155570  # Marketing Spend
COEF_STATE1 = 462.827681    # Dummy 1 (Florida)
COEF_STATE2 = 304.737841    # Dummy 2 (New York)
# California = baseline (both dummies = 0)

# ── Input form ────────────────────────────────────────────────────────────────
st.subheader("Enter Startup Details")

col1, col2 = st.columns(2)

with col1:
    rd_spend = st.number_input(
        "💡 R&D Spend ($)",
        min_value=0.0,
        max_value=500000.0,
        value=80000.0,
        step=1000.0,
        help="Amount spent on Research & Development"
    )
    admin = st.number_input(
        "🏢 Administration ($)",
        min_value=0.0,
        max_value=500000.0,
        value=100000.0,
        step=1000.0,
        help="Administration expenses"
    )

with col2:
    marketing = st.number_input(
        "📣 Marketing Spend ($)",
        min_value=0.0,
        max_value=500000.0,
        value=150000.0,
        step=1000.0,
        help="Amount spent on Marketing"
    )
    state = st.selectbox(
        "📍 State",
        options=["California", "Florida", "New York"],
        help="State where the startup is located"
    )

st.markdown("---")

# ── Predict button ────────────────────────────────────────────────────────────
if st.button("🚀 Predict Profit", use_container_width=True):

    # One-hot encode state (California = baseline)
    florida  = 1 if state == "Florida"  else 0
    new_york = 1 if state == "New York" else 0

    # Apply the regression formula
    profit = (INTERCEPT
              + COEF_RD    * rd_spend
              + COEF_ADMIN * admin
              + COEF_MKT   * marketing
              + COEF_STATE1 * florida
              + COEF_STATE2 * new_york)

    # ── Result display ────────────────────────────────────────────────────────
    st.success("✅ Prediction Complete!")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("💰 Predicted Profit", f"${profit:,.2f}")
    col_b.metric("📊 Model R² Score", "93.59%")
    col_c.metric("📂 Dataset Size", "50 startups")

    st.markdown("---")
    st.markdown("#### 🔍 Input Summary")
    st.table({
        "Feature": ["R&D Spend", "Administration", "Marketing Spend", "State"],
        "Value":   [f"${rd_spend:,.2f}", f"${admin:,.2f}", f"${marketing:,.2f}", state]
    })

# ── Dataset info ──────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 About the Model"):
    st.markdown("""
    - **Algorithm:** Multiple Linear Regression (scikit-learn)
    - **Dataset:** 50 Startups
    - **Features:** R&D Spend, Administration, Marketing Spend, State
    - **Target:** Profit
    - **R² Score:** 93.59%
    - **Encoding:** One-hot encoding for State (California = baseline)

    **Model Coefficients:**
    | Feature | Coefficient |
    |---|---|
    | Intercept | 42,403.73 |
    | R&D Spend | 0.7908 |
    | Administration | 0.0302 |
    | Marketing Spend | 0.0310 |
    | State = Florida | 462.83 |
    | State = New York | 304.74 |
    """)
