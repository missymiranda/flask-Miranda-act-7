import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# =========================================
# DATABASE CONNECTION
# =========================================

def get_db_connection():
    db_path = Path(__file__).with_name("students.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================
# EXISTING LABORATORY ACTIVITY ROUTES
# =========================================

@app.route("/student")
def student():
    return jsonify({
        "student_id": "2024-00076",
        "name": "Missy Miranda",
        "program": "BSIT",
        "year": 3,
        "section": "3B"
    })


@app.route("/hello")
def hello():
    name = request.args.get("name", "Student")
    return jsonify({
        "message": f"Hello, {name}!"
    })


@app.route("/campus")
def campus():
    return jsonify({
        "campus": "San Enrique-Campus",
        "location": "Iloilo",
        "status": "Open",
        "type": "University Campus"
    })


@app.route("/grade")
def grade():
    score = request.args.get("score", type=float)

    if score is None:
        return jsonify({
            "error": "Please provide a valid score."
        }), 400

    if not 0 <= score <= 100:
        return jsonify({
            "error": "Score must be between 0 and 100."
        }), 400

    if score >= 90:
        remarks = "Excellent"
    elif score >= 80:
        remarks = "Very Good"
    elif score >= 75:
        remarks = "Passed"
    else:
        remarks = "Needs Improvement"

    return jsonify({
        "subject": "IT 3120",
        "grade": score,
        "remarks": remarks
    })


# =========================================
# LABORATORY ACTIVITY 7: DATABASE API
# =========================================

# Get all students from the database
@app.route("/students")
def get_students():
    conn = get_db_connection()

    try:
        students = conn.execute(
            "SELECT * FROM students ORDER BY id"
        ).fetchall()

        return jsonify([dict(student) for student in students])
    finally:
        conn.close()


# Get one student by database ID
@app.route("/students/<int:id>")
def get_student_by_id(id):
    conn = get_db_connection()

    try:
        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (id,)
        ).fetchone()

        if student is None:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify(dict(student))
    finally:
        conn.close()


# Additional task: Get students by section
@app.route("/students/section/<section>")
def get_students_by_section(section):
    conn = get_db_connection()

    try:
        students = conn.execute(
            """
            SELECT * FROM students
            WHERE UPPER(section) = UPPER(?)
            ORDER BY id
            """,
            (section,)
        ).fetchall()

        return jsonify([dict(student) for student in students])
    finally:
        conn.close()


# =========================================
# RUN FLASK APPLICATION
# =========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
