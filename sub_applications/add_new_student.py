from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QHBoxLayout, QGridLayout

from linked_array import LinkedArray
from students_serializer import Student
from sub_applications.student_provider import StudentsProvider


class AddNewStudentWindow(QWidget):
    def __init__(self, students_provider: StudentsProvider, parent=None):
        super().__init__(parent)
        self.students_provider = students_provider

        self.layout = QGridLayout()

        self.student_name = QLineEdit(self)
        self.student_name.setPlaceholderText("student name")

        self.student_id = QLineEdit(self)
        self.student_id.setPlaceholderText("student id")

        self.add_button = QPushButton("Add Student", self)
        self.add_button.clicked.connect(self.button_clicked)

        self.layout.addWidget(self.student_name, 0, 0)
        self.layout.addWidget(self.student_id, 0, 1)
        self.layout.addWidget(self.add_button, 1, 0, 2, 0)

        self.setFixedSize(QSize(300, 100))
        self.setLayout(self.layout)
        self.setWindowTitle("Add New Student")


    def button_clicked(self):
        student_name = self.student_name.text()
        student_id = self.student_id.text()

        if not student_name or not student_id:
            return

        self.students_provider.get_students().append(Student(student_name, student_id, []))

        print(f"Student {student_name} with ID {student_id} added.")
        self.close()
