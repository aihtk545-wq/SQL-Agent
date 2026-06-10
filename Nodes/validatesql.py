FORBIDDEN = [
    "DELETE",
    "DROP",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"
]

def validate_sql(state):

    query = state["sql_query"].upper()

    for word in FORBIDDEN:
        if word in query:
            return {
                "error": f"Forbidden command: {word}"
            }

    return {
        "error": ""
    }