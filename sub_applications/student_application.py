from PyQt6.QtCore import Qt, QStringListModel, QModelIndex
from PyQt6.QtWidgets import QWidget, QLineEdit, QGridLayout, QPushButton, QCompleter, QLabel, QVBoxLayout, \
    QHBoxLayout, QSizePolicy, QListView, QAbstractItemView, QStyle, QComboBox

from linked_array import LinkedArray
from student import StudentSerializer, Student
from sub_applications.add_new_student import AddNewStudentWindow
from sub_applications.student_provider import StudentsProvider
from sub_applications.sub_application import SubApplication
from utils import is_float


SORT_ALPHABETIC_LABEL = "Sort Alphabetically"
SORT_AVERAGE_DESCEND_LABEL = "Sort by Grade Average (Descending)"
SORT_AVERAGE_ASCEND_LABEL = "Sort by Grade Average (Ascending)"

class StudentsCompleter(QCompleter):
    def __init__(self, parent=None):
        super().__init__([], parent)

        self.__model: QStringListModel = self.model()

        self.setModel(self.__model)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.max_filter = 4

    def update(self, students_names: list[str]):
        self.__model.setStringList(students_names[:self.max_filter])


class StudentManagerApplication(SubApplication, StudentsProvider):
    def get_students(self) -> LinkedArray[Student]:
        return self.students

    def get_root_widget(self) -> QWidget:
        return self.root_widget

    def display(self):
        self.root_widget.show()

    def exit(self):
        self.root_widget.hide()

    def get_name(self) -> str:
        return "Student Manager"

    def __init__(self):
        super().__init__()

        self.sort_modes = {
            SORT_ALPHABETIC_LABEL : "alphabetic",
            SORT_AVERAGE_DESCEND_LABEL : "average_high_low",
            SORT_AVERAGE_ASCEND_LABEL : "average_low_high"
            }
        
        self.manager_layout = QGridLayout()
        self.max_grades = 10
        self.current_student: Student | None = None

        self.root_widget = QWidget()

        self.file_manger_widget = QWidget()
        self.search_widget: QWidget | None = None
        self.display_widget: QWidget | None = None

        self.search_add_student_button = QPushButton("Add new student")
        self.search_add_student_window = AddNewStudentWindow(self)
        self.search_menu: QListView | None = None
        self.search_menu_model = QStringListModel()
        self.search_text_completer = StudentsCompleter()
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
        self.display_delete_student = QPushButton("Delete the student")

        self.serializer = StudentSerializer()
        self.students: LinkedArray[Student] = LinkedArray()
        self.reload_students()
        self.search_input_callback("")

        self.setup_search_widget()
        self.setup_display_widget()

        self.manager_layout.addWidget(self.search_widget, 0, 0)
        self.manager_layout.addWidget(self.display_widget, 0, 1)

        self.search_widget.setFixedWidth(280)
        self.root_widget.setLayout(self.manager_layout)
        self.root_widget.hide()

    def reload_students(self):
        self.serializer.load_file(self.students)

    def setup_file_manager_widget(self):
        layout = QHBoxLayout()

        button_save = QPushButton("Save to the file")
        button_load = QPushButton("Load from the file")

        button_save.clicked.connect(self.button_save_callback)
        button_load.clicked.connect(self.button_load_callback)

        layout.addWidget(button_save)
        layout.addWidget(button_load)

        self.file_manger_widget.setLayout(layout)

    def button_save_callback(self):
        self.serializer.save_to_file(self.students.to_list())
        self.search_text_input.setText("")
        self.search_input_callback("")

    def button_load_callback(self):
        self.reload_students()
        self.search_text_input.setText("")
        self.search_input_callback("")
        self.clear_display_widget()

    def setup_search_widget(self):
        search_layout = QGridLayout()
        self.search_widget = QWidget()

        self.search_menu = QListView()
        self.search_text_input = QLineEdit()
        self.search_button = QPushButton("Find")

        self.search_text_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.search_text_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.search_menu.setFixedHeight(200)
        self.search_menu.setModel(self.search_menu_model)
        self.search_menu.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.search_menu.clicked.connect(self.menu_item_clicked_callback)

        self.search_text_input.setCompleter(self.search_text_completer)

        self.search_text_input.setPlaceholderText("Enter User ID")
        self.search_add_student_button.clicked.connect(self.handle_add_student)
        self.search_text_input.textEdited.connect(self.search_input_callback)
        self.search_button.clicked.connect(self.find_handle)

        search_layout.addWidget(self.search_add_student_button, 0, 0)
        search_layout.addWidget(self.search_menu, 1, 0)
        search_layout.addWidget(self.search_text_input, 2, 0)
        search_layout.addWidget(self.search_button, 3, 0)

        self.sort_dropmenu = QComboBox()
        self.sort_dropmenu.addItems(self.sort_modes.keys())
        self.sort_dropmenu.setCurrentIndex(0)
        self.sort_dropmenu.textActivated.connect(self.sort_with_label)

        search_layout.addWidget(self.sort_dropmenu, 4 , 0)
        
        # self.setLayout(search_layout)
        self.search_widget.setLayout(search_layout)

    def handle_add_student(self):
        self.search_add_student_window.show()

    def search_input_callback(self, text: str):
        filtered_index = 0
        filtered = []
        max_students_display = 20
        for student in self.students:
            student_string = f"{student.id} {student.name}"
            if filtered_index == max_students_display:
                break
            if text.lower() in student_string.lower():
                filtered.append(student_string)
                filtered_index += 1

        self.search_text_completer.update(filtered)
        self.search_menu_model.setStringList(filtered)

    def sort_by_average(self):
        student_list = self.students.to_list()
        selection_sort_average(student_list)
        return student_list
    
    def sort_with_label(self, label: str):
        sort_mode = self.sort_modes.get(label, self.sort_modes[SORT_ALPHABETIC_LABEL])
        student_list = self.students.to_list()

        if sort_mode == "alphabetic":
            student_list.sort(key= lambda s: s.name.lower())
        
        elif sort_mode == "average_high_low":
            student_list = self.sort_by_average()
        
        elif sort_mode == "average_low_high":
            student_list = self.sort_by_average()
            student_list.reverse()
        
        self.students.clear()
        for student in student_list:
            self.students.append(student)
        
        self.search_input_callback("")
    
    def menu_item_clicked_callback(self, item: QModelIndex):
        self.search_text_input.setText(item.data())
        self.search_input_callback(item.data())

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
        self.display_delete_student.clicked.connect(self.handle_delete_student)
        self.display_name_input.textEdited.connect(
            lambda text: self.current_student.set_name(text) if self.current_student else None)
        self.setup_file_manager_widget()

        layout.addWidget(self.file_manger_widget)
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
            widget.textEdited.connect(self.grade_edited)
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
        grades_control_layout.addWidget(self.display_delete_student, alignment=Qt.AlignmentFlag.AlignRight)

        grades_control_layout.setContentsMargins(0, 0, 0, 0)

        self.display_add_grade_button.setMaximumSize(35, 35)
        self.display_remove_grade_button.setMaximumSize(35, 35)
        self.display_delete_student.setStyleSheet("background-color: red; border-radius: 2px; padding: 2px")

        for grade_layout in grades_layouts:
            grades_widget = QWidget()
            grades_widget.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)

            grades_widget.setLayout(grade_layout)
            layout.addWidget(grades_widget)

        self.display_widget.setLayout(layout)

    def grade_edited(self):
        student_grades = self.current_student.grades
        student_grades.clear()
        for i in range(len(self.display_grades)):
            grade_input = self.display_grades[i]
            if grade_input.isHidden():
                break
            student_grades.append(
                float(grade_input.text()) if grade_input.text() and is_float(grade_input.text()) else 0.0)

    def handle_delete_student(self):
        index = self.students.get_index(self.current_student)
        if index == -1:
            return
        self.students.remove(index)
        self.clear_display_widget()

    def clear_display_widget(self):
        self.display_id_label.setText("")
        self.display_name_input.setText("")
        for grade in self.display_grades:
            grade.setText("")
            grade.hide()

        self.search_input_callback("")

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

        self.current_student.grades.pop(grades_size - 1)
        self.display_grades[grades_size - 1].hide()


def selection_sort_average(student_list):
    list_size = len(student_list)
    
    for i in range(list_size):
        max_avg = i

        for m in range(i+1, list_size):
            current_avg = student_list[max_avg].average_grade()
            compared_avg = student_list[m].average_grade()

            if compared_avg > current_avg:
                max_avg = m
            
            elif current_avg == compared_avg:
                if student_list[m].name.lower() > student_list[max_avg].name.lower():
                    max_avg = m
        
        student_list[i], student_list[max_avg] = student_list[max_avg], student_list[i]
    
    return student_list
    
