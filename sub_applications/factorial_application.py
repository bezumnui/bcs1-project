from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from sub_applications.sub_application import SubApplication
from utils import is_float, float_to_ieee754, get_factorial_recurse, fibonacci


class FactorialApplication(SubApplication):

    def __init__(self):
        self.root_widget = QGroupBox()
        self.layout = QHBoxLayout()
        self.root_widget.setLayout(self.layout)

        self.factorial_text = QLabel("Factorial:")
        self.fibonacci_text = QLabel("Fibonacci:")
        self.input_field = QLineEdit()

        self.maximum_input_number = 20

        self.init_input()
        self.result_init()
        self.root_widget.hide()

    def init_input(self):
        layout = QVBoxLayout()

        button = QPushButton("Get")
        button.clicked.connect(self.button_convert_callback)

        layout.addWidget(self.input_field)
        layout.addWidget(button)

        input_widget = QWidget()
        input_widget.setLayout(layout)

        input_widget.setFixedWidth(170)

        self.layout.addWidget(input_widget)

    def result_init(self):
        layout = QVBoxLayout()

        layout.addWidget(self.factorial_text)
        layout.addWidget(self.fibonacci_text)

        result_widget = QWidget()
        result_widget.setLayout(layout)

        result_widget.setMaximumWidth(600)

        self.layout.addWidget(result_widget)

    def button_convert_callback(self):
        input_text = self.input_field.text()
        if not input_text or not input_text.isdigit():
            self.factorial_text.setText("Factorial: Error. Not a valid number.")
            self.fibonacci_text.setText(f"Fibonacci: Error.")

            return
        input_number = int(input_text)
        if input_number > self.maximum_input_number:
            self.factorial_text.setText(f"Factorial: Error. Please choose a number between 0 and {self.maximum_input_number}")
            self.fibonacci_text.setText(f"Fibonacci: Error.")

            return

        self.factorial_text.setText(f"Factorial: {get_factorial_recurse(input_number)}")
        self.fibonacci_text.setText(f"Fibonacci: {fibonacci(input_number)}")

    def get_root_widget(self) -> QWidget:
        return self.root_widget

    def display(self):
        self.root_widget.show()

    def exit(self):
        self.root_widget.hide()

    def get_name(self) -> str:
        return "Factorial/Fibonacci"
