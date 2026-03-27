# System Architecture: FinPilot AI

## System Diagram

```mermaid
graph TD
    UI[Frontend: Streamlit] --> |JSON Payload| API[Backend: FastAPI]
    API --> ORCH[FinPilotOrchestrator]
    
    ORCH --> PA[Profile Agent]
    PA --> |ProfileData| ORCH
    
    ORCH --> SA[Scoring Agent]
    SA --> |HealthScore| ORCH
    
    ORCH --> PLA[Planning Agent]
    PLA --> |FinancialPlan| ORCH
    
    ORCH --> TA[Tax Agent]
    TA --> |TaxOptimization| ORCH
    
    ORCH --> RA[Recommendation Agent (LLM)]
    RA -.-> |API Call| OAI[(OpenAI GPT-3.5)]
    OAI -.-> RA
    RA --> |Insights String| ORCH
    
    ORCH --> |FinalReport JSON| API
    API --> UI
```

## Agent Interactions and Data Flow

1. **User Input:** The frontend collects 9 key financial metrics from the user and passes them to the API via POST `/analyze`.
2. **Profile Generation:** `Profile Agent` reads `UserInput` and derives ratios: Debt-to-Income, Savings Rate, Emergency MoM, Insurance Multiple.
3. **Scoring Engine:** Using the `ProfileData`, the `Scoring Agent` computes points across 5 dimensions (Emergency Fund, Insurance, Debt, Savings, Retirement). It enforces deterministic, rule-based caps per category (20 max points each) to ensure the system cannot hallucinate a good score.
4. **Planning Engine:** `Planning Agent` reads `UserInput` and `ProfileData` to determine asset allocation (100-minus-age rule, adjusted for DTI limits) and recommends a monthly Systematic Investment Plan (SIP) target.
5. **Tax Optimization:** `Tax Agent` models the complex Indian tax regime (Old vs. New standard logic roughly simulating FY23-24). It mathematically decides which regime is mathematically superior.
6. **Recommendation Synthesis:** All aggregated JSON outputs flow into the `Recommendation Agent`. This agent compiles a structured prompt, injecting the raw metrics to bound the LLM within reality, yielding safe, actionable, personalized advice.
7. **Delivery:** The `FinalReport` object is compiled by the orchestrator and returned to the frontend.

## Error Handling Approach
- Pydantic models validate input types before any agent acts, preventing logic breaks on dirty data.
- The `orchestration.py` runs inside a try-catch block during the API call, defaulting to an HTTP 400/500 JSON response on error.
- The Streamlit App gracefully catches `requests.exceptions` and provides a localized fallback to execute the orchestrator directly, ensuring demo resilience.
- LLM connectivity is handled defensively in `utils/llm_helper.py`, falling back to a sophisticated static mock string if the OpenAI API is unreachable or keys are missing.
