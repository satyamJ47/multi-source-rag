import json
import math
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from app.query_engines.base import CANNOT_ANSWER
from app.query_engines.sqlite_engine import SQLiteQueryEngine

import sys

EVAL_FILE = sys.argv[1] if len(sys.argv) > 1 else "eval/questions.json"
RESULTS_FILE = sys.argv[2] if len(sys.argv) > 2 else "eval/results_sql.json"
ORDERED = {"R4"}      # questions where answer order matters
PAUSE_SECONDS = 10     # gentle on free-tier rate limits


def same(expected, actual, ordered):
    if len(expected) != len(actual):
        return False
    if not ordered:
        expected = sorted(expected, key=str)
        actual = sorted(actual, key=str)
    for e, x in zip(expected, actual):
        if isinstance(e, (int, float)) and isinstance(x, (int, float)):
            if not math.isclose(e, x, abs_tol=1e-6):
                return False
        elif e != x:
            return False
    return True


def first_column(rows):
    # each row is a dict in column order; take its first value
    return [next(iter(row.values())) for row in rows]


def generate_with_retry(engine, question, schema, tries=3):
    for attempt in range(tries):
        try:
            return engine.generate_query(question, schema)
        except Exception as e:
            if "RateLimit" in type(e).__name__ and attempt < tries - 1:
                time.sleep(20 * (attempt + 1))   # wait 20s, then 40s
                continue
            raise

def run_one(engine, schema, q):
    result = {"id": q["id"], "type": q["type"], "question": q["question"],
              "sql": None, "rows": None, "error": None, "passed": False}
    try:
        sql = generate_with_retry(engine, q["question"], schema)
        result["sql"] = sql
        if sql.strip() == CANNOT_ANSWER:
            result["rows"] = [{"answer": CANNOT_ANSWER}]
        else:
            engine.validate_query(sql)
            result["rows"] = engine.execute_query(sql)
        actual = first_column(result["rows"])
        result["passed"] = same(q["expected"], actual, q["id"] in ORDERED)
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {e}"
    return result


data = json.loads(Path(EVAL_FILE).read_text(encoding="utf-8"))
engine = SQLiteQueryEngine()
schema = engine.describe_schema()
results = []

for q in data["questions"]:
    r = run_one(engine, schema, q)
    results.append(r)
    print(f'{r["id"]} {"PASS" if r["passed"] else "FAIL"}  {q["question"]}')
    if not r["passed"]:
        print("   expected:", q["expected"])
        print("   sql     :", r["sql"])
        print("   rows    :", r["rows"])
        print("   error   :", r["error"])
    time.sleep(PAUSE_SECONDS)

by_type = defaultdict(lambda: [0, 0])  # type -> [passed, total]
for r in results:
    by_type[r["type"]][1] += 1
    if r["passed"]:
        by_type[r["type"]][0] += 1

print("\nResults by question type:")
for qtype, (ok, total) in by_type.items():
    print(f"  {qtype:<13} {ok}/{total}")
print(f"  {'OVERALL':<13} {sum(r['passed'] for r in results)}/{len(results)}")

Path(RESULTS_FILE).write_text(json.dumps(results, indent=2), encoding="utf-8")
print(f"\nSaved details to {RESULTS_FILE}")