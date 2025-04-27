from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel
from PyQt6.QtGui import QColor, QPalette, QFont, QLinearGradient, QBrush
from PyQt6.QtCore import Qt


def apply_styles(widget):
    widget.setFont(QFont("Arial", 12))
    widget.setAutoFillBackground(True)
    p = widget.palette()
    p.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    widget.setPalette(p)

    widget.setStyleSheet("""
        QPushButton {
            background-color: #3498db;
            color: white;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #1c6ea4;
        }
        QComboBox {
            background-color: #f1f1f1;
            color: #333;
            border-radius: 5px;
            padding: 8px;
            font-size: 16px;
        }
        QComboBox:hover {
            background-color: #d5e3f2;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            selection-background-color: #2980b9;
        }
    """)


def set_background(widget):
    widget.setAutoFillBackground(True)
    p = widget.palette()

    gradient = QLinearGradient(0, 0, 1, 1)
    gradient.setColorAt(0.0, QColor(52, 152, 219)
    gradient.setColorAt(1.0, QColor(41, 128, 185))  

    p.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
    widget.setPalette(p)


class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()

        self.layout = QVBoxLayout()

        self.title = QLabel("Welcome to the Application")
        self.combo_box = QComboBox()
        self.switch_button = QPushButton("Switch Application")

        self.combo_box.addItems(["Number Converter", "IEEE 754 Converter", "Factorial", "Student Manager"])

        apply_styles(self.title)
        apply_styles(self.combo_box)
        apply_styles(self.switch_button)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.switch_button)

        set_background(self)
      
        self.setLayout(self.layout)
        self.setWindowTitle("Main Menu")
        self.setFixedSize(800, 600)

        self.switch_button.clicked.connect(self.switch_app)

    def switch_app(self):
        print("Switching Application...")

    def resize_window(self):
        self.setFixedSize(self.baseSize())


if __name__ == '__main__':
    app = QApplication([])
    window = MainMenu()
    window.show()
    app.exec()
