import sqlite3
from pathlib import Path
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


# DATABASE CONNECTION
def get_db_connection():
    database_path = Path(__file__).with_name("students.db")
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn


# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# SINGLE STUDENT ENDPOINT
@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "2024-00076",
        "name": "Missy Miranda",
        "program": "BSIT",
        "year": 3,
        "section": "3B"
    })


# HELLO ENDPOINT
@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })


# CAMPUS ENDPOINT
@app.route('/campus')
def get_campus():
    return jsonify({
        "campus": "San Enrique-Campus",
        "location": "Iloilo",
        "status": "Open",
        "type": "University Campus"
    })


# GRADE ENDPOINT
@app.route('/grade')
def get_grade():
    return jsonify({
        "subject": "IT 3120",
        "grade": 95,
        "remarks": "Passed"
    })


# GET ALL STUDENTS
@app.route('/students')
def get_students():
    conn = get_db_connection()

    try:
        students = conn.execute(
            'SELECT * FROM students'
        ).fetchall()

        return jsonify([dict(student) for student in students])
    finally:
        conn.close()


# GET STUDENT BY ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()

    try:
        student = conn.execute(
            'SELECT * FROM students WHERE id = ?',
            (id,)
        ).fetchone()

        if student is None:
            return jsonify({
                "error": "Student not found"
            }), 404

        return jsonify(dict(student))
    finally:
        conn.close()


# GET STUDENTS BY SECTION
# Supports uppercase and lowercase section requests
@app.route('/students/section/<section>')
def get_students_by_section(section):
    conn = get_db_connection()

    try:
        students = conn.execute(
            'SELECT * FROM students WHERE UPPER(section) = ?',
            (section.upper(),)
        ).fetchall()

        return jsonify([dict(student) for student in students])
    finally:
        conn.close()


# RUN FLASK APPLICATION
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
