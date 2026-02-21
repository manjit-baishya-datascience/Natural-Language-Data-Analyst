import pandas as pd


def extract_schema(df: pd.DataFrame) -> dict:
    schema = []

    for col in df.columns:
        schema.append({
            "column_name": col,
            "dtype": str(df[col].dtype),
            "non_null_count": int(df[col].notnull().sum()),
            "unique_values": int(df[col].nunique())
        })

    return {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": schema,
        "sample_rows": df.head(2).to_dict(orient="records")
    }
