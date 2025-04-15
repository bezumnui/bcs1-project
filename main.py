from PyQt6.QtWidgets import QApplication

from gallery import WidgetGallery

if __name__ == '__main__':
    app = QApplication([])
    g = WidgetGallery()
    g.show()

    app.exec()