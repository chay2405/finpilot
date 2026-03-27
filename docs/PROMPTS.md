# FinPilot AI – Prompt Engineering Strategy

## 1. System Prompt

`{"role": "system", "content": "You are FinPilot AI, a highly experienced personal money mentor. Provide clear, actionable, and encouraging financial advice based on the user's data provided."}`

### Why This Format?
- Sets strict guardrails restricting the persona to a financial mentor.
- Avoids overcommitting guarantees.
- Forces empathy to prevent aggressive "you are failing" messaging when scores are low.

## 2. Recommendation Agent Data Injection

When orchestrating the results, we use f-strings to strictly inject JSON outputs (never raw assumptions or conversational back-and-forths).

```python
prompt = f"""
        User Profile:
        Age: {user.age}
        Monthly Income: ₹{user.monthly_income}
        Monthly Expenses: ₹{user.monthly_expenses}
        Retirement Target: {user.target_retirement_age} years
        
        System Findings:
        - Health Score: {score.score}/100 ({score.status})
        - Emergency Fund Gap: Needs ₹{plan.emergency_fund_target}
        - Asset Allocation: {plan.asset_allocation['equity']}% Equity / {plan.asset_allocation['debt']}% Debt
        - Recommended SIP: ₹{plan.recommended_sip}/month
        - Tax Regime: {tax.recommended_regime} (Potential Savings: ₹{tax.potential_savings})
        
        Goals: {', '.join(user.financial_goals)}
        
        Provide clear financial advice, risks, and 3 immediate next steps for the user. Be concise.
"""
```

### Prompt Engineering Decisions:
1. **Fact-Injection (Context Grounding):** We do not let the LLM guess asset allocation. We run the Python agent locally. The LLM only receives the mathematical answer to provide the narrative.
2. **Explicit Output Formatting:** `"Provide clear financial advice, risks, and 3 immediate next steps."` forces the LLM into returning bulleted, digestible info.
3. **Truncation via `"Be concise."`** keeps token costs low (<₹0.5 per request) and ensures users aren't overwhelmed by lengthy financial jargon.

## 3. Dealing With LLM Hallucinations
Because a user interacting directly with an LLM on finance is a major regulatory and liability risk (SEBI / General liability), FinPilot strips the reasoning engine completely from the API call. 
The system mathematically decides if New Regime > Old Regime. 
The LLM merely reads `{tax.recommended_regime}` and outputs the decision kindly. Total override of hallucination.
