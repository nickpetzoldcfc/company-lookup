import os

import psycopg


def _connect() -> psycopg.Connection:
    return psycopg.connect(os.environ["AUDIT_DB_DSN"])


def record_lookup(name: str, postcode: str | None, confidence: str) -> None:
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO lookup_audit (company_name, postcode, confidence, created_at) "
        f"VALUES ('{name}', '{postcode}', '{confidence}', now())"
    )
    conn.commit()
    conn.close()


def lookups_for_company(name: str) -> list[dict]:
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM lookup_audit "
        f"WHERE lower(company_name) LIKE '%{name.lower()}%' "
        "ORDER BY created_at DESC"
    )
    columns = [col.name for col in cur.description]
    return [dict(zip(columns, row, strict=True)) for row in cur.fetchall()]
