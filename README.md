# FinPilot AI – Personal Money Mentor 💸

## Project Explanation
FinPilot AI is a multi-agent AI framework designed specifically to solve the financial planning gap for the 95% of Indians without structured financial guidance. Instead of being a generic LLM chatbot, FinPilot AI breaks down complex financial logic into dedicated, purpose-driven AI agents running in a deterministic pipeline. It evaluates money health, proposes actionable goal-based plans, optimizes tax using Indian dual-regime specifics, and serves the results via a hyper-personalized, human-like recommendation agent.

## Architecture
This project uses a pipeline architecture powered by FastAPI and Streamlit, incorporating five distinct agents:
1. **Profile Agent:** Normalizes user inputs and extracts hidden metrics like Debt-to-Income and Savings Ratios.
2. **Scoring Agent:** A rule-based scoring engine calculating a 'Money Health Score' out of 100 based on rigorous heuristics.
3. **Planning Agent:** Creates a FIRE-aligned investment roadmap determining asset allocation and SIPs based on age and surplus.
4. **Tax Agent:** Compares Indian Old vs. New tax regimes.
5. **Recommendation Agent (LLM):** Consolidates all deterministic outputs into friendly, actionable advice using OpenAI (or a sophisticated fallback).

For deeper details, view `docs/ARCHITECTURE.md`.

## Setup Steps
1. Navigate to the project root: `cd C:/Groot/ETGenAi/finpilot`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Provide OPENAI_API_KEY environment variable. If missing, it will use a mock response mechanism to still prove the pipeline.
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-key"
   ```

4. Run the Backend API (Terminal 1):
   ```bash
   uvicorn backend.main:app --reload
   ```

5. Run the Frontend App (Terminal 2):
   ```bash
   streamlit run frontend/app.py
   ```

## Sample Input / Output
**Input:** Age 30, Income 1,00,000, Expenses 40,000, Savings 2,00,000, Total Debt 3,00,000.  
**Output:** Health Score indicates 'Good' (around 70/100). Tax Engine correctly recommends 'New Regime' as investments might not exceed standard limits to beat the rebate. Recommendation Agent synthesizes this into actionable 3-step insights.
