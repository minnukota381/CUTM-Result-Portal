import sqlite3

def fetch_subjects_and_grades(db_file, reg_no):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT Subject_Name, Grade FROM CUTM WHERE Reg_No = ?", (reg_no,))
        subjects = cursor.fetchall()

        return subjects

    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        if conn:
            conn.close()

def update_grade(db_file, reg_no, subject_name, new_grade):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("UPDATE CUTM SET Grade = ? WHERE Reg_No = ? AND Subject_Name = ?", (new_grade, reg_no, subject_name))

        conn.commit()

        if cursor.rowcount > 0:
            print("Update successful!")
        else:
            print("No rows updated. Please check if the provided Registration Number and Subject Name exist.")

    except sqlite3.Error as e:
        print(f"Error updating data: {e}")

    finally:
        if conn:
            conn.close()

db_file = "database.db"

reg_no = input("Enter the Registration Number: ")

subjects_and_grades = fetch_subjects_and_grades(db_file, reg_no)

if subjects_and_grades:
    print("Subjects and Grades:")
    for i, (subject, grade) in enumerate(subjects_and_grades, 1):
        print(f"{i}. {subject}: {grade}")

    subject_index = int(input("Enter the index of the subject you want to update: ")) - 1
    if 0 <= subject_index < len(subjects_and_grades):
        selected_subject, current_grade = subjects_and_grades[subject_index]
        new_grade = input(f"Enter the new grade for {selected_subject}: ")
        update_grade(db_file, reg_no, selected_subject, new_grade)
    else:
        print("Invalid subject index entered.")
else:
    print("No subjects found for the provided Registration Number.")
