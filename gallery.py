
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QComboBox, QFrame, QLabel, QGridLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from sub_applications.bin_hex_octal_converter import BinHexOctalConverterApplication
from sub_applications.factorial_application import FactorialApplication
from sub_applications.ieee_754_converter_application import IEEE754ConverterApplication
from sub_applications.student_application import StudentManagerApplication
from sub_applications.sub_application import SubApplication


class MainMenuCombo:
    NUMBER_CONVERTER = "Number Converter"
    IEEE = "IEEE 754"
    FACTORIAL = "Factorial"
    STUDENT_MANAGER = "Student Manager"


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.main_layout = QVBoxLayout()

        self.top_layout = QHBoxLayout()

        self.mode_combo_box = QComboBox()
        self.mode_combo_box.addItems([MainMenuCombo.NUMBER_CONVERTER, MainMenuCombo.IEEE, MainMenuCombo.FACTORIAL,
                                      MainMenuCombo.STUDENT_MANAGER])
        self.mode_combo_box.setStyleSheet("background-color: #444444; color: white; padding: 5px;")
        self.mode_combo_box.textActivated.connect(self.change_mode)
        self.top_layout.addWidget(self.mode_combo_box)

        self.content_frame = QFrame()
        self.content_layout = QVBoxLayout(self.content_frame)

        self.bin_hex_octal_converter_application = BinHexOctalConverterApplication()
        self.ieee_754_application = IEEE754ConverterApplication()
        self.factorial_application = FactorialApplication()
        self.student_manager_application = StudentManagerApplication()

        self.bin_hex_octal_converter_application.register_widget(self.content_layout)
        self.ieee_754_application.register_widget(self.content_layout)
        self.factorial_application.register_widget(self.content_layout)
        self.student_manager_application.register_widget(self.content_layout)

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.content_frame)

        self.setLayout(self.main_layout)

        self.current_application = self.bin_hex_octal_converter_application
        self.setWindowTitle(self.current_application.get_name())
        self.current_application.display()

        self.setWindowTitle("Enhanced Application")
        self.setWindowIcon(QIcon("img/icon.png")) 
        self.resize(900, 700)
        self.setStyleSheet("background-color: #222222; color: white;")

    def replace_application(self, new_app: SubApplication):
        self.current_application.exit()
        self.current_application = new_app
        self.current_application.display()
        self.setWindowTitle(self.current_application.get_name())

    def change_mode(self, data):
        match data:
            case MainMenuCombo.NUMBER_CONVERTER:
                self.replace_application(self.bin_hex_octal_converter_application)

            case MainMenuCombo.IEEE:
                self.replace_application(self.ieee_754_application)

            case MainMenuCombo.FACTORIAL:
                self.replace_application(self.factorial_application)

            case MainMenuCombo.STUDENT_MANAGER:
                self.replace_application(self.student_manager_application)
