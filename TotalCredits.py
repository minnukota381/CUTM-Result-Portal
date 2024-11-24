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
