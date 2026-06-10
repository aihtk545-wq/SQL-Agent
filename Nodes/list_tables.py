from sqlalchemy import text
from db import engine

def list_tables(state):

    sql = """
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE='BASE TABLE'
    """

    with engine.connect() as conn:
        rows = conn.execute(text(sql)).fetchall()

    tables = [r[0] for r in rows]

    return {
        "tables": "\n".join(tables)
    }