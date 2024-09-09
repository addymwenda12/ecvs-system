from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Credential, User
from django.utils import timezone
from unittest.mock import patch

class CredentialAPITest(TestCase):
    """
    Test cases for the Credential API.
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student')
        self.client.force_authenticate(user=self.user)
        self.credential_data = {
            "degree": "Bachelor of Science",
            "institution": "University of Example",
            "date_issued": "2023-05-01",
            "credential_id": "123456",
            "user_id": self.user.id
        }

    def test_create_credential(self):
        """
        Test the creation of a new credential.
        """
        response = self.client.post('/api/credentials/', self.credential_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_credential_invalid_degree(self):
        """
        Test the validation for minimum degree length.
        """
        invalid_data = self.credential_data.copy()
        invalid_data['degree'] = 'A'
        response = self.client.post('/api/credentials/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('degree', response.data)

    def test_create_credential_invalid_institution(self):
        """
        Test the validation for minimum institution name length.
        """
        invalid_data = self.credential_data.copy()
        invalid_data['institution'] = 'A'
        response = self.client.post('/api/credentials/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('institution', response.data)

    def test_create_credential_future_date(self):
        """
        Test the validation for future dates.
        """
        invalid_data = self.credential_data.copy()
        invalid_data['date_issued'] = (timezone.now() + timezone.timedelta(days=1)).date().isoformat()
        response = self.client.post('/api/credentials/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('date_issued', response.data)

    def test_create_credential_duplicate_id(self):
        """
        Test the unique constraint on credential_id.
        """
        self.client.post('/api/credentials/', self.credential_data, format='json')
        response = self.client.post('/api/credentials/', self.credential_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('credential_id', response.data)

    def test_get_credentials(self):
        """
        Test the retrieval of all credentials.
        """
        response = self.client.get('/api/credentials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_credential(self):
        """
        Test the update of a credential.
        """
        self.client.post('/api/credentials/', self.credential_data, format='json')
        updated_data = {"degree": "Master of Science"}
        response = self.client.patch('/api/credentials/1/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_credential_invalid_degree(self):
        """
        Test validation during update operations.
        """
        self.client.post('/api/credentials/', self.credential_data, format='json')
        invalid_data = {"degree": "A"}
        response = self.client.patch('/api/credentials/1/', invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('degree', response.data)

    def test_delete_credential(self):
        """
        Test the deletion of a credential.
        """
        self.client.post('/api/credentials/', self.credential_data, format='json')
        response = self.client.delete('/api/credentials/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch('server.blockchain.ethereum_utils.verify_credential')
    def test_verify_credential(self, mock_verify):
        """
        Test the verification of a credential.
        """
        mock_verify.return_value = True
        self.client.post('/api/credentials/', self.credential_data, format='json')
        response = self.client.post('/api/credentials/1/verify/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_verified'])

    @patch('server.blockchain.ethereum_utils.verify_credential')
    def test_verify_nonexistent_credential(self, mock_verify):
        """
        Test the verification of a nonexistent credential.
        """
        mock_verify.return_value = False
        response = self.client.post('/api/credentials/999/verify/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)