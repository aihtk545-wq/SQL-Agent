import pandas as pd
from db import engine

def execute_sql(state):

    if state.get("error"):
        return {}

    try:
        df = pd.read_sql(
            state["sql_query"],
            engine
        )

        return {
            "sql_result": df.to_string(),
            "error": ""
        }

    except Exception as e:

        return {
            "error": str(e)
        }