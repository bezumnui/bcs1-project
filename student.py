import dataclasses
from tkinter.font import names

from linked_array import LinkedArray


@dataclasses.dataclass
class Student:
    name: str
    id: str
    grades: list[float]

    def set_name(self, name: str):
        self.name = name

    def average_grade(self):
        if len(self.grades) > 0:
            average = sum(self.grades) / len(self.grades)
            return round(average, 2)
        else:
            return 0.0
    
    def serialize(self):
        result = f"{self.name};{self.id};"
        for i in range(len(self.grades)):
            if i > 0:
                result += ","
            result += "{0:.2f}".format(self.grades[i])
        return result + "\n"

    @staticmethod
    def deserialize(text: str):
        name, id_, grades_raw = text.split(";")
        raw_grades = grades_raw[:-1]
        if raw_grades:
            grades = raw_grades.split(",")
        else:
            grades = []
        return Student(name, id_, list(map(float, grades)))

    def __repr__(self):
        return f"Student(name: \"{self.name}\", id: {self.id}, grades: {self.grades})"


class StudentSerializer:
    def __init__(self, filename="students.txt"):
        self.filename = filename

    def load_file(self, students: LinkedArray):
        students.clear()
        with open(self.filename, "r") as f:
            while line := f.readline():
                students.append(Student.deserialize(line))
        return students

    def save_to_file(self, students: list[Student]):
        with open(self.filename, "w") as f:
            for student in students:
                f.write(student.serialize())
