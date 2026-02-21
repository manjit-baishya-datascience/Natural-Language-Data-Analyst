import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

_api_key = None
_model = None


def configure(api_key: str = None, model_name: str = "gemini-2.5-flash"):
    """Configure the Gemini client. Reads `GEMINI_API_KEY` from env if not provided."""
    global _api_key, _model

    if api_key:
        _api_key = api_key
    else:
        _api_key = os.getenv("GEMINI_API_KEY")

    if not _api_key:
        raise ValueError("GEMINI_API_KEY not set in environment.")

    genai.configure(api_key=_api_key)
    _model = genai.GenerativeModel(model_name)
    return _model


def _ensure_model():
    global _model
    if _model is None:
        configure()
    return _model


def query_gemini(prompt: str) -> str:
    model = _ensure_model()
    response = model.generate_content(prompt)
    return response.text


def extract_json_block(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        return text[start:end+1]
    return text


def parse_llm_output(raw_output: str):
    import json
    try:
        json_str = extract_json_block(raw_output)
        return json.loads(json_str)
    except Exception as e:
        print("JSON Parsing Failed:", e)
        print("Raw Output:\n", raw_output)
        return None
