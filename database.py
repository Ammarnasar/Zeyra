import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("""
CREATE TABLE applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    age TEXT,
    national_id TEXT,
    english_level TEXT,
    cv TEXT,
    id_front TEXT,
    id_back TEXT
)
""")

c.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()

print("Database Created ✅")