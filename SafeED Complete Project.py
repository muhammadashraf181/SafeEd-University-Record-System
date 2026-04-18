import hashlib
from datetime import datetime

def log_event(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("safeed_security_log.txt", "a") as log:
        log.write(f"[{timestamp}] {event}\n")

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password_hash(stored_hash, password):
    return stored_hash == hashlib.sha256(password.encode()).hexdigest()

teachers_raw = [
    {"id": 1, "username": "Muhammad Ahsan Khan", "password": "ahsan123", "students": [101, 102, 103, 104, 105]},
    {"id": 2, "username": "Mr. Babar", "password": "babar123", "students": [104, 105]},
    {"id": 3, "username": "Sir Maqsood Razi", "password": "maqsoodrazi123", "students": [104, 105]},
    {"id": 4, "username": "Mr. Maaz", "password": "maaz123", "students": [104, 105]},
]

students_raw = [
    {"id": 101, "username": "Miral Naz", "password": "miral101", "grades": 95, "attendance": 92, "fee": "Paid"},
    {"id": 102, "username": "Muhammad Ashraf", "password": "ashraf102", "grades": 78, "attendance": 89, "fee": "Unpaid"},
    {"id": 103, "username": "Hunain Imran", "password": "hunain103", "grades": 78, "attendance": 89, "fee": "Unpaid"},
    {"id": 104, "username": "Ahmed", "password": "ahmed104", "grades": 85, "attendance": 92, "fee": "Paid"},
    {"id": 105, "username": "Mahnoor Khan", "password": "mahnoor105", "grades": 78, "attendance": 89, "fee": "Unpaid"},
    {"id": 106, "username": "Sami", "password": "sami106", "grades": 70, "attendance": 76, "fee": "Paid"},
    {"id": 107, "username": "Ali", "password": "ali107", "grades": 82, "attendance": 88, "fee": "Paid"},
    {"id": 108, "username": "Misbah", "password": "misbah108", "grades": 70, "attendance": 80, "fee": "Unpaid"},
]

teachers = []
students = []


def initialize_users():
    for t in teachers_raw:
        teachers.append({
            "id": t["id"],
            "username": t["username"],
            "password_hash": generate_password_hash(t["password"]),
            "students": t["students"]
        })

    for s in students_raw:
        students.append({
            "id": s["id"],
            "username": s["username"],
            "password_hash": generate_password_hash(s["password"]),
            "grades": s["grades"],
            "attendance": s["attendance"],
            "fee": s["fee"]
        })

initialize_users()

def find_teacher_by_username(username):
    return next((t for t in teachers if t["username"] == username), None)

def find_student_by_username(username):
    return next((s for s in students if s["username"] == username), None)

def find_student_by_id(student_id):
    return next((s for s in students if s["id"] == student_id), None)

def teacher_can_view_student(teacher, student_id):
    return student_id in teacher["students"]

def authenticate(username, password):
    teacher = find_teacher_by_username(username)
    if teacher and check_password_hash(teacher["password_hash"], password):
        log_event(f"LOGIN SUCCESS -> Role: Teacher | Username: {username}")
        return "teacher", teacher

    student = find_student_by_username(username)
    if student and check_password_hash(student["password_hash"], password):
        log_event(f"LOGIN SUCCESS -> Role: Student | Username: {username}")
        return "student", student

    log_event(f"LOGIN FAILED -> Username Tried: {username}")
    return None, None

def student_menu(student):
    log_event(f"STUDENT DASHBOARD ACCESS -> Student ID: {student['id']} | Name: {student['username']}")

    print("\n--- Student Dashboard ---")
    print("Applying Bell-LaPadula: You can view only your own record.")
    print(f"ID: {student['id']}")
    print(f"Name: {student['username']}")
    print(f"Grades: {student['grades']}")
    print(f"Attendance: {student['attendance']}%")
    print(f"Fee Status: {student['fee']}")
    print("\nData Confidentiality ensured.")
    
def teacher_menu(teacher):
    log_event(f"TEACHER DASHBOARD ACCESS -> Teacher: {teacher['username']}")

    print("\n--- Teacher Dashboard ---")
    print(f"Welcome, {teacher['username']}")
    print("Assigned Students:")

    for sid in teacher["students"]:
        s = find_student_by_id(sid)
        if s:
            print("-" * 40)
            print(f"ID: {s['id']}")
            print(f"Name: {s['username']}")
            print(f"Grades: {s['grades']}")
            print(f"Attendance: {s['attendance']}%")
            print(f"Fee Status: {s['fee']}")

    while True:
        choice = input("\nDo you want to update a student's record? (y/n): ").lower()
        if choice == "n":
            log_event(f"TEACHER LOGOUT -> Teacher: {teacher['username']}")
            print("Logging out...")
            break

        try:
            sid = int(input("Enter Student ID to update: "))
            if not teacher_can_view_student(teacher, sid):
                log_event(f"UNAUTHORIZED UPDATE ATTEMPT -> Teacher: {teacher['username']} | Student ID: {sid}")
                print("Unauthorized access! You can only update assigned students.")
                continue

            student = find_student_by_id(sid)
            if not student:
                print("Student not found.")
                continue

            new_grade = input("Enter new grade (leave blank to skip): ")
            new_attendance = input("Enter new attendance (leave blank to skip): ")
            new_fee = input("Enter new fee status (Paid/Unpaid, leave blank to skip): ")

            if new_grade:
                student["grades"] = int(new_grade)
            if new_attendance:
                student["attendance"] = int(new_attendance)
            if new_fee:
                student["fee"] = new_fee

            log_event(
                f"STUDENT RECORD UPDATED -> Teacher: {teacher['username']} | "
                f"Student ID: {sid} | Grade:{new_grade or 'No Change'} | "
                f"Attendance:{new_attendance or 'No Change'} | Fee:{new_fee or 'No Change'}"
            )

            print("Student record updated successfully.")

        except ValueError:
            print("Invalid input.")

def main():
    print("=" * 50)
    print("----- SAFEED SECURITY MODEL -----")
    print("=" * 50)

    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    role, user = authenticate(username, password)

    if role == "teacher":
        teacher_menu(user)
    elif role == "student":
        student_menu(user)
        log_event(f"STUDENT LOGOUT -> Student: {user['username']}")
    else:
        print("Invalid credentials.")

if __name__ == "__main__":
    while True:
        main()
        again = input("\nDo you want to login again? (y/n): ").lower()
        if again != "y":
            log_event("SYSTEM EXIT -> SafeEd Program Closed")
            print("Thank you for using SafeEd Console System.")
            break
