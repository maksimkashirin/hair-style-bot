import sqlite3
from datetime import datetime


DB_NAME = "bot_database.db"


def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            task_type TEXT NOT NULL,
            photo_path TEXT,
            result_path TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_generation(
    user_id: int,
    username: str | None,
    task_type: str,
    photo_path: str,
    result_path: str
):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO generations (
            user_id,
            username,
            task_type,
            photo_path,
            result_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        username,
        task_type,
        photo_path,
        result_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()
    connection.close()