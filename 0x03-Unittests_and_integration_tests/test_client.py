#!/usr/bin/env python3
"""Unit tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test GithubOrgClient.org returns correct data"""
        expected_payload = {"login": "test_org"}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("test_org")
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org")

    @patch.object(GithubOrgClient, 'org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url returns the correct URL"""
        expected_url = "https://api.github.com/orgs/test_org/repos"
        mock_org.return_value = {"repos_url": expected_url}

        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo list"""
        # Mock repo payload returned by get_json
        mock_repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value = mock_repos_payload

        client = GithubOrgClient("test_org")

        # Patch the _public_repos_url property to a dummy URL
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test_org/repos"

            # Call the method under test without license filter
            repos = client.public_repos()

            # Validate the returned repo names (all repos regardless of license)
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            # Check that mocks were called exactly once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")


if __name__ == '__main__':
    unittest.main()
