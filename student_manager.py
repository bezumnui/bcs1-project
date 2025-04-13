
from PyQt6.QtCore import Qt, QStringListModel
from PyQt6.QtWidgets import QWidget, QLineEdit, QGridLayout, QPushButton, QCompleter, QLabel, QVBoxLayout, \
    QHBoxLayout, QSizePolicy, QListView

from linked_array import LinkedArray
from students_serializer import StudentSerializer, Student


#
#
class StudentsCompleter(QCompleter):
    def __init__(self, students: LinkedArray[Student], parent=None):
        super().__init__([], parent)
        self.students = students

        self.students_strings = []
        self.__model: QStringListModel = self.model()
        # self.__model = QStringListModel()

        self.setModel(self.__model)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.max_filter = 4
        self.update_students()
        self.update("")


    def update(self, text):
        filtered_index = 0
        filtered = []
        for student in self.students_strings:
            if filtered_index == self.max_filter:
                break
            if text.lower() in student.lower():
                filtered.append(student)
                filtered_index += 1
        self.__model.setStringList(filtered)

    def update_students(self):
        self.students_strings.clear()

        for student in self.students:
            self.students_strings.append(f"{student.id} {student.name}")


class StudentManager(QWidget):
    def __init__(self):
        super().__init__()
        self.manager_layout = QGridLayout()
        self.max_grades = 10
        self.current_student: Student | None = None


        self.search_widget: QWidget | None = None
        self.display_widget: QWidget | None = None

        self.search_menu: QListView | None = None
        self.search_text_completer: QCompleter | None = None
        self.search_text_input: QLineEdit | None = None
        self.search_button: QPushButton | None = None

        self.display_id_label_label: QLabel | None = None
        self.display_id_label: QLabel | None = None

        self.display_name_input_label: QLabel | None = None
        self.display_name_input: QLineEdit | None = None

        self.display_grades_label: QLabel | None = None

        self.display_grades: list[QLineEdit] = []
        self.display_add_grade_button: QPushButton | None = None
        self.display_remove_grade_button: QPushButton | None = None

        self.serializer = StudentSerializer()
        self.students = LinkedArray()
        self.reload_students()


        self.setup_search_widget()
        self.setup_display_widget()

        self.manager_layout.addWidget(self.search_widget, 0, 0)
        self.manager_layout.addWidget(self.display_widget, 0, 1)

        self.search_widget.setFixedWidth(280)
        self.setLayout(self.manager_layout)


    def reload_students(self):
        self.serializer.load_file(self.students)

    # def get_student

    def setup_search_widget(self):
        search_layout = QGridLayout()
        self.search_widget = QWidget()

        self.search_menu = QListView()
        self.search_text_input = QLineEdit()
        self.search_button = QPushButton("Find")

        self.search_text_completer = StudentsCompleter(self.students)
        self.search_text_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.search_text_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        # self.search_text_completer.setModel(QStringListModel(self.search_text_completer))

        self.search_menu.setFixedHeight(200)
        # self.search_menu.

        self.search_text_input.setCompleter(self.search_text_completer)

        self.search_text_input.setPlaceholderText("Enter User ID")
        self.search_text_input.textEdited.connect(self.search_text_completer.update)
        self.search_button.clicked.connect(self.find_handle)

        search_layout.addWidget(self.search_menu, 0, 0)
        search_layout.addWidget(self.search_text_input, 1, 0)
        search_layout.addWidget(self.search_button, 2, 0)
        # self.setLayout(search_layout)
        self.search_widget.setLayout(search_layout)

    def find_handle(self):
        text = self.search_text_input.text().split(" ")
        if len(text) == 0:
            return
        id_to_search = text[0]

        for student in self.students:
            if id_to_search == str(student.id):
                self.display_name_input.setText(student.name)
                self.display_id_label.setText(str(student.id))
                grades_size = len(student.grades)
                self.current_student = student
                for i in range(len(self.display_grades)):
                    grade = self.display_grades[i]
                    if grades_size > i:
                        grade.setText(str(student.grades[i]))
                        grade.show()
                    else:
                        grade.hide()


    def setup_display_widget(self):
        layout = QVBoxLayout()
        self.display_widget = QWidget()

        self.display_id_label_label = QLabel("Student ID:")
        self.display_id_label = QLabel("0")

        self.display_name_input_label = QLabel("Student's full name:")
        self.display_name_input = QLineEdit()

        self.display_grades_label = QLabel("Grades:")
        self.display_add_grade_button = QPushButton("+")
        self.display_remove_grade_button = QPushButton("-")

        self.display_name_input.setPlaceholderText("Student Name")
        self.display_add_grade_button.clicked.connect(self.handle_add_grade)
        self.display_remove_grade_button.clicked.connect(self.handle_remove_grade)

        layout.addWidget(self.display_id_label_label)
        layout.addWidget(self.display_id_label)

        layout.addWidget(self.display_name_input_label)
        layout.addWidget(self.display_name_input)

        layout.addWidget(self.display_grades_label)

        grades_layouts: [QHBoxLayout] = []



        for i in range(self.max_grades):
            if len(grades_layouts) == i // 5:
                current_layout = QHBoxLayout()
                grades_layouts.append(current_layout)

            current_layout = grades_layouts[i // 5]
            widget = QLineEdit()
            current_layout.addWidget(widget, alignment=Qt.AlignmentFlag.AlignLeft)
            widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

            current_layout.setStretch(i % 5, 0)

            widget.setFixedWidth(35)
            widget.hide()
            self.display_grades.append(widget)


        grades_control_layout = QHBoxLayout()
        grades_layouts.append(grades_control_layout)
        grades_control_layout.addWidget(self.display_add_grade_button, alignment=Qt.AlignmentFlag.AlignLeft)
        grades_control_layout.addWidget(self.display_remove_grade_button, alignment=Qt.AlignmentFlag.AlignLeft)
        grades_control_layout.setContentsMargins(0, 0, 0, 0)

        self.display_add_grade_button.setMaximumSize(35, 35)
        self.display_remove_grade_button.setMaximumSize(35, 35)

        for grade_layout in grades_layouts:
            grades_widget = QWidget()
            grades_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

            grades_widget.setLayout(grade_layout)
            layout.addWidget(grades_widget)

        self.display_widget.setLayout(layout)

    def handle_add_grade(self):
        if not self.current_student:
            return
        grades = self.current_student.grades
        grades_size = len(grades)

        if grades_size == self.max_grades:
            return

        self.current_student.grades.append(0)
        self.display_grades[grades_size].setText("0.00")
        self.display_grades[grades_size].show()

    def handle_remove_grade(self):
        if not self.current_student:
            return
        grades = self.current_student.grades
        grades_size = len(grades)

        if grades_size == 0:
            return

        self.current_student.grades.pop(grades_size-1)
        self.display_grades[grades_size-1].hide()