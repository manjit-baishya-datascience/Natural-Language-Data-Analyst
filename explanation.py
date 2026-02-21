from llm_interface import query_gemini


def build_explanation_prompt(question: str, pandas_code: str, result) -> str:
    return f"""
You are a data analyst.

The user asked:
{question}

The system executed this pandas expression:
{pandas_code}

The computed result is:
{result}

Explain the result clearly in simple English.

Be concise.
Do not mention internal system details.
"""


def generate_explanation(question: str, pandas_code: str, result: object) -> str:
    prompt = build_explanation_prompt(question, pandas_code, result)
    response = query_gemini(prompt)
    return response.strip()
