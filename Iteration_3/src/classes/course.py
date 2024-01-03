import json
import os


class Course:
    def __init__(
        self,
        course_code=None,
        course_name=None,
        lecturer=None,
        students=[],
        prerequisites=[],
        credits=None,
        year=0,
    ):
        self.course_code = course_code
        self.course_name = course_name
        self.lecturer = lecturer
        self.students = students
        self.prerequisites = prerequisites
        self.credits = credits
        self.year = year

    def enroll_student(self, student):
        if student not in self.students:
            self.students.append(student)

    def get_course_code(self):
        return self.course_code

    def get_course_year(self):
        return self.year

    def get_prerequisites(self):
        return self.prerequisites

    def get_course_name(self):
        return self.course_name

    @staticmethod
    def get_list_info(list):
        if len(list) == 0:
            return ""
        all_info = ""
        for item in list:
            all_info += item.get_info()
        return all_info

    def get_info(self):
        return f"course_code: {self.course_code}\ncourse_name: {self.course_name}\nlecturer: {self.lecturer}\nstudents: {self.students}\nprerequisites: {self.prerequisites}\ncredits: {self.credits}\nyear: {self.year}"

    def to_json_file(self):
        filename = f"database/courses/{self.course_code}.json"
        with open(filename, "w") as json_file:
            json.dump(self.get_info(), json_file, indent=2)
        return filename

    @classmethod
    def from_json_file(cls, user_id):
        filename = f"{user_id}.json"
        if os.path.exists(filename):
            with open(filename, "r") as json_file:
                student_data = json.load(json_file)
                return cls(**student_data)
        else:
            raise FileNotFoundError(f"File {filename} does not exist.")