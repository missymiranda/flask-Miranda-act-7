import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# Database connection
def get_db_connection():
    database_path = Path(__file__).with_name("students.db")
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Student API
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00076",
        "name": "Missy Miranda",
        "program": "BSIT",
        "year": 3,
        "section": "3B"
    })


# Greeting API
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# Custom Campus API - Activity 4
@app.route('/campus')
def get_campus():
    return jsonify({
        "campus": "San Enrique-Campus",
        "location": "Iloilo",
        "status": "Open",
        "type": "University Campus"
    })


# Second custom API endpoint - Activity 4
@app.route('/grade')
def get_grade():
    return jsonify({
        "subject": "IT 3120",
        "grade": 95,
        "remarks": "Passed"
    })


# Get all students from the database
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


# Get one student by database ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?',
        (id,)
    ).fetchone()
    conn.close()

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(dict(student))


# Additional endpoint: Get students by section
@app.route('/students/section/<section>')
def get_students_by_section(section):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE section = ?',
        (section,)
    ).fetchall()
    conn.close()

    return jsonify([dict(student) for student in students])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
