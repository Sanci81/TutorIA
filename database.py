"""SQLite adatbázis kezelés a TutorIA alkalmazáshoz.

Két tábla:
  - parents:  szülői fiókok (email + jelszó hash)
  - children: gyerek profilok, a szülőhöz kötve
"""

import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.environ.get("DATABASE_PATH", Path(__file__).parent / "tutoria.db"))


def get_connection():
    """Új kapcsolat, sorok dict-szerű elérésével."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Létrehozza a táblákat, ha még nem léteznek."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS parents (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS children (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id   INTEGER NOT NULL,
            name        TEXT    NOT NULL,
            age         INTEGER NOT NULL,
            grade       TEXT    NOT NULL,
            country     TEXT    NOT NULL,
            region      TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (parent_id) REFERENCES parents (id) ON DELETE CASCADE
        )
        """
    )

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Szülő (parent) műveletek
# ---------------------------------------------------------------------------

def create_parent(email, password_hash):
    """Új szülő létrehozása. Visszaadja az új sor id-ját, vagy None ha az
    email már foglalt."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO parents (email, password_hash) VALUES (?, ?)",
            (email.strip().lower(), password_hash),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def get_parent_by_email(email):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM parents WHERE email = ?", (email.strip().lower(),)
    ).fetchone()
    conn.close()
    return row


def get_parent_by_id(parent_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM parents WHERE id = ?", (parent_id,)
    ).fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------------------
# Gyerek (child) műveletek
# ---------------------------------------------------------------------------

def create_child(parent_id, name, age, grade, country, region):
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO children (parent_id, name, age, grade, country, region)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (parent_id, name.strip(), age, grade.strip(), country, region),
    )
    conn.commit()
    child_id = cur.lastrowid
    conn.close()
    return child_id


def get_children_for_parent(parent_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM children WHERE parent_id = ? ORDER BY created_at DESC",
        (parent_id,),
    ).fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print(f"Adatbázis inicializálva: {DB_PATH}")
