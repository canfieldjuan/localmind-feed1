import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

AGENTS = {
    "strategist": "You are a strategic thinker helping with planning and high-level goals.",
    "coder": "You are a Python expert assisting with code development and debugging.",
    "analyst": "You analyze and interpret data trends accurately.",
    "toolmaster": "You have access to tools and can use them when needed.",
    "sentinel": "You analyze sentiment and report it concisely.",
    "planner": "You break down tasks and route them to the right agents for execution."
}

def call_agent(agent, input_text):
    prompt = AGENTS.get(agent, "") + f"\nUser: {input_text}\nAgent:"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Chained Agent Error: {e}"
