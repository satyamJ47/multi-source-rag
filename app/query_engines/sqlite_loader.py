import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from app.query_engines.naming import make_table_name, clean_columns

DB_PATH = "./data/structured.db"

def _ensure_catalog(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS _sources (
            table_name  TEXT PRIMARY KEY,
            source_name TEXT NOT NULL,
            sheet_name  TEXT NOT NULL,
            row_count   INTEGER NOT NULL,
            ingested_at TEXT NOT NULL
        )
        """
    )

def load_excel_to_sqlite(source_path: str, db_path: str = DB_PATH) -> list[str]:
    # print(source_path)
    # source_name = Path(source_path)
    # print(source_name)
    source_name = Path(source_path).name
    # print("source_name: ",source_name)
    

    # 1. Read and clean EVERYTHING first, so a bad file fails before we touch the DB
    sheets = pd.read_excel(source_path, sheet_name=None)  # dict: sheet name -> DataFrame
    # print("sheets")
    # print(sheets)
    prepared = {}
    for sheet_name, df in sheets.items():
        df.columns = clean_columns(df.columns)
        prepared[sheet_name] = (make_table_name(source_name,sheet_name),df)
        # print(prepared)
        # print(sheet_name)
        # print(prepared[sheet_name])

    conn = sqlite3.connect(db_path)
    try:
        _ensure_catalog(conn)

        # 2. Drop tables from any previous ingestion of this source
        old = conn.execute(
            "SELECT table_name FROM _sources WHERE source_name = ?", (source_name,)
        ).fetchall()
        for (table,) in old:
            conn.execute(f'DROP TABLE IF EXISTS "{table}"')
        conn.execute("DELETE FROM _sources WHERE source_name = ?", (source_name,))

         # 3. Create the fresh tables and catalog rows
        now = datetime.now(timezone.utc).isoformat()
        created = []
        for sheet_name, (table, df) in prepared.items():
            df.to_sql(table, conn, index=False, if_exists="replace")
            conn.execute(
                "INSERT INTO _sources VALUES (?, ?, ?, ?, ?)",
                (table, source_name, sheet_name, len(df), now),
            )
            created.append(table)

        conn.commit()
        return created
    finally:
        conn.close()

    