from pydantic import BaseModel
from typing import List, Optional, Dict

class UserInput(BaseModel):
    age: int
    monthly_income: float
    monthly_expenses: float
    current_savings: float
    current_investments: float
    total_debt: float
    insurance_coverage: float
    target_retirement_age: int
    financial_goals: List[str]

class ProfileData(BaseModel):
    monthly_surplus: float
    debt_to_income_ratio: float
    savings_ratio: float
    emergency_fund_months: float
    insurance_multiple: float

class HealthScore(BaseModel):
    score: int
    breakdown: Dict[str, int]
    status: str

class Plan(BaseModel):
    recommended_sip: float
    asset_allocation: Dict[str, int]
    emergency_fund_target: float
    years_to_retirement: int

class TaxInfo(BaseModel):
    old_regime_tax: float
    new_regime_tax: float
    recommended_regime: str
    potential_savings: float
    deductions_suggested: List[str]

class FinalReport(BaseModel):
    health_score: HealthScore
    financial_plan: Plan
    tax_optimization: TaxInfo
    ai_insights: str

class LifeEventRequest(BaseModel):
    user_input: UserInput
    event_type: str
    event_amount: float
    additional_details: str

class CoupleInput(BaseModel):
    partner_1: UserInput
    partner_2: UserInput
    joint_goals: List[str]

class TaxWizardInput(BaseModel):
    basic_salary: float
    hra: float
    lta: float
    special_allowance: float
    provident_fund: float
    home_loan_interest: float
    health_insurance_premium: float
    other_80c: float

class MFXRayRequest(BaseModel):
    statement_text: str

class CoupleReport(BaseModel):
    total_net_worth: float
    hra_optimization: str
    nps_optimization: str
    sip_splits: str
    insurance_strategy: str

class MFXRayReport(BaseModel):
    xirr: float
    overlap_warning: str
    expense_ratio_drag: float
    benchmark_comparison: str
    rebalancing_plan: str
