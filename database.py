"""SQLite adatbázis kezelés a TutorIA alkalmazáshoz.

Két tábla:
  - parents:  szülői fiókok (email + jelszó hash)
  - children: gyerek profilok, a szülőhöz kötve
"""

import hashlib
import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
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

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id  INTEGER NOT NULL,
            token_hash TEXT    NOT NULL UNIQUE,
            expires_at TEXT    NOT NULL,
            used_at    TEXT,
            created_at TEXT    NOT NULL DEFAULT (datetime('now')),
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


# ---------------------------------------------------------------------------
# Jelszó-visszaállítás
# ---------------------------------------------------------------------------

RESET_TOKEN_HOURS = 1


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_password_reset_token(parent_id: int) -> str:
    """Új visszaállító token; visszaadja a nyers tokent (e-mail linkhez)."""
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = (
        datetime.now(timezone.utc) + timedelta(hours=RESET_TOKEN_HOURS)
    ).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    conn.execute(
        "DELETE FROM password_reset_tokens WHERE parent_id = ? AND used_at IS NULL",
        (parent_id,),
    )
    conn.execute(
        """
        INSERT INTO password_reset_tokens (parent_id, token_hash, expires_at)
        VALUES (?, ?, ?)
        """,
        (parent_id, token_hash, expires_at),
    )
    conn.commit()
    conn.close()
    return token


def get_password_reset_by_token(token: str):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT t.*, p.email
        FROM password_reset_tokens t
        JOIN parents p ON p.id = t.parent_id
        WHERE t.token_hash = ?
          AND t.used_at IS NULL
          AND datetime(t.expires_at) > datetime('now')
        """,
        (_hash_token(token),),
    ).fetchone()
    conn.close()
    return row


def mark_reset_token_used(token_id: int) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE password_reset_tokens SET used_at = datetime('now') WHERE id = ?",
        (token_id,),
    )
    conn.commit()
    conn.close()


def update_parent_password(parent_id: int, password_hash: str) -> None:
    conn = get_connection()
    conn.execute(
        "UPDATE parents SET password_hash = ? WHERE id = ?",
        (password_hash, parent_id),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Adatbázis inicializálva: {DB_PATH}")
