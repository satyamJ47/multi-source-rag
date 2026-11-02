import re
from pathlib import Path

def to_identifier(name:str)->str:
    name = name.strip().lower()
    # print("start",name)
    name = re.sub(r"[^a-z0-9]+","_",name)   # runs of non-alphanumerics -> one underscore
    # print("before: ",name)
    name = name.strip("_")
    # print("after: ",name)
    if not name or name[0].isdigit():
        name = "t_" + name      # SQL identifiers shouldn't start with a digit
    return name

def make_table_name(source_name: str, sheet_name: str) ->  str:
    stem = Path(source_name).stem    # "Sales 2024.xlsx" -> "Sales 2024"
    # print(stem)
    return f"{to_identifier(stem)}__{to_identifier(sheet_name)}"

def clean_columns(columns) -> list[str]:
    seen: dict[str, int] = {}
    result = []
    for col in columns:
        base = to_identifier(str(col))
        seen[base] = seen.get(base, 0) + 1
        result.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    return result