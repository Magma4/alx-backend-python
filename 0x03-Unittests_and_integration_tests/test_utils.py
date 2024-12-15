#!/usr/bin/env python3

"""
This module contains unit tests for the utility functions
in the `utils` module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit tests for the access_nested_map function.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the expected result
        for valid inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that access_nested_map raises a KeyError
        for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), f"'{context.exception.args[0]}'")


class TestGetJson(unittest.TestCase):
    """
    Unit tests for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json makes an HTTP GET request to the
        correct URL and returns the expected JSON response.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Unit tests for the memoize decorator.
    """

    def test_memoize(self):
        """
        Test that the memoize decorator caches the result
        of a method.
        """
        class TestClass:
            """
            Class to test the memoize decorator.
            """

            def a_method(self):
                """
                Method that will be cached by memoize.
                """
                return 42

            @memoize
            def a_property(self):
                """
                Property method decorated with memoize.
                """
                return self.a_method()

        test_obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
