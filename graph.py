from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from Nodes.list_tables import list_tables
from Nodes.get_schema import get_schema
from Nodes.execute_sql import run_sql

llm = ChatOllama(model="qwen3:8b")

tools = [list_tables, get_schema, run_sql]

agent = create_react_agent(llm, tools)

print("SQL Agent ready! Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        break
    if not question:
        continue

    result = agent.invoke({
        "messages": [("human", question)]
    })

    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                if tc["name"] == "run_sql":
                    print(f"\nSQL Query:\n{tc['args'].get('sql', '')}")
        if hasattr(msg, "name") and msg.name == "run_sql":
            print(f"\nSQL Result:\n{msg.content}")

    print(f"\nAgent: {result['messages'][-1].content}\n")
