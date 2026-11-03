import json
import math
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import pandas as pd

from app.connectors.connector_factory import ConnectorFactory
from app.generation.llm_client import get_llm_client
from app.generation.prompt_builder import build_prompt
from app.processing.chunker import chunk_documents
from app.retrieval.retriever import Retriever
from app.vectorstore.chroma_store import ChromaVectorStore

EXCEL = "data/students.xlsx"
COLLECTION = "eval_baseline"   # separate from the main "rag_chunks" collection
PAUSE_SECONDS = 5

NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
REFUSAL_RE = re.compile(
    r"don['\u2019]?t have enough|do not have enough|not enough information|"
    r"cannot|can['\u2019]?t|unable|no information|not (?:provided|available|mentioned)",
    re.IGNORECASE,
)


def has_name(answer: str, name: str) -> bool:
    return re.search(rf"\b{re.escape(name)}\b", answer, re.IGNORECASE) is not None


def has_number(answer: str, value) -> bool:
    numbers = [float(n) for n in NUMBER_RE.findall(answer)]
    return any(math.isclose(n, float(value), abs_tol=0.05) for n in numbers)


def score(expected: list, answer: str, all_names: set) -> tuple[bool, bool]:
    """Returns (lenient, strict)."""
    if expected == ["CANNOT_ANSWER"]:
        ok = REFUSAL_RE.search(answer) is not None
        return ok, ok
    if all(isinstance(x, str) for x in expected):
        found = all(has_name(answer, n) for n in expected)
        extra = [n for n in all_names if n not in expected and has_name(answer, n)]
        return found, found and not extra
    ok = all(has_number(answer, x) for x in expected)
    return ok, ok


def generate_with_retry(prompt: str, tries: int = 3) -> str:
    llm = get_llm_client()
    for attempt in range(tries):
        try:
            return llm.generate(prompt)
        except Exception as e:
            if "RateLimit" in type(e).__name__ and attempt < tries - 1:
                time.sleep(20 * (attempt + 1))
                continue
            raise


def ask(retriever: Retriever, question: str, top_k: int):
    chunks = retriever.retrieve(question, top_k)
    if not chunks:
        return "No relevant data found for that question", []
    answer = generate_with_retry(build_prompt(question, chunks))
    return answer, [c.text for c in chunks]


def main():
    eval_file = sys.argv[1] if len(sys.argv) > 1 else "eval/questions.json"
    results_file = sys.argv[2] if len(sys.argv) > 2 else "eval/results_vector.json"
    top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    all_names = set()
    for df in pd.read_excel(EXCEL, sheet_name=None).values():
        all_names.update(df["Name"].tolist())

    store = ChromaVectorStore(collection_name=COLLECTION)
    chunks = chunk_documents(ConnectorFactory.create("excel", EXCEL).load())
    store.add(chunks)
    print(f"Ingested {len(chunks)} chunks, top_k={top_k}\n")
    retriever = Retriever(store)

    data = json.loads(Path(eval_file).read_text(encoding="utf-8"))
    results = []
    by_type = defaultdict(lambda: [0, 0, 0])   # type -> [lenient, strict, total]

    for q in data["questions"]:
        entry = {"id": q["id"], "type": q["type"], "question": q["question"],
                 "expected": q["expected"], "top_k": top_k, "answer": None,
                 "retrieved": None, "lenient": False, "strict": False, "error": None}
        try:
            answer, retrieved = ask(retriever, q["question"], top_k)
            entry["answer"], entry["retrieved"] = answer, retrieved
            entry["lenient"], entry["strict"] = score(q["expected"], answer, all_names)
        except Exception as e:
            entry["error"] = f"{type(e).__name__}: {e}"

        results.append(entry)
        stats = by_type[q["type"]]
        stats[0] += entry["lenient"]
        stats[1] += entry["strict"]
        stats[2] += 1

        print(f'{q["id"]} {"PASS" if entry["lenient"] else "FAIL"}'
              f'{"" if entry["strict"] == entry["lenient"] else " (strict: FAIL)"}  {q["question"]}')
        if not entry["lenient"]:
            print("   expected:", q["expected"])
            print("   answer  :", (entry["answer"] or entry["error"] or "")[:200].replace("\n", " "))
        time.sleep(PAUSE_SECONDS)

    print("\nResults by question type (lenient / strict):")
    for qtype, (lenient, strict, total) in by_type.items():
        print(f"  {qtype:<13} {lenient}/{total}  /  {strict}/{total}")
    total = len(results)
    print(f"  {'OVERALL':<13} {sum(r['lenient'] for r in results)}/{total}"
          f"  /  {sum(r['strict'] for r in results)}/{total}")

    Path(results_file).write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nSaved details to {results_file}")


if __name__ == "__main__":
    main()