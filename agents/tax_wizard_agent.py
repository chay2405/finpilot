import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import TaxWizardInput
from utils.llm_helper import generate_insights_with_llm

class TaxWizardAgent:
    def __init__(self):
        pass

    def evaluate_tax(self, data: TaxWizardInput) -> dict:
        """
        Deep tax analysis showing missing deductions and regime comparisons.
        """
        gross = data.basic_salary + data.hra + data.lta + data.special_allowance
        total_80c = min(150000, data.provident_fund + data.other_80c)
        total_80d = min(25000, data.health_insurance_premium)
        total_24b = min(200000, data.home_loan_interest)
        
        # Simplified standard ded for both
        std_deduction = 50000
        
        # Old regime taxable
        taxable_old = max(0, gross - std_deduction - total_80c - total_80d - total_24b)
        # New regime taxable (fewer exemptions)
        taxable_new = max(0, gross - std_deduction)
        
        tax_old = taxable_old * 0.20 if taxable_old > 500000 else 0
        tax_new = taxable_new * 0.10 if taxable_new > 700000 else 0
        
        # We also want to find what they missed.
        missed_80c = max(0, 150000 - total_80c)
        missed_80d = max(0, 25000 - total_80d)
        
        prompt = f"""
        User Salary Structure:
        Gross: ₹{gross}
        Claimed 80C: ₹{total_80c}/150000
        Claimed 80D: ₹{total_80d}/25000
        
        Calculated Old Tax: ₹{tax_old}
        Calculated New Tax: ₹{tax_new}
        
        Missed Opportunities:
        - 80C gap: ₹{missed_80c}
        - 80D gap: ₹{missed_80d}
        
        Recommend highest impact tax-saving investments (ELSS vs NPS vs PPF) tailored for them.
        Keep it to 4 bullet points.
        """
        advice = generate_insights_with_llm(prompt)
        
        return {
            "gross_salary": gross,
            "old_regime_tax": tax_old,
            "new_regime_tax": tax_new,
            "recommended_regime": "Old Regime" if tax_old < tax_new else "New Regime",
            "missed_80c": missed_80c,
            "missed_80d": missed_80d,
            "advice": advice
        }
