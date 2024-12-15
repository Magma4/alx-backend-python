#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient  # Import the class to be tested


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_response, mock_get_json):
        mock_get_json.return_value = expected_response
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_response)

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the expected URL based on the mocked org payload.
        """
        # Define the mocked payload
        mock_payload = {"repos_url": "https://api.github.com/orgs/test-org/repos"}

        # Set the return value of the mocked org property
        mock_org.return_value = mock_payload

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("test-org")

        # Access _public_repos_url and verify the result
        result = client._public_repos_url
        expected = "https://api.github.com/orgs/test-org/repos"
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
