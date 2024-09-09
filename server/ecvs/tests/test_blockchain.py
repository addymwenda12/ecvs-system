from django.test import TestCase
from unittest.mock import patch, MagicMock
from ..models import Credential, User
from ...blockchain.ethereum_utils import issue_credential, verify_credential
from web3 import Web3

class BlockchainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student')
        self.credential = Credential.objects.create(
            degree="Test Degree",
            institution="Test Institution",
            date_issued="2023-01-01",
            credential_id="TEST123",
            user=self.user
        )

    @patch('server.blockchain.ethereum_utils.w3')
    def test_issue_credential(self, mock_w3):
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}

        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

    @patch('server.blockchain.ethereum_utils.credential_contract')
    def test_verify_credential(self, mock_contract):
        mock_contract.functions.verifyCredential.return_value.call.return_value = True

        result = verify_credential(self.credential.credential_id)
        self.assertTrue(result)

    @patch('server.blockchain.ethereum_utils.w3')
    def test_network_error(self, mock_w3):
        mock_w3.eth.send_raw_transaction.side_effect = Exception("Network error")

        with self.assertRaises(Exception):
            issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))

    @patch('server.blockchain.ethereum_utils.credential_contract')
    def test_invalid_credential(self, mock_contract):
        mock_contract.functions.verifyCredential.return_value.call.return_value = False

        result = verify_credential("INVALID123")
        self.assertFalse(result)

    @patch('server.blockchain.ethereum_utils.w3')
    def test_gas_price_fluctuation(self, mock_w3):
        mock_w3.eth.gas_price = 20000000000  # 20 Gwei
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}

        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

        # Simulate gas price increase
        mock_w3.eth.gas_price = 50000000000  # 50 Gwei

        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)