import json
from llm_interface import query_gemini, parse_llm_output
from executor import safe_execute


def execute_with_repair(parsed_output: dict, df, dataset_info: dict, question: str, max_retries: int = 2):
    current_output = parsed_output

    for attempt in range(max_retries + 1):
        code = current_output["pandas_code"]

        try:
            result = safe_execute(code, df)
            return result, current_output

        except Exception as e:
            print(f"Attempt {attempt+1} failed.")
            print("Error:", str(e))

            if attempt == max_retries:
                raise RuntimeError("Max retries exceeded.")

            repair_prompt = f"""
The following pandas expression failed:

Expression:
{code}

Error:
{str(e)}

Dataset Metadata:
{json.dumps(dataset_info, indent=2)}

User Question:
{question}

Return corrected JSON with:
- analysis_type
- pandas_code
- reasoning

Return ONLY valid JSON.
"""

            raw = query_gemini(repair_prompt)
            repaired = parse_llm_output(raw)

            if repaired is None:
                raise RuntimeError("Repair output not parseable.")

            current_output = repaired
