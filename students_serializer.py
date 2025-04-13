import dataclasses
from tkinter.font import names

from linked_array import LinkedArray


@dataclasses.dataclass
class Student:
    name: str
    id: int
    grades: list[float]

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
        grades = grades_raw[:-1].split(",")
        return Student(name, int(id_), list(map(float, grades)))

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
        # must be stored as first_name last_name;student_id;0.5,4.5,2.5;\n
        with open(self.filename, "w") as f:
            for student in students:
                f.write(student.serialize())

    # def merge_by_id(self, ):


if __name__ == '__main__':
    StudentSerializer().save_to_file([
        Student("George Viznyuk", 2023, [10, 24.5, 3.5]),
        Student("Heorhii Vizniuk", 2024, [1.22514, 24.5, 3.5]),
    ])
    print(StudentSerializer().load_file())