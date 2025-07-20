#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient.org using parameterized and patch decorators
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data and calls get_json once"""
        mock_payload = {"login": org_name, "id": 1}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org()

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, mock_payload)


if __name__ == "__main__":
    unittest.main()
