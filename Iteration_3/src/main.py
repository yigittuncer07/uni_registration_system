from classes.advisor import Advisor
from classes.course import Course
from classes.draft import Draft
from classes.grade import Grade
from classes.lecturer import Lecturer
from classes.staff import Staff
from classes.student_affairs_staff import Student_Affairs_Staff
from classes.student import Student
from classes.transcript import Transcript
import json
import logging
import time

# GLOBAL VARIABLES
users = []
courses = []
incorrect_attempts = 0

# LOGGING CONFIG
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logfile.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def system_exit():
    save_users_to_json()
    save_courses_to_json()
    exit()


def print_title(message):
    print("\n\033[1;94m" + message + "\033[0m")


def print_info(message):
    print("\n\033[92m" + message + "\033[0m")


def print_error(message):
    print("\n\033[91m" + message + "\033[0m")


def print_commands(message):
    print("\n\033[93m" + message + "\033[0m")


def save_users_to_json():
    logger.info("save students to file called")
    for item in users:
        item.to_json_file()


def save_courses_to_json():
    logger.info("save courses to file called")
    for item in courses:
        item.to_json_file()


def get_user_with_id(id):
    for item in users:
        if item.get_user_id() == id:
            return item
    return None


def get_users_from_json():
    print("get all from json called")

def student_login():
    print_title("STUDENT LOGIN")
    student_id_input = input("enter student id: ")
    student = get_user_with_id(student_id_input)

    while student == None or not isinstance(student, Student):
        print_error(f"no student with studentID  {student_id_input}")
        student_id_input = input("enter student id: ")
        if student_id_input == "":
            return
        student = get_user_with_id(student_id_input)

    student_password_input = input("enter password: ")
    global incorrect_attempts
    if student.get_password() != student_password_input:
        print_error("Wrong Password!")
        incorrect_attempts += 1
        if incorrect_attempts == 3:
            print_error("Maximum password attempts reached. Please wait for 10 seconds.")
            time.sleep(10)  # Pause the program for 10 seconds
            incorrect_attempts = 0  # Reset the incorrect attempts counter

        if incorrect_attempts <= 3:
            return

    print_title("STUDENT INTERFACE")
    print_info(f"Welcome {student.get_name()}")

    while True:
        print_commands("1-> see transcript\n2-> register to a course\n3-> exit")
        user_input = input("==> ")

        while not user_input in ["1", "2", "3"]:
            print_error("invalid input!")
            print_commands("1-> see transcript\n2-> register to a course\n3-> exit")
            user_input = input("==> ")

        if user_input == "1":
            print_title("TRANSCRIPT")
            if student.get_transcript() == None:
                print_error("transcript not found! contact student affairs")
            else:
                print_info(student.get_transcript().to_string())
        elif user_input == "2":
            print_title("COURSE REGISTRATION")
            eligable_courses = student.get_eligible_courses(courses)
            draft = student.get_draft()
            advisor = student.get_advisor()

            while True:
                print_info("Eligable Courses:")
                if len(eligable_courses) == 0:
                    print("no eligable courses")
                else:
                    for course in eligable_courses:
                        print(course.get_course_code() + " " + course.get_course_name())

                print_info("Current Draft:")
                for course in draft.get_courses():
                    print(course.get_course_code())

                print_commands(
                    'add "course" -> add to draft\nremove "course" -> remove from draft\nsubmit -> send draft to advisor for approval\nexit -> save draft and exit'
                )
                user_input = input("==> ")
                user_input = user_input.split()
                if user_input[0] == "add":
                    course_found = False
                    for course in eligable_courses:
                        if course.get_course_code() == user_input[1]:
                            if draft.add_to_draft(course):
                                print_info("course added")
                                eligable_courses.remove(course)
                            else:
                                print_error("course couldnt be added!")
                            course_found = True

                    if not course_found:
                        print_error("no such course!")

                elif user_input[0] == "remove":
                    course_found = False

                    for course in draft.get_courses():
                        if course.get_course_code() == user_input[1]:
                            course_found = True
                            if draft.remove_from_draft(course):
                                print_info("course removed")
                                eligable_courses.append(course)
                            else:
                                print_error("course couldnt be removed")

                    if not course_found:
                        print_error("no such course in draft!")

                elif user_input[0] == "submit":
                    if len(draft.get_courses()) == 0:
                        print_error("cannot send empty draft!")
                    else:
                        if advisor.add_draft(draft):
                            print_info("draft updated")
                        else:
                            print_info("draft sent for approval")

                elif user_input[0] == "exit":
                    print_info("draft saved!")
                    return
                else:
                    print_error("Invalid Input!")

        elif user_input == "3":
            return


def staff_login():
    print_title("STAFF LOGIN")
    staff_id_input = input("enter staff id: ")
    staff = get_user_with_id(staff_id_input)

    while staff == None or not isinstance(staff, Staff):
        print_error(f"no staff with staffId  {staff_id_input}")
        staff_id_input = input("enter staff id: ")
        if staff_id_input == "":
            return
        staff = get_user_with_id(staff_id_input)

    staff_password_input = input("enter password: ")
    global incorrect_attempts
    if staff.get_password() != staff_password_input:
        print_error("Wrong Password!")
        incorrect_attempts += 1
        if incorrect_attempts == 3:
            print_error("Maximum password attempts reached. Please wait for 10 seconds.")
            time.sleep(10)  # Pause the program for 10 seconds
            incorrect_attempts = 0  # Reset the incorrect attempts counter

        if incorrect_attempts <= 3:
            return

    if isinstance(staff, Lecturer):
        if isinstance(staff, Advisor):
            # Implement Advisor interface
            print_title("ADVISOR INTERFACE")
            print_info(f"Welcome {staff.get_name()}")
            while True:
                print_commands("1-> student registrations\n2-> exit")
                user_input = input("==> ")
    
                while not user_input in ["1", "2"]:
                    print_error("invalid input!")
                    print_commands("1->exit")
                    user_input = input("==> ")

                if user_input == "2":
                    return
                
                if user_input == "1":
                    print_title("STUDENT REGISTRATIONS")

                    while True:
                        print_commands("1-> evaluate pending drafts\n2-> exit")
                        user_input = input("==> ")

                        while not user_input in ["1", "2"]:
                            print_error("invalid input!")
                            print_commands("1-> evaluate pending drafts\n2-> exit")
                            user_input = input("==> ")

                        if user_input == "1":                               
                            draft_approval_process(Advisor)

                        if user_input == "2":
                            return
        else:
            # Implement Lecturer interface
            print_title("LECTURER INTERFACE")
            print_info(f"Welcome {staff.get_name()}")
            while True:
                print_commands("1-> exit")
                user_input = input("==> ")

                while not user_input in ["1"]:
                    print_error("invalid input!")
                    print_commands("1->exit")
                    user_input = input("==> ")

                if user_input == "1":
                    return

    elif isinstance(staff, Student_Affairs_Staff):
        # Implement Student Affairs Staff interface
        print_title("STUDENT AFFAIRS INTERFACE")
        print_info(f"Welcome {staff.get_name()}")

        while True:
            print_commands("1-> exit")
            user_input = input("==> ")

            while not user_input in ["1"]:
                print_error("invalid input!")
                print_commands("1->exit")
                user_input = input("==> ")

            if user_input == "1":
                return


def init():
    grade0 = Grade("CSE101", "AA", "98", True)
    grade1 = Grade("CSE201", "AA", "99", True)
    grade2 = Grade("CSE301", "AA", "100", True)

    grades = []
    grades.append(grade0)
    grades.append(grade1)
    grades.append(grade2)

    transcript = Transcript(3.98, grades)

    lecturer = Lecturer(
        user_id="160111",
        name="Talip Demirel",
        password="111",
        email="talipdemirel@marun.edu.tr",
        department="science",
        field="applied mathematics",
    )
    student0 = Student(
        user_id="150111",
        name="Yigit Tuncer",
        password="111",
        email="yigittuncer@marun.edu.tr",
        transcript=Transcript(),
        year=2,
    )
    student1 = Student(
        user_id="150031",
        name="Kerem Demirel",
        password="111",
        email="keremozkan@marun.edu.tr",
        transcript=Transcript(),
        year=3,
    )
    student2 = Student(
        user_id="150333",
        name="Ceren Ozge",
        password="111",
        email="cerenozge@marun.edu.tr",
        transcript=transcript,
        year=3,
    )
    student3 = Student(
        user_id="150444",
        name="Cem Mazlum",
        password="111",
        transcript=Transcript(),
        email="cemmazlum@marun.edu.tr",
        year=3,
    )

    students = []
    students.append(student0)
    students.append(student1)
    students.append(student2)
    students.append(student3)

    drafts = []
    advisor = Advisor(
        user_id="150555",
        name="Nazmi Emir Arslan",
        password="111",
        email="emirarslan@marun.edu.tr",
        department="science",
        field="statistician",
        students=students,
        drafts=drafts
        
    )

    for student in students:
        student.set_advisor(advisor)

    course0 = Course(course_code="CSE101",course_name="Intro to Rust Programming", lecturer=lecturer)
    course1 = Course(course_code="CSE201",course_name="Intermediate Rust Programming", lecturer=lecturer)
    course3 = Course(course_code="IAC",course_name="Interior Architecture with AI", lecturer=lecturer)
    course4 = Course(course_code="CSE401",course_name="Final Project")

    prerequisites = []
    prerequisites.append(course0)
    prerequisites.append(course1)

    course2 = Course(
        "CSE301", "Advanced Rust Programming", lecturer, students, prerequisites, 12, 2
    )

    courses.append(course0)
    courses.append(course1)
    courses.append(course2)
    courses.append(course3)
    courses.append(course4)

    draft = Draft(student=student2)

    student_affairs_staff = Student_Affairs_Staff(
        user_id="160222",
        name="Hasan Pekedis",
        password="111",
        email="hasanpekedis@marun.edu.tr",
        department="engineering",
        students=students,
    )

    users.append(student0)
    users.append(student1)
    users.append(student2)
    users.append(student3)
    users.append(lecturer)
    users.append(advisor)
    users.append(student_affairs_staff)

    for student in students:
        student.set_advisor(advisor)

def draft_approval_process(advisor):
                                
    if not Advisor.draft:
        print("No drafts to approve currently")
        return

    print("\nPlease proceed with this draft:\n")
    
    for draft in advisor.super().__init__.drafts:
        student = get_user_with_id(draft.student.student_id, "Student")
        print(student.get_info() + "\nStudentID: " + str(student.student_id) + "\n\nCourses:")

        for course in draft.courses:
            print(course.course_name + " " + course.course_code)
            advisor_input = input("Do you approve of this course? (yes/no): ")

            if advisor_input.lower() == "yes":

                print.info(f"Draft course approved by: {advisor.staff_id} from ID: {student.student_id}")
            elif advisor_input.lower() == "no":
                print.info(f"Draft course rejected by: {advisor.staff_id} from ID: {student.student_id}")
            else:
                print("Unknown input!")
                print.error("Invalid input entered.")

        print(f"Draft for student {student.student_id} complete")
        print.info(f"Draft completed by: {advisor.staff_id}")

# MAIN PROCESS
init()
while True:
    print_title("BYS")
    print_commands("1-> student login\n2-> staff login\n3-> exit")
    user_input = input("==> ")

    while not user_input in ["1", "2", "3"]:
        print_error("invalid input!")
        print_commands("1-> student login\n2-> staff login\n3-> exit")
        user_input = input("==> ")

    if user_input == "1":
        student_login()
    elif user_input == "2":
        staff_login()
    elif user_input == "3":
        system_exit()
