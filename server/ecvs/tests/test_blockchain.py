from django.test import TestCase
from unittest.mock import patch, MagicMock
from ..models import Credential, User, Wallet
from blockchain.ethereum_utils import issue_credential, issue_credential_with_retry, verify_credential, get_balance, generate_ethereum_address
from web3 import Web3

class BlockchainTest(TestCase):
    @patch('blockchain.ipfs_utils.connect_to_ipfs')
    def setUp(self, mock_connect_to_ipfs):
        mock_ipfs_client = MagicMock()
        mock_connect_to_ipfs.return_value = mock_ipfs_client
        
        self.user = User.objects.create_user(username='testuser', password='testpass', role='student')
        self.credential = Credential.objects.create(
            degree="Test Degree",
            institution="Test University",
            date_issued="2023-01-01",
            credential_id="TEST123",
            user_id=1
        )
        self.wallet = Wallet.objects.create(user=self.user)

    @patch('blockchain.ethereum_utils.w3')
    def test_issue_credential(self, mock_w3):
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)
        self.assertEqual(result['status'], 1)
    @patch('blockchain.ethereum_utils.credential_contract')
    def test_verify_credential(self, mock_contract):
        mock_contract.functions.verifyCredential.return_value.call.return_value = True
        mock_contract.functions.verifyCredential.return_value.call.return_value = True
        result = verify_credential(self.credential.credential_id)
        self.assertTrue(result)
        self.assertTrue(result)
    @patch('blockchain.ethereum_utils.w3')
    def test_network_error(self, mock_w3):
        mock_w3.eth.send_raw_transaction.side_effect = Exception("Network error")
    @patch('blockchain.ethereum_utils.w3')
    def test_invalid_credential(self, mock_w3):
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
        mock_w3.eth.get_transaction_count.return_value = 0
        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

    @patch('blockchain.ethereum_utils.credential_contract')
    def test_invalid_credential(self, mock_contract):
        mock_contract.functions.verifyCredential.return_value.call.return_value = False
        result = verify_credential("INVALID123")
        self.assertFalse(result)

    @patch('blockchain.ethereum_utils.w3')
    def test_gas_price_fluctuation(self, mock_w3):
        mock_w3.eth.gas_price = 20000000000  # 20 Gwei
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
        mock_w3.eth.get_transaction_count.return_value = 0
        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

        # Simulate gas price increase
        mock_w3.eth.gas_price = 50000000000  # 50 Gwei

        result = issue_credential(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

    @patch('blockchain.ethereum_utils.w3')
    def test_get_balance(self, mock_w3):
        mock_w3.eth.get_balance.return_value = Web3.to_wei(1.5, 'ether')
        mock_w3.from_wei.return_value = 1.5
        balance = get_balance(self.wallet.address)
        self.assertEqual(balance, 1.5)

    def test_generate_ethereum_address(self):
        address, private_key = generate_ethereum_address()
        self.assertTrue(Web3.is_address(address))
        self.assertEqual(len(private_key), 64)  # 32 bytes in hex

    def test_wallet_encryption(self):
        test_private_key = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        self.wallet.set_private_key(test_private_key)
        self.assertNotEqual(self.wallet.encrypted_private_key, test_private_key)
        decrypted_key = self.wallet.get_private_key()
        self.assertEqual(decrypted_key, test_private_key)

    @patch('blockchain.ethereum_utils.w3')
    def test_issue_credential_with_retry(self, mock_w3):
        mock_w3.eth.account.from_key.return_value = MagicMock()
        mock_w3.eth.get_transaction_count.return_value = 0
        mock_w3.eth.send_raw_transaction.return_value = b'test_hash'
        mock_w3.eth.wait_for_transaction_receipt.return_value = {'status': 1}
        
        result = issue_credential_with_retry(self.credential.credential_id, Web3.keccak(text=self.credential.credential_id))
        self.assertEqual(result['status'], 1)

    @patch('blockchain.ethereum_utils.verify_credential')
    def test_verify_credential_with_retry(self, mock_verify):
        mock_verify.return_value = (True, 'test_ipfs_hash')
        
        is_verified, ipfs_hash = verify_credential_with_retry(self.credential.credential_id)
        self.assertTrue(is_verified)
        self.assertEqual(ipfs_hash, 'test_ipfs_hash')