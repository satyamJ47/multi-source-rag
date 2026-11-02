import sqlite3
from app.query_engines.sqlite_loader import load_excel_to_sqlite, DB_PATH

print(load_excel_to_sqlite("./data/students.xlsx"))
print(load_excel_to_sqlite("./data/students.xlsx"))  # second run: re-ingestion

conn = sqlite3.connect(DB_PATH)
print("select * from _sources")
print(conn.execute("SELECT * FROM _sources").fetchall())
tables = conn.execute("SELECT table_name FROM _sources").fetchall()
print("tables: ",tables)
table = tables[0][0]
print("table: ",table)
print("count * from ")
print(conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone())
print("Avg of total ")
print(conn.execute('''SELECT "t_" FROM (
  SELECT "t_", "maths", ROW_NUMBER() OVER (ORDER BY "maths" DESC) AS rn
  FROM (
    SELECT "t_", "maths" FROM "students__div_a"
    UNION ALL
    SELECT "t_", "maths" FROM "students__div_b"
  )
) WHERE rn = 3''').fetchone())
conn.close()