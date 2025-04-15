import abc

from PyQt6.QtWidgets import QWidget, QLayout


class SubApplication(abc.ABC):
    """
    Abstract base class for sub-applications.
    """

    @abc.abstractmethod
    def get_root_widget(self) -> QWidget:
        raise NotImplementedError()

    @abc.abstractmethod
    def display(self):
        """Called every time when the sub-application required to be displayed"""
        raise NotImplementedError()

    @abc.abstractmethod
    def exit(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError()

    def register_widget(self, top_layout: QLayout):
        top_layout.addWidget(self.get_root_widget())
