from dictparser import DictionaryParser, NameSpace, Param
from dictparser.exceptions import (
    ParserRequiredParameterError,
    ParserInvalidChoiceError,
    ParserInvalidParameterError,
    ParserDuplicateParameterError,
    ParserInvalidDataTypeError
)

from functools import partial
import unittest


class TestParser(unittest.TestCase):

    def test_str_without_type(self):

        parser = DictionaryParser()
        parser.add_param("name")
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_with_type(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_to_int_str(self):

        parser = DictionaryParser()
        parser.add_param("num", str)
        params: NameSpace = parser.parse_params({"num": 1})
        self.assertEqual(params.num, "1")

    def test_str_to_float(self):

        parser = DictionaryParser()
        parser.add_param("num", float)
        params: NameSpace = parser.parse_params({"num": "1.1"})
        self.assertEqual(params.num, 1.1)

    def test_int(self):

        parser = DictionaryParser()
        parser.add_param("one")
        params: NameSpace = parser.parse_params({"one": 1})
        self.assertEqual(params.one, 1)

    def test_int_with_type(self):

        parser = DictionaryParser()
        parser.add_param("one", int)
        params: NameSpace = parser.parse_params({"one": 1})
        self.assertEqual(params.one, 1)

    def test_required(self):

        parser = DictionaryParser()
        parser.add_param("name", str, required=True)
        params: NameSpace = parser.parse_params({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_required_missing(self):

        parser = DictionaryParser()
        parser.add_param("name", str, required=True)

        with self.assertRaises(ParserRequiredParameterError):
            params: NameSpace = parser.parse_params({"one": "two"})

    def test_dest(self):

        parser = DictionaryParser()
        parser.add_param("name", str, dest="hello")
        params: NameSpace = parser.parse_params({"name": "world"})
        self.assertEqual(params.hello, "world")

    def test_value_in_choices(self):

        parser = DictionaryParser()
        parser.add_param("num", int, choices=[1, 2, 3])
        params: NameSpace = parser.parse_params({"num": 1})
        self.assertEqual(params.num, 1)

    def test_value_not_in_choices(self):

        parser = DictionaryParser()
        parser.add_param("num", int, choices=[1, 2, 3])

        with self.assertRaises(ParserInvalidChoiceError):
            params: NameSpace = parser.parse_params({"num": 4})

    def test_action(self):

        parser = DictionaryParser()
        parser.add_param("num", int, action=lambda x: x*2)
        params: NameSpace = parser.parse_params({"num": 2})
        self.assertEqual(params.num, 4)

    def test_action_split_string(self):

        parser = DictionaryParser()
        parser.add_param("nums", str, action=lambda x: x.split(","))
        params: NameSpace = parser.parse_params({"nums": "1,2,3,4,5"})
        self.assertEqual(params.nums, ["1", "2", "3", "4", "5"])

    def test_action_with_function(self):

        def double(x):
            return x*2

        parser = DictionaryParser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_params({"num": 6})
        self.assertEqual(params.num, 12)

    def test_action_with_type_cast_function(self):

        def double(x):
            return x*2

        parser = DictionaryParser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_params({"num": "6"})
        self.assertEqual(params.num, 12)

    def test_action_with_partial(self):

        def f(x, y, z=3):
            return x*y*z

        p = partial(f, 2)

        parser = DictionaryParser()
        parser.add_param("num", int, action=p)
        params: NameSpace = parser.parse_params({"num": "6"})
        self.assertEqual(params.num, 36)

    def test_list_to_tuple(self):

        parser = DictionaryParser()
        parser.add_param("nums", tuple)
        params: NameSpace = parser.parse_params({"nums": [1, 2, 3]})
        self.assertEqual(params.nums, (1, 2, 3))

    def test_default(self):

        parser = DictionaryParser()
        parser.add_param("num", int, default=2)
        params: NameSpace = parser.parse_params({"foo": "bar"})
        self.assertEqual(params.num, 2)

    def test_strict(self):

        parser = DictionaryParser()
        parser.add_param("num", int)

        with self.assertRaises(ParserInvalidParameterError):
            params: NameSpace = parser.parse_params({"num": 1, "foo": "bar"}, strict=True)

    def test_duplicate_param(self):

        parser = DictionaryParser()
        with self.assertRaises(ParserDuplicateParameterError):
            parser.add_param("num", int)
            parser.add_param("num", float)

    def test_invalid_data_type(self):

        parser = DictionaryParser()
        parser.add_param("num", int)
        parser.add_param("name", str)

        with self.assertRaises(ParserInvalidDataTypeError):
            params: NameSpace = parser.parse_params([1, 2, 3])

    def test_regex_match(self):

        parser = DictionaryParser()
        parser.add_param("name", str, regex=r"^\w{3} bar \w{3}$")
        params: NameSpace = parser.parse_params({"name": "foo bar baz"})

        self.assertEqual(params.name, "foo bar baz")

    def test_regex_no_match(self):

        parser = DictionaryParser()
        parser.add_param("name", str, regex=r"^\w{3} bar \w{3}$")
        params: NameSpace = parser.parse_params({"name": "foo tar baz"})

        self.assertEqual(params.name, None)

    def test_regex_match_int(self):

        parser = DictionaryParser()
        parser.add_param("num", int, regex=r"1")
        params: NameSpace = parser.parse_params({"num": "1"})

        self.assertEqual(params.num, 1)

    def test_namespace_to_dict(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_params({"name": "foo", "num": 1})

        self.assertEqual(params.to_dict(), {"name": "foo", "num": 1})

    def test_namespace_get(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_params({"name": "foo", "num": 1})

        self.assertEqual(params.get("name"), "foo")

    def test_namespace_get_param_object(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_params({"name": "foo", "num": 1})

        self.assertIsInstance(params.get_param("name"), Param)

    def test_namespace_get_returns_default_none(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_params({"name": "foo", "num": 1})

        self.assertEqual(params.get("bar"), None)

    def test_namespace_get_returns_default_supplied(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_params({"name": "foo", "num": 1})

        self.assertEqual(params.get("bar", 22), 22)

    def test_parser_with_empty_value(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_params({"name": ""})

        self.assertEqual(params.name, None)

    def test_parser_with_empty_value_and_default(self):

        parser = DictionaryParser()
        parser.add_param("name", str, default="")
        params: NameSpace = parser.parse_params({"name": ""})

        self.assertEqual(params.name, "")

    def test_parser_with_json_string_data(self):

        parser = DictionaryParser()
        parser.add_param("name", str, default="")
        params: NameSpace = parser.parse_params('{"name": "foo"}')

        self.assertEqual(params.name, "foo")

    def test_parser_with_string_data_not_dict(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        with self.assertRaises(ParserInvalidDataTypeError):
            params: NameSpace = parser.parse_params('["name", "foo"]')

    def test_parser_invalid_json_string(self):
        parser = DictionaryParser()
        parser.add_param("name", str)
        with self.assertRaises(ParserInvalidDataTypeError) as e:
            params: NameSpace = parser.parse_params("('name', 'foo')")
            self.assertEqual(str(e.exception), "Invalid JSON string for param 'data'. Could not decode JSON to dict")


if __name__ == "__main__":
    unittest.main()
