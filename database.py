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
    func,
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
    # Mikor járt itt utoljára. Ebből derül ki, hogy egy család MÉG HASZNÁLJA-e
    # a szolgáltatást – a teszt legfontosabb kérdése. Utólag nem pótolható:
    # ami nem íródik ki menet közben, az örökre elveszett.
    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # Milyen gyakran kérjen jelentést a gyerekei haladásáról:
    # "heti" (alap) | "havi" | "napi" | "ki". CSAK a szülő állíthatja –
    # jelszóval a Fiókom oldalon, vagy a levélben lévő leiratkozó linkkel.
    ertesites: Mapped[str] = mapped_column(String(10), nullable=False,
                                           server_default="heti")
    utolso_ertesites: Mapped[date | None] = mapped_column(Date, nullable=True)

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
    grade_hu: Mapped[int] = mapped_column(Integer, nullable=True)
    grade_es: Mapped[int] = mapped_column(Integer, nullable=True)
    country: Mapped[str] = mapped_column(String(2), nullable=False)
    curriculum: Mapped[str] = mapped_column(String(2), nullable=False, default="HU")
    region: Mapped[str | None] = mapped_column(String(10))
    # A tanár hangja tantervenként: "female" vagy "male".
    # A tanár NEVE ebből származik (lásd app.py TEACHER_PROFILES).
    voice_gender_hu: Mapped[str | None] = mapped_column(String(10), nullable=True)
    voice_gender_es: Mapped[str | None] = mapped_column(String(10), nullable=True)
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
    grade: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
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
            "language",
            "topic_id",
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
    topic_id: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
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
    # "voice" vagy "text": hangosan tanult-e a gyerek ebben az órában.
    # A chat oldal egészére vonatkozik, mert a gyerek ott választ módot –
    # ezért a SESSION szintjén tároljuk, nem fordulónként.
    mode: Mapped[str | None] = mapped_column(String(10), nullable=True)
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
    # Hányszor kapott már PONTOT ebből a témakörből. Ebből tudjuk, hogy a
    # mostani sikeres teszt az első teljesítés-e, vagy már ismétlés.
    pont_jutalom: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ChildUsage(Base):
    """Napi fogyasztás gyerekenként – ebből derül ki a VALÓDI költség.

    Enélkül minden árazás tipp. Három dolgot mérünk, mert ez a három kerül
    pénzbe: a felolvasott karakterek (Azure/OpenAI hang), a felismert hang
    másodpercei, és az AI beszélgetés tokenjei.
    """

    __tablename__ = "child_usage"
    __table_args__ = (
        UniqueConstraint("child_id", "nap", name="uq_child_usage_nap"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    nap: Mapped[date] = mapped_column(Date, nullable=False)
    tts_karakter: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hang_mp: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    be_token: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ki_token: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    keres: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


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


class ChildWallet(Base):
    """A gyerek pénztárcája – gyerekenként EGY sor.

    A child_progress tantárgyanként külön sor, ezért a tasakra költhető
    pont nem oda való: azt a gyerek egészére kell gyűjteni.

    pont          – elkölthető, ebből vesz tasakot
    osszes_pont   – amennyit valaha szerzett (csak statisztika, sosem csökken)
    erme          – duplikátumokból jön, később cserére lesz jó
    ingyen_tasak  – három azonos ritkaságú duplikátum egy ingyen tasakot ad
    """

    __tablename__ = "child_wallet"

    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), primary_key=True
    )
    pont: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    osszes_pont: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    erme: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    ingyen_tasak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tasak_szam: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Kinézetek: melyik az aktív, és melyeket oldotta már fel ("alap,szivek").
    kinezet: Mapped[str] = mapped_column(String(32), nullable=False, default="alap")
    kinezetek: Mapped[str] = mapped_column(Text, nullable=False, default="alap")
    # Egyszeri átvezetés: a régi, tantárgyankénti coins összegét egyszer
    # hozzáadjuk az érméhez, hogy a gyereknek ne tűnjön el, amit összegyűjtött.
    regi_erme_atvezetve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Egyetlen valuta lett: a pont beolvadt az érmébe. Ez a jelző mondja meg,
    # hogy a régi pontegyenleget már hozzáadtuk-e.
    pont_atvezetve: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class ChildCard(Base):
    """Megszerzett tudáskártya (gyerek + kártya azonosító).

    A kártyák tartalma a kartyak.py-ban van, ide csak az azonosító kerül.
    A `darab` a duplikátumokat számolja: az első megszerzés 1, minden további
    ugyanabból a lapból növeli.
    """

    __tablename__ = "child_cards"
    __table_args__ = (
        UniqueConstraint("child_id", "card_id", name="uq_child_card"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    child_id: Mapped[int] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"), nullable=False
    )
    card_id: Mapped[str] = mapped_column(String(120), nullable=False)
    darab: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    # Beragasztotta-e már az albumba. A megszerzés és a beragasztás két külön
    # dolog: a Panini-élmény fele az, hogy a gyerek maga teszi a helyére.
    beragasztva: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    szerezve: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
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
        "last_seen": parent.last_seen,
        "ertesites": parent.ertesites or "heti",
        "utolso_ertesites": parent.utolso_ertesites,
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
    grade_hu = child.grade_hu
    grade_es = child.grade_es
    if grade_hu is None:
        try:
            grade_hu = int(child.grade)
        except (ValueError, TypeError):
            grade_hu = 1
    if grade_es is None:
        try:
            grade_es = min(int(child.grade), 6)
        except (ValueError, TypeError):
            grade_es = 1
    return {
        "id": child.id,
        "parent_id": child.parent_id,
        "name": child.name,
        "birth_date": bd.isoformat() if bd else None,
        "age": age_val,
        "grade": child.grade,
        "grade_hu": grade_hu,
        "grade_es": grade_es,
        "country": child.country,
        "curriculum": getattr(child, "curriculum", child.country) or child.country,
        "region": child.region,
        "voice_gender_hu": getattr(child, "voice_gender_hu", None) or "female",
        "voice_gender_es": getattr(child, "voice_gender_es", None) or "female",
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
    ensure_children_grade_columns()
    ensure_vocabulary_topic_id_column()
    ensure_chat_sessions_grade_column()
    ensure_children_voice_columns()
    ensure_child_cards_table()
    ensure_child_wallet_table()
    ensure_child_usage_table()
    ensure_parents_last_seen_column()
    ensure_learning_time_mode_column()
    ensure_parents_ertesites_columns()


def ensure_parents_last_seen_column() -> None:
    """parents.last_seen – mikor volt a szülő utoljára aktív."""
    from sqlalchemy import text

    try:
        with _get_engine().begin() as conn:
            conn.execute(text(
                "ALTER TABLE parents ADD COLUMN IF NOT EXISTS "
                "last_seen TIMESTAMPTZ"))
    except Exception as exc:
        logger.warning("ensure_parents_last_seen_column: kihagyva: %s", exc)


def ensure_parents_ertesites_columns() -> None:
    """A szülői jelentés beállítása és a legutóbbi küldés napja."""
    from sqlalchemy import text

    for stmt in (
        "ALTER TABLE parents ADD COLUMN IF NOT EXISTS "
        "ertesites VARCHAR(10) NOT NULL DEFAULT 'heti'",
        "ALTER TABLE parents ADD COLUMN IF NOT EXISTS utolso_ertesites DATE",
    ):
        try:
            with _get_engine().begin() as conn:
                conn.execute(text(stmt))
        except Exception as exc:
            logger.warning("ensure_parents_ertesites_columns: kihagyva: %s", exc)


def ensure_learning_time_mode_column() -> None:
    """child_learning_time.mode – hangos vagy szöveges órán tanult-e."""
    from sqlalchemy import text

    try:
        with _get_engine().begin() as conn:
            conn.execute(text(
                "ALTER TABLE child_learning_time ADD COLUMN IF NOT EXISTS "
                "mode VARCHAR(10)"))
    except Exception as exc:
        logger.warning("ensure_learning_time_mode_column: kihagyva: %s", exc)


def ensure_children_voice_columns() -> None:
    """voice_gender_hu / voice_gender_es oszlopok (tanár hangja tantervenként)."""
    from sqlalchemy import text

    engine = _get_engine()
    stmts = (
        "ALTER TABLE children ADD COLUMN IF NOT EXISTS "
        "voice_gender_hu VARCHAR(10)",
        "ALTER TABLE children ADD COLUMN IF NOT EXISTS "
        "voice_gender_es VARCHAR(10)",
        "UPDATE children SET voice_gender_hu = 'female' WHERE voice_gender_hu IS NULL",
        "UPDATE children SET voice_gender_es = 'female' WHERE voice_gender_es IS NULL",
    )
    for stmt in stmts:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception as exc:
            logger.warning(
                "ensure_children_voice_columns: kihagyva (%s): %s", stmt, exc
            )


def ensure_children_grade_columns() -> None:
    """grade_hu / grade_es oszlopok hozzáadása + backfill a régi grade-ből."""
    from sqlalchemy import text

    engine = _get_engine()
    stmts = (
        "ALTER TABLE children ADD COLUMN IF NOT EXISTS grade_hu INTEGER",
        "ALTER TABLE children ADD COLUMN IF NOT EXISTS grade_es INTEGER",
        "UPDATE children SET grade_hu = CAST(grade AS INTEGER) WHERE grade_hu IS NULL",
        "UPDATE children SET grade_es = LEAST(CAST(grade AS INTEGER), 6) WHERE grade_es IS NULL",
    )
    for stmt in stmts:
        try:
            with engine.begin() as conn:
                conn.execute(text(stmt))
        except Exception as exc:
            logger.warning(
                "ensure_children_grade_columns: kihagyva (%s): %s",
                exc.__class__.__name__,
                stmt,
            )


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


def ensure_vocabulary_topic_id_column() -> None:
    """vocabulary.topic_id oszlop + új unique constraint (child_id, subject, language, topic_id, word_native, word_foreign)."""
    from sqlalchemy import text

    engine = _get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE vocabulary ADD COLUMN IF NOT EXISTS "
                    "topic_id VARCHAR(100)"
                )
            )
            # Régi constraint eldobása, új létrehozása
            conn.execute(
                text(
                    "ALTER TABLE vocabulary DROP CONSTRAINT IF EXISTS "
                    "uq_vocab_child_subject_words"
                )
            )
            conn.execute(
                text(
                    "ALTER TABLE vocabulary ADD CONSTRAINT uq_vocab_child_subject_words "
                    "UNIQUE (child_id, subject, language, topic_id, word_native, word_foreign)"
                )
            )
    except Exception as exc:
        logger.warning(
            "ensure_vocabulary_topic_id_column: kihagyva (%s): %s",
            exc.__class__.__name__,
            exc,
        )


def ensure_chat_sessions_grade_column() -> None:
    """chat_sessions.grade oszlop hozzáadása (évfolyam szerinti session szétválasztás)."""
    from sqlalchemy import text

    engine = _get_engine()
    try:
        with engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE chat_sessions ADD COLUMN IF NOT EXISTS "
                    "grade INTEGER"
                )
            )
    except Exception as exc:
        logger.warning(
            "ensure_chat_sessions_grade_column: kihagyva (%s): %s",
            exc.__class__.__name__,
            exc,
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
        conn.execute(
            text(
                "ALTER TABLE child_topic_scores ADD COLUMN IF NOT EXISTS "
                "pont_jutalom INTEGER NOT NULL DEFAULT 0"
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


def touch_parent(parent_id: int) -> None:
    """A szülő utolsó aktivitásának frissítése. Hibára SOHA nem dob: a mérés
    nem akadályozhatja meg, hogy valaki használja az appot."""
    if not parent_id:
        return
    try:
        db = _session()
        try:
            p = db.get(Parent, parent_id)
            if p is not None:
                p.last_seen = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()
    except Exception:
        logger.warning("touch_parent sikertelen", exc_info=True)


ERTESITES_MODOK = ("napi", "heti", "havi", "ki")
_ERTESITES_NAPOK = {"napi": 1, "heti": 7, "havi": 30}


def szulo_ertesites_beallit(parent_id: int, mod: str) -> bool:
    """A jelentés gyakoriságának beállítása. Ismeretlen értéket elutasít."""
    if mod not in ERTESITES_MODOK:
        return False
    db = _session()
    try:
        p = db.get(Parent, parent_id)
        if p is None:
            return False
        p.ertesites = mod
        db.commit()
        return True
    except Exception:
        db.rollback()
        return False
    finally:
        db.close()


def ertesitendo_szulok(ma: date | None = None) -> list[dict[str, Any]]:
    """Kinek jár MA jelentés.

    A küldés napja a REGISZTRÁCIÓ napjához igazodik, nem mindenkinek
    ugyanaznap – így nem megy ki száz levél egyszerre, és belefér a
    szolgáltató napi keretébe.
    """
    ma = ma or datetime.now(timezone.utc).date()
    db = _session()
    try:
        ki: list[dict[str, Any]] = []
        for p in db.scalars(select(Parent)).all():
            mod = (p.ertesites or "heti").strip().lower()
            koz = _ERTESITES_NAPOK.get(mod)
            if not koz:
                continue                       # "ki" vagy ismeretlen
            if p.utolso_ertesites and (ma - p.utolso_ertesites).days < koz:
                continue                       # még nem esedékes
            if not p.utolso_ertesites:
                # Első alkalom: a regisztráció napjához igazítjuk, hogy a
                # küldések szétterüljenek a héten/hónapon belül.
                alap = (p.created_at.date() if p.created_at else ma)
                if koz > 1 and (ma - alap).days % koz != 0:
                    continue
            ki.append({"id": p.id, "email": p.email, "mod": mod,
                       "utolso": p.utolso_ertesites})
        return ki
    finally:
        db.close()


def ertesites_elkuldve(parent_id: int, nap: date | None = None) -> None:
    """Feljegyzi, hogy ma ment ki jelentés. Enélkül holnap újra kimenne."""
    db = _session()
    try:
        p = db.get(Parent, parent_id)
        if p is not None:
            p.utolso_ertesites = nap or datetime.now(timezone.utc).date()
            db.commit()
    except Exception:
        db.rollback()
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
# GDPR: adatkivitel és fióktörlés
#
# Ez nem "szép ha van" funkció: a törléshez való jog (GDPR 17. cikk) és az
# adathordozhatóság (20. cikk) kötelező, és egy hatóság ezt kéri számon
# elsőként. Ezért NEM a rendszer beállításaira bízzuk, hogy a kapcsolódó
# sorok eltűnnek-e: mind a tizenkét táblát KÉZZEL takarítjuk ki, sorrendben.
# ---------------------------------------------------------------------------

# A gyerekhez kötött táblák. Ha új tábla születik, IDE is fel kell venni –
# különben a törlés után árva adat marad a gyerekről.
_GYEREK_TABLAK = (
    Vocabulary, ChildLearningTime, ChildTopicScore,
    ChildUsage, ChildProgress, ChildWallet, ChildCard,
)


def export_parent_data(parent_id: int) -> dict[str, Any]:
    """A szülőről és gyerekeiről tárolt ÖSSZES adat, letölthető alakban.

    Az adathordozhatósághoz kell: a felhasználó bármikor megkaphatja, amit
    róla tárolunk. A jelszó kivonata természetesen nem kerül bele.
    """
    db = _session()
    try:
        szulo = db.get(Parent, parent_id)
        if szulo is None:
            return {}
        ki: dict[str, Any] = {
            "szulo": {"email": szulo.email,
                      "regisztralt": szulo.created_at.isoformat()
                      if szulo.created_at else None},
            "gyerekek": [],
        }
        gyerekek = db.scalars(
            select(Child).where(Child.parent_id == parent_id)).all()
        for gy in gyerekek:
            sor: dict[str, Any] = {
                "nev": gy.name,
                "osztaly": gy.grade,
                "tanterv": gy.curriculum,
                "letrehozva": gy.created_at.isoformat() if gy.created_at else None,
                "beszelgetesek": [],
                "tanulasi_ido": [],
                "eredmenyek": [],
            }
            munkamenetek = db.scalars(
                select(ChatSession).where(ChatSession.child_id == gy.id)).all()
            for m in munkamenetek:
                uzenetek = db.scalars(
                    select(ChatMessage)
                    .where(ChatMessage.session_id == m.id)
                    .order_by(ChatMessage.id)).all()
                sor["beszelgetesek"].append({
                    "tantargy": m.subject,
                    "temakor": m.topic_id,
                    "uzenetek": [{"ki": u.role, "szoveg": u.content}
                                 for u in uzenetek],
                })
            for t in db.scalars(select(ChildLearningTime)
                                .where(ChildLearningTime.child_id == gy.id)).all():
                sor["tanulasi_ido"].append({
                    "datum": t.date.isoformat() if t.date else None,
                    "tantargy": t.subject, "perc": t.minutes})
            for e in db.scalars(select(ChildTopicScore)
                                .where(ChildTopicScore.child_id == gy.id)).all():
                sor["eredmenyek"].append({
                    "tantargy": getattr(e, "subject", None),
                    "temakor": getattr(e, "topic_id", None),
                    "szazalek": getattr(e, "score", None)})
            ki["gyerekek"].append(sor)
        return ki
    finally:
        db.close()


def delete_parent_account(parent_id: int) -> bool:
    """A szülő és MINDEN hozzá tartozó adat végleges törlése.

    Sorrend számít: előbb az üzenetek, mert azok a beszélgetéshez kötődnek,
    és csak a végén maga a szülő. Egyetlen tranzakció – ha bármi elhasal,
    semmi nem törlődik, és nem marad félig üres fiók.
    """
    db = _session()
    try:
        gyerek_idk = list(db.scalars(
            select(Child.id).where(Child.parent_id == parent_id)).all())

        if gyerek_idk:
            munkamenet_idk = list(db.scalars(
                select(ChatSession.id)
                .where(ChatSession.child_id.in_(gyerek_idk))).all())
            if munkamenet_idk:
                db.execute(delete(ChatMessage).where(
                    ChatMessage.session_id.in_(munkamenet_idk)))
            db.execute(delete(ChatSession).where(
                ChatSession.child_id.in_(gyerek_idk)))
            for tabla in _GYEREK_TABLAK:
                db.execute(delete(tabla).where(tabla.child_id.in_(gyerek_idk)))
            db.execute(delete(Child).where(Child.parent_id == parent_id))

        db.execute(delete(PasswordResetToken).where(
            PasswordResetToken.parent_id == parent_id))
        eredmeny = db.execute(delete(Parent).where(Parent.id == parent_id))
        db.commit()
        logger.info("Fiok torolve: parent_id=%s, gyerekek=%s",
                    parent_id, len(gyerek_idk))
        return bool(eredmeny.rowcount)
    except Exception:
        db.rollback()
        logger.exception("Fioktorles sikertelen: parent_id=%s", parent_id)
        return False
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
    *,
    grade_hu: int | None = None,
    grade_es: int | None = None,
) -> int:
    db = _session()
    try:
        g_hu = grade_hu
        if g_hu is None:
            try:
                g_hu = int(grade)
            except (ValueError, TypeError):
                g_hu = 1
        g_es = grade_es
        if g_es is None:
            try:
                g_es = min(int(grade), 6)
            except (ValueError, TypeError):
                g_es = 1
        child = Child(
            parent_id=parent_id,
            name=name.strip(),
            birth_date=birth_date,
            age=child_age_from_birth(birth_date),
            grade=grade.strip(),
            grade_hu=g_hu,
            grade_es=g_es,
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
    grade_hu: int | None = None,
    grade_es: int | None = None,
    voice_gender_hu: str | None = None,
    voice_gender_es: str | None = None,
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
        if grade_hu is not None:
            child.grade_hu = grade_hu
        if grade_es is not None:
            child.grade_es = grade_es
        child.country = country
        child.curriculum = curriculum
        child.region = region
        if voice_gender_hu in ("female", "male"):
            child.voice_gender_hu = voice_gender_hu
        if voice_gender_es in ("female", "male"):
            child.voice_gender_es = voice_gender_es
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


def promote_child_grade(child_id: int, parent_id: int, curriculum: str) -> dict[str, Any] | None:
    """Automatikus osztálylépés egy tantervben (grade_hu++ vagy grade_es++).
    Visszaadja a frissített child dict-et, vagy None-t ha nem található."""
    db = _session()
    try:
        child = db.scalar(
            select(Child).where(Child.id == child_id, Child.parent_id == parent_id)
        )
        if not child:
            return None
        curr = (curriculum or "").upper()
        if curr == "ES":
            old = child.grade_es or 1
            new = min(old + 1, 6)
            child.grade_es = new
            if str(child.grade) == str(old):
                child.grade = str(new)
            child.curriculum = "ES"
        else:
            old = child.grade_hu or 1
            new = min(old + 1, 8)
            child.grade_hu = new
            if str(child.grade) == str(old):
                child.grade = str(new)
            child.curriculum = "HU"
        db.commit()
        db.refresh(child)
        return _child_dict(child)
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
        "grade": row.grade,
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
    grade: int | None = None,
    curriculum_position: dict | None = None,
    force_new: bool = False,
) -> dict[str, Any]:
    lang_key = (language or "").strip().lower()
    tpid = topic_id.strip() if topic_id else ""
    db = _session()
    try:
        if not force_new:
            stmt = (
                select(ChatSession)
                .where(
                    ChatSession.child_id == child_id,
                    ChatSession.subject == subject,
                    ChatSession.language == lang_key,
                    ChatSession.topic_id == tpid,
                )
                .order_by(ChatSession.created_at.desc())
            )
            if grade is not None:
                stmt = stmt.where(ChatSession.grade == grade)
            row = db.scalar(stmt)
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
            grade=grade,
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


def replace_first_assistant_message(session_id: int, new_content: str) -> bool:
    """Lecseréli a session első assistant üzenetének tartalmát (pl. üdvözlő nyelvének javítása)."""
    db = _session()
    try:
        msg = db.scalar(
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id, ChatMessage.role == "assistant")
            .order_by(ChatMessage.created_at.asc())
        )
        if msg is not None:
            msg.content = new_content.strip()
            db.commit()
            return True
        return False
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
        "pont_jutalom": getattr(row, "pont_jutalom", 0) or 0,
    }


def bump_topic_reward(child_id: int, subject: str, grade: int,
                      topic_id: str) -> int:
    """Megjelöli, hogy ebből a témakörből most pont járt.

    Visszaadja, hogy a NÖVELÉS ELŐTT hányszor kapott már pontot – ebből
    tudja a hívó, hogy ez az első teljesítés (0) vagy már ismétlés.
    """
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
        if row is None:
            return 0
        elozo = row.pont_jutalom or 0
        row.pont_jutalom = elozo + 1
        db.commit()
        return elozo
    finally:
        db.close()


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


def get_child_topic_history(
    child_id: int, subject: str, grade: int
) -> list[dict[str, Any]]:
    """A diák eddigi témakör-eredményei (szűrve child_id + subject + grade).
    completed_at szerint rendezve. Üres lista, ha nincs adat."""
    db = _session()
    try:
        rows = db.scalars(
            select(ChildTopicScore)
            .where(
                ChildTopicScore.child_id == child_id,
                ChildTopicScore.subject == subject,
                ChildTopicScore.grade == grade,
            )
            .order_by(ChildTopicScore.completed_at.asc().nullsfirst())
        ).all()
        return [_topic_score_dict(r) for r in rows]
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
        "topic_id": row.topic_id,
        "word_native": row.word_native,
        "word_foreign": row.word_foreign,
        "learned_at": row.learned_at,
    }


def get_vocabulary(
    child_id: int,
    subject: str,
    *,
    language: str | None = None,
    topic_id: str | None = None,
) -> list[dict[str, Any]]:
    db = _session()
    try:
        stmt = select(Vocabulary).where(
            Vocabulary.child_id == child_id,
            Vocabulary.subject == subject,
        )
        if language:
            stmt = stmt.where(Vocabulary.language == language)
        if topic_id is not None:
            stmt = stmt.where(Vocabulary.topic_id == topic_id)
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
    topic_id: str | None = None,
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
                Vocabulary.language == (language or "").strip().lower(),
                Vocabulary.topic_id == topic_id,
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
            topic_id=topic_id,
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
    mode: str | None = None,
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
            mode=(mode or None),
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
            "mode": row.mode,
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


def get_topic_learning_minutes_since(
    child_id: int, subject: str, topic_id: str, since_dt: datetime
) -> float:
    """Visszaadja a témakörben `since_dt` utáni tanulási perceket."""
    db = _session()
    try:
        q = select(ChildLearningTime).where(
            ChildLearningTime.child_id == child_id,
            ChildLearningTime.subject == subject,
            ChildLearningTime.topic_id == topic_id,
            ChildLearningTime.session_start >= since_dt,
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


# ---------------------------------------------------------------------------
# Tudáskártyák
# ---------------------------------------------------------------------------


def ensure_child_cards_table() -> None:
    """Biztosítja, hogy a child_cards tábla létezik, a beragasztva oszloppal."""
    from sqlalchemy import text

    ChildCard.__table__.create(bind=_get_engine(), checkfirst=True)
    with _get_engine().begin() as conn:
        conn.execute(text(
            "ALTER TABLE child_cards ADD COLUMN IF NOT EXISTS "
            "beragasztva BOOLEAN NOT NULL DEFAULT FALSE"))


def add_child_card(child_id: int, card_id: str) -> dict[str, Any]:
    """Kártya jóváírása.

    Visszaad: {"uj": True/False, "darab": n}
    Ha a gyereknek már megvolt a lap, csak a darabszám nő – a hívó ebből
    tudja, hogy duplikátumért érmét kell adnia.
    """
    db = _session()
    try:
        row = db.scalars(
            select(ChildCard).where(
                ChildCard.child_id == child_id,
                ChildCard.card_id == card_id,
            )
        ).first()
        if row is None:
            row = ChildCard(child_id=child_id, card_id=card_id, darab=1)
            db.add(row)
            db.commit()
            return {"uj": True, "darab": 1}
        row.darab = (row.darab or 1) + 1
        db.commit()
        return {"uj": False, "darab": row.darab}
    finally:
        db.close()


# ══ pénztárca ═══════════════════════════════════════════════════════════════
def ensure_child_wallet_table() -> None:
    """Biztosítja, hogy a child_wallet tábla létezik, a kinézet-oszlopokkal."""
    from sqlalchemy import text

    ChildWallet.__table__.create(bind=_get_engine(), checkfirst=True)
    engine = _get_engine()
    with engine.begin() as conn:
        for oszlop in (
            "kinezet VARCHAR(32) NOT NULL DEFAULT 'alap'",
            "kinezetek TEXT NOT NULL DEFAULT 'alap'",
            "regi_erme_atvezetve BOOLEAN NOT NULL DEFAULT FALSE",
            "pont_atvezetve BOOLEAN NOT NULL DEFAULT FALSE",
        ):
            conn.execute(text(
                f"ALTER TABLE child_wallet ADD COLUMN IF NOT EXISTS {oszlop}"))


def ensure_child_usage_table() -> None:
    """Biztosítja, hogy a child_usage tábla létezik."""
    ChildUsage.__table__.create(bind=_get_engine(), checkfirst=True)


def add_usage(child_id: int, *, tts_karakter: int = 0, hang_mp: float = 0.0,
              be_token: int = 0, ki_token: int = 0, keres: int = 1) -> None:
    """Fogyasztás hozzáadása a mai naphoz. Hibára NEM dob: a mérés soha ne
    akadályozza meg a gyereket a tanulásban."""
    if not child_id:
        return
    try:
        db = _session()
        try:
            ma = datetime.now(timezone.utc).date()
            row = db.scalar(select(ChildUsage).where(
                ChildUsage.child_id == child_id, ChildUsage.nap == ma))
            if row is None:
                row = ChildUsage(child_id=child_id, nap=ma)
                db.add(row)
                db.flush()
            row.tts_karakter = (row.tts_karakter or 0) + max(0, int(tts_karakter))
            row.hang_mp = (row.hang_mp or 0.0) + max(0.0, float(hang_mp))
            row.be_token = (row.be_token or 0) + max(0, int(be_token))
            row.ki_token = (row.ki_token or 0) + max(0, int(ki_token))
            row.keres = (row.keres or 0) + max(0, int(keres))
            db.commit()
        finally:
            db.close()
    except Exception:
        logger.warning("add_usage sikertelen", exc_info=True)


def mai_tts_karakter(child_id: int) -> int:
    """Mennyi felolvasást használt el a gyerek MA. A napi kerethez kell."""
    db = _session()
    try:
        ma = datetime.now(timezone.utc).date()
        row = db.scalar(select(ChildUsage).where(
            ChildUsage.child_id == child_id, ChildUsage.nap == ma))
        return int(row.tts_karakter or 0) if row else 0
    finally:
        db.close()


def get_usage(child_id: int | None = None, napok: int = 30) -> list[dict[str, Any]]:
    """Az elmúlt N nap fogyasztása. child_id nélkül minden gyerekre."""
    db = _session()
    try:
        hatar = datetime.now(timezone.utc).date() - timedelta(days=max(1, napok))
        q = select(ChildUsage).where(ChildUsage.nap >= hatar)
        if child_id:
            q = q.where(ChildUsage.child_id == child_id)
        rows = db.scalars(q.order_by(ChildUsage.nap.desc())).all()
        return [{
            "child_id": r.child_id, "nap": r.nap.isoformat(),
            "tts_karakter": r.tts_karakter or 0, "hang_mp": r.hang_mp or 0.0,
            "be_token": r.be_token or 0, "ki_token": r.ki_token or 0,
            "keres": r.keres or 0,
        } for r in rows]
    finally:
        db.close()


# ---------------------------------------------------------------------------
# ADMIN ÖSSZESÍTŐ – az üzemeltető egyetlen kérdésére válaszol:
# ki használja, mire, és mennyibe kerül.
#
# Egy hívásban gyűjti össze az összes családot, hogy ne kelljen családonként
# külön lekérdezni – tíz családnál még mindegy, százan már nem.
# ---------------------------------------------------------------------------


def admin_csaladok(napok: int = 30) -> list[dict[str, Any]]:
    """Minden család, gyerekeivel, tanulási idejével és fogyasztásával."""
    db = _session()
    try:
        hatar_nap = datetime.now(timezone.utc).date() - timedelta(days=max(1, napok))

        gyerek_szulo: dict[int, int] = {}
        csaladok: dict[int, dict[str, Any]] = {}
        for p in db.scalars(select(Parent).order_by(Parent.created_at)).all():
            csaladok[p.id] = {
                "id": p.id, "email": p.email,
                "regisztralt": p.created_at, "utoljara": p.last_seen,
                "gyerekek": [],
            }
        for c in db.scalars(select(Child)).all():
            if c.parent_id not in csaladok:
                continue
            gyerek_szulo[c.id] = c.parent_id
            csaladok[c.parent_id]["gyerekek"].append({
                "id": c.id, "nev": c.name, "osztaly": c.grade,
                "tanterv": (c.curriculum or "HU"),
                "perc_hang": 0.0, "perc_szoveg": 0.0, "perc_ismeretlen": 0.0,
                "napi": {},
                "tantargyak": {},
                "tts_karakter": 0, "hang_mp": 0.0,
                "be_token": 0, "ki_token": 0, "keres": 0,
                "utolso_tanulas": None,
            })

        gyerek_mutato = {gy["id"]: gy
                         for cs in csaladok.values() for gy in cs["gyerekek"]}

        for t in db.scalars(select(ChildLearningTime)
                            .where(ChildLearningTime.date >= hatar_nap)).all():
            gy = gyerek_mutato.get(t.child_id)
            if gy is None:
                continue
            perc = float(t.minutes or 0.0)
            kulcs = {"voice": "perc_hang", "text": "perc_szoveg"}.get(
                t.mode or "", "perc_ismeretlen")
            gy[kulcs] += perc
            gy["tantargyak"][t.subject] = gy["tantargyak"].get(t.subject, 0.0) + perc
            if gy["utolso_tanulas"] is None or t.date > gy["utolso_tanulas"]:
                gy["utolso_tanulas"] = t.date

        for u in db.scalars(select(ChildUsage)
                            .where(ChildUsage.nap >= hatar_nap)).all():
            gy = gyerek_mutato.get(u.child_id)
            if gy is None:
                continue
            gy["tts_karakter"] += u.tts_karakter or 0
            gy["hang_mp"] += u.hang_mp or 0.0
            gy["be_token"] += u.be_token or 0
            gy["ki_token"] += u.ki_token or 0
            gy["keres"] += u.keres or 0
            # naponkénti bontás is, hogy családonként látszódjon a lefutás
            n = gy["napi"].setdefault(u.nap, {
                "nap": u.nap, "tts_karakter": 0, "hang_mp": 0.0,
                "be_token": 0, "ki_token": 0, "keres": 0})
            n["tts_karakter"] += u.tts_karakter or 0
            n["hang_mp"] += u.hang_mp or 0.0
            n["be_token"] += u.be_token or 0
            n["ki_token"] += u.ki_token or 0
            n["keres"] += u.keres or 0

        for cs in csaladok.values():
            cs["gyerekek"].sort(key=lambda g: g["nev"] or "")
            csalad_napi: dict[Any, dict[str, Any]] = {}
            for gy in cs["gyerekek"]:
                gy["tantargyak"] = sorted(gy["tantargyak"].items(),
                                          key=lambda x: -x[1])
                for nap, n in gy["napi"].items():
                    cn = csalad_napi.setdefault(nap, {
                        "nap": nap, "tts_karakter": 0, "hang_mp": 0.0,
                        "be_token": 0, "ki_token": 0, "keres": 0})
                    for k in ("tts_karakter", "hang_mp", "be_token",
                              "ki_token", "keres"):
                        cn[k] += n[k]
                gy["napi"] = sorted(gy["napi"].values(), key=lambda x: x["nap"])
            cs["napi"] = sorted(csalad_napi.values(), key=lambda x: x["nap"])
        return sorted(csaladok.values(),
                      key=lambda c: (c["utoljara"] is None, 
                                     -(c["utoljara"].timestamp() if c["utoljara"] else 0)))
    finally:
        db.close()


def napi_fogyasztas(napok: int = 30) -> list[dict[str, Any]]:
    """Naponkénti összesítés az egész szolgáltatásra. Ebből látszik, mikor
    ugrik meg a használat – és mikor a számla."""
    db = _session()
    try:
        hatar = datetime.now(timezone.utc).date() - timedelta(days=max(1, napok))
        ossz: dict[Any, dict[str, Any]] = {}
        for u in db.scalars(select(ChildUsage).where(ChildUsage.nap >= hatar)).all():
            n = ossz.setdefault(u.nap, {
                "nap": u.nap, "tts_karakter": 0, "hang_mp": 0.0,
                "be_token": 0, "ki_token": 0, "keres": 0, "gyerek": set()})
            n["tts_karakter"] += u.tts_karakter or 0
            n["hang_mp"] += u.hang_mp or 0.0
            n["be_token"] += u.be_token or 0
            n["ki_token"] += u.ki_token or 0
            n["keres"] += u.keres or 0
            n["gyerek"].add(u.child_id)
        for n in ossz.values():
            n["gyerek"] = len(n["gyerek"])
        return sorted(ossz.values(), key=lambda x: x["nap"])
    finally:
        db.close()


def torol_meresi_adatokat(parent_id: int | None = None) -> tuple[int, int]:
    """A mérési adatok törlése. (fogyasztási sor, tanulási sor).

    A gyerekek, a haladás és a fiókok ÉRINTETLENEK: csak a statisztika ürül.
    parent_id nélkül mindenkire vonatkozik.
    """
    db = _session()
    try:
        if parent_id:
            gyerekek = [c.id for c in db.scalars(
                select(Child).where(Child.parent_id == parent_id)).all()]
        else:
            gyerekek = [c.id for c in db.scalars(select(Child)).all()]
        if not gyerekek:
            return (0, 0)
        u = db.query(ChildUsage).filter(
            ChildUsage.child_id.in_(gyerekek)).delete(synchronize_session=False)
        t = db.query(ChildLearningTime).filter(
            ChildLearningTime.child_id.in_(gyerekek)).delete(synchronize_session=False)
        db.commit()
        return (int(u or 0), int(t or 0))
    except Exception:
        db.rollback()
        logger.warning("torol_meresi_adatokat sikertelen", exc_info=True)
        return (0, 0)
    finally:
        db.close()


def szuloi_jelentes(parent_id: int, napok: int = 7) -> dict[str, Any]:
    """A szülői levél nyersanyaga: mit tanult a gyerek, mi ment jól, hol gyenge.

    Egy hívásban gyűjti össze, mert a levélküldő nem akar tízszer kérdezni.
    Ha egy gyerek nem tanult, ATTÓL IS kikerül a levélbe – a szülőnek az is
    információ, hogy a héten nem történt semmi.
    """
    ma = datetime.now(timezone.utc).date()
    hatar = ma - timedelta(days=max(1, napok))
    db = _session()
    try:
        gyerekek = []
        for c in db.scalars(select(Child).where(
                Child.parent_id == parent_id).order_by(Child.name)).all():
            percek: dict[str, float] = {}
            ossz = 0.0
            napok_halmaz = set()
            for t in db.scalars(select(ChildLearningTime).where(
                    ChildLearningTime.child_id == c.id,
                    ChildLearningTime.date >= hatar)).all():
                p = float(t.minutes or 0.0)
                if p <= 0:
                    continue
                percek[t.subject] = percek.get(t.subject, 0.0) + p
                ossz += p
                napok_halmaz.add(t.date)

            kesz, gyenge = [], []
            for sz in db.scalars(select(ChildTopicScore).where(
                    ChildTopicScore.child_id == c.id)).all():
                mikor = getattr(sz, "completed_at", None)
                if not mikor or mikor.date() < hatar:
                    continue
                tetel = {"nev": sz.topic_name or sz.topic_id,
                         "pont": int(sz.score or 0),
                         "targy": sz.subject}
                (kesz if sz.passed else gyenge).append(tetel)

            uj_szo = db.scalar(select(func.count()).select_from(Vocabulary)
                               .where(Vocabulary.child_id == c.id)) or 0
            kartya = db.scalar(select(func.count()).select_from(ChildCard)
                               .where(ChildCard.child_id == c.id)) or 0

            gyerekek.append({
                "nev": c.name,
                "osztaly": c.grade,
                "perc": round(ossz),
                "napok": len(napok_halmaz),
                "tantargyak": sorted(percek.items(), key=lambda x: -x[1]),
                "teljesitett": kesz[:6],
                "gyenge": gyenge[:4],
                "szavak": int(uj_szo),
                "kartyak": int(kartya),
            })

        p = db.get(Parent, parent_id)
        return {
            "parent_id": parent_id,
            "email": p.email if p else "",
            "mod": (p.ertesites if p else "heti") or "heti",
            "napok": napok,
            "tol": hatar, "ig": ma,
            "gyerekek": gyerekek,
            "van_tanulas": any(g["perc"] > 0 for g in gyerekek),
        }
    finally:
        db.close()


def _wallet_row(db, child_id: int) -> "ChildWallet":
    row = db.get(ChildWallet, child_id)
    if row is None:
        row = ChildWallet(child_id=child_id)
        db.add(row)
        db.flush()
    # Egyszeri átvezetés: a régi, tantárgyankénti `coins` összege ide kerül,
    # hogy a gyereknek ne tűnjön el, amit korábban összegyűjtött. Minden
    # pénztárca-hozzáférésnél lefut egyszer, aztán a jelző lezárja.
    if not (row.regi_erme_atvezetve or False):
        regi = db.scalar(
            select(func.coalesce(func.sum(ChildProgress.coins), 0))
            .where(ChildProgress.child_id == child_id)
        ) or 0
        row.erme = (row.erme or 0) + int(regi)
        row.regi_erme_atvezetve = True
        db.flush()
    # A pont beolvasztása az érmébe – egyszer, gyerekenként.
    if not (row.pont_atvezetve or False):
        row.erme = (row.erme or 0) + int(row.pont or 0)
        row.pont = 0
        row.pont_atvezetve = True
        db.flush()
    return row


def get_wallet(child_id: int) -> dict[str, Any]:
    """A gyerek pénztárcája. Egy érme van az egész alkalmazásban: ez.

    Első olvasáskor egyszer átvezeti ide a régi, tantárgyankénti `coins`
    összeget, hogy a gyereknek ne tűnjön el, amit korábban összegyűjtött.
    """
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        db.commit()
        return {
            # EGY valuta van. A "pont" kulcs megmaradt a régi hívók kedvéért,
            # de ugyanazt az egy egyenleget mutatja, mint az "erme".
            "pont": r.erme or 0,
            "osszes_pont": r.osszes_pont or 0,
            "erme": r.erme or 0,
            "ingyen_tasak": r.ingyen_tasak or 0,
            "tasak_szam": r.tasak_szam or 0,
            "kinezet": r.kinezet or "alap",
            "kinezetek": r.kinezetek or "alap",
        }
    finally:
        db.close()


def spend_coins_wallet(child_id: int, mennyi: int) -> bool:
    """Érme levonása. False, ha nincs elég – ilyenkor semmit nem változtat."""
    if mennyi <= 0:
        return True
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        if (r.erme or 0) < mennyi:
            db.commit()
            return False
        r.erme = (r.erme or 0) - mennyi
        db.commit()
        return True
    finally:
        db.close()


def unlock_kinezet(child_id: int, kinezet_id: str) -> str:
    """Kinézet feloldása. Visszaadja a feloldottak új listáját."""
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        meglevo = [s.strip() for s in (r.kinezetek or "alap").split(",") if s.strip()]
        if kinezet_id not in meglevo:
            meglevo.append(kinezet_id)
        r.kinezetek = ",".join(meglevo)
        db.commit()
        return r.kinezetek
    finally:
        db.close()


def set_kinezet(child_id: int, kinezet_id: str) -> bool:
    """Aktív kinézet beállítása. False, ha nincs feloldva."""
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        meglevo = [s.strip() for s in (r.kinezetek or "alap").split(",") if s.strip()]
        if kinezet_id not in meglevo:
            db.commit()
            return False
        r.kinezet = kinezet_id
        db.commit()
        return True
    finally:
        db.close()


def add_points(child_id: int, mennyi: int) -> dict[str, Any]:
    """Jutalom jóváírása. EGY valuta van: az érme.

    A név megmaradt, mert sok helyről hívjuk, de az összeg az érmére megy –
    a gyereknek egyetlen számot kell követnie, és mindenre költheti.
    """
    if mennyi <= 0:
        return get_wallet(child_id)
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        r.erme = (r.erme or 0) + mennyi
        r.osszes_pont = (r.osszes_pont or 0) + mennyi   # életút-összeg
        db.commit()
        return {"pont": r.erme, "osszes_pont": r.osszes_pont,
                "erme": r.erme, "ingyen_tasak": r.ingyen_tasak or 0,
                "tasak_szam": r.tasak_szam or 0}
    finally:
        db.close()


def spend_points(child_id: int, mennyi: int) -> bool:
    """Levonás az érméből. False, ha nincs elég – ilyenkor nem változtat."""
    return spend_coins_wallet(child_id, mennyi)


def add_coins_wallet(child_id: int, mennyi: int) -> int:
    """Érme jóváírása duplikátumért. Visszaadja az új egyenleget."""
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        r.erme = (r.erme or 0) + max(0, mennyi)
        db.commit()
        return r.erme
    finally:
        db.close()


def add_free_pack(child_id: int, mennyi: int = 1) -> int:
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        r.ingyen_tasak = (r.ingyen_tasak or 0) + max(0, mennyi)
        db.commit()
        return r.ingyen_tasak
    finally:
        db.close()


def use_free_pack(child_id: int) -> bool:
    """Ingyen tasak beváltása. False, ha nincs."""
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        if (r.ingyen_tasak or 0) < 1:
            db.commit()
            return False
        r.ingyen_tasak -= 1
        db.commit()
        return True
    finally:
        db.close()


def bump_pack_counter(child_id: int) -> int:
    """A kibontott tasakok száma – ebből lesz a tasak sorszáma a bontáskor."""
    db = _session()
    try:
        r = _wallet_row(db, child_id)
        r.tasak_szam = (r.tasak_szam or 0) + 1
        db.commit()
        return r.tasak_szam
    finally:
        db.close()


def get_child_cards(child_id: int) -> dict[str, dict[str, Any]]:
    """card_id -> {"darab": n, "szerezve": datetime}"""
    db = _session()
    try:
        rows = db.scalars(
            select(ChildCard).where(ChildCard.child_id == child_id)
        ).all()
        return {
            r.card_id: {"darab": r.darab or 1, "szerezve": r.szerezve,
                        "beragasztva": bool(getattr(r, "beragasztva", False))}
            for r in rows
        }
    finally:
        db.close()


def beragaszt(child_id: int, card_id: str) -> bool:
    """A gyerek beragasztotta a lapot az albumba.

    False, ha nincs is meg neki – így a böngészőből nem lehet olyan lapot
    beragasztani, amit nem szerzett meg.
    """
    db = _session()
    try:
        row = db.scalars(select(ChildCard).where(
            ChildCard.child_id == child_id,
            ChildCard.card_id == card_id,
        )).first()
        if row is None:
            return False
        row.beragasztva = True
        db.commit()
        return True
    finally:
        db.close()


def count_child_cards(child_id: int) -> int:
    """Hány KÜLÖNBÖZŐ lapja van a gyereknek."""
    db = _session()
    try:
        return len(
            db.scalars(
                select(ChildCard.card_id).where(ChildCard.child_id == child_id)
            ).all()
        )
    finally:
        db.close()
