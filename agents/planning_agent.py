import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, ProfileData, Plan

class PlanningAgent:
    def __init__(self):
        pass

    def compute_plan(self, user_input: UserInput, profile: ProfileData) -> Plan:
        """
        Computes SIP, asset allocation, and financial roadmap based on FIRE/Goal principles.
        """
        # 1. Recommended SIP
        # Typically suggested at 20-30% of income, or whatever the monthly surplus can accommodate comfortably.
        ideal_sip_ratio = 0.25
        ideal_sip = user_input.monthly_income * ideal_sip_ratio
        
        # Adjust based on debt
        if profile.debt_to_income_ratio > 30:
            # Over 30% DTI, reduce SIP recommendation and focus on debt
            recommended_sip = max(0, min(ideal_sip, profile.monthly_surplus * 0.4))
        else:
            # Under 30% DTI, allocate up to 80% of surplus to SIP
            recommended_sip = max(0, min(ideal_sip, profile.monthly_surplus * 0.8))

        # 2. Asset Allocation based on Age (Rule of 100 minus age for Equity)
        equity_ratio = max(0, min(100 - user_input.age, 100))
        debt_ratio = 100 - equity_ratio
        
        # Adjust if nearing retirement
        years_to_retirement = user_input.target_retirement_age - user_input.age
        if years_to_retirement < 5:
            # Shift heavily to debt
            equity_ratio = max(0, equity_ratio - 20)
            debt_ratio = 100 - equity_ratio

        asset_allocation = {
            "equity": int(equity_ratio),
            "debt": int(debt_ratio)
        }

        # 3. Emergency fund target (6 months of expenses)
        emergency_fund_target = user_input.monthly_expenses * 6

        return Plan(
            recommended_sip=float(recommended_sip),
            asset_allocation=asset_allocation,
            emergency_fund_target=float(emergency_fund_target),
            years_to_retirement=max(0, years_to_retirement)
        )
