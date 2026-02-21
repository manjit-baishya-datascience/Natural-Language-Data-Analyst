# LLM-powered Data Analyst (Streamlit)

Professional, production-ready Streamlit application that wraps an LLM-backed data analysis pipeline. The app accepts uploaded datasets, runs a guarded LLM prompt to generate safe pandas expressions, executes them inside a sandboxed evaluator, repairs failing expressions via an LLM repair loop, and returns results with a human-readable explanation.

---

## Features

- Accepts CSV, TSV, Parquet, and JSON uploads and saves them to `data/`.
- Extracts dataset schema and metadata for prompt context.
- Uses a dedicated LLM interface (`llm_interface.py`) — API keys are never exposed in the UI.
- Enforces a strict safety pipeline: static keyword checks, AST validation (only single expressions), and sandboxed `eval` with tightly controlled builtins.
- Automatic repair loop that requests corrected pandas expressions from the LLM when execution fails.
- Daily logging with per-day log files written to `logs/YYYY-MM-DD.log`.
- UI shows the computed result, explanation, generated pandas code and raw LLM output (for debugging), with collapsible sections.

---

## Repository layout

- `app.py` — Streamlit UI and orchestration.
- `schema_extractor.py` — schema extraction and sample rows.
- `prompt_builder.py` — constructs LLM prompts using dataset metadata.
- `llm_interface.py` — encapsulates Gemini API calls and parsing.
- `executor.py` — safety checks, AST validation, sandboxed execution and normalization.
- `repair_loop.py` — automatic repair loop for retrying corrected expressions.
- `explanation.py` — builds explanation prompts and requests explanations from the LLM.
- `logger.py` — logging helper that writes daily log files to `logs/`.
- `requirements.txt` — minimal dependency list.
- `data/` — where uploaded datasets are stored (created at runtime).
- `logs/` — daily log files are stored here (created at runtime).

---

## Security & Safety

- The app never exposes the Gemini API key in the UI. Always provide the key via environment variables.
- Core safety layers are preserved:
  - Keyword blacklist (`FORBIDDEN_KEYWORDS`).
  - AST validation that ensures only a single expression and restricts allowed names.
  - Sandboxed execution via `eval` with a reduced `__builtins__` mapping containing only safe callables (`len`, `sum`, `min`, `max`).
- Do not modify these layers unless you understand the security implications.

---

## Installation

1. Create and activate a virtual environment (recommended):

   Windows (PowerShell):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r "requirements.txt"
   ```

3. Set your Gemini API key as an environment variable (example, PowerShell):

   ```powershell
   $env:GEMINI_API_KEY = "your_api_key_here"
   ```

   Important: never commit API keys to source control.

---

## Running the app

Start the Streamlit application:

```powershell
streamlit run "app.py"
```

The web UI will allow file upload and running natural-language questions against the dataset.

---

## Logging

- All app activity (uploads, errors, successful runs) is logged to `logs/YYYY-MM-DD.log`.
- The `logger.py` utility configures a rotating-per-day file named by ISO date and also writes to the console.

---

## Operational notes

- Supported file types: `.csv`, `.tsv`, `.parquet`, `.json`.
- Uploaded files are saved to `data/` using their original filenames.
- Prompts sent to the LLM contain dataset metadata but never include secrets or raw API keys.

---

## Development

- To run a quick lint/import check locally, run your favorite linter (e.g., `flake8`) against the repository.
- Unit tests are not included by default; consider adding tests for `executor.py` safety checks and `repair_loop.py` behavior.

---

## Contributing

Contributions are welcome. Please open issues or pull requests. When contributing, ensure:

- Safety and sandboxing logic in `executor.py` and `repair_loop.py` are preserved.
- Secrets (API keys) are never checked into source control.

---

## License

This project is released under the MIT License. See the `LICENSE` file at the repository root for the full license text. The MIT License allows reuse, modification and distribution with attribution; it is a permissive license well-suited for prototypes and internal tooling.

If you intend to relicense or redistribute this project under different terms, update the `LICENSE` file accordingly and ensure contributors agree to the new terms.
