import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, TaxInfo

class TaxAgent:
    def __init__(self):
        pass

    def calculate_tax(self, user_input: UserInput) -> TaxInfo:
        """
        Calculates tax liability under Old and New regimes (Simplified Indian Tax rules).
        Suggests deductions like 80C, 80D if Old Regime is chosen.
        """
        annual_income = user_input.monthly_income * 12
        
        # Base standard deduction valid in both regimes (simplified approx 50K)
        std_deduction = 50000
        taxable_base = max(0, annual_income - std_deduction)

        # 1. Old Regime Calculation
        # Assuming maximum 80C: 1,50,000, 80D: 25,000
        # If the user has savings/investments that we can assume fall under 80C
        # We will assume they maximize 80C + 80D = 1,75,000 deduction
        max_80c_80d = 175000
        
        # We assume they invest optimally to take old regime benefit
        taxable_old = max(0, taxable_base - max_80c_80d)
        
        # Basic slabs for Old Regime:
        # 0-2.5L: 0%
        # 2.5-5L: 5% (Rebate under 87A up to 12.5k -> effectively 0 if taxable <= 5L)
        # 5-10L: 20%
        # >10L: 30%
        tax_old = 0
        if taxable_old <= 500000:
            tax_old = 0
        else:
            tax_old += 12500  # for 2.5L to 5L
            if taxable_old <= 1000000:
                tax_old += (taxable_old - 500000) * 0.20
            else:
                tax_old += 100000  # 20% of 5L
                tax_old += (taxable_old - 1000000) * 0.30
        
        # 2. New Regime Calculation
        # Basic slabs for New Regime (simplified 2023-24):
        # 0-3L: 0%
        # 3-6L: 5%
        # 6-9L: 10%
        # 9-12L: 15%
        # 12-15L: 20%
        # >15L: 30%
        # Rebate up to 7L taxable income -> effectively 0
        taxable_new = taxable_base
        tax_new = 0
        if taxable_new <= 700000:
            tax_new = 0
        else:
            slabs = [
                (300000, 600000, 0.05),
                (600000, 900000, 0.10),
                (900000, 1200000, 0.15),
                (1200000, 1500000, 0.20),
                (1500000, float('inf'), 0.30)
            ]
            for bottom, top, rate in slabs:
                if taxable_new > bottom:
                    taxable_amount_in_slab = min(taxable_new, top) - bottom
                    tax_new += taxable_amount_in_slab * rate

        # Compare and decide
        potential_savings = abs(tax_old - tax_new)
        if tax_old < tax_new:
            recommended = "Old Regime"
        else:
            recommended = "New Regime"

        deductions = [
            "Section 80C: Up to ₹1.5 Lakhs (ELSS, PPF, EPF, LIC)",
            "Section 80D: Up to ₹25,000 for Health Insurance",
            "Section 24(b): Up to ₹2 Lakhs for Home Loan Interest"
        ]

        return TaxInfo(
            old_regime_tax=max(0, tax_old),
            new_regime_tax=max(0, tax_new),
            recommended_regime=recommended,
            potential_savings=potential_savings,
            deductions_suggested=deductions if recommended == "Old Regime" else ["New regime is better. Focus on pure wealth creation without locking capital in tax instruments."]
        )
