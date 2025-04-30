import typing
from copy import copy


class Stack:

    def __init__(self):
        self.__array = []

    def pop(self):
        """:raise IndexError"""
        self.__array.pop(len(self.__array) - 1)

    def trunk(self):
        """:raise IndexError"""
        self.__array.pop(0)

    def push(self, obj: typing.Any):
        self.__array.append(obj)

    def to_list(self):
        return copy(self.__array)

    def __len__(self):
        return self.__array.__len__()
