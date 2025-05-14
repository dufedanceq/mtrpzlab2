from typing import List as PyList, Union


class CharArrayList:

    def __init__(self, initial_elements: Union[PyList[str], str, None] = None):
        self._data: PyList[str] = []
        if initial_elements:
            if isinstance(initial_elements, str):
                for char_element in initial_elements:
                    self.append(char_element)
            elif isinstance(initial_elements, list):
                for char_element in initial_elements:
                    self.append(char_element)
            else:
                raise TypeError(
                    "Initial elements must be a list of characters or a string."
                )

    def _validate_char(self, element: str) -> None:
        if not isinstance(element, str) or len(element) != 1:
            raise TypeError(
                f"Element '{element}' must be a single character (str of length 1)."
            )

    def _validate_index(self, index: int, for_insertion: bool = False) -> None:
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        current_length = self.length()
        if for_insertion:
            if not (0 <= index <= current_length):
                raise IndexError(
                    f"Index {index} out of bounds for insertion. List length is {current_length}."
                )
        else:
            if current_length == 0:
                raise IndexError(f"Index {index} out of bounds. List is empty.")
            if not (0 <= index < current_length):
                raise IndexError(
                    f"Index {index} out of bounds. Valid range is 0 to {current_length - 1}."
                )

    def length(self) -> int:
        return len(self._data)

    def append(self, element: str) -> None:
        self._validate_char(element)
        self._data.append(element)

    def insert(self, element: str, index: int) -> None:
        self._validate_char(element)
        self._validate_index(index, for_insertion=True)
        self._data.insert(index, element)

    def delete(self, index: int) -> str:
        if self.length() == 0:
            raise IndexError("Cannot delete from an empty list.")
        self._validate_index(index)
        return self._data.pop(index)

    def deleteAll(self, element: str) -> None:
        self._validate_char(element)
        self._data = [item for item in self._data if item != element]

    def get(self, index: int) -> str:
        if self.length() == 0:
            raise IndexError("Cannot get from an empty list.")
        self._validate_index(index)
        return self._data[index]

    def clone(self) -> "CharArrayList":
        new_list = CharArrayList()
        for item in self._data:
            new_list.append(item)
        return new_list

    def reverse(self) -> None:
        self._data.reverse()

    def findFirst(self, element: str) -> int:
        self._validate_char(element)
        try:
            return self._data.index(element)
        except ValueError:
            return -1

    def findLast(self, element: str) -> int:
        self._validate_char(element)
        for i in range(self.length() - 1, -1, -1):
            if self._data[i] == element:
                return i
        return -1

    def clear(self) -> None:
        self._data = []

    def extend(self, elements: "CharArrayList") -> None:
        if not isinstance(elements, CharArrayList):
            raise TypeError("Argument must be an instance of CharArrayList.")
        for i in range(elements.length()):
            self.append(elements.get(i))

    def __str__(self) -> str:
        return f"CharArrayList([{', '.join(repr(char) for char in self._data)}])"

    def __repr__(self) -> str:
        return f"CharArrayList({self._data})"
