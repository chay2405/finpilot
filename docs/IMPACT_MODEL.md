# The Impact Model: FinPilot AI

## 1. The Core Problem
Most Indians don't seek professional financial advice because traditional planners charge ₹10,000 to ₹30,000 per year for a basic plan. The remaining 95% of individuals use generic internet advice, leading to:
- Overpaying taxes by staying in the incorrect tax regime
- Losing wealth to non-compounding, low-interest savings accounts
- Underinsuring their dependents

## 2. Quantified Assumptions
* **Target Audience:** 50,000 active middle-class salary earners in Tier 1/2 cities.
* **Cost to Serve (LLM + Cloud):** ~₹0.5 / user-plan generation.
* **Annual Savings per User:**
    * **Tax Optimization:** Average ₹12,000 / yr saved by correctly choosing between New vs. Old Regime.
    * **SIP Compounding Advantage:** Activating an extra ₹5,000 / mo in equity vs FD yields an extra ~₹30 Lakhs over 15 years.
    * **Debt Consolidation/Foreclosure advice:** Saves an average of ₹10,000 / yr in simple interest.

## 3. Scalability & Financial Benefit
- On a 100,000 active user base, assuming a modest conversion rate of 10% actually executing the plan:
- **Total Micro-Savings Generated for Economy:** 10,000 users x ₹22,000 (Tax + Debt interest) = ₹22 Crores annually unlocked for individuals.
- **Venture Scalability:** FinPilot doesn't require scaling human advisors linearly. A user base scaling 100x simply scales compute, allowing the company to monetize via lead generation for specific mutual funds, insurance providers, and tax-filing services at high margins.

## 4. Why Multi-Agent?
Instead of building a simple generative wrapper that frequently hallucinates mathematically wrong tax brackets or unachievable SIP targets, FinPilot breaks the math down into modular Python agents. The LLM is restricted *only* to translating deterministic JSON outputs into empathetic human advice, capping downside API risks and ensuring 100% regulatory compliance.
