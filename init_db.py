import sqlite3
from pathlib import Path

# Database connection
database_path = Path(__file__).with_name("students.db")
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
""")

# Clear existing records
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'students'")

# Five sample student records
students = [
    ("2024-1001", "Karol Vincent Pedregosa", "BSA", 4, "ANSCI"),
    ("2024-1002", "Liza Java", "BEED", 1, "D"),
    ("2024-1003", "Paul Joseph Miranda", "BSCS", 2, "A"),
    ("2024-1004", "Issa Kailah Javier", "BSHM", 3, "C"),
    ("2024-1005", "Rizza Anthea Malacad", "BSED-Filipino", 4, "B")
]

# Insert records into the database
cursor.executemany("""
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
""", students)

# Save and close the database
connection.commit()
connection.close()

print("Database created successfully.")
