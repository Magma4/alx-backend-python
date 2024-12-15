import unittest
from unittest.mock import patch
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


if __name__ == "__main__":
    unittest.main()
