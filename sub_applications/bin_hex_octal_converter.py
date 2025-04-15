from PyQt6.QtWidgets import QWidget, QGroupBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

from sub_applications.sub_application import SubApplication
from utils import is_float, float_to_ieee754


class BinHexOctalConverterApplication(SubApplication):

    def __init__(self):
        self.root_widget = QGroupBox()
        self.layout = QHBoxLayout()
        self.root_widget.setLayout(self.layout)

        self.result_text_bin = QLabel("bin:")
        self.result_text_hex = QLabel("hex:")
        self.result_text_octal = QLabel("octal:")
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

        layout.addWidget(self.result_text_bin)
        layout.addWidget(self.result_text_hex)
        layout.addWidget(self.result_text_octal)

        result_widget = QWidget()
        result_widget.setLayout(layout)

        result_widget.setMaximumWidth(600)

        self.layout.addWidget(result_widget)


    def button_convert_callback(self):
        input_text = self.input_field.text()
        if not input_text or not is_float(input_text):
            self.set_bin("Error. Not a number")
            self.set_hex("Error. Not a number")
            self.set_octal("Error. Not a number")
            return
        number_to_convert = int(input_text)
        self.set_bin(bin(number_to_convert)[2:])
        self.set_hex(hex(number_to_convert)[2:])
        self.set_octal(oct(number_to_convert)[2:])

    def set_bin(self, text: str):
        self.result_text_bin.setText(f"bin: {text}")

    def set_hex(self, text: str):
        self.result_text_hex.setText(f"hex: {text}")

    def set_octal(self, text: str):
        self.result_text_octal.setText(f"octal: {text}")


    def get_root_widget(self) -> QWidget:
        return self.root_widget

    def display(self):
        self.root_widget.show()

    def exit(self):
        self.root_widget.hide()

    def get_name(self) -> str:
        return "Multi-converter"