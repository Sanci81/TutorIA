"""PostgreSQL adatbázis kezelés SQLAlchemy-vel (TutorIA).

A kapcsolati URL a DATABASE_URL environment variable-ből jön
(Railway PostgreSQL). Táblák:
  - parents:  szülői fiókok
  - children: gyerek profilok
  - password_reset_tokens: jelszó-visszaállító tokenek
  - chat_sessions, chat_messages: AI tanár beszélgetés
  - child_progress: tantárgyankénti haladás
  - vocabulary: idegen nyelvi szójegyzék
"""

from __future__ import annotations

import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import (
    DateTime,
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
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    grade: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
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
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
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


def _child_dict(child: Child) -> dict[str, Any]:
    return {
        "id": child.id,
        "parent_id": child.parent_id,
        "name": child.name,
        "age": child.age,
        "grade": child.grade,
        "country": child.country,
        "region": child.region,
        "created_at": child.created_at,
    }


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def init_db() -> None:
    """Létrehozza a táblákat, ha még nem léteznek."""
    Base.metadata.create_all(bind=_get_engine())


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
    age: int,
    grade: str,
    country: str,
    region: str | None,
) -> int:
    db = _session()
    try:
        child = Child(
            parent_id=parent_id,
            name=name.strip(),
            age=age,
            grade=grade.strip(),
            country=country,
            region=region,
        )
        db.add(child)
        db.commit()
        db.refresh(child)
        return child.id
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
        "updated_at": row.updated_at,
    }


def get_or_create_chat_session(
    child_id: int, subject: str, *, curriculum_position: dict | None = None
) -> dict[str, Any]:
    db = _session()
    try:
        row = db.scalar(
            select(ChatSession)
            .where(ChatSession.child_id == child_id, ChatSession.subject == subject)
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
            curriculum_position=curriculum_position or {},
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return _chat_session_dict(row)
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
            )
            db.add(row)
        else:
            if topics_completed is not None:
                row.topics_completed = topics_completed
            if last_position is not None:
                row.last_position = last_position
            if level is not None:
                row.level = level
            row.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(row)
        return _progress_dict(row)
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


if __name__ == "__main__":
    init_db()
    print("PostgreSQL táblák inicializálva.")
