import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import CoupleInput, CoupleReport
from utils.llm_helper import generate_insights_with_llm

class CoupleAgent:
    def __init__(self):
        pass

    def evaluate_couple(self, request: CoupleInput) -> CoupleReport:
        """
        Takes data from both partners and combines insights for optimization.
        """
        p1 = request.partner_1
        p2 = request.partner_2
        
        total_nw = (p1.current_savings + p1.current_investments - p1.total_debt) + \
                   (p2.current_savings + p2.current_investments - p2.total_debt)
        
        total_income = p1.monthly_income + p2.monthly_income
        total_expenses = p1.monthly_expenses + p2.monthly_expenses
        
        # Simple heuristics for couple's combined optimization
        higher_earner = 1 if p1.monthly_income > p2.monthly_income else 2
        
        prompt = f"""
        Couple's Financial Data:
        Total Income: ₹{total_income}/mo
        Total Expenses: ₹{total_expenses}/mo
        Combined Net Worth: ₹{total_nw}
        
        Partner 1 Income: ₹{p1.monthly_income} | Debt: ₹{p1.total_debt}
        Partner 2 Income: ₹{p2.monthly_income} | Debt: ₹{p2.total_debt}
        
        Goals: {', '.join(request.joint_goals)}
        
        Provide optimizations for:
        1. HRA or Home loan interest claims (Should higher earner claim?)
        2. Splitting SIP allocations for balancing tax
        3. Joint insurance cover benefits
        
        Keep it concise and actionable.
        """
        
        advice = generate_insights_with_llm(prompt)
        
        return CoupleReport(
            total_net_worth=total_nw,
            hra_optimization="Higher earner should prioritize HRA/Home Loan claims.",
            nps_optimization="Both partners should maximize 80CCD(1B) ₹50,000 extra limit independently.",
            sip_splits="Split investments to keep capital gains under ₹1L threshold for both partners individually.",
            insurance_strategy=advice
        )
