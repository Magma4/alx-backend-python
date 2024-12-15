#!/usr/bin/env python3

"""
Unit tests for the GithubOrgClient class in the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        """
        Test that GithubOrgClient.org calls get_json with the correct URL
        and returns the expected response.
        """
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_response)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the expected URL
        based on the mocked org payload.
        """
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/test-org/repos"
        }
        mock_org.return_value = mock_payload

        client = GithubOrgClient("test-org")
        result = client._public_repos_url
        expected = "https://api.github.com/orgs/test-org/repos"
        self.assertEqual(result, expected)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that GithubOrgClient.public_repos returns the expected list
        of repository names based on the mocked response.
        """
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_public_repos_url = "https://api.github.com/orgs/test-org/repos"

        mock_get_json.return_value = mock_repos_payload

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=mock_public_repos_url,
        ) as mock_url:
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            expected = ["repo1", "repo2", "repo3"]

            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_public_repos_url)


if __name__ == "__main__":
    unittest.main()
