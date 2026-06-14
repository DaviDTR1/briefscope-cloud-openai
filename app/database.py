from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DB_PATH

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_conn, _record):
    """Enable WAL mode and foreign-key enforcement on every new connection."""
    cur = dbapi_conn.cursor()
    cur.execute("PRAGMA journal_mode=WAL")       # concurrent reads while writing
    cur.execute("PRAGMA foreign_keys=ON")         # DB-level cascade enforcement
    cur.execute("PRAGMA synchronous=NORMAL")      # safe + faster than FULL
    cur.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    from app import models  # noqa: F401 – registers all models
    Base.metadata.create_all(bind=engine)
    _ensure_indexes()


def _ensure_indexes():
    """Idempotently create indexes on existing databases that predate the definitions."""
    stmts = [
        "CREATE INDEX IF NOT EXISTS ix_documents_project_id    ON documents(project_id)",
        "CREATE INDEX IF NOT EXISTS ix_conversations_project_id ON conversations(project_id)",
        "CREATE INDEX IF NOT EXISTS ix_messages_conversation_id ON messages(conversation_id)",
        "CREATE INDEX IF NOT EXISTS ix_messages_is_compacted    ON messages(is_compacted)",
    ]
    with engine.connect() as conn:
        for stmt in stmts:
            conn.execute(text(stmt))
        conn.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
