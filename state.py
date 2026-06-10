from typing import TypedDict

class AgentState(TypedDict):
    question: str

    tables: str
    schema: str

    sql_query: str
    sql_result: str

    answer: str
    error: str