import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import LifeEventRequest
from utils.llm_helper import generate_insights_with_llm

class LifeEventAgent:
    def __init__(self):
        pass

    def evaluate_life_event(self, request: LifeEventRequest) -> str:
        """
        Provides specific advice on lump sum windfalls or life events 
        (bonus, inheritance, marriage, baby).
        """
        # We can lean on the LLM to structure this with our deterministic prompt constraints.
        prompt = f"""
        User is facing a life event: {request.event_type}
        Amount involved: ₹{request.event_amount}
        Additional Info: {request.additional_details}
        
        User Context:
        Age: {request.user_input.age}
        Income: ₹{request.user_input.monthly_income}
        Debt: ₹{request.user_input.total_debt}
        Savings: ₹{request.user_input.current_savings}
        
        Using financial best practices:
        1. Should they clear debt first?
        2. How much to allocate to emergency fund vs invesment?
        3. Are there tax implications?
        
        Provide a bulleted, step-by-step action plan tailored to this event. Keep it concise.
        """
        
        insights = generate_insights_with_llm(prompt)
        return insights
