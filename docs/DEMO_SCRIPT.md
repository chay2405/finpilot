# Demo Flow Script: FinPilot AI

## Presenter Pre-Requisites
1. Open terminal and run `uvicorn backend.main:app --host 0.0.0.0 --port 8000`.
2. Open second terminal and run `streamlit run frontend/app.py`.
3. Have `localhost:8501` open in your browser on the left.
4. Have your IDE or architectural diagram open on the right (optional).

## Step 1: The Hook (0:00 - 0:30)
- "Hi Judges, 95% of Indians lack structured financial planning. Advisors are costly. Content is generic. FinPilot AI bridges this gap with deterministic AI agents to act as your personalized money mentor."
- Point out the UI and the simplicity of capturing core metrics, bypassing complex onboarding.

## Step 2: The Agentic Core (0:30 - 1:30)
- "Let's input a realistic user profile:"
    - **Age:** 30
    - **Monthly Income:** ₹1,00,000
    - **Monthly Expenses:** ₹60,000 (Simulating a slight over-spender)
    - **Current Savings:** ₹1,00,000 (Low emergency fund)
    - **Current Investments:** ₹2,00,000
    - **Total Debt:** ₹6,00,000 (Car/Personal Loan)
    - **Life Insurance:** ₹20,00,000 (Underinsured)
    - **Goals:** "Buy a house in 5 years, clear debt"
- Click **"Generate Financial Plan"**.
- Emphasize the speed and the multi-agent nature.
- "Notice this isn't just an LLM writing an essay. We have a robust backend where 5 separate agents process the data."

## Step 3: Actionable Output (1:30 - 2:30)
- **Dashboard:** "Agent 1 & 2 scored their health a 35/100 (Needs Attention). It flagged the massive gap in emergency funding (Target ₹3.6L vs ₹1L)."
- **Plan Breakdown:** "Our Planning agent calculated a tailored SIP and adjusted asset allocation recognizing the high debt ratio, pulling equity down dynamically."
- **Tax Optimization:** "The Tax agent deterministically proved that under current slabs, the New Regime saves them ₹12,000 instantly without locking capital into ELSS."
- **AI Advisor:** "Finally, our LLM Recommendation Agent consumed these deterministic outputs and generated this simple, 3-step action plan preventing hallucinated financial advice."

## Step 4: The Impact (2:30 - 3:00)
- "FinPilot AI isn't a toy—it's a mathematically grounded engine that democratizes financial advisory at near-zero marginal cost per user, ready to scale for millions."
- Conclude and ask for questions.
