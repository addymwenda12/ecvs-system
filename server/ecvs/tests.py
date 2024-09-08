from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Credential

class CredentialAPITest(TestCase):
    """
    Test cases for the Credential API.
    """
    def setUp(self):
        self.client = APIClient()
        self.credential_data = {
            "degree": "Bachelor of Science",
            "institution": "University of Example",
            "date_issued": "2023-05-01",
            "credential_id": "123456"
        }

    def test_create_credential(self):
        """
        Test the creation of a new credential.
        """
        response = self.client.post('/api/credentials/', self.credential_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_credentials(self):
        """
        Test the retrieval of all credentials.
        """
        response = self.client.get('/api/credentials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
