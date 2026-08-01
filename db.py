import sqlite3


DB_FILE = "checks.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT NOT NULL,
        verdict TEXT NOT NULL,
        score INTEGER NOT NULL,
        country TEXT,
        isp TEXT,
        total_reports INTEGER,
        checked_at TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized")