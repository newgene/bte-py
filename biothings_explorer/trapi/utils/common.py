def remove_quotes_from_query(query_string):
    if query_string.startswith('"') and query_string.endswith('"'):
        return query_string[1:-1]
    elif query_string.startswith("'") and query_string.endswith("'"):
        return query_string[1:-1]
    else:
        return query_string
