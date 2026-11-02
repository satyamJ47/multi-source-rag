import re

from app.query_engines.base import QueryValidationError

FORBIDDEN_KEYWORDS = [
    "insert", "update", "delete", "drop", "alter", "create", "attach",
    "detach", "pragma", "vacuum", "reindex", "truncate", "grant", "revoke",
    "sqlite_master", "sqlite_schema",
]
_FORBIDDEN_RE = re.compile(r"\b(" + "|".join(FORBIDDEN_KEYWORDS) + r")\b", re.IGNORECASE)


def validate_select_only(sql: str) -> None:
    if not sql.strip():
        raise QueryValidationError("Empty query.")
    if ";" in sql:
        raise QueryValidationError("Multiple statements are not allowed.")
    if "--" in sql or "/*" in sql:
        raise QueryValidationError("SQL comments are not allowed.")
    if not re.match(r"\s*(select|with)\b", sql, re.IGNORECASE):
        raise QueryValidationError("Only SELECT queries are allowed.")
    found = _FORBIDDEN_RE.search(sql)
    if found:
        raise QueryValidationError(f"Forbidden keyword: {found.group(1).upper()}")

def extract_sql(text: str) -> str:
    text = text.strip()
    match = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    return text.rstrip(";").strip()