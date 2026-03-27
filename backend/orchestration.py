import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import UserInput, FinalReport
from agents.profile_agent import ProfileAgent
from agents.scoring_agent import ScoringAgent
from agents.planning_agent import PlanningAgent
from agents.tax_agent import TaxAgent
from agents.recommendation_agent import RecommendationAgent

class FinPilotOrchestrator:
    def __init__(self):
        self.profile_agent = ProfileAgent()
        self.scoring_agent = ScoringAgent()
        self.planning_agent = PlanningAgent()
        self.tax_agent = TaxAgent()
        self.recommendation_agent = RecommendationAgent()

    def run_pipeline(self, user_input: UserInput) -> FinalReport:
        """
        Executes the multi-agent pipeline and returns a FinalReport.
        """
        # 1. Profile Creation
        profile_data = self.profile_agent.process_profile(user_input)
        
        # 2. Score Calculation
        health_score = self.scoring_agent.calculate_health_score(user_input, profile_data)
        
        # 3. Financial Planning
        plan = self.planning_agent.compute_plan(user_input, profile_data)
        
        # 4. Tax Optimization
        tax_info = self.tax_agent.calculate_tax(user_input)
        
        # 5. LLM Recommendations
        insights = self.recommendation_agent.generate_recommendations(user_input, health_score, plan, tax_info)
        
        return FinalReport(
            health_score=health_score,
            financial_plan=plan,
            tax_optimization=tax_info,
            ai_insights=insights
        )
