import json
import math
from pathlib import Path

import pandas as pd
import sys

EXCEL = "data/students.xlsx"
# EVAL_FILE = "eval/questions.json"
# EVAL_FILE = "eval/heldout.json"
# EVAL_FILE = "eval/heldout2.json"
EVAL_FILE = sys.argv[1] if len(sys.argv) > 1 else "eval/questions.json"
ORDERED = {"R4"}  # questions where the order of the answer matters

a = pd.read_excel(EXCEL, sheet_name="Div A")
b = pd.read_excel(EXCEL, sheet_name="Div B")
both = pd.concat([a, b], ignore_index=True)


def third_highest_science():
    third = sorted(both["Science"].unique(), reverse=True)[2]
    return both.loc[both["Science"] == third, "Name"].tolist()

def second_lowest_total():
    second = sorted(both["Total"].unique())[1]
    return both.loc[both["Total"] == second, "Name"].tolist()

def nth_distinct(col, n, ascending=False):
    value = sorted(both[col].unique(), reverse=not ascending)[n - 1]
    return both.loc[both[col] == value, "Name"].tolist()

def top_n_distinct(col, n, ascending=False):
    values = sorted(both[col].unique(), reverse=not ascending)[:n]
    return both.loc[both[col].isin(values), "Name"].tolist()

# question id -> function that computes the answer with pandas
PANDAS_ANSWERS = {
    "L1": lambda: both.loc[both["Name"] == "Chloe", "Maths"].tolist(),
    "L2": lambda: both.loc[both["Name"] == "Hannah", "Science"].tolist(),
    "L3": lambda: both.loc[both["Name"] == "David", "Total"].tolist(),
    "L4": lambda: both.loc[both["Name"] == "Julia", "Geography"].tolist(),
    "A1": lambda: [float(a["Maths"].mean())],
    "A2": lambda: [float(b["Science"].mean())],
    "A3": lambda: [float(both["English"].mean())],
    "A4": lambda: [int(a["History"].sum())],
    "A5": lambda: [int((both["Maths"] > 90).sum())],
    "A6": lambda: [len(both)],
    "A7": lambda: [float(both["Total"].mean())],
    "R1": lambda: both.loc[both["Maths"] == both["Maths"].max(), "Name"].tolist(),
    "R2": lambda: both.loc[both["Total"] == both["Total"].max(), "Name"].tolist(),
    "R3": third_highest_science,
    "R4": lambda: both.nlargest(3, "Total")["Name"].tolist(),
    "R5": lambda: both.loc[both["Science"] == both["Science"].min(), "Name"].tolist(),
    "R6": lambda: a.loc[a["Total"] == a["Total"].max(), "Name"].tolist(),
    "R7": lambda: both.loc[both["English"] == both["English"].max(), "Name"].tolist(),
    "R8": second_lowest_total,
    "H1": lambda: nth_distinct("History", 2, ascending=True),
    "H2": lambda: nth_distinct("Maths", 5),
    "H3": lambda: top_n_distinct("Science", 2, ascending=True),
    "H4": lambda: [int((both["History"] < 70).sum())],
    "H5": lambda: nth_distinct("English", 5),
    "H6": lambda: b.loc[b["Geography"] == b["Geography"].max(), "Name"].tolist(),
    "H7": lambda: top_n_distinct("Total", 3, ascending=True),
    "H8": lambda: top_n_distinct("Maths", 6),
    "H9": lambda: top_n_distinct("History", 2, ascending=True),
}


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


data = json.loads(Path(EVAL_FILE).read_text(encoding="utf-8"))
passed = failed = skipped = 0

for q in data["questions"]:
    qid = q["id"]
    print(f'{qid} [{q["type"]}] {q["question"]}')
    print(f'   expected (eval file): {q["expected"]}')

    if qid not in PANDAS_ANSWERS:
        print("   pandas              : not computable with pandas, skipped\n")
        skipped += 1
        continue

    actual = PANDAS_ANSWERS[qid]()
    ok = same(q["expected"], actual, qid in ORDERED)
    print(f"   pandas              : {actual}")
    print(f"   {'PASS' if ok else 'FAIL'}\n")
    if ok:
        passed += 1
    else:
        failed += 1

print(f"Passed: {passed}  Failed: {failed}  Skipped: {skipped}")