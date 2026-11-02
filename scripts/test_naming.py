# from app.query_engines.naming import make_table_name

# print(make_table_name("Sales 2024.xlsx", "Q1 Revenue"))
# print(make_table_name("2024 data.xlsx", "Sheet1"))
# print(make_table_name("x; DROP &$TABLE y.xlsx", "!!!"))

# import re

# text = "q1 - revenue (%)"
# print(re.sub(r"[^a-z0-9]+", "_", text))   # with +
# print(re.sub(r"[^a-z0-9]", "_", text))    # without +

from app.query_engines.naming import clean_columns
print(clean_columns(["Total $", "Total %", "Order Date", 2024, "Total $"]))