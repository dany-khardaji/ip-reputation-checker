import sqlite3
from datetime import datetime               # Used to generate the checked_at timestamp


DB_FILE = "checks.db"                       # The database file, gitignored (generated, not source)


# Creates the checks table if it doesn't exist. Run once at setup.
def init_db():
    conn = sqlite3.connect(DB_FILE)         # opens the file, creates it if missing
    cursor = conn.cursor()                  # the object that actually runs SQL

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   -- SQLite fills this in automatically
        ip TEXT NOT NULL,
        verdict TEXT NOT NULL,
        score INTEGER NOT NULL,
        country TEXT,                           -- nullable, private IPs have no country
        isp TEXT,                               -- nullable, same reason
        total_reports INTEGER,
        checked_at TEXT NOT NULL                -- YYYY-MM-DD HH:MM:SS, sorts chronologically
    )
    """)

    conn.commit()
    conn.close()


# Writes one check result from check_ip() into the database as a new row.
def save_check(result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO checks (ip, verdict, score, country, isp, total_reports, checked_at)   -- id is left out, AUTOINCREMENT fills it in
        VALUES (?, ?, ?, ?, ?, ?, ?)        -- placeholders, filled safely by the tuple below
    """, (
        result["ip"],                       # these six come from check_ip()'s return dict
        result["verdict"],
        result["score"],
        result["country"],
        result["isp"],
        result["total_reports"],
        time_stamp                          # AbuseIPDB doesn't send a time, we make one                          
    ))

    conn.commit()
    conn.close()


# Only runs when db.py is executed directly
if __name__ == "__main__":                  
    init_db()
    print("Database initialized")