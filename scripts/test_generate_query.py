from dotenv import load_dotenv
load_dotenv()

from app.query_engines.sqlite_engine import SQLiteQueryEngine

engine = SQLiteQueryEngine()
schema = engine.describe_schema()

questions = [
    "Who is 3rd topper?",
    "What is the average of Science",
    "Who is 3rd highest in Maths",
    "What is the weather in Pune?",
]

for q in questions:
    print("Q:", q)
    print("SQL:", engine.generate_query(q, schema))
    print()