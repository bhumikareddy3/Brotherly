import sqlite3
from pathlib import Path

# Absolute path to backend/database/brotherly.db
DB_PATH = Path(__file__).resolve().parent / "brotherly.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assessments (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER REFERENCES users(id),

        name TEXT,
        age INTEGER,
        education TEXT,
        current_status TEXT,
        experience INTEGER,

        primary_recommendation TEXT,
        secondary_recommendation TEXT,

        career_path TEXT,

        risk_score INTEGER,
        financial_score INTEGER,
        leadership_score INTEGER,
        readiness_score INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER REFERENCES users(id),

        user_message TEXT,

        ai_response TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------------------------------
# Users
# --------------------------------------------------------------------------

def create_user(name, email, password_hash):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (name, email, password_hash)
    VALUES (?, ?, ?)
    """, (name, email.lower().strip(), password_hash))

    user_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return user_id


def get_user_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, password_hash FROM users WHERE email = ?",
        (email.lower().strip(),),
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {"id": row[0], "name": row[1], "email": row[2], "password_hash": row[3]}


def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (user_id,),
    )
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {"id": row[0], "name": row[1], "email": row[2]}


# --------------------------------------------------------------------------
# Assessments
# --------------------------------------------------------------------------

def save_assessment(
    user_id,
    name,
    age,
    education,
    current_status,
    experience,
    primary,
    secondary,
    career_path,
    scores
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO assessments (

        user_id,

        name,
        age,
        education,
        current_status,
        experience,

        primary_recommendation,
        secondary_recommendation,

        career_path,

        risk_score,
        financial_score,
        leadership_score,
        readiness_score

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_id,

        name,
        age,
        education,
        current_status,
        experience,

        primary,
        secondary,

        career_path,

        scores["risk"],
        scores["financial"],
        scores["leadership"],
        scores["readiness"]
    ))

    conn.commit()
    conn.close()


ASSESSMENT_COLUMNS = [
    "id", "user_id", "name", "age", "education", "current_status", "experience",
    "primary_recommendation", "secondary_recommendation", "career_path",
    "risk_score", "financial_score", "leadership_score", "readiness_score",
    "created_at",
]


def get_all_assessments(user_id):
    """Return all of this user's assessments (newest first) as a list of dicts."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM assessments WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cursor.fetchall()

    conn.close()

    return [dict(zip(ASSESSMENT_COLUMNS, row)) for row in rows]


def get_latest_assessment(user_id):
    """Return this user's most recent assessment as a dict, or None."""

    assessments = get_all_assessments(user_id)
    return assessments[0] if assessments else None


def get_total_assessments(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM assessments WHERE user_id = ?",
        (user_id,),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_recommendation_counts(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        primary_recommendation,
        COUNT(*)
    FROM assessments
    WHERE user_id = ?
    GROUP BY primary_recommendation
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_career_path_counts(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        career_path,
        COUNT(*)
    FROM assessments
    WHERE user_id = ?
    GROUP BY career_path
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------------------------------------------------
# Chats
# --------------------------------------------------------------------------

def save_chat(user_id, user_message, ai_response):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chats (
        user_id,
        user_message,
        ai_response
    )
    VALUES (?, ?, ?)
    """, (
        user_id,
        user_message,
        ai_response
    ))

    conn.commit()
    conn.close()


def get_chats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        user_message,
        ai_response,
        created_at

    FROM chats

    WHERE user_id = ?

    ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_recent_chats(user_id, limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        user_message,
        ai_response
    FROM chats
    WHERE user_id = ?
    ORDER BY id DESC
    LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_total_chats(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM chats WHERE user_id = ?",
        (user_id,),
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count
