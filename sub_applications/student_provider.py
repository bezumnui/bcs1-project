import abc
from abc import abstractmethod

from linked_array import LinkedArray
from students_serializer import Student


class StudentsProvider(abc.ABC):
    @abstractmethod
    def get_students(self) -> LinkedArray[Student]:
        """Returns a list of students."""
        raise NotImplementedError()
