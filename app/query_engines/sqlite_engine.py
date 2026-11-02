import os
import sqlite3
from pathlib import Path
from typing import Any

from app.query_engines.base import BaseQueryEngine, QueryValidationError, MAX_ROWS
from app.query_engines.sql_utils import extract_sql, validate_select_only
from app.generation.llm_client import get_llm_client
from app.generation.sql_prompt_builder import build_sql_prompt

SAMPLE_ROWS = 10  # rows shown to the LLM per table


class SQLiteQueryEngine(BaseQueryEngine):
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.getenv("SQLITE_DB_PATH", "./data/structured.db")

    def _connect(self) -> sqlite3.Connection:
        uri = Path(self.db_path).resolve().as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        conn.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DML, False)
        conn.setconfig(sqlite3.SQLITE_DBCONFIG_DQS_DDL, False)
        return conn
    
    def describe_schema(self) -> str:
        conn = self._connect()
        try:
            tables = conn.execute(
                "SELECT table_name, source_name, sheet_name, row_count "
                "FROM _sources ORDER BY table_name"
            ).fetchall()

            parts = []
            for table, source, sheet, row_count in tables:
                cols = conn.execute(f'PRAGMA table_info("{table}")').fetchall()
                col_lines = [f'  - "{c[1]}" {c[2]}' for c in cols]
                sample = conn.execute(
                    f'SELECT * FROM "{table}" LIMIT {SAMPLE_ROWS}'
                ).fetchall()
                sample_lines = [f"  {row}" for row in sample]

                parts.append(
                    f'Table "{table}" (from {source}, sheet "{sheet}", {row_count} rows)\n'
                    "Columns:\n" + "\n".join(col_lines) + "\n"
                    "Sample rows (in column order):\n" + "\n".join(sample_lines)
                )
            return "\n\n".join(parts)
        finally:
            conn.close()

    # Placeholders: we build these in the next steps
    def generate_query(self, question: str, schema: str) -> str:
        prompt = build_sql_prompt(question,schema)
        # print(prompt)
        raw = get_llm_client().generate(prompt)
        # print(raw)
        return extract_sql(raw)
    
    def validate_query(self, query: str) -> None:
        validate_select_only(query)
        conn = self._connect()
        try:
            conn.execute(f"EXPLAIN {query}")
        except sqlite3.Error as e:
            raise QueryValidationError(f"SQLite rejected the query: {e}") from e
        finally:
            conn.close()

    def execute_query(self, query: str) -> list[dict[str, Any]]:
        conn = self._connect()
        try:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query)
            rows = cursor.fetchmany(MAX_ROWS)
            # row = rows[0]
            # print(row)
            # print(rows[0][0])
            # print(row["name"])       # Hannah    (by column name, the new ability)
            # print(row.keys())        # ['name', 'total']
            # print(dict(row))  
            # return []
            return [dict(row) for row in rows]
        finally:
            conn.close()