import json


def build_prompt(dataset_info: dict, question: str) -> str:
    return f"""
You are a senior data analyst.

You are given:
1. Dataset metadata
2. A user question

Your task:
- Generate SAFE pandas code using ONLY dataframe `df`
- Do NOT import anything
- Do NOT assign variables
- Return a JSON object with keys:
    - analysis_type
    - pandas_code
    - reasoning

Rules:
- pandas_code must be a SINGLE expression
- No loops
- No comprehensions
- No file access
- No __ usage
- Only pandas operations on df

Dataset Metadata:
{json.dumps(dataset_info, indent=2)}

User Question:
{question}

Return ONLY valid JSON.
"""
