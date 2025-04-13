import typing

T = typing.TypeVar('T')

class LinkedArray(typing.Generic[T]):
    def __init__(self):
        self.__obj = None
        self.__next: LinkedArray | None = None

    def __getitem__(self, index_: int) -> T:
        if index_ == 0:
            return self.__obj
        if self.__next:
            return self.__next.__getitem__(index_ - 1)
        raise IndexError("index is out of the array")

    def __len__(self):
        return self.size()

    def append(self, obj_: T):
        if not self.__obj:
            self.__obj = self.__obj = obj_
        elif self.__next:
            self.__next.append(obj_)
        else:
            self.__next = LinkedArray()
            self.__next.__obj = obj_


    def remove(self, index_: int, last_object: "LinkedArray" = None) -> "LinkedArray":
        if index_ == 0:
            if last_object:
                last_object.__next = self.__next
                return last_object
            if self.__next:
                return self.__next
            return LinkedArray()
        if self.__next:
            return self.__next.remove(index_ - 1, self)
        raise IndexError("index is out of the array")

    def size(self):
        if self.__obj:
            if self.__next:
                return 1 + self.__next.size()
            return 1
        return 0


    def to_list(self, _result: list = None):
        if not _result:
            _result = list()

        if self.__obj:
            _result.append(self.__obj)
        if self.__next:
            self.__next.to_list(_result)
        return _result

    def clear(self):
        if self.__next:
            self.__next.clear()

        self.__obj = None
        self.__next = None

if __name__ == '__main__':
    l = LinkedArray()
    l.append("1")
    l.append("2")
    l.append("3")
    l.append("4")

    print(l.to_list())
    # l.clear()
    print(l[2])


    # print(a)
    for i in range(l.size()):
        print(l[i])
