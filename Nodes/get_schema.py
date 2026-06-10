from sqlalchemy import text

def get_schema(state):

    sql = """
    SELECT
        TABLE_NAME,
        COLUMN_NAME,
        DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql)).fetchall()

    schema_text = "\n".join(
        f"{r[0]}.{r[1]} ({r[2]})"
        for r in rows
    )

    return {
        "schema": schema_text
    }