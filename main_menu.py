# main_menu.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtWidgets import QApplication


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Manager App")
        self.setGeometry(100, 100, 500, 400)

        # Set background color
        self.setStyleSheet("background-color: #2C3E50;")

        # Main layout
        main_layout = QVBoxLayout()

        # Title label
        title_label = QLabel("Welcome to the Student Manager App")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white; padding: 20px;")

        # Add title label to layout
        main_layout.addWidget(title_label)

        # Add combo box for selection of app sections
        mode_combo_box = QComboBox()
        mode_combo_box.addItems(["Number Converter", "IEEE 754", "Factorial", "Student Manager"])
        mode_combo_box.setStyleSheet("background-color: #34495E; color: white; font-size: 14px; padding: 10px;")
        mode_combo_box.setFont(QFont("Arial", 12))

        # Add combo box to layout
        main_layout.addWidget(mode_combo_box)

        # Button to navigate to the student manager page
        student_manager_button = QPushButton("Go to Student Manager")
        student_manager_button.setStyleSheet("""
            background-color: #16A085;
            color: white;
            font-size: 16px;
            border: none;
            padding: 15px;
            border-radius: 10px;
        """)
        student_manager_button.setFont(QFont("Arial", 12))
        student_manager_button.setFixedWidth(200)

        # Hover effect for buttons
        student_manager_button.setStyleSheet("""
            QPushButton {
                background-color: #16A085;
                color: white;
            }
            QPushButton:hover {
                background-color: #1ABC9C;
            }
        """)

        # Add button to layout
        main_layout.addWidget(student_manager_button)

        # Adding spacing and adjusting layout
        main_layout.addStretch(1)

        # Set layout for the widget
        self.setLayout(main_layout)


# Create the application and show the main menu
if __name__ == "__main__":
    app = QApplication([])

    window = MainMenu()
    window.show()

    app.exec()
