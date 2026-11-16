import sqlite3
from pathlib import Path
from .config import settings
def connect():
    if not settings.database_url.startswith("sqlite:///"):
        raise RuntimeError("Starter currently supports SQLite; configure PostgreSQL for production.")
    path = settings.database_url.replace("sqlite:///", "", 1)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path, check_same_thread=False)
    c.row_factory = sqlite3.Row
    return c
def init_db():
    with connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL)")
        c.commit()
