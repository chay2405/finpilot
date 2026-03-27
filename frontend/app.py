import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="FinPilot AI", page_icon="💸", layout="wide")

# Custom UI styling for a friendlier feel
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
    st.markdown("Don't want to type your exact numbers? Pick a profile to see how it works:")
    
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

# Default Profile if not set
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
    st.markdown("Find out your financial health score and exactly how much you need to save to hit your goals.")
    
    # Using sliders makes it much less intimidating for "real people"
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
            res = requests.post(f"{API_BASE}/analyze", json=st.session_state.base_profile)
            if res.status_code == 200:
                st.balloons()
                data = res.json()
                h = data["health_score"]
                p = data["financial_plan"]
                
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
                    st.success(data["ai_insights"])

# ----------------- PAGE 2: LIFE EVENT ADVISOR -----------------
elif "Life Event" in page:
    st.header("⚡ Life Event Financial Guide")
    st.markdown("Sudden financial changes can be scary or exciting. Let AI guide your next move.")
    
    col1, col2 = st.columns(2)
    with col1:
        event = st.selectbox("What happened?", ["Got a big Bonus!", "Medical Emergency", "Having a Baby", "Getting Married"])
        amount = st.slider("Amount Involved (₹)", 10000, 5000000, 200000, step=10000)
    with col2:
        details = st.text_area("Any specifics?", "e.g., I want to put some of it into a fixed deposit safely.")
        
    if st.button("Give me a strategy", type="primary"):
        payload = {"user_input": pr, "event_type": event, "event_amount": amount, "additional_details": details}
        with st.spinner("Reviewing your profile against this event..."):
            res = requests.post(f"{API_BASE}/life-event", json=payload)
            st.info(res.json().get("advice", "Error connecting."))

# ----------------- PAGE 3: TAX WIZARD -----------------
elif "Tax" in page:
    st.header("🛡️ Tax Optimization Wizard")
    st.markdown("Stop guessing. Enter your simple salary components and figure out exactly what regime to choose.")
    
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
        payload = {"basic_salary": basic, "hra": hra, "lta": 0, "special_allowance": 400000, 
                   "provident_fund": pf, "home_loan_interest": home, 
                   "health_insurance_premium": health, "other_80c": other_80c}
        with st.spinner("Comparing Old vs New Regime against the latest slabs..."):
            d = requests.post(f"{API_BASE}/tax-wizard", json=payload).json()
            st.success(f"### 🎉 Recommended: {d['recommended_regime']}")
            
            c1, c2 = st.columns(2)
            c1.metric("Old Regime Tax", f"₹{d['old_regime_tax']:,.0f}")
            c2.metric("New Regime Tax", f"₹{d['new_regime_tax']:,.0f}")
            
            if d['missed_80c'] > 0:
                st.warning(f"**Missed 80C Limit:** You can still invest ₹{d['missed_80c']:,.0f} to save more tax.")
            st.info(d.get("advice", ""))

# ----------------- PAGE 4: COUPLE'S PLANNER -----------------
elif "Couple" in page:
    st.header("❤️ Couple's Wealth Planner")
    st.markdown("Planning as a team? Maximize joint benefits like HRA swapping and splitting capital gains.")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Partner A")
        pa_inc = st.number_input("Monthly Income (A)", value=120000, step=10000)
    with c2:
        st.subheader("Partner B")
        pb_inc = st.number_input("Monthly Income (B)", value=90000, step=10000)
        
    if st.button("Generate Joint Plan", type="primary"):
        p1, p2 = pr.copy(), pr.copy()
        p1["monthly_income"], p2["monthly_income"] = pa_inc, pb_inc
        p1["total_debt"], p2["total_debt"] = 200000, 0
        
        with st.spinner("Finding joint tax loopholes..."):
            r = requests.post(f"{API_BASE}/couple-planner", json={"partner_1": p1, "partner_2": p2, "joint_goals": ["Buy a House"]}).json()
            st.markdown("### The Couple's Playbook")
            st.write(f"🏠 **HRA Strategy:** {r['hra_optimization']}")
            st.write(f"📈 **SIP Splitting:** {r['sip_splits']}")
            st.info(r['insurance_strategy'])

# ----------------- PAGE 5: MF X-RAY -----------------
elif "X-Ray" in page:
    st.header("📊 Mutual Fund X-Ray")
    st.markdown("See if you bought 5 different funds that all hold the exact same stocks!")
    
    text = st.text_area("Paste your mutual fund names here (simulating a statement PDF):", "HDFC Midcap - 20%\nSBI Small Cap - 15%\nAxis Bluechip - 30%\nParag Parikh Flexi - 10%\nKotak Emerging - 15%\nNippon Small - 10%")
    
    if st.button("Scan Portfolio", type="primary"):
        with st.spinner("Analyzing overlaps..."):
            d = requests.post(f"{API_BASE}/mf-xray", json={"statement_text": text}).json()
            st.error(d['overlap_warning']) if "High" in d['overlap_warning'] else st.warning(d['overlap_warning'])
            
            c1, c2 = st.columns(2)
            c1.metric("Est. Return (XIRR)", f"{d['xirr']}%", d['benchmark_comparison'])
            c2.metric("Expense Ratio Drag", f"{d['expense_ratio_drag']}% (paying too much in fees!)")
            
            st.success(d['rebalancing_plan'])
