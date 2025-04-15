from PyQt6.QtWidgets import (QDialog, QGridLayout, QVBoxLayout, QComboBox, QFrame)

from screenstate import ScreenState
from sub_applications.bin_hex_octal_converter import BinHexOctalConverterApplication
from sub_applications.factorial_application import FactorialApplication
from sub_applications.ieee_754_converter_application import IEEE754ConverterApplication
from sub_applications.student_application import StudentManagerApplication
from sub_applications.sub_application import SubApplication


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.converter_layout = QGridLayout()
        self.student_manager = QGridLayout()


        self.main_frame = QFrame()

        self.bin_hex_octal_converter_application = BinHexOctalConverterApplication()
        self.ieee_754_application = IEEE754ConverterApplication()
        self.factorial_application = FactorialApplication()
        self.student_manager_application = StudentManagerApplication()


        self.top_layout = QVBoxLayout()
        mode_combo_box = QComboBox()
        mode_combo_box.addItems(["Number Converter", "IEEE 754", "Factorial", "Student Manager"])
        mode_combo_box.textActivated.connect(self.change_mode)
        self.top_layout.addWidget(mode_combo_box)


        self.ieee_754_application.register_widget(self.top_layout)
        self.bin_hex_octal_converter_application.register_widget(self.top_layout)
        self.factorial_application.register_widget(self.top_layout)
        self.student_manager_application.register_widget(self.top_layout)

        self.setLayout(self.top_layout)

        self.current_application = self.bin_hex_octal_converter_application
        self.setWindowTitle(self.current_application.get_name())
        self.current_application.display()


    def resize_window(self):
        self.setFixedSize(self.baseSize())

    def replace_application(self, new_app: SubApplication):
        self.current_application.exit()
        self.current_application = new_app
        self.current_application.display()
        self.setWindowTitle(self.current_application.get_name())

    def change_mode(self, data):

        if data == "IEEE 754":
            self.replace_application(self.ieee_754_application)

        elif data == "Number Converter":
            self.replace_application(self.bin_hex_octal_converter_application)

        elif data == "Factorial":
            self.replace_application(self.factorial_application)

        if data == "Student Manager":
            self.replace_application(self.student_manager_application)


