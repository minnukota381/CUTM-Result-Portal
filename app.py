from flask import Flask, render_template, request, redirect, jsonify
import os
import sqlite3
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import pytz

load_dotenv()

app = Flask(__name__)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(MONGO_URI)


def convert_to_ist(gmt_time):
    ist_timezone = pytz.timezone('Asia/Kolkata')  
    gmt_time = gmt_time.replace(tzinfo=pytz.utc)  
    ist_time = gmt_time.astimezone(ist_timezone)  
    formatted_time = ist_time.strftime('%Y-%m-%d %I:%M:%S %p IST')  
    return formatted_time

def convert_grade_to_integer(grade):
    grade_mapping = {
        'O': 10,
        'E': 9,
        'A': 8,
        'B': 7,
        'C': 6,
        'D': 5,
        'S': 0,
        'M': 0,
        'F': 0
    }
    return grade_mapping.get(grade, 0)  

def calculate_sgpa(result):
    total_credits = 0
    total_weighted_grades = 0
    
    for row in result:
        credits_parts = [float(part) for part in row[7].split('+')]
        total_credits += sum(credits_parts)
        
        if set(row[8]) <= {'O', 'E', 'A', 'B', 'C', 'D', 'S', 'M', 'F'}:
            grade = convert_grade_to_integer(row[8])
        else:
            grade = float(row[8])
        
        weighted_grade = grade * sum(credits_parts)
        total_weighted_grades += weighted_grade
    
    sgpa = total_weighted_grades / total_credits if total_credits != 0 else 0  
    return sgpa, total_credits

def calculate_cgpa(registration, name):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT Credits, Grade FROM CUTM WHERE (Reg_No = ? OR LOWER(Name) = LOWER(?))", (registration, name))
    rows = cur.fetchall()
    conn.close()

    total_credits = 0
    total_weighted_grades = 0

    for row in rows:
        credits_parts = [float(part) for part in row[0].split('+')]
        
        if set(row[1]) <= {'O', 'E', 'A', 'B', 'C', 'D', 'S', 'M', 'F'}:
            grade = convert_grade_to_integer(row[1])
        else:
            grade = float(row[1])
        
        total_credits += sum(credits_parts)
        weighted_grade = grade * sum(credits_parts)
        total_weighted_grades += weighted_grade

    cgpa = total_weighted_grades / total_credits if total_credits != 0 else 0

    return cgpa

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     try:
#         conn = sqlite3.connect('database.db')
#         cur = conn.cursor()

#         if request.method == 'POST' and request.form.get('registration'):
#             registration = request.form.get('registration')
#             cur.execute("SELECT DISTINCT Sem FROM `CUTM` WHERE Reg_No = ?", (registration,))
#         else:
#             cur.execute("SELECT DISTINCT Sem FROM `CUTM`")
        
#         semesters = [row[0] for row in cur.fetchall()]
#         conn.close()

#         result = None
#         count = 0
#         sgpa = None
#         total_credits = None
#         cgpa = None
#         message = None

#         if request.method == 'POST':
#             name = request.form.get('name')
#             registration = request.form.get('registration')
#             semester = request.form.get('semester')

#             conn = sqlite3.connect('database.db')
#             cur = conn.cursor()

#             cur.execute("SELECT * FROM `CUTM` WHERE (Reg_No = ? OR LOWER(Name) = LOWER(?)) AND Sem = ?", (registration, name, semester))
#             result = cur.fetchall()
#             count = len(result)

#             if count == 0:
#                 message = "No records found for the entered name or registration number."

#             if result:
#                 sgpa, total_credits = calculate_sgpa(result)

#             cgpa = calculate_cgpa(registration, name)
#             conn.close()

#             current_time_utc = datetime.utcnow()
#             current_time_ist = convert_to_ist(current_time_utc)

#             client = MongoClient(MONGO_URI)
#             db = client.get_database('cutm')
#             collection = db.get_collection('userInput')

#             data = {
#                 'registration': registration,
#                 'semester': semester,
#                 'time': current_time_ist
#             }

#             collection.insert_one(data)

#             return render_template('display.html', result=result, count=count, sgpa=sgpa, total_credits=total_credits, cgpa=cgpa, message=message, selected_semester=semester, semesters=semesters)

#         return render_template('index.html', semesters=semesters)
#     except Exception as e:
#         return render_template('index.html', error=str(e))

@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        if request.method == 'POST' and request.form.get('registration'):
            registration = request.form.get('registration')
            cur.execute("SELECT DISTINCT Sem FROM `CUTM` WHERE Reg_No = ?", (registration,))
        else:
            cur.execute("SELECT DISTINCT Sem FROM `CUTM`")
        
        semesters = [row[0] for row in cur.fetchall()]
        conn.close()

        result = None
        count = 0
        sgpa = None
        total_credits = None
        cgpa = None
        total_all_semester_credits = 0  # To store total credits from all semesters
        message = None

        if request.method == 'POST':
            name = request.form.get('name')
            registration = request.form.get('registration')
            semester = request.form.get('semester')

            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            cur.execute("SELECT * FROM `CUTM` WHERE (Reg_No = ? OR LOWER(Name) = LOWER(?)) AND Sem = ?", (registration, name, semester))
            result = cur.fetchall()
            count = len(result)

            if count == 0:
                message = "No records found for the entered name or registration number."

            if result:
                sgpa, total_credits = calculate_sgpa(result)

            # Calculate total credits across all semesters
            cur.execute("SELECT Credits FROM `CUTM` WHERE Reg_No = ?", (registration,))
            all_credits = cur.fetchall()
            total_all_semester_credits = sum([sum([float(part) for part in row[0].split('+')]) for row in all_credits])

            cgpa = calculate_cgpa(registration, name)
            conn.close()

            current_time_utc = datetime.utcnow()
            current_time_ist = convert_to_ist(current_time_utc)

            client = MongoClient(MONGO_URI)
            db = client.get_database('cutm')
            collection = db.get_collection('userInput')

            data = {
                'registration': registration,
                'semester': semester,
                'time': current_time_ist
            }

            collection.insert_one(data)

            return render_template('display.html', result=result, count=count, sgpa=sgpa, total_credits=total_credits, cgpa=cgpa, total_all_semester_credits=total_all_semester_credits, message=message, selected_semester=semester, semesters=semesters)

        return render_template('index.html', semesters=semesters)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/semesters', methods=['POST'])
def get_semesters():
    try:
        registration = request.form.get('registration')
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT Sem FROM `CUTM` WHERE Reg_No = ?", (registration,))
        semesters = [row[0] for row in cur.fetchall()]
        conn.close()
        return jsonify(semesters=semesters)
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect('/admin/panel')
        else:
            error = 'Invalid username or password'
            return render_template('admin_login.html', error=error)
    return render_template('admin_login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin/panel')
def admin_panel():
    return render_template('admin_panel.html')

if __name__ == '__main__':
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT Sem FROM CUTM")
    semesters = [row[0] for row in cur.fetchall()]

    conn.close()

    app.run(port=5000, host="0.0.0.0", debug=True)
