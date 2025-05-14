from typing import Optional, Union, List as PyList

class CharDoublyLinkedList:
    class _Node:
        def __init__(self,
                     data: str,
                     prev_node: Optional['CharDoublyLinkedList._Node'] = None,
                     next_node: Optional['CharDoublyLinkedList._Node'] = None
                    ):
            self.data: str = data
            self.prev: Optional[CharDoublyLinkedList._Node] = prev_node
            self.next: Optional[CharDoublyLinkedList._Node] = next_node
        def __repr__(self) -> str:
            return f"Node({self.data})"

    def __init__(self, initial_elements: Union[PyList[str], str, None] = None):
        self.head: Optional[CharDoublyLinkedList._Node] = None
        self.tail: Optional[CharDoublyLinkedList._Node] = None
        self._size: int = 0
        if initial_elements:
            if isinstance(initial_elements, str):
                for char_element in initial_elements: self.append(char_element)
            elif isinstance(initial_elements, list):
                for char_element in initial_elements: self.append(char_element)
            else:
                raise TypeError("Initial elements must be a list of characters or a string.")

    def _validate_char(self, element: str) -> None:
        if not isinstance(element, str) or len(element) != 1:
            raise TypeError(f"Element '{element}' must be a single character (str of length 1).")

    def _validate_index(self, index: int, for_insertion: bool = False) -> None:
        if not isinstance(index, int): raise TypeError("Index must be an integer.")
        current_length = self.length()
        if for_insertion:
            if not (0 <= index <= current_length):
                raise IndexError(f"Index {index} out of bounds for insertion. List length is {current_length}.")
        else:
            if current_length == 0: raise IndexError(f"Index {index} out of bounds. List is empty.")
            if not (0 <= index < current_length):
                raise IndexError(f"Index {index} out of bounds. Valid range is 0 to {current_length - 1}.")

    def _get_node_at_index(self, index: int) -> 'CharDoublyLinkedList._Node':
        if index < self._size // 2:
            current = self.head
            for _ in range(index):
                if current: current = current.next
                else: raise RuntimeError("Internal error: Node traversal failed.")
        else:
            current = self.tail
            for _ in range(self._size - 1 - index):
                if current: current = current.prev
                else: raise RuntimeError("Internal error: Node traversal failed.")
        if current is None: raise IndexError("Cannot get node from an empty or improperly indexed list.")
        return current

    def length(self) -> int: return self._size

    def append(self, element: str) -> None:
        self._validate_char(element)
        new_node = self._Node(element)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def insert(self, element: str, index: int) -> None:
        self._validate_char(element)
        self._validate_index(index, for_insertion=True)
        if index == self._size: self.append(element); return
        new_node = self._Node(element)
        if index == 0:
            if self.head:
                new_node.next = self.head
                self.head.prev = new_node
            self.head = new_node
            if self.tail is None: self.tail = new_node
        else:
            target_node = self._get_node_at_index(index)
            prev_node_of_target = target_node.prev
            new_node.next = target_node
            new_node.prev = prev_node_of_target
            if prev_node_of_target: prev_node_of_target.next = new_node
            target_node.prev = new_node
        self._size += 1

    def delete(self, index: int) -> str:
        if self.length() == 0: raise IndexError("Cannot delete from an empty list.")
        self._validate_index(index)
        node_to_delete = self._get_node_at_index(index)
        deleted_data = node_to_delete.data
        prev_node = node_to_delete.prev
        next_node = node_to_delete.next
        if prev_node: prev_node.next = next_node
        else: self.head = next_node
        if next_node: next_node.prev = prev_node
        else: self.tail = prev_node
        node_to_delete.prev = None; node_to_delete.next = None
        self._size -= 1
        if self._size == 0: self.head = None; self.tail = None
        return deleted_data

    def deleteAll(self, element: str) -> None:
        self._validate_char(element)
        current = self.head
        while current:
            next_node_to_check = current.next
            if current.data == element:
                prev_node = current.prev
                if prev_node: prev_node.next = next_node_to_check
                else: self.head = next_node_to_check
                if next_node_to_check: next_node_to_check.prev = prev_node
                else: self.tail = prev_node
                current.prev = None; current.next = None
                self._size -= 1
            current = next_node_to_check
        if self._size == 0: self.head = None; self.tail = None

    def get(self, index: int) -> str:
        if self.length() == 0: raise IndexError("Cannot get from an empty list.")
        self._validate_index(index)
        node = self._get_node_at_index(index)
        return node.data

    def clone(self) -> 'CharDoublyLinkedList':
        new_list = CharDoublyLinkedList()
        current = self.head
        while current: new_list.append(current.data); current = current.next
        return new_list

    def reverse(self) -> None:
        if self._size < 2: return
        current = self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        self.head, self.tail = self.tail, self.head

    def findFirst(self, element: str) -> int:
        self._validate_char(element)
        current = self.head; index = 0
        while current:
            if current.data == element: return index
            current = current.next; index += 1
        return -1

    def findLast(self, element: str) -> int:
        self._validate_char(element)
        current = self.tail; index = self._size - 1
        while current:
            if current.data == element: return index
            current = current.prev; index -= 1
        return -1

    def clear(self) -> None:
        current = self.head
        while current:
            next_node = current.next
            current.prev = None; current.next = None
            current = next_node
        self.head = None; self.tail = None; self._size = 0

    def extend(self, elements_list: 'CharDoublyLinkedList') -> None:
        if not isinstance(elements_list, CharDoublyLinkedList):
            raise TypeError("Argument must be an instance of CharDoublyLinkedList.")
        current_other = elements_list.head
        while current_other: self.append(current_other.data); current_other = current_other.next

    def __str__(self) -> str:
        if not self.head: return "CharDoublyLinkedList([])"
        elements = [repr(current.data) for current in self._iter_nodes()]
        return f"CharDoublyLinkedList([{', '.join(elements)}])"

    def __repr__(self) -> str:
        if not self.head: return "CharDoublyLinkedList(head=None, tail=None, size=0)"
        elements_str = "".join([current.data for current in self._iter_nodes()])
        return f"CharDoublyLinkedList(elements='{elements_str}', size={self._size}, head='{self.head.data if self.head else None}', tail='{self.tail.data if self.tail else None}')"

    def _iter_nodes(self):
        current = self.head
        while current:
            yield current
            current = current.next