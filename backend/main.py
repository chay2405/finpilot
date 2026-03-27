import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models import (
    UserInput, FinalReport, 
    LifeEventRequest, CoupleInput, CoupleReport,
    TaxWizardInput, MFXRayRequest, MFXRayReport
)
from backend.orchestration import FinPilotOrchestrator
from agents.life_event_agent import LifeEventAgent
from agents.couple_agent import CoupleAgent
from agents.tax_wizard_agent import TaxWizardAgent
from agents.mf_xray_agent import MFXRayAgent

app = FastAPI(title="FinPilot AI API v2", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

orchestrator = FinPilotOrchestrator()
life_event_agent = LifeEventAgent()
couple_agent = CoupleAgent()
tax_wizard_agent = TaxWizardAgent()
mf_xray_agent = MFXRayAgent()

@app.post("/analyze", response_model=FinalReport)
def analyze_finances(user_input: UserInput):
    """ Main FIRE & Money Health Pipeline """
    try:
        return orchestrator.run_pipeline(user_input)
    except Exception as e:
        return {"error": str(e)}

@app.post("/life-event", response_model=dict)
def analyze_life_event(req: LifeEventRequest):
    try:
        advice = life_event_agent.evaluate_life_event(req)
        return {"advice": advice}
    except Exception as e:
        return {"error": str(e)}

@app.post("/tax-wizard", response_model=dict)
def analyze_tax_wizard(req: TaxWizardInput):
    try:
        return tax_wizard_agent.evaluate_tax(req)
    except Exception as e:
        return {"error": str(e)}

@app.post("/couple-planner", response_model=CoupleReport)
def analyze_couple(req: CoupleInput):
    try:
        return couple_agent.evaluate_couple(req)
    except Exception as e:
        return {"error": str(e)}

@app.post("/mf-xray", response_model=MFXRayReport)
def analyze_mf_xray(req: MFXRayRequest):
    try:
        return mf_xray_agent.evaluate_portfolio(req)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
