from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QApplication, QDialog, QGridLayout, QGroupBox, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QWidget, QComboBox, QHBoxLayout, QFrame)

from screenstate import ScreenState
from student_manager import StudentManager
from utils import float_to_ieee754, get_factorial_recurse


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.converter_layout = QGridLayout()
        self.student_manager = QGridLayout()

        self.student_manager_widget = StudentManager()

        self.main_frame = QFrame()


        self.converter_widget: QWidget = QWidget()

        self.input_widget: QWidget | None = None
        self.multiconverter_widget: QWidget | None = None
        self.ieee_754_widget: QWidget | None = None
        self.current_right_widget: QWidget | None = None
        self.factorial_widget: QWidget | None = None


        self.input_number: QLineEdit | None = None
        self.binary_string: QLabel | None = None
        self.octal_string: QLabel | None = None
        self.hex_string: QLabel | None = None
        self.ieee754_string: QLabel | None = None
        self.factorial_string: QLabel | None = None

        self.top_layout = QVBoxLayout()
        mode_combo_box = QComboBox()
        mode_combo_box.addItems(["Number Converter", "IEEE 754", "Factorial", "Student Manager"])
        mode_combo_box.textActivated.connect(self.change_mode)
        self.top_layout.addWidget(mode_combo_box)

        self.setup_input_widget()
        self.setup_multiconverter_widget()
        self.setup_ieee_754_widget()
        self.setup_factorial_widget()


        self.converter_widget.setLayout(self.converter_layout)
        self.student_manager_widget.setLayout(self.converter_layout)

        self.top_layout.addWidget(self.converter_widget)
        self.top_layout.addWidget(self.student_manager_widget)
        self.student_manager_widget.hide()

        # self.top_layout.addWidget(self.main_widget)
        self.setLayout(self.top_layout)

        self.setWindowTitle("Number Converter")

        self.current_right_widget = self.multiconverter_widget
        self.current_screen = ScreenState.converter
        # self.setFixedSize(QSize(300, 200))

    def resize_window(self):
        self.setFixedSize(self.baseSize())


    def change_mode(self, data):
        # self.resize_window()

        self.current_right_widget.hide()

        if data == "IEEE 754":
            self.converter_layout.replaceWidget(self.current_right_widget, self.ieee_754_widget)
            self.ieee_754_widget.show()
            self.current_right_widget = self.ieee_754_widget
            self.current_screen = ScreenState.ieee_754

        elif data == "Number Converter":
            self.converter_layout.replaceWidget(self.current_right_widget, self.multiconverter_widget)
            self.multiconverter_widget.show()
            self.current_right_widget = self.multiconverter_widget
            self.current_screen = ScreenState.converter

        elif data == "Factorial":
            self.converter_layout.replaceWidget(self.current_right_widget, self.factorial_widget)
            self.factorial_widget.show()
            self.current_right_widget = self.factorial_widget
            self.current_screen = ScreenState.factorial

        if data == "Student Manager":
            # self.setFixedSize(QSize(400, 400))

            self.setWindowTitle("Student Manager")
            self.converter_widget.hide()
            self.student_manager_widget.show()
        else:
            self.setWindowTitle("Number Converter")
            # self.setFixedSize(QSize(300, 200))

            self.converter_widget.show()
            self.student_manager_widget.hide()



    def setup_ieee_754_widget(self):
        self.ieee_754_widget = QGroupBox()

        self.ieee754_string = QLabel("IEEE 754:")
        layout = QVBoxLayout()
        layout.addWidget(self.ieee754_string)


        self.ieee_754_widget.setLayout(layout)

    def setup_factorial_widget(self):
        self.factorial_widget = QGroupBox()

        self.factorial_string = QLabel("Factorial:")
        layout = QVBoxLayout()
        layout.addWidget(self.factorial_string)
        self.factorial_widget.setLayout(layout)

    def setup_multiconverter_widget(self):
        self.multiconverter_widget = QGroupBox()

        self.binary_string = QLabel("Binary:")
        self.octal_string = QLabel("Octal:")
        self.hex_string = QLabel("Hex:")



        layout = QVBoxLayout()
        layout.addWidget(self.binary_string)
        layout.addWidget(self.octal_string)
        layout.addWidget(self.hex_string)

        self.multiconverter_widget.setLayout(layout)
        self.converter_layout.addWidget(self.multiconverter_widget, 0, 1)


    def setup_input_widget(self):

        self.input_widget = QGroupBox()

        self.input_number = QLineEdit('10')
        self.input_number.setEchoMode(QLineEdit.EchoMode.Normal)
        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.button_callback)


        layout = QGridLayout()
        layout.addWidget(self.input_number, 0, 0, 1, 2)
        layout.addWidget(convert_button, 1, 0, 1, 2)

        self.input_widget.setLayout(layout)
        self.converter_layout.addWidget(self.input_widget, 0, 0)

    def ieee754_callback(self):
        number = self.input_number.text()
        # implement ieee 754 here
        check_number = number
        if number.startswith("-"):
            check_number = number[1:]

        if not check_number.isdecimal() and check_number:
            self.ieee754_string.setText("Error! Please enter a number.")
            return

        self.ieee754_string.setText(f"IEEE 754: {float_to_ieee754(float(number))}")

    def convert_button_callback(self):
        number = self.input_number.text()
        sign = 0
        if number and number[0] == '-':
            sign = 1
            number = number[1:]
        if not number.isdecimal():
            self.binary_string.setText("Error! Please enter a number.")
            self.octal_string.setText("")
            self.hex_string.setText("")
            return

        typed_number = int(number)
        sign_string = "-" if sign else ""
        self.binary_string.setText(f"Binary: {sign_string}{bin(typed_number)[2:]}")
        self.octal_string.setText(f"Octal: {sign_string}{oct(typed_number)[2:]}")
        self.hex_string.setText(f"Hex: {sign_string}{hex(typed_number)[2:]}")


    def factorial_button_callback(self):
        number = self.input_number.text()
        if not number.isdecimal() and number:
            self.factorial_string.setText("Error! Please enter a number.\nIt must be more or equal to 0.")
            return

        self.factorial_string.setText(f"Factorial: {get_factorial_recurse(int(number))}")



    def button_callback(self):
        if self.current_screen == ScreenState.converter:
            self.convert_button_callback()
        elif self.current_screen == ScreenState.ieee_754:
            self.ieee754_callback()
        elif self.current_screen == ScreenState.factorial:
            self.factorial_button_callback()