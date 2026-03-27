import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, HealthScore, Plan, TaxInfo
from utils.llm_helper import generate_insights_with_llm

class RecommendationAgent:
    def __init__(self):
        pass

    def generate_recommendations(self, user: UserInput, score: HealthScore, plan: Plan, tax: TaxInfo) -> str:
        """
        Converts outputs into human-friendly insights using an LLM.
        """
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
        
        insights = generate_insights_with_llm(prompt)
        return insights
