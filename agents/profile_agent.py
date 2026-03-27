import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, ProfileData

class ProfileAgent:
    def __init__(self):
        pass

    def process_profile(self, user_input: UserInput) -> ProfileData:
        """
        Parses user input and creates a structured financial profile.
        """
        monthly_surplus = user_input.monthly_income - user_input.monthly_expenses
        
        debt_to_income_ratio = 0.0
        if user_input.monthly_income > 0:
            # Assuming monthly EMI is approx 5% of total debt for simple heuristic
            estimated_emi = user_input.total_debt * 0.05
            debt_to_income_ratio = (estimated_emi / user_input.monthly_income) * 100

        savings_ratio = 0.0
        if user_input.monthly_income > 0:
            savings_ratio = (monthly_surplus / user_input.monthly_income) * 100

        emergency_fund_months = 0.0
        if user_input.monthly_expenses > 0:
            emergency_fund_months = user_input.current_savings / user_input.monthly_expenses

        insurance_multiple = 0.0
        annual_income = user_input.monthly_income * 12
        if annual_income > 0:
            insurance_multiple = user_input.insurance_coverage / annual_income

        return ProfileData(
            monthly_surplus=monthly_surplus,
            debt_to_income_ratio=debt_to_income_ratio,
            savings_ratio=savings_ratio,
            emergency_fund_months=emergency_fund_months,
            insurance_multiple=insurance_multiple
        )

if __name__ == "__main__":
    pass
