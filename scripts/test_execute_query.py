from app.query_engines.sqlite_engine import SQLiteQueryEngine

engine = SQLiteQueryEngine()
sql = 'SELECT "name", "total" FROM "students__div_b" ORDER BY "total" DESC LIMIT 2'
engine.validate_query(sql)
print(engine.execute_query(sql))