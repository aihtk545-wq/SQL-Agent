from sqlalchemy import text
from db import engine

def get_schema(state):

    col_sql = """
    SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    """

    fk_sql = """
    SELECT
        fk.TABLE_NAME,
        cu.COLUMN_NAME,
        pk.TABLE_NAME AS REFERENCED_TABLE,
        pt.COLUMN_NAME AS REFERENCED_COLUMN
    FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS rc
    JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS fk ON rc.CONSTRAINT_NAME = fk.CONSTRAINT_NAME
    JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS pk ON rc.UNIQUE_CONSTRAINT_NAME = pk.CONSTRAINT_NAME
    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE cu ON rc.CONSTRAINT_NAME = cu.CONSTRAINT_NAME
    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE pt ON rc.UNIQUE_CONSTRAINT_NAME = pt.CONSTRAINT_NAME
    """

    with engine.connect() as conn:
        col_rows = conn.execute(text(col_sql)).fetchall()
        fk_rows = conn.execute(text(fk_sql)).fetchall()

    schema_text = "\n".join(f"{r[0]}.{r[1]} ({r[2]})" for r in col_rows)

    fk_text = "\n".join(
        f"{r[0]}.{r[1]} -> {r[2]}.{r[3]}"
        for r in fk_rows
    )

    return {
        "schema": f"Columns:\n{schema_text}\n\nRelationships:\n{fk_text}"
    }
