# Simple Student Grade Manager
# Author: Sumayo Enbeye
# Description: A small program to manage and display student grades using lists.

def add_grade(grades):
    """Add a new grade to the list."""
    try:
        grade = float(input("Enter grade (0-100): "))
        if 0 <= grade <= 100:
            grades.append(grade)
            print(f"Grade {grade} added successfully!")
        else:
            print("Grade must be between 0 and 100.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def show_grades(grades):
    """Display all grades."""
    if not grades:
        print("No grades yet.")
    else:
        print("\nAll grades:")
        for i, g in enumerate(grades, 1):
            print(f"{i}. {g}")

def show_stats(grades):
    """Show average, highest, and lowest grade."""
    if not grades:
        print("No grades to calculate.")
        return
    avg = sum(grades) / len(grades)
    print(f"\nAverage grade: {avg:.2f}")
    print(f"Highest grade: {max(grades)}")
    print(f"Lowest grade: {min(grades)}")

def main():
    grades = []
    while True:
        print("\n--- Grade Manager ---")
        print("1. Add grade")
        print("2. Show all grades")
        print("3. Show statistics")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            add_grade(grades)
        elif choice == '2':
            show_grades(grades)
        elif choice == '3':
            show_stats(grades)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
