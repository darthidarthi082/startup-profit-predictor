import streamlit as st

st.set_page_config(
    page_title="Startup Profit Predictor",
    page_icon="📈",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Hide default streamlit header */
    #MainMenu, footer, header {visibility: hidden;}

    /* Page background */
    .stApp { background-color: #f5f7fa; }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 { color: #ffffff; font-size: 2rem; margin: 0 0 0.5rem; }
    .hero p  { color: #a0aec0; font-size: 1rem; margin: 0; }

    /* Section card */
    .card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1.25rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Input labels */
    label { font-weight: 500 !important; color: #4a5568 !important; font-size: 0.9rem !important; }

    /* Predict button */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        transition: opacity 0.2s;
        letter-spacing: 0.3px;
    }
    .stButton > button:hover { opacity: 0.92; }

    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 14px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    .result-label { color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-bottom: 0.5rem; }
    .result-value { color: #ffffff; font-size: 2.6rem; font-weight: 700; margin: 0; }
    .result-sub   { color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 0.5rem; }

    /* Metric cards row */
    .metric-row { display: flex; gap: 12px; margin: 1.25rem 0; }
    .metric-card {
        flex: 1;
        background: #f7f8fc;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e8ecf4;
    }
    .metric-card .m-val { font-size: 1.3rem; font-weight: 700; color: #2d3748; }
    .metric-card .m-lbl { font-size: 0.78rem; color: #718096; margin-top: 2px; }

    /* Summary table */
    .summary-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
    .summary-table td { padding: 8px 4px; border-bottom: 1px solid #edf2f7; color: #4a5568; }
    .summary-table td:last-child { text-align: right; font-weight: 600; color: #2d3748; }

    /* Coefficient table */
    .coef-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .coef-table th { padding: 8px; background: #f7f8fc; color: #4a5568; text-align: left; font-weight: 600; border-bottom: 2px solid #e8ecf4; }
    .coef-table td { padding: 8px; border-bottom: 1px solid #edf2f7; color: #4a5568; }
    .coef-table td:last-child { text-align: right; font-family: monospace; color: #553c9a; font-weight: 600; }

    /* Badge */
    .badge {
        display: inline-block;
        background: #ebf4ff;
        color: #2b6cb0;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Model coefficients (from notebook) ───────────────────────────────────────
INTERCEPT   = 42403.7318072
COEF_RD     = 0.790838939
COEF_ADMIN  = 0.0301972395
COEF_MKT    = 0.0310155570
COEF_FLORIDA  = 462.827681
COEF_NEWYORK  = 304.737841

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>📈 Startup Profit Predictor</h1>
  <p>Multiple Linear Regression · 50 Startups Dataset · R² = 93.59%</p>
</div>
""", unsafe_allow_html=True)

# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">🏢 Enter Startup Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    rd_spend = st.number_input("💡 R&D Spend ($)", min_value=0.0, max_value=500000.0,
                                value=80000.0, step=1000.0)
    admin    = st.number_input("🏛️ Administration ($)", min_value=0.0, max_value=500000.0,
                                value=100000.0, step=1000.0)
with col2:
    marketing = st.number_input("📣 Marketing Spend ($)", min_value=0.0, max_value=500000.0,
                                 value=150000.0, step=1000.0)
    state     = st.selectbox("📍 State", ["California", "Florida", "New York"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
predict = st.button("🚀 Predict Profit")

if predict:
    florida  = 1 if state == "Florida"  else 0
    new_york = 1 if state == "New York" else 0

    profit = (INTERCEPT
              + COEF_RD      * rd_spend
              + COEF_ADMIN   * admin
              + COEF_MKT     * marketing
              + COEF_FLORIDA * florida
              + COEF_NEWYORK * new_york)

    avg  = 112013
    diff = profit - avg
    arrow = "▲" if diff >= 0 else "▼"
    note  = f"{arrow} ${abs(diff):,.0f} {'above' if diff >= 0 else 'below'} dataset average"

    # Result banner
    st.markdown(f"""
    <div class="result-box">
      <div class="result-label">Predicted Profit</div>
      <div class="result-value">${profit:,.2f}</div>
      <div class="result-sub">{note}</div>
    </div>
    """, unsafe_allow_html=True)

    # Metric cards
    total_spend = rd_spend + admin + marketing
    roi = ((profit - total_spend) / total_spend * 100) if total_spend > 0 else 0
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card">
        <div class="m-val">${total_spend:,.0f}</div>
        <div class="m-lbl">Total Spend</div>
      </div>
      <div class="metric-card">
        <div class="m-val">{roi:+.1f}%</div>
        <div class="m-lbl">ROI</div>
      </div>
      <div class="metric-card">
        <div class="m-val">93.59%</div>
        <div class="m-lbl">Model R² Score</div>
      </div>
      <div class="metric-card">
        <div class="m-val">{state}</div>
        <div class="m-lbl">State</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Summary table
    st.markdown('<div class="card"><div class="card-title">🔍 Input Summary</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="summary-table">
      <tr><td>💡 R&D Spend</td><td>${rd_spend:,.2f}</td></tr>
      <tr><td>🏛️ Administration</td><td>${admin:,.2f}</td></tr>
      <tr><td>📣 Marketing Spend</td><td>${marketing:,.2f}</td></tr>
      <tr><td>📍 State</td><td>{state}</td></tr>
      <tr><td>💰 Predicted Profit</td><td>${profit:,.2f}</td></tr>
    </table>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── About the model ───────────────────────────────────────────────────────────
with st.expander("📋 About the Model & Coefficients"):
    st.markdown("""
    <div style="font-size:0.9rem; color:#4a5568; margin-bottom:1rem;">
    <b>Algorithm:</b> Multiple Linear Regression &nbsp;|&nbsp;
    <b>Library:</b> scikit-learn &nbsp;|&nbsp;
    <b>R² Score:</b> 93.59% &nbsp;|&nbsp;
    <b>Dataset:</b> 50 Startups
    </div>
    <table class="coef-table">
      <tr><th>Feature</th><th>Coefficient</th></tr>
      <tr><td>Intercept</td><td>42,403.73</td></tr>
      <tr><td>R&D Spend</td><td>0.7908</td></tr>
      <tr><td>Administration</td><td>0.0302</td></tr>
      <tr><td>Marketing Spend</td><td>0.0310</td></tr>
      <tr><td>State = Florida</td><td>462.83</td></tr>
      <tr><td>State = New York</td><td>304.74</td></tr>
      <tr><td>State = California</td><td>0 (baseline)</td></tr>
    </table>
    """, unsafe_allow_html=True)
