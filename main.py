
    from PyQt6.QtWidgets import QApplication
from gallery import WidgetGallery  # Import the updated gallery with the new GUI

if __name__ == '__main__':
    app = QApplication([])
    g = WidgetGallery()  # Initialize the new GUI
    g.show()  # Show the window

    app.exec()  # Start the application event loop
