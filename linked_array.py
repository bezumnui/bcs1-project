import typing


class Node:
    def __init__(self, value=None):
        self.value = value
        self.next: Node | None = None

class LinkedArray:
    def __init__(self):
        self.head: Node | None = None
        self.size_ = 0

    def __getitem__(self, index_: int):
        if index_ < 0 or index_ >= self.size_:
            raise IndexError("index is out of the array")
        current = self.head
        for _ in range(index_):
            current = current.next
        return current.value

    def __len__(self):
        return self.size_

    def append(self, obj_):
        new_node = Node(obj_)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size_ += 1

    def remove(self, index_: int):
        if index_ < 0 or index_ >= self.size_:
            raise IndexError("index is out of the array")
        if index_ == 0:
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index_ - 1):
                current = current.next
            current.next = current.next.next
        self.size_ -= 1

    def get_index(self, object_to_search) -> int:
        current = self.head
        index = 0
        while current:
            if current.value == object_to_search:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def clear(self):
        self.head = None
        self.size_ = 0

    def __iter__(self):
        current = self.head
        while current:
            yield current.value
            current = current.next

if __name__ == '__main__':
    l = LinkedArray()
    l.append("1")
    l.append("2")
    l.append("3")
    l.append("4")

    print(l.to_list())
    # l.clear()
    print(l[2])



