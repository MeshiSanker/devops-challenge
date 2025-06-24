import unittest
import os
from unittest.mock import patch, MagicMock
from app.main import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test the /health endpoint."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'healthy')
        self.assertIn('project', json_data)
        self.assertIn('container', json_data)

    @patch('app.main.get_secret_from_dynamodb')
    def test_secret_endpoint(self, mock_get_secret):
        """Test the /secret endpoint with a mocked DynamoDB call."""
        mock_get_secret.return_value = "supersecretcode"
        
        # We need to reload the SECRET_CODE in the context of the app
        with patch.dict('os.environ', {'CODE_NAME': 'thedoctor'}):
             # Since SECRET_CODE is loaded at startup, we need to mock it differently or restart the app logic
             # For simplicity in this test, we will patch the SECRET_CODE variable directly.
            with patch('app.main.SECRET_CODE', "supersecretcode"):
                response = self.app.get('/secret')
                self.assertEqual(response.status_code, 200)
                json_data = response.get_json()
                self.assertEqual(json_data['secret_code'], "supersecretcode")

    @patch('boto3.resource')
    def test_get_secret_from_dynamodb_success(self, mock_boto_resource):
        """Test the DynamoDB function successfully fetches the secret."""
        mock_table = MagicMock()
        mock_table.get_item.return_value = {
            'Item': {
                'secret_code': 'test_secret'
            }
        }
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto_resource.return_value = mock_dynamodb

        with patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'fake_key', 'AWS_SECRET_ACCESS_KEY': 'fake_secret'}):
            from app.main import get_secret_from_dynamodb
            secret = get_secret_from_dynamodb('thedoctor')
            self.assertEqual(secret, 'test_secret')

    @patch('boto3.resource')
    def test_get_secret_from_dynamodb_no_item(self, mock_boto_resource):
        """Test the DynamoDB function when the item is not found."""
        mock_table = MagicMock()
        mock_table.get_item.return_value = {}
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto_resource.return_value = mock_dynamodb

        with patch.dict('os.environ', {'AWS_ACCESS_KEY_ID': 'fake_key', 'AWS_SECRET_ACCESS_KEY': 'fake_secret'}):
            from app.main import get_secret_from_dynamodb
            result = get_secret_from_dynamodb('unknown_doctor')
            self.assertIn("Error: Item with code_name 'unknown_doctor' not found.", result)

if __name__ == '__main__':
    unittest.main() 