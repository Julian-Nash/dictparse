from dictparse import DictionaryParser

import unittest


class TestNamespace(unittest.TestCase):

    def test_namespace_to_dict(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("age", int)
        parser.add_param("csrf_token", str, required=True)
        params = parser.parse_dict(
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )
        self.assertEqual(
            params.to_dict(),
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )

    def test_namespace_to_dict_returns_none_values(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("age", int)
        parser.add_param("foo")
        parser.add_param("csrf_token", str, required=True)
        params = parser.parse_dict(
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )

        self.assertEqual(
            params.to_dict(),
            {"name": "foo", "age": 32, "foo": None, "csrf_token": "1234xyz"}
        )

    def test_namespace_to_dict_exclude_list(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("age", int)
        parser.add_param("csrf_token", str, required=True)
        params = parser.parse_dict(
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )
        self.assertEqual(
            params.to_dict(exclude=["csrf_token"]),
            {"name": "foo", "age": 32}
        )

    def test_namespace_to_dict_exclude_tuple(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("age", int)
        parser.add_param("csrf_token", str, required=True)
        params = parser.parse_dict(
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )
        self.assertEqual(
            params.to_dict(exclude=("csrf_token")),
            {"name": "foo", "age": 32}
        )

    def test_namespace_to_dict_exclude_set(self):

        parser = DictionaryParser()
        parser.add_param("name", str)
        parser.add_param("age", int)
        parser.add_param("csrf_token", str, required=True)
        params = parser.parse_dict(
            {"name": "foo", "age": 32, "csrf_token": "1234xyz"}
        )
        self.assertEqual(
            params.to_dict(exclude={"csrf_token"}),
            {"name": "foo", "age": 32}
        )