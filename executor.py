import ast
import numpy as np
import pandas as pd

FORBIDDEN_KEYWORDS = [
    "import",
    "__",
    "exec",
    "eval",
    "open",
    "write",
    "read",
    "os",
    "sys",
    "subprocess",
    "pickle",
    "to_csv",
    "to_excel"
]


def basic_safety_check(code: str):
    for word in FORBIDDEN_KEYWORDS:
        if word in code:
            raise ValueError(f"Unsafe keyword detected: {word}")


def ast_validate(code: str) -> bool:
    try:
        tree = ast.parse(code, mode="eval")  # only expressions allowed
    except Exception:
        raise ValueError("Code is not a valid single expression.")

    for node in ast.walk(tree):

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Imports not allowed.")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id not in ["len", "sum", "min", "max"]:
                    # Allow pandas method calls via df only
                    pass

        if isinstance(node, ast.Name):
            if node.id not in ["df", "len", "sum", "min", "max"]:
                raise ValueError(f"Unauthorized variable: {node.id}")

    return True


def normalize_result(result):
    # Convert numpy scalars to native Python
    if isinstance(result, (np.integer, np.int64)):
        return int(result)

    if isinstance(result, (np.floating, np.float64)):
        return float(result)

    # Convert pandas Series
    if isinstance(result, pd.Series):
        return result.to_dict()

    # Convert pandas DataFrame
    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")

    return result


def safe_execute(code: str, df):
    basic_safety_check(code)
    ast_validate(code)

    allowed_builtins = {
        "len": len,
        "sum": sum,
        "min": min,
        "max": max
    }

    safe_globals = {"__builtins__": allowed_builtins}
    safe_locals = {"df": df}

    try:
        result = eval(code, safe_globals, safe_locals)
        return normalize_result(result)
    except Exception as e:
        raise RuntimeError(f"Execution error: {e}")
