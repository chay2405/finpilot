import sys
import os
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import MFXRayRequest, MFXRayReport
from utils.llm_helper import generate_insights_with_llm

class MFXRayAgent:
    def __init__(self):
        pass

    def evaluate_portfolio(self, request: MFXRayRequest) -> MFXRayReport:
        """
        Mocks reading a Statement format (PDF parsed to text) and finds inefficiencies.
        We pseudo-calculate XIRR and overlaps for demo purposes since we don't have
        real NAV history databases loaded inside this hackathon prototype.
        """
        # Pseudo analysis logic: check if the text mentions lots of funds
        num_funds = max(3, len(request.statement_text.split(',')) if ',' in request.statement_text else 5)
        
        # Simulate an overlap warning if they have too many funds
        overlap_warning = "Significant overlap detected. Your X mutual funds and Y have 65% stock overlap."
        if num_funds > 5:
            overlap_warning = f"High structural overlap. You have {num_funds} funds, meaning you are over-diversified and almost mimicking the index minus active fees."
        
        xirr = round(random.uniform(9.5, 14.5), 1)
        expense_ratio_drag = round(num_funds * 0.4, 2)
        
        prompt = f"""
        User submitted a mutual fund parsed output: {request.statement_text[:300]}...
        Calculations: {num_funds} funds detected.
        Simulated XIRR: {xirr}%
        
        Analyze briefly:
        1. Compare {xirr}% to a Nifty 50 benchmark (12% average).
        2. Propose a consolidation rebalancing plan. (Drop underperformers, keep index + flexi cap).
        Keep it to 2 concise bullet points.
        """
        
        rebalancing_plan = generate_insights_with_llm(prompt)
        
        return MFXRayReport(
            xirr=xirr,
            overlap_warning=overlap_warning,
            expense_ratio_drag=expense_ratio_drag,
            benchmark_comparison=f"Your return is {xirr}%, compared to benchmark 12.0%.",
            rebalancing_plan=rebalancing_plan
        )
