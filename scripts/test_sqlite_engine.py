from app.query_engines.sqlite_engine import SQLiteQueryEngine

engine = SQLiteQueryEngine()
print(engine.describe_schema())

# Writes must be blocked by the read-only connection
# conn = engine._connect()
# try:
#     conn.execute("CREATE TABLE hack (x INTEGER)")
#     # data = conn.execute("SELECT * FROM std_6th__div_a LIMIT 3").fetchall()
#     # print(data)
# except Exception as e:
#     print("Good, write blocked:", e)
# finally:
#     conn.close()