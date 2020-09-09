from requestparser import Parser, NameSpace
from requestparser.exceptions import (
    ParserRequiredParameterError,
    ParserInvalidChoiceError,
    ParserInvalidParameterError,
    ParserDuplicateParameterError,
    ParserInvalidDataTypeError
)

import unittest
from functools import partial


class TestParser(unittest.TestCase):

    def test_str_without_type(self):

        parser = Parser()
        parser.add_param("name")
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_with_type(self):

        parser = Parser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_to_int_str(self):

        parser = Parser()
        parser.add_param("num", str)
        params: NameSpace = parser.parse_params({"num": 1})
        self.assertEqual(params.num, "1")

    def test_str_to_float(self):

        parser = Parser()
        parser.add_param("num", float)
        params: NameSpace = parser.parse_params({"num": "1.1"})
        self.assertEqual(params.num, 1.1)

    def test_int(self):

        parser = Parser()
        parser.add_param("one")
        params: NameSpace = parser.parse_params({"one": 1})
        self.assertEqual(params.one, 1)

    def test_int_with_type(self):

        parser = Parser()
        parser.add_param("one", int)
        params: NameSpace = parser.parse_params({"one": 1})
        self.assertEqual(params.one, 1)

    def test_required(self):

        parser = Parser()
        parser.add_param("name", str, required=True)
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_required_missing(self):

        parser = Parser()
        parser.add_param("name", str, required=True)

        with self.assertRaises(ParserRequiredParameterError):
            params: NameSpace = parser.parse_params({"one": "two"})

    def test_dest(self):

        parser = Parser()
        parser.add_param("name", str, dest="hello")
        params: NameSpace = parser.parse_params({"name": "world"})
        self.assertEqual(params.hello, "world")

    def test_value_in_choices(self):

        parser = Parser()
        parser.add_param("num", int, choices=[1, 2, 3])
        params: NameSpace = parser.parse_params({"num": 1})
        self.assertEqual(params.num, 1)

    def test_value_not_in_choices(self):

        parser = Parser()
        parser.add_param("num", int, choices=[1, 2, 3])

        with self.assertRaises(ParserInvalidChoiceError):
            params: NameSpace = parser.parse_params({"num": 4})

    def test_action(self):

        parser = Parser()
        parser.add_param("num", int, action=lambda x: x*2)
        params: NameSpace = parser.parse_params({"num": 2})
        self.assertEqual(params.num, 4)

    def test_action_split_string(self):

        parser = Parser()
        parser.add_param("nums", str, action=lambda x: x.split(","))
        params: NameSpace = parser.parse_params({"nums": "1,2,3,4,5"})
        self.assertEqual(params.nums, ["1", "2", "3", "4", "5"])

    def test_action_with_function(self):

        def double(x):
            return x*2

        parser = Parser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_params({"num": 6})
        self.assertEqual(params.num, 12)

    def test_action_with_type_cast_function(self):
        """ Do the type cast on the value before calling the action """

        def double(x):
            return x*2

        parser = Parser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_params({"num": "6"})
        self.assertEqual(params.num, 12)

    def test_action_with_partial(self):

        def f(x, y, z=3):
            return x*y*z

        p = partial(f, 2)

        parser = Parser()
        parser.add_param("num", int, action=p)
        params: NameSpace = parser.parse_params({"num": "6"})
        self.assertEqual(params.num, 36)

    def test_list_to_tuple(self):

        parser = Parser()
        parser.add_param("nums", tuple)
        params: NameSpace = parser.parse_params({"nums": [1, 2, 3]})
        self.assertEqual(params.nums, (1, 2, 3))

    def test_default(self):

        parser = Parser()
        parser.add_param("num", int, default=2)
        params: NameSpace = parser.parse_params({"foo": "bar"})
        self.assertEqual(params.num, 2)

    def test_strict(self):

        parser = Parser()
        parser.add_param("num", int)

        with self.assertRaises(ParserInvalidParameterError):
            params: NameSpace = parser.parse_params({"num": 1, "foo": "bar"}, strict=True)

    def test_duplicate_param(self):

        parser = Parser()
        with self.assertRaises(ParserDuplicateParameterError):
            parser.add_param("num", int)
            parser.add_param("num", float)

    def test_invalid_data_type(self):

        parser = Parser()
        parser.add_param("num", int)
        parser.add_param("name", str)

        with self.assertRaises(ParserInvalidDataTypeError):
            params: NameSpace = parser.parse_params([1, 2, 3])


if __name__ == "__main__":
    unittest.main()
