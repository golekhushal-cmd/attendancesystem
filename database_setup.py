import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "attendance.db"
)


def create_database():

    connection = sqlite3.connect(
        DB_PATH
    )

    cursor = connection.cursor()

   

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT
        )
    """)

 

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            date TEXT,
            time TEXT
        )
    """)

    connection.commit()
    connection.close()

    print(
        "Database Created Successfully!" 
    )


if __name__ == "__main__":
    create_database()