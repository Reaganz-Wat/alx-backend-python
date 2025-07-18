#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns the correct value"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_message):
        """Test that access_nested_map raises KeyError when path is invalid"""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), expected_message)

class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # Mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the actual function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)  # Verify correct URL used
        self.assertEqual(result, test_payload)  # Verify returned JSON


if __name__ == "__main__":
    unittest.main()
