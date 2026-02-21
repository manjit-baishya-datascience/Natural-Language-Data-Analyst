import os
import streamlit as st
import pandas as pd

from schema_extractor import extract_schema
import prompt_builder
import llm_interface
import repair_loop
import explanation
import llm_interface as llm
from logger import get_logger


log = get_logger()


st.set_page_config(page_title="LLM Data Analyst", layout="wide")

st.title("LLM-powered Data Analyst")

st.markdown("Upload a dataset (CSV, TSV, Parquet, JSON). The file will be saved to `data/`.")

uploaded = st.file_uploader("Choose a file", type=["csv", "tsv", "parquet", "json"], accept_multiple_files=False)

df = None
dataset_info = None

if uploaded is not None:
    os.makedirs("data", exist_ok=True)
    save_path = os.path.join("data", uploaded.name)
    with open(save_path, "wb") as f:
        f.write(uploaded.getbuffer())
    log.info(f"File uploaded and saved: {uploaded.name}")

    try:
        name = uploaded.name.lower()
        if name.endswith(".csv"):
            df = pd.read_csv(save_path)
        elif name.endswith(".tsv"):
            df = pd.read_csv(save_path, sep="\t")
        elif name.endswith(".parquet"):
            df = pd.read_parquet(save_path)
        elif name.endswith(".json"):
            df = pd.read_json(save_path)
        else:
            df = pd.read_csv(save_path)

    except Exception as e:
        st.error(f"Failed to read uploaded file: {e}")
        log.error(f"Failed to read uploaded file {uploaded.name}: {e}", exc_info=True)

if df is not None:
    st.subheader("Preview")
    st.dataframe(df.head())

    dataset_info = extract_schema(df)
    with st.expander("Dataset Metadata"):
        st.json(dataset_info)

    question = st.text_input("Ask a question about the dataset")

    if st.button("Run"):
        if not question:
            st.warning("Please enter a question.")
        else:
            log.info(f"Processing question for file {uploaded.name}")
            try:
                # Build prompt and call LLM via llm_interface
                prompt = prompt_builder.build_prompt(dataset_info, question)

                log.info("Calling LLM for question (prompt not logged)")
                raw_output = llm_interface.query_gemini(prompt)
                parsed = llm_interface.parse_llm_output(raw_output)

                if parsed is None:
                    st.error("LLM output could not be parsed as JSON.")
                    log.warning("LLM output could not be parsed as JSON for question")
                else:
                    result, final_output = repair_loop.execute_with_repair(parsed, df, dataset_info, question)

                    explanation_text = explanation.generate_explanation(
                        question, final_output.get("pandas_code", ""), result
                    )

                    st.subheader("Result")
                    st.json(result)

                    st.subheader("Explanation")
                    st.write(explanation_text)

                    with st.expander("Generated pandas code"):
                        st.code(final_output.get("pandas_code", ""))

                    with st.expander("Raw LLM Output"):
                        st.text(raw_output)

                    log.info(f"Processing succeeded for question: {question}")

            except Exception as e:
                st.error(f"Processing failed: {e}")
                log.error(f"Processing failed for question: {question}: {e}", exc_info=True)

else:
    st.info("Upload a file to begin.")
