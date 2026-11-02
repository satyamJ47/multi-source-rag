from app.query_engines.base import QueryValidationError
from app.query_engines.sqlite_engine import SQLiteQueryEngine

engine = SQLiteQueryEngine()

good = [
    'SELECT AVG("maths") FROM "students__div_a"',
    'SELECT "name" FROM "students__div_b" ORDER BY "total" DESC LIMIT 1',
    'WITH t AS (SELECT "name" FROM "students__div_a") SELECT * FROM t',
]
bad = [
    'DROP TABLE "students__div_a"',
    'SELECT * FROM "students__div_a"; DROP TABLE "students__div_b"',
    'SELECT 1 -- sneaky',
    'UPDATE "students__div_a" SET "maths" = 100',
    'PRAGMA table_info("students__div_a")',
    'WITH t AS (SELECT 1) DELETE FROM "students__div_a"',
    'SELECT "marks" FROM "students__div_a"',      # hallucinated column
    'SELECT * FROM "students__div_z"',            # hallucinated table
    "",
]

for q in good:
    engine.validate_query(q)
    print("OK      :", q)

for q in bad:
    try:
        engine.validate_query(q)
        print("MISSED  :", q)
    except QueryValidationError as e:
        print("BLOCKED :", q, "->", e)