import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

# Direct imports bypass the need for a separate FastAPI backend on Streamlit Cloud
from backend.models import UserInput, LifeEventRequest, CoupleInput, TaxWizardInput, MFXRayRequest
from backend.orchestration import FinPilotOrchestrator
from agents.life_event_agent import LifeEventAgent
from agents.tax_wizard_agent import TaxWizardAgent
from agents.couple_agent import CoupleAgent
from agents.mf_xray_agent import MFXRayAgent

# Initialize Agents
@st.cache_resource
def get_agents():
    return {
        "orchestrator": FinPilotOrchestrator(),
        "life_event": LifeEventAgent(),
        "tax_wizard": TaxWizardAgent(),
        "couple": CoupleAgent(),
        "mf_xray": MFXRayAgent()
    }

agents = get_agents()

st.set_page_config(page_title="FinPilot AI", page_icon="💸", layout="wide")

st.markdown("""
<style>
    div[data-testid="stMetricValue"] { color: #1E88E5; font-weight: bold; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("💸 FinPilot AI")
st.markdown("### Your personal finance mentor. Simplified for real people.")

# Sidebar Navigation & Presets
with st.sidebar:
    st.header("1. Choose a Tool")
    page = st.radio("Navigation", [
        "🎯 FIRE & Money Health Score",
        "⚡ Life Event Strategy",
        "🛡️ Tax Optimization Wizard",
        "❤️ Couple's Wealth Planner",
        "📊 Mutual Fund X-Ray"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.header("2. Quick Load Personas")
    
    if st.button("👨‍💻 The 30yo Engineer"):
        st.session_state.base_profile = {
            "age": 30, "monthly_income": 120000, "monthly_expenses": 60000,
            "current_savings": 200000, "current_investments": 800000, "total_debt": 400000,
            "insurance_coverage": 10000000, "target_retirement_age": 50,
            "financial_goals": ["Buy a car", "Retire Early"]
        }
        st.success("Loaded Engineer Profile!")
        
    if st.button("👩‍🏫 The Cautious Saver"):
        st.session_state.base_profile = {
            "age": 35, "monthly_income": 70000, "monthly_expenses": 30000,
            "current_savings": 500000, "current_investments": 100000, "total_debt": 0,
            "insurance_coverage": 0, "target_retirement_age": 60,
            "financial_goals": ["Child Education", "Safe Retirement"]
        }
        st.success("Loaded Saver Profile!")

if "base_profile" not in st.session_state:
    st.session_state.base_profile = {
        "age": 28, "monthly_income": 80000, "monthly_expenses": 40000,
        "current_savings": 100000, "current_investments": 150000, "total_debt": 0,
        "insurance_coverage": 0, "target_retirement_age": 55,
        "financial_goals": ["First Home", "Travel"]
    }

pr = st.session_state.base_profile

# ----------------- PAGE 1: MONEY HEALTH & FIRE -----------------
if "FIRE" in page:
    st.header("🎯 Money Health & FIRE Roadmap")
    
    with st.expander("🛠️ Tweak Your Numbers", expanded=False):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.slider("Age", 18, 70, pr["age"])
            ret = st.slider("Retirement Target", 40, 75, pr["target_retirement_age"])
            inc = st.number_input("Monthly Income (₹)", value=pr["monthly_income"], step=5000)
        with c2:
            exp = st.number_input("Monthly Expenses (₹)", value=pr["monthly_expenses"], step=5000)
            sav = st.number_input("Current Savings (₹)", value=pr["current_savings"], step=10000)
            inv = st.number_input("Current Investments (₹)", value=pr["current_investments"], step=50000)
        with c3:
            debt = st.number_input("Total Debt (₹)", value=pr["total_debt"], step=50000)
            ins = st.number_input("Life Ins. Cover (₹)", value=pr["insurance_coverage"], step=500000)
            goals = st.text_input("Your Goals", ",".join(pr["financial_goals"]))

        if st.button("Save Profile Updates"):
            st.session_state.base_profile.update({
                "age": age, "monthly_income": inc, "monthly_expenses": exp,
                "current_savings": sav, "current_investments": inv, "total_debt": debt,
                "insurance_coverage": ins, "target_retirement_age": ret,
                "financial_goals": [g.strip() for g in goals.split(",")]
            })
            st.rerun()

    if st.button("Analyze Financial Health ✨", type="primary", use_container_width=True):
        with st.spinner("Calculating 6 core metrics..."):
            try:
                user_obj = UserInput(**st.session_state.base_profile)
                report = agents["orchestrator"].run_pipeline(user_obj)
                
                st.balloons()
                h = report.health_score.model_dump()
                p = report.financial_plan.model_dump()
                t = report.tax_optimization.model_dump()
                
                st.markdown("---")
                cols = st.columns([1, 2])
                with cols[0]:
                    st.metric(label="Overall Health Score", value=f"{h['score']} / 100", delta=h['status'])
                    st.progress(h['score'] / 100.0)
                    st.markdown("### The Foundation")
                    for k, v in h["breakdown"].items():
                        st.write(f"**{k.replace('_', ' ').title()}:** {v}/20 pt")
                        st.progress(v / 20.0)
                
                with cols[1]:
                    st.markdown("### 🗺️ The Action Plan")
                    c1, c2 = st.columns(2)
                    c1.metric("Recommended Mo. SIP", f"₹{p['recommended_sip']:,.0f}")
                    c2.metric("Emergency Target", f"₹{p['emergency_fund_target']:,.0f}")
                    st.info(f"**Optimal Asset Split:** {p['asset_allocation']['equity']}% Equity / {p['asset_allocation']['debt']}% Safe Debt")
                    
                    st.markdown("### 🤖 FinPilot's Advice")
                    st.success(report.ai_insights)
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------- PAGE 2: LIFE EVENT ADVISOR -----------------
elif "Life Event" in page:
    st.header("⚡ Life Event Financial Guide")
    
    col1, col2 = st.columns(2)
    with col1:
        event = st.selectbox("What happened?", ["Got a big Bonus!", "Medical Emergency", "Having a Baby", "Getting Married"])
        amount = st.slider("Amount Involved (₹)", 10000, 5000000, 200000, step=10000)
    with col2:
        details = st.text_area("Any specifics?", "e.g., I want to put some of it into a fixed deposit safely.")
        
    if st.button("Give me a strategy", type="primary"):
        with st.spinner("Reviewing your profile against this event..."):
            try:
                req = LifeEventRequest(
                    user_input=UserInput(**pr),
                    event_type=event,
                    event_amount=amount,
                    additional_details=details
                )
                advice = agents["life_event"].evaluate_life_event(req)
                st.info(advice)
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------- PAGE 3: TAX WIZARD -----------------
elif "Tax" in page:
    st.header("🛡️ Tax Optimization Wizard")
    
    c1, c2 = st.columns(2)
    with c1:
        basic = st.number_input("Basic Salary", value=600000, step=50000)
        hra = st.number_input("HRA Claimed", value=150000, step=10000)
        pf = st.number_input("Provident Fund (Employee)", value=72000, step=5000)
    with c2:
        other_80c = st.number_input("80C Investments (LIC, ELSS, PPF)", value=30000, step=10000)
        health = st.number_input("80D Medical Ins.", value=15000, step=5000)
        home = st.number_input("Home Loan Interest", value=0, step=50000)
        
    if st.button("Calculate Tax Moves", type="primary"):
        with st.spinner("Comparing Old vs New Regime against the latest slabs..."):
            try:
                req = TaxWizardInput(
                    basic_salary=basic, hra=hra, lta=0, special_allowance=400000,
                    provident_fund=pf, home_loan_interest=home,
                    health_insurance_premium=health, other_80c=other_80c
                )
                d = agents["tax_wizard"].evaluate_tax(req)
                st.success(f"### 🎉 Recommended: {d['recommended_regime']}")
                
                c1, c2 = st.columns(2)
                c1.metric("Old Regime Tax", f"₹{d['old_regime_tax']:,.0f}")
                c2.metric("New Regime Tax", f"₹{d['new_regime_tax']:,.0f}")
                
                if d['missed_80c'] > 0:
                    st.warning(f"**Missed 80C Limit:** You can still invest ₹{d['missed_80c']:,.0f} to save more tax.")
                st.info(d.get("advice", ""))
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------- PAGE 4: COUPLE'S PLANNER -----------------
elif "Couple" in page:
    st.header("❤️ Couple's Wealth Planner")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Partner A")
        pa_inc = st.number_input("Monthly Income (A)", value=120000, step=10000)
    with c2:
        st.subheader("Partner B")
        pb_inc = st.number_input("Monthly Income (B)", value=90000, step=10000)
        
    if st.button("Generate Joint Plan", type="primary"):
        with st.spinner("Finding joint tax loopholes..."):
            try:
                p1 = pr.copy()
                p2 = pr.copy()
                p1["monthly_income"], p2["monthly_income"] = pa_inc, pb_inc
                p1["total_debt"], p2["total_debt"] = 200000, 0
                
                req = CoupleInput(
                    partner_1=UserInput(**p1),
                    partner_2=UserInput(**p2),
                    joint_goals=["Buy a House"]
                )
                r = agents["couple"].evaluate_couple(req).model_dump()
                
                st.markdown("### The Couple's Playbook")
                st.subheader(f"Combined Net Worth: ₹{r['total_net_worth']:,.0f}")
                
                st.write(f"🏠 **HRA Strategy:** {r['hra_optimization']}")
                st.write(f"📈 **SIP Splitting:** {r['sip_splits']}")
                st.info(r['insurance_strategy'])
            except Exception as e:
                st.error(f"Error: {e}")

# ----------------- PAGE 5: MF X-RAY -----------------
elif "X-Ray" in page:
    st.header("📊 Mutual Fund X-Ray")
    
    text = st.text_area("Paste your mutual fund names here (simulating a statement PDF):", "HDFC Midcap - 20%\nSBI Small Cap - 15%\nAxis Bluechip - 30%\nParag Parikh Flexi - 10%\nKotak Emerging - 15%\nNippon Small - 10%")
    
    if st.button("Scan Portfolio", type="primary"):
        with st.spinner("Analyzing overlaps..."):
            try:
                req = MFXRayRequest(statement_text=text)
                d = agents["mf_xray"].evaluate_portfolio(req).model_dump()
                
                st.error(d['overlap_warning']) if "High" in d['overlap_warning'] else st.warning(d['overlap_warning'])
                
                c1, c2 = st.columns(2)
                c1.metric("Est. Return (XIRR)", f"{d['xirr']}%", d['benchmark_comparison'])
                c2.metric("Expense Ratio Drag", f"{d['expense_ratio_drag']}% (paying too much in fees!)")
                
                st.success(d['rebalancing_plan'])
            except Exception as e:
                st.error(f"Error: {e}")
