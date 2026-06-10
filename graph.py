from langgraph.graph import StateGraph, START, END
from state import AgentState
from Nodes.list_tables import list_tables
from Nodes.get_schema import get_schema
from Nodes.generate_sql import generate_sql
from Nodes.validatesql import validate_sql
from Nodes.execute_sql import execute_sql
from Nodes.generate_reply import generate_reply

builder = StateGraph(AgentState)

builder.add_node("list_tables", list_tables)
builder.add_node("get_schema", get_schema)
builder.add_node("generate_sql", generate_sql)
builder.add_node("validate_sql", validate_sql)
builder.add_node("execute_sql", execute_sql)
builder.add_node("generate_reply", generate_reply)



builder.add_edge(START, "list_tables")

builder.add_edge(
    "list_tables",
    "get_schema"
)

builder.add_edge(
    "get_schema",
    "generate_sql"
)

builder.add_edge(
    "generate_sql",
    "validate_sql"
)

builder.add_edge(
    "validate_sql",
    "execute_sql"
)

builder.add_edge(
    "execute_sql",
    "generate_reply"
)

builder.add_edge(
    "generate_reply",
    END
)



graph = builder.compile()


print("SQL Agent ready! Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        break
    if not question:
        continue

    result = graph.invoke({"question": question})
    print(f"\nAgent: {result.get('answer', result.get('error', 'No response'))}\n")