# test_char_list.py
import unittest
from char_array_list import CharArrayList
from char_doubly_linked_list import CharDoublyLinkedList


class ListTestsMixin:
    ListClass = None

    def setUp(self):
        self.empty_list = self.ListClass()
        self.list1 = self.ListClass("abc")
        self.list2 = self.ListClass(["x", "y", "z", "y"])

    def test_initialization_and_length(self):
        self.assertEqual(self.empty_list.length(), 0)
        self.assertEqual(self.list1.length(), 3)
        self.assertEqual(self.list2.length(), 4)

        list_from_list_of_chars = self.ListClass(["d", "e"])
        self.assertEqual(list_from_list_of_chars.length(), 2)
        self.assertEqual(list_from_list_of_chars.get(0), "d")

        list_from_long_string = self.ListClass("toolong")
        self.assertEqual(list_from_long_string.length(), 7)
        self.assertEqual(list_from_long_string.get(0), "t")
        self.assertEqual(list_from_long_string.get(6), "g")

        with self.assertRaises(TypeError):
            self.ListClass([1, 2])
        with self.assertRaises(TypeError):
            self.ListClass(["aa", "b"])

        with self.assertRaises(TypeError):
            self.ListClass(123)

    def test_append(self):
        lst = self.ListClass()
        lst.append("a")
        self.assertEqual(lst.length(), 1)
        self.assertEqual(lst.get(0), "a")
        lst.append("b")
        self.assertEqual(lst.length(), 2)
        self.assertEqual(lst.get(1), "b")
        with self.assertRaises(TypeError):
            lst.append("ab")
        with self.assertRaises(TypeError):
            lst.append(1)

    def test_insert(self):
        lst = self.ListClass("ad")
        lst.insert("c", 1)
        self.assertEqual(lst.length(), 3)
        self.assertEqual(lst.get(0), "a")
        self.assertEqual(lst.get(1), "c")
        self.assertEqual(lst.get(2), "d")

        lst.insert("x", 0)
        self.assertEqual(lst.get(0), "x")
        self.assertEqual(lst.length(), 4)

        lst.insert("z", lst.length())
        self.assertEqual(lst.get(lst.length() - 1), "z")
        self.assertEqual(lst.length(), 5)

        with self.assertRaises(IndexError):
            lst.insert("e", -1)
        with self.assertRaises(IndexError):
            lst.insert("e", lst.length() + 1)
        with self.assertRaises(TypeError):
            lst.insert("ee", 0)
        with self.assertRaises(TypeError):
            lst.insert("e", "0")

    def test_get(self):
        self.assertEqual(self.list1.get(0), "a")
        self.assertEqual(self.list1.get(2), "c")
        with self.assertRaises(IndexError):
            self.list1.get(3)
        with self.assertRaises(IndexError):
            self.list1.get(-1)
        with self.assertRaises(IndexError):
            self.empty_list.get(0)

    def test_delete(self):
        lst = self.ListClass("abcd")
        deleted = lst.delete(1)
        self.assertEqual(deleted, "b")
        self.assertEqual(lst.length(), 3)
        self.assertEqual(lst.get(0), "a")
        self.assertEqual(lst.get(1), "c")

        deleted = lst.delete(0)
        self.assertEqual(deleted, "a")
        self.assertEqual(lst.length(), 2)
        self.assertEqual(lst.get(0), "c")

        deleted = lst.delete(lst.length() - 1)
        self.assertEqual(deleted, "d")
        self.assertEqual(lst.length(), 1)
        self.assertEqual(lst.get(0), "c")

        with self.assertRaises(IndexError):
            self.empty_list.delete(0)
        with self.assertRaises(IndexError):
            lst.delete(1)

    def test_deleteAll(self):
        lst = self.ListClass("abacaba")
        lst.deleteAll("a")
        self.assertEqual(lst.length(), 3)
        self.assertEqual(lst.get(0), "b")
        self.assertEqual(lst.get(1), "c")
        self.assertEqual(lst.get(2), "b")

        lst.deleteAll("b")
        self.assertEqual(lst.length(), 1)
        self.assertEqual(lst.get(0), "c")

        lst.deleteAll("c")
        self.assertEqual(lst.length(), 0)

        lst2 = self.ListClass("aaaa")
        lst2.deleteAll("a")
        self.assertEqual(lst2.length(), 0)

        lst3 = self.ListClass("abc")
        lst3.deleteAll("d")
        self.assertEqual(lst3.length(), 3)

        with self.assertRaises(TypeError):
            lst.deleteAll("aa")

    def test_clone(self):
        clone = self.list1.clone()
        self.assertIsNot(self.list1, clone)
        self.assertEqual(self.list1.length(), clone.length())
        for i in range(self.list1.length()):
            self.assertEqual(self.list1.get(i), clone.get(i))

        clone.append("d")
        self.assertNotEqual(self.list1.length(), clone.length())

        empty_clone = self.empty_list.clone()
        self.assertIsNot(self.empty_list, empty_clone)
        self.assertEqual(empty_clone.length(), 0)

    def test_reverse(self):
        lst = self.ListClass("abcde")
        lst.reverse()
        self.assertEqual(lst.get(0), "e")
        self.assertEqual(lst.get(1), "d")
        self.assertEqual(lst.get(2), "c")
        self.assertEqual(lst.get(3), "b")
        self.assertEqual(lst.get(4), "a")
        self.assertEqual(lst.length(), 5)

        lst.reverse()
        self.assertEqual(lst.get(0), "a")

        one_item_list = self.ListClass("a")
        one_item_list.reverse()
        self.assertEqual(one_item_list.get(0), "a")
        self.assertEqual(one_item_list.length(), 1)

        self.empty_list.reverse()
        self.assertEqual(self.empty_list.length(), 0)

    def test_findFirst(self):
        self.assertEqual(self.list2.findFirst("y"), 1)
        self.assertEqual(self.list2.findFirst("x"), 0)
        self.assertEqual(self.list2.findFirst("z"), 2)
        self.assertEqual(self.list2.findFirst("a"), -1)
        self.assertEqual(self.empty_list.findFirst("a"), -1)
        with self.assertRaises(TypeError):
            self.list2.findFirst("yy")

    def test_findLast(self):
        self.assertEqual(self.list2.findLast("y"), 3)
        self.assertEqual(self.list2.findLast("x"), 0)
        self.assertEqual(self.list2.findLast("z"), 2)
        self.assertEqual(self.list2.findLast("a"), -1)
        self.assertEqual(self.empty_list.findLast("a"), -1)
        with self.assertRaises(TypeError):
            self.list2.findLast("yy")

    def test_clear(self):
        self.list1.clear()
        self.assertEqual(self.list1.length(), 0)
        with self.assertRaises(IndexError):
            self.list1.get(0)

        self.empty_list.clear()
        self.assertEqual(self.empty_list.length(), 0)

    def test_extend(self):
        lst_a = self.ListClass("ab")
        lst_b = self.ListClass("cd")
        lst_a.extend(lst_b)
        self.assertEqual(lst_a.length(), 4)
        self.assertEqual(lst_a.get(0), "a")
        self.assertEqual(lst_a.get(1), "b")
        self.assertEqual(lst_a.get(2), "c")
        self.assertEqual(lst_a.get(3), "d")

        lst_b.append("e")
        self.assertEqual(lst_a.length(), 4)

        lst_c = self.ListClass("12")
        empty_lst = self.ListClass()
        lst_c.extend(empty_lst)
        self.assertEqual(lst_c.length(), 2)

        empty_lst.extend(lst_c)
        self.assertEqual(empty_lst.length(), 2)
        self.assertEqual(empty_lst.get(0), "1")

        with self.assertRaises(TypeError):
            lst_a.extend("not a list object")

    def test_str_repr(self):
        self.assertTrue(isinstance(str(self.list1), str))
        self.assertTrue(isinstance(repr(self.list1), str))
        self.assertTrue(isinstance(str(self.empty_list), str))
        self.assertTrue(isinstance(repr(self.empty_list), str))


class TestCharArrayList(ListTestsMixin, unittest.TestCase):
    ListClass = CharArrayList


class TestCharDoublyLinkedList(ListTestsMixin, unittest.TestCase):
    ListClass = CharDoublyLinkedList


if __name__ == "__main__":
    unittest.main()
