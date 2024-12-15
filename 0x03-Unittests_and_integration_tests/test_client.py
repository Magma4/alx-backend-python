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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test GithubOrgClient.public_repos.
        """

        # Define mocked payloads
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_public_repos_url = "https://api.github.com/orgs/test-org/repos"

        # Mock get_json to return the payload
        mock_get_json.return_value = mock_repos_payload

        # Mock _public_repos_url property using a context manager
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
            return_value=mock_public_repos_url,
        ) as mock_url:
            # Create an instance of GithubOrgClient
            client = GithubOrgClient("test-org")

            # Call public_repos
            result = client.public_repos()

            # Expected list of repo names
            expected = ["repo1", "repo2", "repo3"]

            # Assertions
            self.assertEqual(result, expected)  # Test the repo list matches
            mock_url.assert_called_once()  # Ensure _public_repos_url was called once
            mock_get_json.assert_called_once_with(mock_public_repos_url)

if __name__ == "__main__":
    unittest.main()
