"""Egyszeri migrációs script: xp és game_level oszlopok hozzáadása a child_progress táblához.
Használat: python add_xp_columns.py
A script a DATABASE_URL környezeti változóból olvassa a kapcsolati stringet (ugyanúgy, mint database.py).
"""

import os
import sys
from sqlalchemy import create_engine, text

def _database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("❌ HIBA: DATABASE_URL nincs beállítva.")
        print("   Állítsd be, pl.: set DATABASE_URL=postgresql://user:pass@host/db")
        sys.exit(1)
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


def main():
    url = _database_url()
    engine = create_engine(url, pool_pre_ping=True)

    columns = [
        ("xp", "INTEGER NOT NULL DEFAULT 0"),
        ("game_level", "INTEGER NOT NULL DEFAULT 1"),
    ]

    print(f"Kapcsolódás: {url[:30]}...")

    with engine.connect() as conn:
        # Ellenőrizzük, hogy a tábla létezik-e
        result = conn.execute(
            text(
                "SELECT EXISTS (SELECT FROM information_schema.tables "
                "WHERE table_name = 'child_progress')"
            )
        )
        exists = result.scalar()
        if not exists:
            print("❌ A 'child_progress' tábla nem létezik. Először indítsd el az alkalmazást (init_db).")
            sys.exit(1)

        # Meglévő oszlopok lekérése
        result = conn.execute(
            text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name = 'child_progress'"
            )
        )
        existing = {row[0] for row in result}
        print(f"Meglévő oszlopok: {', '.join(sorted(existing))}")

        for col_name, col_type in columns:
            if col_name in existing:
                print(f"⏭️  '{col_name}' már létezik, kihagyva.")
                continue
            try:
                conn.execute(text(f"ALTER TABLE child_progress ADD COLUMN {col_name} {col_type}"))
                print(f"✅ '{col_name}' ({col_type}) hozzáadva.")
            except Exception as e:
                print(f"❌ '{col_name}' hozzáadása sikertelen: {e}")

        conn.commit()

    print("\n🎉 Migráció kész! Az xp és game_level oszlopok elérhetők a child_progress táblában.")
    print("   Az új sorok automatikusan xp=0, game_level=1 értékkel jönnek létre.")
    print("   A meglévő sorokban: xp=0, game_level=1 (az ALTER TABLE által beállított DEFAULT).")


if __name__ == "__main__":
    main()
