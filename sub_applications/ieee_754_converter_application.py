from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from sub_applications.sub_application import SubApplication
from utils import is_float, float_to_ieee754


class IEEE754ConverterApplication(SubApplication):

    def __init__(self):
        self.root_widget = QGroupBox()
        self.layout = QHBoxLayout()
        self.root_widget.setLayout(self.layout)

        self.result_text = QLabel("IEEE 754:")
        self.input_field = QLineEdit()

        self.init_input()
        self.result_init()
        self.root_widget.hide()

    def init_input(self):
        layout = QVBoxLayout()

        button = QPushButton("Convert")
        button.clicked.connect(self.button_convert_callback)

        layout.addWidget(self.input_field)
        layout.addWidget(button)

        input_widget = QWidget()
        input_widget.setLayout(layout)

        input_widget.setFixedWidth(170)

        self.layout.addWidget(input_widget)

    def result_init(self):
        layout = QVBoxLayout()

        layout.addWidget(self.result_text)

        result_widget = QWidget()
        result_widget.setLayout(layout)

        result_widget.setMaximumWidth(600)

        self.layout.addWidget(result_widget)

    def button_convert_callback(self):
        input_text = self.input_field.text()
        if not input_text or not is_float(input_text):
            self.result_text.setText("IEEE 754: Error. Not a valid number.")
            return
        self.result_text.setText(f"IEEE 754: {float_to_ieee754(float(input_text))}")

    def get_root_widget(self) -> QWidget:
        return self.root_widget

    def display(self):
        self.root_widget.show()

    def exit(self):
        self.root_widget.hide()

    def get_name(self) -> str:
        return "IEEE 754 converter"
