from dictparse import DictionaryParser, NameSpace, Param
from dictparse.exceptions import (
    ParserTypeError,
    ParserRequiredKeyError,
    ParserInvalidChoiceError,
    ParserInvalidKeyError,
    ParserDuplicateKeyError,
    ParserInvalidDataTypeError
)

from functools import partial
import unittest


class TestParser(unittest.TestCase):

    def test_add_param_name_incorrect_type_for_name(self):
        """ Raises a TypeError when name is an int """

        parser = DictionaryParser()

        with self.assertRaises(TypeError):
            parser.add_param(name=1)

    def test_add_param_name_illegal_name_get(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="get")

    def test_add_param_name_illegal_name_containing_dunders(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="__str__")

    def test_add_param_name_illegal_name_containing_keyword(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="def")

    def test_add_param_name_illegal_name_get_param(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="get_param")

    def test_add_param_name_illegal_name_to_dict(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="to_dict")

    def test_add_param_name_illegal_string_int(self):
        """ Raises a ValueError when name starts with an int """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="1foo")

    def test_add_param_name_illegal_string_space(self):
        """ Raises a ValueError when name starts with a space """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name=" foo")

    def test_add_param_name_illegal_string_dot(self):
        """ Raises a ValueError when name starts with a dot """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name=".foo")

    def test_add_param_dest_incorrect_type_for_dest(self):
        """ Raises a TypeError when dest is an int """

        parser = DictionaryParser()

        with self.assertRaises(TypeError):
            parser.add_param(name="foo", dest=1)

    def test_add_param_dest_illegal_string_int(self):
        """ Raises a ValueError when dest starts with an int """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="foo", dest="1day")

    def test_add_param_dest_illegal_string_space(self):
        """ Raises a ValueError when dest starts with a space """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="foo", dest=" day")

    def test_add_param_dest_illegal_string_dot(self):
        """ Raises a ValueError when dest starts with a dot """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="foo", dest=".day")

    def test_add_param_dest_illegal_string_char(self):
        """ Raises a ValueError when dest contains an illegal char """

        parser = DictionaryParser()

        with self.assertRaises(ValueError):
            parser.add_param(name="foo", dest="foo%day")

    def test_parser_type_error(self):

        parser = DictionaryParser()
        parser.add_param("name", int)

        with self.assertRaises(ParserTypeError):
            params: NameSpace = parser.parse_dict({"name": "foo"})

    def test_parser_choices_not_valid_type(self):

        parser = DictionaryParser()

        with self.assertRaises(TypeError):
            parser.add_param("name", int, choices="foo")

    def test_parser_action_not_callable(self):

        parser = DictionaryParser()

        with self.assertRaises(TypeError):
            parser.add_param("name", int, action="foo")

    def test_str_without_type(self):

        parser = DictionaryParser()
        parser.add_param("name")
        params: NameSpace = parser.parse_dict({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_with_type(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_dict({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_str_to_int_str(self):

        parser = DictionaryParser()
        parser.add_param("num", str)
        params: NameSpace = parser.parse_dict({"num": 1})
        self.assertEqual(params.num, "1")

    def test_str_to_float(self):

        parser = DictionaryParser()
        parser.add_param("num", float)
        params: NameSpace = parser.parse_dict({"num": "1.1"})
        self.assertEqual(params.num, 1.1)

    def test_int(self):

        parser = DictionaryParser()
        parser.add_param("one")
        params: NameSpace = parser.parse_dict({"one": 1})
        self.assertEqual(params.one, 1)

    def test_int_with_type(self):

        parser = DictionaryParser()
        parser.add_param("one", int)
        params: NameSpace = parser.parse_dict({"one": 1})
        self.assertEqual(params.one, 1)

    def test_required(self):

        parser = DictionaryParser()
        parser.add_param("name", str, required=True)
        params: NameSpace = parser.parse_dict({"name": "foo"})
        self.assertEqual(params.name, "foo")

    def test_required_missing(self):

        parser = DictionaryParser()
        parser.add_param("name", str, required=True)

        with self.assertRaises(ParserRequiredKeyError):
            params: NameSpace = parser.parse_dict({"one": "two"})

    def test_dest(self):

        parser = DictionaryParser()
        parser.add_param("name", str, dest="hello")
        params: NameSpace = parser.parse_dict({"name": "world"})
        self.assertEqual(params.hello, "world")

    def test_value_in_choices(self):

        parser = DictionaryParser()
        parser.add_param("num", int, choices=[1, 2, 3])
        params: NameSpace = parser.parse_dict({"num": 1})
        self.assertEqual(params.num, 1)

    def test_value_not_in_choices(self):

        parser = DictionaryParser()
        parser.add_param("num", int, choices=[1, 2, 3])

        with self.assertRaises(ParserInvalidChoiceError):
            params: NameSpace = parser.parse_dict({"num": 4})

    def test_action(self):

        parser = DictionaryParser()
        parser.add_param("num", int, action=lambda x: x * 2)
        params: NameSpace = parser.parse_dict({"num": 2})
        self.assertEqual(params.num, 4)

    def test_action_split_string(self):

        parser = DictionaryParser()
        parser.add_param("nums", str, action=lambda x: x.split(","))
        params: NameSpace = parser.parse_dict({"nums": "1,2,3,4,5"})
        self.assertEqual(params.nums, ["1", "2", "3", "4", "5"])

    def test_action_with_function(self):

        def double(x):
            return x*2

        parser = DictionaryParser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_dict({"num": 6})
        self.assertEqual(params.num, 12)

    def test_action_with_type_cast_function(self):

        def double(x):
            return x*2

        parser = DictionaryParser()
        parser.add_param("num", int, action=double)
        params: NameSpace = parser.parse_dict({"num": "6"})
        self.assertEqual(params.num, 12)

    def test_action_with_partial(self):

        def f(x, y, z=3):
            return x*y*z

        p = partial(f, 2)

        parser = DictionaryParser()
        parser.add_param("num", int, action=p)
        params: NameSpace = parser.parse_dict({"num": "6"})
        self.assertEqual(params.num, 36)

    def test_list_to_tuple(self):

        parser = DictionaryParser()
        parser.add_param("nums", tuple)
        params: NameSpace = parser.parse_dict({"nums": [1, 2, 3]})
        self.assertIsInstance(params.nums, tuple)
        self.assertEqual(params.nums, (1, 2, 3))

    def test_list_to_set(self):

        parser = DictionaryParser()
        parser.add_param("nums", set)
        params: NameSpace = parser.parse_dict({"nums": [1, 2, 3, 3, 3]})
        self.assertIsInstance(params.nums, set)
        self.assertEqual(params.nums, {1, 2, 3})

    def test_default(self):

        parser = DictionaryParser()
        parser.add_param("num", int, default=2)
        params: NameSpace = parser.parse_dict({"foo": "bar"})
        self.assertEqual(params.num, 2)

    def test_param_default_is_none(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_dict({"foo": "bar"})
        self.assertIs(params.name, None)

    def test_strict(self):

        parser = DictionaryParser()
        parser.add_param("num", int)

        with self.assertRaises(ParserInvalidKeyError):
            params: NameSpace = parser.parse_dict({"num": 1, "foo": "bar"}, strict=True)

    def test_duplicate_param(self):

        parser = DictionaryParser()
        with self.assertRaises(ParserDuplicateKeyError):
            parser.add_param("num", int)
            parser.add_param("num", float)

    def test_invalid_data_type(self):

        parser = DictionaryParser()
        parser.add_param("num", int)
        parser.add_param("name", str)

        with self.assertRaises(TypeError):
            params: NameSpace = parser.parse_dict([1, 2, 3])

    def test_regex_match(self):

        parser = DictionaryParser()
        parser.add_param("name", str, regex=r"^\w{3} bar \w{3}$")
        params: NameSpace = parser.parse_dict({"name": "foo bar baz"})

        self.assertEqual(params.name, "foo bar baz")

    def test_regex_no_match(self):

        parser = DictionaryParser()
        parser.add_param("name", str, regex=r"^\w{3} bar \w{3}$")
        params: NameSpace = parser.parse_dict({"name": "foo tar baz"})

        self.assertEqual(params.name, None)

    def test_regex_match_int(self):

        parser = DictionaryParser()
        parser.add_param("num", int, regex=r"1")
        params: NameSpace = parser.parse_dict({"num": "1"})

        self.assertEqual(params.num, 1)

    def test_namespace_to_dict(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_dict({"name": "foo", "num": 1})

        self.assertEqual(params.to_dict(), {"name": "foo", "num": 1})

    def test_namespace_get(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_dict({"name": "foo", "num": 1})

        self.assertEqual(params.get("name"), "foo")

    def test_namespace_get_param_object(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_dict({"name": "foo", "num": 1})

        self.assertIsInstance(params.get_param("name"), Param)

    def test_namespace_get_returns_default_none(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_dict({"name": "foo", "num": 1})

        self.assertEqual(params.get("bar"), None)

    def test_namespace_get_returns_default_supplied(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("num", int)
        params: NameSpace = parser.parse_dict({"name": "foo", "num": 1})

        self.assertEqual(params.get("bar", 22), 22)

    def test_parser_with_empty_value(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        params: NameSpace = parser.parse_dict({"name": ""})

        self.assertEqual(params.name, None)

    def test_parser_with_empty_value_and_default(self):

        parser = DictionaryParser()
        parser.add_param("name", str, default="")
        params: NameSpace = parser.parse_dict({"name": ""})

        self.assertEqual(params.name, "")

    def test_parser_with_string_data_not_dict(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        with self.assertRaises(TypeError):
            params: NameSpace = parser.parse_dict('["name", "foo"]')

    def test_parser_action(self):

        parser = DictionaryParser()
        parser.add_param("foo", str)
        parser.add_param("bar", str)
        parser.add_param("baz", str)
        params = parser.parse_dict({"foo": "foo", "bar": "bar", "baz": "baz"}, action=lambda x: x.upper())
        self.assertEqual(params.foo, "FOO")
        self.assertEqual(params.bar, "BAR")
        self.assertEqual(params.baz, "BAZ")

    def test_parser_action_int(self):

        def square(x):
            return x ** 2

        parser = DictionaryParser()
        parser.add_param("foo", int)
        parser.add_param("bar", int)
        parser.add_param("baz", int)
        params = parser.parse_dict({"foo": 1, "bar": 2, "baz": 3}, action=square)
        self.assertEqual(params.foo, 1)
        self.assertEqual(params.bar, 4)
        self.assertEqual(params.baz, 9)

    def test_parser_action_with_none(self):

        parser = DictionaryParser()
        parser.add_param("foo", str)
        params = parser.parse_dict({"foo": None}, action=lambda x: x.upper())
        self.assertEqual(params.foo, None)

    def test_parse_params_raises_exception_with_list(self):

        parser = DictionaryParser()
        parser.add_param("foo", str)

        with self.assertRaises(ParserInvalidDataTypeError):
            params = parser.parse_dict([1, 2, 3])

    def test_parse_params_raises_exception_with_str(self):

        parser = DictionaryParser()
        parser.add_param("foo", str)

        with self.assertRaises(ParserInvalidDataTypeError):
            params = parser.parse_dict("foo")

    def test_param_dest(self):

        parser = DictionaryParser()
        parser.add_param("foo", str, dest="bar")
        params = parser.parse_dict({"foo": 42})

        param = params.get_param("bar")
        self.assertEqual(param.name, "foo")

    def test_add_param_invalid_type(self):

        parser = DictionaryParser()

        with self.assertRaises(TypeError):
            parser.add_param("foo", object)

    def test_parse_dict_invalid_action(self):

        parser = DictionaryParser()
        parser.add_param("foo", str)
        parser.add_param("bar", str)

        with self.assertRaises(TypeError):
            params = parser.parse_dict({"foo": 1, "bar": 2}, action=1)

    def test_bools_with_string(self):

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": "1"})
        self.assertEqual(params.active, True)

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": "0"})
        self.assertEqual(params.active, False)

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": "true"})
        self.assertEqual(params.active, True)

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": "false"})
        self.assertEqual(params.active, False)

    def test_bools_with_int(self):

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": 1})
        self.assertEqual(params.active, True)

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": 0})
        self.assertEqual(params.active, False)

    def test_bools_with_bools(self):

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": True})
        self.assertEqual(params.active, True)

        parser = DictionaryParser()
        parser.add_param("active", bool)
        params: NameSpace = parser.parse_dict({"active": False})
        self.assertEqual(params.active, False)