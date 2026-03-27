import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, ProfileData, HealthScore

class ScoringAgent:
    def __init__(self):
        pass

    def calculate_health_score(self, user_input: UserInput, profile: ProfileData) -> HealthScore:
        """
        Calculates Money Health Score using rule-based logic.
        Score out of 100 based on:
        - Emergency fund (max 20)
        - Insurance coverage (max 20)
        - Diversification / Savings (max 20)
        - Debt health (max 20)
        - Retirement readiness (max 20)
        """
        breakdown = {}
        total_score = 0
        
        # 1. Emergency Fund (Max 20)
        # 6 months or more optimal
        em_score = min(20, int((profile.emergency_fund_months / 6.0) * 20))
        breakdown['emergency_fund'] = max(0, em_score)
        
        # 2. Insurance Coverage (Max 20)
        # 10x annual income optimal
        ins_score = min(20, int((profile.insurance_multiple / 10.0) * 20))
        breakdown['insurance_coverage'] = max(0, ins_score)
        
        # 3. Savings Ratio (Max 20)
        # 20% or more optimal
        sav_score = min(20, int((profile.savings_ratio / 20.0) * 20))
        breakdown['savings_health'] = max(0, sav_score)
        
        # 4. Debt Health (Max 20)
        # Debt ratio < 40% optimal. Score decreases as ratio goes up.
        if profile.debt_to_income_ratio <= 10:
            debt_score = 20
        elif profile.debt_to_income_ratio <= 40:
            debt_score = 15
        elif profile.debt_to_income_ratio <= 60:
            debt_score = 5
        else:
            debt_score = 0
        breakdown['debt_health'] = debt_score
        
        # 5. Retirement readiness (Max 20)
        years_to_retire = user_input.target_retirement_age - user_input.age
        if years_to_retire <= 0:
            ret_score = 20 # Already retired
        else:
            # simple heuristic: current investments should grow to support life later 
            # we'll use a simplified check: are there investments >= annual income
            annual_income = user_input.monthly_income * 12
            if annual_income > 0:
                inv_ratio = user_input.current_investments / annual_income
                ret_score = min(20, int(inv_ratio * 5)) # Needs at least 4x for full points
            else:
                ret_score = 0
        breakdown['retirement_readiness'] = max(0, ret_score)
        
        # Calculate total
        total_score = sum(breakdown.values())
        
        # Determine status
        if total_score >= 80:
            status = "Excellent"
        elif total_score >= 60:
            status = "Good"
        elif total_score >= 40:
            status = "Fair"
        else:
            status = "Needs Attention"
            
        return HealthScore(score=total_score, breakdown=breakdown, status=status)
