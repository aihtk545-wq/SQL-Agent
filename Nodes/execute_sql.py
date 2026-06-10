import re
import pandas as pd
from langchain_core.tools import tool
from db import engine

FORBIDDEN = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]

def clean_sql(sql: str) -> str:
    sql = re.sub(r"```sql|```", "", sql)
    sql = re.sub(r"\bLIMIT\s+\d+", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"\bTOP\s+\d+\s*;?\s*$", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"OFFSET\s+\d+\s+ROWS.*", "", sql, flags=re.IGNORECASE)
    return sql.strip().rstrip(";")

@tool
def run_sql(sql: str) -> str:
    """Validates and executes a T-SQL query against the database. Returns the result as a table."""

    sql = clean_sql(sql)

    for word in FORBIDDEN:
        if word in sql.upper():
            return f"Error: Forbidden command '{word}' is not allowed."

    try:
        df = pd.read_sql(sql, engine)
        return df.to_string()
    except Exception as e:
        return f"Error: {str(e)}"
