"""PostgreSQL adatbázis kezelés SQLAlchemy-vel (TutorIA).

A kapcsolati URL a DATABASE_URL environment variable-ből jön
(railway PostgreSQL). Táblák:
  - parents:  szülői fiókok
  - children: gyerek profilok
  - password_reset_tokens: jelszó-visszaállító tokenek
  - chat_sessions, chat_messages: AI tanár beszélgetés
  - child_progress: tantárgyankénti haladás
  - vocabulary: idegen nyelvi szójegyzék
  - child_learning_time: tanulási idő követés
"""

from __future__ import annotations

import hashlib
import logging
import os
import secrets
from datetime import date, datetime, timedelta, timezone
from typing import Any

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    create_engine,
    delete,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

logger = logging.getLogger(__name__)

RESET_TOKEN_HOURS = 24


def _database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "A DATABASE_URL environment variable nincs beállítva. "
            "Railway-en add hozzá a PostgreSQL service-hez."
        )
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(_database_url(), pool_pre_ping=True)
    return _engine


def _get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=_get_engine(), autoflush=False, autocommit=False
        )
    return _SessionLocal


class Base(DeclarativeBase):
    pass


class Parent(Base):
    __tablename__ = "parents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    children: Mapped[list["Child"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    reset_tokens: Mapped[list["PasswordResetToken"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )


class Child(Base):
    __tablename__ = "children"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    grade: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    curriculum: Mapped[str] = mapped_column(String(2), nullable=False, default="HU")
    region: Mapped[str | None] = mapped_column(String(10))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent: Mapped["Parent"] = relationship(back_populates="children")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("parents.id", ondelete="CASCADE"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    parent: Mapped["Parent"] = relationship(back_populates="reset_tokens")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    topic_id: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    curriculum_position: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    session: Mapped["ChatSession"] = relationship(back_populates="messages")


class Vocabulary(Base):
    __tablename__ = "vocabulary"
    __table_args__ = (
        UniqueConstraint(
            "child_id",
            "subject",
            "word_native",
            "word_foreign",
            name="uq_vocab_child_subject_words",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    word_native: Mapped[str] = mapped_column(String(255), nullable=False)
    word_foreign: Mapped[str] = mapped_column(String(255), nullable=False)
    learned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ChildLearningTime(Base):
    """Tanulási idő követés – session-alapú."""
    __tablename__ = "child_learning_time"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    topic_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    minutes: Mapped[float] = mapped_column(
        Float, nullable=False, default=0.0
    )
    session_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    session_end: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ChildTopicScore(Base):
    """Témakörönkénti teszt eredmény (child + subject + grade + topic_id)."""

    __tablename__ = "child_topic_scores"
    __table_args__ = (
        UniqueConstraint(
            "child_id",
            "subject",
            "grade",
            "topic_id",
            name="uq_child_topic_score",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    topic_id: Mapped[str] = mapped_column(String(32), nullable=False)
    topic_name: Mapped[str] = mapped_column(String(512), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    topic_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    topic_learning_minutes: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)


class ChildProgress(Base):
    __tablename__ = "child_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    topics_completed: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    last_position: Mapped[str | None] = mapped_column(String(255))
    level: Mapped[int] = mapped_column(Integer, default=0)
    early_placement_attempts: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Új gamifikációs mezők:
    xp: Mapped[int] = mapped_column(Integer, default=0)
    game_level: Mapped[int] = mapped_column(Integer, default=1)
    coins: Mapped[int] = mapped_column(Integer, default=0)
    streak_days: Mapped[int] = mapped_column(Integer, default=0)
    streak_last_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Virtuális bolt – skinek:
    unlocked_skins: Mapped[str] = mapped_column(
        String(500), nullable=False, default="default"
    )
    active_skin: Mapped[str] = mapped_column(
        String(100), nullable=False, default="default"
    )


# ---------------------------------------------------------------------------
# Segédek
# ---------------------------------------------------------------------------


def _session() -> Session:
    return _get_session_factory()()


def _parent_dict(parent: Parent) -> dict[str, Any]:
    return {
        "id": parent.id,
        "email": parent.email,
        "password_hash": parent.password_hash,
        "created_at": parent.created_at,
    }


def child_age_from_birth(birth_date: date) -> int:
    """Életkor születési dátumból (éves közelítés)."""
    return max(1, (date.today() - birth_date).days // 365)


def approximate_birth_from_age(age: int) -> date:
    """Régi profilok: közelítő születési dátum az age mezőből."""
    return date.today() - timedelta(days=int(age) * 365)


def compute_child_age(
    *,
    birth_date: date | None = None,
    age_legacy: int | None = None,
) -> int | None:
    """Megjelenített / logikai életkor – birth_date elsőbbsége."""
    if birth_date:
        return child_age_from_birth(birth_date)
    if age_legacy is not None:
        try:
            return int(age_legacy)
        except (TypeError, ValueError):
            pass
    return None


def _child_dict(child: Child) -> dict[str, Any]:
    bd = child.birth_date
    age_val = compute_child_age(birth_date=bd, age_legacy=child.age)
    return {
        "id": child.id,
        "parent_id": child.parent_id,
        "name": child.name,
        "birth_date": bd.isoformat() if bd else None,
        "age": age_val,
        "grade": child.grade,
        "country": child.country,
        "curriculum": getattr(child, "curriculum", child.country) or child.country,
        "region": child.region,
        "created_at": child.created_at,
        "needs_birth_date": bd is None,
    }


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def init_db() -> None:
    """Létrehozza a táblákat, ha még nem léteznek."""
    Base.metadata.create_all(bind=_get_engine())
    ensure_children_birth_date_column()
    ensure_chat_sessions_language_column()
    ensure_chat_sessions_topic_id_column()
    ensure_child_learning_time_table()
    ensure_child_progress_extra_columns()
    ensure_topic_scores_extra_columns()
    ensure_children_curriculum_column()


def ensure_children_curriculum_column() -> None:
    """curriculum oszlop hozzáadása a children táblához (HU | ES)."""
    from sqlalchemy import text

    engine = _get_engine()
    stmts = (
        "ALTER TABLE children ADD COLUMN IF NOT EXISTS "
        "curriculum TEXT NOT NULL DEFAULT 'HU'",
        "UPDATE children SET curriculum = country "
        "WHERE curriculum IS NULL",
    )
    for stmt in stmts:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception as exc:
            logger.warning(
                "ensure_children_curriculum_column: kihagyva (%s): %s",
                exc.__class__.__name__,
                stmt,
            )


def ensure_children_birth_date_column() -> None:
    """birth_date oszlop + régi age → közelítő birth_date migráció."""
    from sqlalchemy import text

    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE children ADD COLUMN IF NOT EXISTS birth_date DATE")
        )
        conn.execute(
            text("ALTER TABLE children ALTER COLUMN age DROP NOT NULL")
        )
        conn.execute(
            text(
                """
                UPDATE children
                SET birth_date = CURRENT_DATE - (age * INTERVAL '365 days')
                WHERE birth_date IS NULL AND age IS NOT NULL
                """
            )
        )


def ensure_chat_sessions_language_column() -> None:
    """Chat session nyelv – külön előzmény angol / német / spanyol."""
    from sqlalchemy import text

    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS "
                "language VARCHAR(20) NOT NULL DEFAULT ''"
            )
        )


def ensure_chat_sessions_topic_id_column() -> None:
    """Chat session topic_id – külön előzmény témakörönként."""
    from sqlalchemy import text

    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS "
                "topic_id VARCHAR(100) NOT NULL DEFAULT ''"
            )
        )


def ensure_child_learning_time_table() -> None:
    """Biztosítja, hogy a child_learning_time tábla létezik."""
    ChildLearningTime.__table__.create(bind=_get_engine(), checkfirst=True)


def ensure_child_progress_extra_columns() -> None:
    """early_placement_attempts, xp, game_level, skin oszlopok hozzáadása.

    Minden ALTER külön, biztonságos tranzakcióban fut: ha egy oszlop
    már létezik vagy az adott DB nem támogatja az IF NOT EXISTS-t (pl. SQLite),
    az NEM gátolja meg az app elindulását.
    """
    from sqlalchemy import text

    statements = (
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "early_placement_attempts INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "xp INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "game_level INTEGER NOT NULL DEFAULT 1",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "coins INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "streak_days INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "streak_last_date DATE",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "unlocked_skins VARCHAR(500) NOT NULL DEFAULT 'default'",
        "ALTER TABLE child_progress ADD COLUMN IF NOT EXISTS "
        "active_skin VARCHAR(100) NOT NULL DEFAULT 'default'",
    )

    engine = _get_engine()
    for stmt in statements:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "ensure_child_progress_extra_columns: kihagyva (%s): %s",
                exc.__class__.__name__,
                stmt,
            )


def ensure_topic_scores_extra_columns() -> None:
    """topic_attempts és topic_learning_minutes oszlopok hozzáadása."""
    from sqlalchemy import text

    engine = _get_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE child_topic_scores ADD COLUMN IF NOT EXISTS "
                "topic_attempts INTEGER NOT NULL DEFAULT 0"
            )
        )
        conn.execute(
            text(
                "ALTER TABLE child_topic_scores ADD COLUMN IF NOT EXISTS "
                "topic_learning_minutes FLOAT NOT NULL DEFAULT 0.0"
            )
        )


def ensure_password_reset_table() -> None:
    """Biztosítja, hogy a password_reset_tokens tábla létezik (PostgreSQL)."""
    PasswordResetToken.__table__.create(bind=_get_engine(), checkfirst=True)


# ---------------------------------------------------------------------------
# Szülő (parent) műveletek
# ---------------------------------------------------------------------------


def create_parent(email: str, password_hash: str) -> int | None:
    """Új szülő létrehozása. Visszaadja az id-t, vagy None ha az email foglalt."""
    db = _session()
    try:
        parent = Parent(email=email.strip().lower(), password_hash=password_hash)
        db.add(parent)
        db.commit()
        db.refresh(parent)
        return parent.id
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()


def get_parent_by_email(email: str) -> dict[str, Any] | None:
    db = _session()
    try:
        parent = db.scalar(
            select(Parent).where(Parent.email == email.strip().lower())
        )
        return _parent_dict(parent) if parent else None
    finally:
        db.close()


def get_parent_by_id(parent_id: int) -> dict[str, Any] | None:
    db = _session()
    try:
        parent = db.get(Parent, parent_id)
        return _parent_dict(parent) if parent else None
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Gyerek (child) műveletek
# ---------------------------------------------------------------------------


def create_child(
    parent_id: int,
    name: str,
    birth_date: date,
    grade: str,
    country: str,
    region: str | None,
    curriculum: str = "HU",
) -> int:
    db = _session()
    try:
        child = Child(
            parent_id=parent_id,
            name=name.strip(),
            birth_date=birth_date,
            age=child_age_from_birth(birth_date),
            grade=grade.strip(),
            country=country,
            curriculum=curriculum,
            region=region,
        )
        db.add(child)
        db.commit()
        db.refresh(child)
        return child.id
    finally:
        db.close()


def update_child(
    child_id: int,
    parent_id: int,
    *,
    name: str,
    birth_date: date,
    grade: str,
    country: str,
    region: str | None,
    curriculum: str = "HU",
) -> bool:
    """Gyerek profil szerkesztése – csak a megadott szülő gyerekéhez."""
    db = _session()
    try:
        child = db.scalar(
            select(Child).where(
                Child.id == child_id,
                Child.parent_id == parent_id,
            )
        )
        if not child:
            return False
        child.name = name.strip()
        child.birth_date = birth_date
        child.age = child_age_from_birth(birth_date)
        child.grade = grade.strip()
        child.country = country
        child.curriculum = curriculum
        child.region = region
        db.commit()
        return True
    finally:
        db.close()


def update_child_curriculum(
    child_id: int,
    parent_id: int,
    curriculum: str,
) -> bool:
    """Gyerek tanterv oszlopának frissítése (kapcsoló állításakor)."""
    db = _session()
    try:
        child = db.scalar(
            select(Child).where(Child.id == child_id, Child.parent_id == parent_id)
        )
        if not child:
            return False
        child.curriculum = curriculum
        db.commit()
        return True
    finally:
        db.close()


def get_children_for_parent(parent_id: int) -> list[dict[str, Any]]:
    db = _session()
    try:
        children = db.scalars(
            select(Child)
            .where(Child.parent_id == parent_id)
            .order_by(Child.created_at.desc())
        ).all()
        return [_child_dict(c) for c in children]
    finally:
        db.close()


def get_child_by_id(child_id: int, parent_id: int) -> dict[str, Any] | None:
    """Gyerek profil lekérése – csak a megadott szülőhöz tartozó rekord."""
    db = _session()
    try:
        child = db.scalar(
            select(Child).where(Child.id == child_id, Child.parent_id == parent_id)
        )
        return _child_dict(child) if child else None
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Jelszó-visszaállítás
# ---------------------------------------------------------------------------


def create_password_reset_token(parent_id: int) -> str:
    """Új visszaállító token; visszaadja a nyers tokent (e-mail linkhez)."""
    ensure_password_reset_table()
    expires_at = datetime.now(timezone.utc) + timedelta(hours=RESET_TOKEN_HOURS)

    db = _session()
    try:
        for _ in range(3):
            token = secrets.token_urlsafe(32)
            token_hash = _hash_token(token)
            try:
                db.execute(
                    delete(PasswordResetToken).where(
                        PasswordResetToken.parent_id == parent_id,
                        PasswordResetToken.used_at.is_(None),
                    )
                )
                db.add(
                    PasswordResetToken(
                        parent_id=parent_id,
                        token_hash=token_hash,
                        expires_at=expires_at,
                    )
                )
                db.commit()
                return token
            except IntegrityError:
                db.rollback()

        raise RuntimeError("Nem sikerült visszaállító tokent létrehozni")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_password_reset_by_token(token: str) -> dict[str, Any] | None:
    db = _session()
    try:
        row = db.execute(
            select(PasswordResetToken, Parent.email)
            .join(Parent, Parent.id == PasswordResetToken.parent_id)
            .where(
                PasswordResetToken.token_hash == _hash_token(token),
                PasswordResetToken.used_at.is_(None),
                PasswordResetToken.expires_at > func.now(),
            )
        ).first()
        if not row:
            return None
        reset_token, email = row
        return {
            "id": reset_token.id,
            "parent_id": reset_token.parent_id,
            "token_hash": reset_token.token_hash,
            "expires_at": reset_token.expires_at,
            "used_at": reset_token.used_at,
            "created_at": reset_token.created_at,
            "email": email,
        }
    finally:
        db.close()


def mark_reset_token_used(token_id: int) -> None:
    db = _session()
    try:
        reset_token = db.get(PasswordResetToken, token_id)
        if reset_token:
            reset_token.used_at = datetime.now(timezone.utc)
            db.commit()
    finally:
        db.close()


def update_parent_password(parent_id: int, password_hash: str) -> None:
    db = _session()
    try:
        parent = db.get(Parent, parent_id)
        if parent:
            parent.password_hash = password_hash
            db.commit()
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Chat és haladás
# ---------------------------------------------------------------------------


def _chat_session_dict(row: ChatSession) -> dict[str, Any]:
    return {
        "id": row.id,
        "child_id": row.child_id,
        "subject": row.subject,
        "language": row.language or "",
        "topic_id": row.topic_id or "",
        "curriculum_position": row.curriculum_position or {},
        "created_at": row.created_at,
    }


def _chat_message_dict(row: ChatMessage) -> dict[str, Any]:
    return {
        "id": row.id,
        "session_id": row.session_id,
        "role": row.role,
        "content": row.content,
        "created_at": row.created_at,
    }


def _progress_dict(row: ChildProgress) -> dict[str, Any]:
    return {
        "id": row.id,
        "child_id": row.child_id,
        "subject": row.subject,
        "topics_completed": list(row.topics_completed or []),
        "last_position": row.last_position,
        "level": row.level,
        "early_placement_attempts": row.early_placement_attempts,
        "updated_at": row.updated_at,
        "xp": row.xp,
        "game_level": row.game_level,
        "coins": getattr(row, "coins", 0) or 0,
        "streak_days": getattr(row, "streak_days", 0) or 0,
        "streak_last_date": getattr(row, "streak_last_date", None),
        "unlocked_skins": getattr(row, "unlocked_skins", None) or "default",
        "active_skin": getattr(row, "active_skin", None) or "default",
    }


def get_or_create_chat_session(
    child_id: int,
    subject: str,
    *,
    language: str = "",
    topic_id: str = "",
    curriculum_position: dict | None = None,
) -> dict[str, Any]:
    lang_key = (language or "").strip().lower()
    tpid = topic_id.strip() if topic_id else ""
    db = _session()
    try:
        row = db.scalar(
            select(ChatSession)
            .where(
                ChatSession.child_id == child_id,
                ChatSession.subject == subject,
                ChatSession.language == lang_key,
                ChatSession.topic_id == tpid,
            )
            .order_by(ChatSession.created_at.desc())
        )
        if row:
            if curriculum_position and row.curriculum_position != curriculum_position:
                row.curriculum_position = curriculum_position
                db.commit()
            return _chat_session_dict(row)

        row = ChatSession(
            child_id=child_id,
            subject=subject,
            language=lang_key,
            topic_id=tpid,
            curriculum_position=curriculum_position or {},
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _chat_session_dict(row)
    finally:
        db.close()


def get_chat_session_for_child(
    session_id: int,
    child_id: int,
    subject: str,
    *,
    language: str = "",
) -> dict[str, Any] | None:
    """Chat session ellenőrzése küldéskor (child + tantárgy + nyelv)."""
    lang_key = (language or "").strip().lower()
    db = _session()
    try:
        row = db.scalar(
            select(ChatSession).where(
                ChatSession.id == session_id,
                ChatSession.child_id == child_id,
                ChatSession.subject == subject,
                ChatSession.language == lang_key,
            )
        )
        return _chat_session_dict(row) if row else None
    finally:
        db.close()


def update_chat_session_position(session_id: int, position: dict) -> None:
    db = _session()
    try:
        row = db.get(ChatSession, session_id)
        if row:
            row.curriculum_position = position
            db.commit()
    finally:
        db.close()


def get_chat_messages(session_id: int, *, limit: int = 20) -> list[dict[str, Any]]:
    db = _session()
    try:
        rows = db.scalars(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        ).all()
        ordered = list(reversed(rows))
        return [_chat_message_dict(m) for m in ordered]
    finally:
        db.close()


def add_chat_message(session_id: int, role: str, content: str) -> dict[str, Any]:
    db = _session()
    try:
        msg = ChatMessage(session_id=session_id, role=role, content=content.strip())
        db.add(msg)
        db.commit()
        db.refresh(msg)
        return _chat_message_dict(msg)
    finally:
        db.close()


def get_child_progress(child_id: int, subject: str) -> dict[str, Any] | None:
    db = _session()
    try:
        row = db.scalar(
            select(ChildProgress).where(
                ChildProgress.child_id == child_id,
                ChildProgress.subject == subject,
            )
        )
        return _progress_dict(row) if row else None
    finally:
        db.close()


def get_or_create_child_progress(
    child_id: int,
    subject: str,
    *,
    last_position: str | None = None,
) -> dict[str, Any]:
    db = _session()
    try:
        row = db.scalar(
            select(ChildProgress).where(
                ChildProgress.child_id == child_id,
                ChildProgress.subject == subject,
            )
        )
        if row:
            return _progress_dict(row)

        row = ChildProgress(
            child_id=child_id,
            subject=subject,
            topics_completed=[],
            last_position=last_position,
            level=0,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _progress_dict(row)
    finally:
        db.close()


def update_child_progress(
    child_id: int,
    subject: str,
    *,
    topics_completed: list[str] | None = None,
    last_position: str | None = None,
    level: int | None = None,
    xp: int | None = None,
    game_level: int | None = None,
    coins: int | None = None,
    streak_days: int | None = None,
    streak_last_date: date | None = None,
    unlocked_skins: str | None = None,
    active_skin: str | None = None,
) -> dict[str, Any]:
    db = _session()
    try:
        row = db.scalar(
            select(ChildProgress).where(
                ChildProgress.child_id == child_id,
                ChildProgress.subject == subject,
            )
        )
        if not row:
            row = ChildProgress(
                child_id=child_id,
                subject=subject,
                topics_completed=topics_completed or [],
                last_position=last_position,
                level=level if level is not None else 0,
                xp=xp if xp is not None else 0,
                game_level=game_level if game_level is not None else 1,
                coins=coins if coins is not None else 0,
                streak_days=streak_days if streak_days is not None else 0,
                streak_last_date=streak_last_date,
                unlocked_skins=unlocked_skins if unlocked_skins is not None else "default",
                active_skin=active_skin if active_skin is not None else "default",
            )
            db.add(row)
        else:
            if topics_completed is not None:
                row.topics_completed = topics_completed
            if last_position is not None:
                row.last_position = last_position
            if level is not None:
                row.level = level
            if xp is not None:
                row.xp = xp
            if game_level is not None:
                row.game_level = game_level
            if coins is not None:
                row.coins = coins
            if streak_days is not None:
                row.streak_days = streak_days
            if streak_last_date is not None:
                row.streak_last_date = streak_last_date
            if unlocked_skins is not None:
                row.unlocked_skins = unlocked_skins
            if active_skin is not None:
                row.active_skin = active_skin
            row.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(row)
        return _progress_dict(row)
    finally:
        db.close()


def increment_early_placement_attempts(child_id: int, subject: str) -> int:
    """Növeli a korai szintfelmérő próbálkozások számát. Visszaadja az új értéket."""
    db = _session()
    try:
        row = db.scalar(
            select(ChildProgress).where(
                ChildProgress.child_id == child_id,
                ChildProgress.subject == subject,
            )
        )
        if not row:
            row = ChildProgress(
                child_id=child_id,
                subject=subject,
                topics_completed=[],
                level=0,
            )
            db.add(row)
        row.early_placement_attempts = (row.early_placement_attempts or 0) + 1
        db.commit()
        return row.early_placement_attempts
    except Exception:
        db.rollback()
        return 0
    finally:
        db.close()


def _topic_score_dict(row: ChildTopicScore) -> dict[str, Any]:
    return {
        "topic_id": row.topic_id,
        "topic_name": row.topic_name,
        "score": row.score,
        "passed": row.passed,
        "completed_at": row.completed_at.isoformat() if row.completed_at else None,
        "topic_attempts": row.topic_attempts,
        "topic_learning_minutes": row.topic_learning_minutes,
    }


def get_topic_scores(
    child_id: int, subject: str, grade: int
) -> dict[str, dict[str, Any]]:
    """topic_id -> {score, passed, completed_at, topic_name}."""
    db = _session()
    try:
        rows = db.scalars(
            select(ChildTopicScore).where(
                ChildTopicScore.child_id == child_id,
                ChildTopicScore.subject == subject,
                ChildTopicScore.grade == grade,
            )
        ).all()
        return {r.topic_id: _topic_score_dict(r) for r in rows}
    finally:
        db.close()


def get_topic_score(child_id: int, subject: str, grade: int, topic_id: str) -> dict[str, Any] | None:
    """Egyetlen témakör score dictje, vagy None ha nincs még eredmény."""
    db = _session()
    try:
        row = db.scalar(
            select(ChildTopicScore).where(
                ChildTopicScore.child_id == child_id,
                ChildTopicScore.subject == subject,
                ChildTopicScore.grade == grade,
                ChildTopicScore.topic_id == topic_id,
            )
        )
        return _topic_score_dict(row) if row else None
    finally:
        db.close()


def save_topic_test_result(
    child_id: int,
    subject: str,
    grade: int,
    topic_id: str,
    topic_name: str,
    score: int,
    *,
    pass_threshold: int = 70,
    topic_learning_minutes: float = 0.0,
) -> dict[str, Any]:
    passed = score >= pass_threshold
    now = datetime.now(timezone.utc)
    db = _session()
    try:
        row = db.scalar(
            select(ChildTopicScore).where(
                ChildTopicScore.child_id == child_id,
                ChildTopicScore.subject == subject,
                ChildTopicScore.grade == grade,
                ChildTopicScore.topic_id == topic_id,
            )
        )
        if row:
            row.score = score
            row.passed = passed
            row.topic_name = topic_name
            row.completed_at = now
            row.topic_attempts = (row.topic_attempts or 0) + 1
            row.topic_learning_minutes = topic_learning_minutes
        else:
            row = ChildTopicScore(
                child_id=child_id,
                subject=subject,
                grade=grade,
                topic_id=topic_id,
                topic_name=topic_name,
                score=score,
                passed=passed,
                completed_at=now,
                topic_attempts=1,
                topic_learning_minutes=topic_learning_minutes,
            )
            db.add(row)
        db.commit()
        db.refresh(row)
        return _topic_score_dict(row)
    finally:
        db.close()


def _vocabulary_dict(row: Vocabulary) -> dict[str, Any]:
    return {
        "id": row.id,
        "child_id": row.child_id,
        "subject": row.subject,
        "language": row.language,
        "word_native": row.word_native,
        "word_foreign": row.word_foreign,
        "learned_at": row.learned_at,
    }


def get_vocabulary(
    child_id: int,
    subject: str,
    *,
    language: str | None = None,
) -> list[dict[str, Any]]:
    db = _session()
    try:
        stmt = select(Vocabulary).where(
            Vocabulary.child_id == child_id,
            Vocabulary.subject == subject,
        )
        if language:
            stmt = stmt.where(Vocabulary.language == language)
        rows = db.scalars(
            stmt.order_by(Vocabulary.word_native.asc())
        ).all()
        return [_vocabulary_dict(r) for r in rows]
    finally:
        db.close()


def add_vocabulary_word(
    child_id: int,
    subject: str,
    *,
    language: str,
    word_native: str,
    word_foreign: str,
) -> dict[str, Any] | None:
    """Új szó hozzáadása – None ha már létezik."""
    native = word_native.strip()
    foreign = word_foreign.strip()
    if not native or not foreign:
        return None

    db = _session()
    try:
        existing = db.scalar(
            select(Vocabulary).where(
                Vocabulary.child_id == child_id,
                Vocabulary.subject == subject,
                Vocabulary.word_native == native,
                Vocabulary.word_foreign == foreign,
            )
        )
        if existing:
            return None

        row = Vocabulary(
            child_id=child_id,
            subject=subject,
            language=(language or "").strip().lower(),
            word_native=native,
            word_foreign=foreign,
        )
        db.add(row)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return None
        db.refresh(row)
        return _vocabulary_dict(row)
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Tanulási idő (child_learning_time)
# ---------------------------------------------------------------------------


def start_learning_session(
    child_id: int,
    subject: str,
    topic_id: str | None = None,
) -> dict[str, Any] | None:
    """Rögzíti a tanulási session kezdetét. Visszaadja a session adatait."""
    db = _session()
    try:
        now = datetime.now(timezone.utc)
        row = ChildLearningTime(
            child_id=child_id,
            subject=subject,
            topic_id=topic_id,
            date=now.date(),
            minutes=0.0,
            session_start=now,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return {
            "id": row.id,
            "child_id": row.child_id,
            "subject": row.subject,
            "topic_id": row.topic_id,
            "date": row.date.isoformat(),
            "minutes": row.minutes,
            "session_start": row.session_start.isoformat(),
            "session_end": row.session_end.isoformat() if row.session_end else None,
        }
    except Exception:
        db.rollback()
        return None
    finally:
        db.close()


def end_learning_session(session_id: int, minutes: float) -> bool:
    """Zárja a tanulási session-t a pontos percekkel."""
    db = _session()
    try:
        row = db.get(ChildLearningTime, session_id)
        if not row:
            return False
        row.session_end = datetime.now(timezone.utc)
        row.minutes = round(minutes, 1)
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()


def get_learning_time_today(
    child_id: int, subject: str | None = None
) -> float:
    """Visszaadja a mai tanulási percek összegét (opcionálisan tantárgyra szűrve)."""
    db = _session()
    try:
        today = date.today()
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.date == today,
        )
        if subject:
            q = q.where(ChildLearningTime.subject == subject)
        rows = db.scalars(q).all()
        return round(sum(r.minutes for r in rows), 1)
    finally:
        db.close()


def get_learning_time_today_for_date(
    child_id: int, target_date: date
) -> float:
    """Visszaadja a megadott nap tanulási perceinek összegét (tantárgytól függetlenül)."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.date == target_date,
        )
        rows = db.scalars(q).all()
        return round(sum(r.minutes for r in rows), 1)
    finally:
        db.close()


def get_learning_time_weekly(
    child_id: int, subject: str
) -> list[dict[str, Any]]:
    """Heti bontás: hét napjai 0-6 (H=0, V=6), perc összeg."""
    db = _session()
    try:
        today = date.today()
        # hétfő = 0, vasárnap = 6
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)

        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.subject == subject,
            ChildLearningTime.date >= monday,
            ChildLearningTime.date <= sunday,
        )
        rows = db.scalars(q).all()
        day_minutes = {i: 0.0 for i in range(7)}
        for r in rows:
            dow = r.date.weekday()  # 0=H
            day_minutes[dow] = round(day_minutes[dow] + r.minutes, 1)
        return [
            {"day": i, "minutes": day_minutes[i]} for i in range(7)
        ]
    finally:
        db.close()


def get_learning_time_summary(child_id: int) -> list[dict[str, Any]]:
    """Összesítés tantárgyanként (mai + heti + összes perc)."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
        )
        rows = db.scalars(q).all()
        today = date.today()
        monday = today - timedelta(days=today.weekday())

        subjects: dict[str, dict[str, float]] = {}
        for r in rows:
            subj = r.subject
            if subj not in subjects:
                subjects[subj] = {"today": 0.0, "week": 0.0, "total": 0.0}
            subjects[subj]["total"] = round(
                subjects[subj]["total"] + r.minutes, 1
            )
            if r.date == today:
                subjects[subj]["today"] = round(
                    subjects[subj]["today"] + r.minutes, 1
                )
            if monday <= r.date <= today:
                subjects[subj]["week"] = round(
                    subjects[subj]["week"] + r.minutes, 1
                )

        return [
            {"subject": s, **v} for s, v in subjects.items()
        ]
    finally:
        db.close()


def get_learning_time_total(child_id: int, subject: str) -> float:
    """Visszaadja a tantárgyhoz tartozó összes tanulási percet."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.subject == subject,
        )
        rows = db.scalars(q).all()
        return round(sum(r.minutes for r in rows), 1)
    finally:
        db.close()


def get_topic_learning_minutes(child_id: int, subject: str, topic_id: str) -> float:
    """Visszaadja a témakörhöz tartozó összes tanulási percet."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.subject == subject,
            ChildLearningTime.topic_id == topic_id,
        )
        rows = db.scalars(q).all()
        return round(sum(r.minutes for r in rows), 1)
    finally:
        db.close()


def get_incomplete_learning_sessions(child_id: int) -> list[dict[str, Any]]:
    """Megnyitott (session_end IS NULL) session-ök, időtúllépés kezeléshez."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.session_end.is_(None),
        )
        rows = db.scalars(q).all()
        return [
            {
                "id": r.id,
                "child_id": r.child_id,
                "subject": r.subject,
                "session_start": r.session_start.isoformat(),
                "date": r.date,
            }
            for r in rows
        ]
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("PostgreSQL táblák inicializálva.")


if __name__ == "__main__":
    init_db()
    print("PostgreSQL táblák inicializálva.")
