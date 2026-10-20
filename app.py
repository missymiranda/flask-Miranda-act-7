from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
