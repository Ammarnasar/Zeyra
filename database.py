import sqlite3

conn = sqlite3.connect("database.db")
c = conn.cursor()

# 🔥 Applicants Table (UPDATED)
c.execute("""
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    email TEXT,
    phone TEXT,
    phone_alt TEXT,

    dob TEXT,
    nationality TEXT,
    national_id TEXT,
    address TEXT,

    gender TEXT,
    marital_status TEXT,

    degree TEXT,
    major TEXT,
    graduation_year TEXT,

    experience_years TEXT,
    employment_status TEXT,
    current_salary TEXT,
    expected_salary TEXT,

    skills TEXT,

    language TEXT,
    language_level TEXT,

    cv TEXT,
    id_front TEXT,
    id_back TEXT
)
""")

# 🔥 Messages Table
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject TEXT,
    message TEXT
)
""")

conn.commit()
conn.close()

print("Database Ready (FULL SYSTEM) ✅")