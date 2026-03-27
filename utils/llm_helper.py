import os

def generate_insights_with_llm(context_text: str) -> str:
    """
    Simulates or calls an LLM to generate financial insights based on the context.
    If an OPENAI_API_KEY is present, it uses the real API.
    Otherwise, it returns a sophisticated mock response for the demo.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            import openai
            openai.api_key = api_key
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are FinPilot AI, a highly experienced personal money mentor. Provide clear, actionable, and encouraging financial advice based on the user's data provided."},
                    {"role": "user", "content": context_text}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error contacting LLM: {str(e)}"
    else:
        # Mock Response based on context for Demo
        lower_prompt = context_text.lower()
        if "life event" in lower_prompt or "bonus" in lower_prompt or "sudden" in lower_prompt:
            return "💡 **Life Event Strategy:**\n\n1. Move 30% of this amount into a liquid emergency fund.\n2. Use 40% to clear out high-interest debts.\n3. Invest the remaining 30% into your SIP goals."
        elif "couple" in lower_prompt or "partner" in lower_prompt:
            return "💡 **Joint Advice:**\n\nSince Partner 1 is in a higher tax bracket, they should claim the full HRA and Home Loan Interest deductions. You both should also maximize your individual ₹50k NPS tier-1 accounts."
        elif "mutual fund" in lower_prompt or "xirr" in lower_prompt or "overlap" in lower_prompt:
            return "💡 **Rebalancing Advice:**\n\nDrop the Kotak Emerging and Nippon Small Cap—they overlap heavily with SBI. Consolidate into 1 Index Fund (60%) and 1 Flexi Cap (40%) to reduce your massive fee drag."
        elif "tax" in lower_prompt or "gross" in lower_prompt:
            return "💡 **Tax Move Set:**\n\n- Immediately open an ELSS fund to plug the ₹20k gap in your 80C.\n- Buy a standard Medical plan to utilize 80D section.\n- Given current slabs, avoid complicated lock-ins if you prefer the New Regime."
        else:
            return (
                "🚀 **FinPilot AI Recommendations:**\n\n"
                "**1. Build your Emergency Fund:** Focus on redirecting some of your monthly surplus to a liquid sweep-in Fixed Deposit.\n\n"
                "**2. Optimize Your Investments:** Start the recommended SIP amount split across a Nifty 50 Index Fund (60%) and a Flexi Cap Fund (40%).\n\n"
                "**3. Insurance Gap:** Consider a pure term plan to secure your dependents.\n\n"
                "**4. Tax Planning:** Implement the recommended tax regime deductions."
            )
