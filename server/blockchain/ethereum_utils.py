from web3 import Web3
from dotenv import load_dotenv
import os
import json
from .contract_abi import CONTRACT_ABI

load_dotenv()

# Connect to the Ethereum network
w3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_NODE_URL')))

# Check if the connection is successful
if not w3.is_connected():
    raise Exception("Failed to connect to the Ethereum network")

# Get the chain ID
chain_id = w3.eth.chain_id

# Load contract ABI and address
current_dir = os.path.dirname(os.path.abspath(__file__))
contract_path = os.path.join(current_dir, '..', 'build', 'contracts', 'CredentialContract.json')
with open(contract_path) as f:
    contract_json = json.load(f)
contract_abi = contract_json['abi']
contract_address = os.getenv('CONTRACT_ADDRESS')

# Create cotract instance
credential_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def issue_credential(credential_id, hash_value):
    """
    Issue a credential on the blockchain
    """
    account = w3.eth.account.from_key(os.getenv('PRIVATE_KEY'))
    nonce = w3.eth.get_transaction_count(account.address)
    
    txn = credential_contract.functions.issueCredential(credential_id, hash_value).build_transaction({
        'chainId': chain_id,  # Mainnet
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })

    signed_txn = account.sign_transaction(txn)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def verify_credential(credential_id):
    """
    Verify a credential on the blockchain
    """
    try:
        print(f"Attempting to verify credential with ID: {credential_id}")
        result = credential_contract.functions.verifyCredential(credential_id).call()
        print(f"Verification result for credential {credential_id}: {result}")
        return result
    except Exception as e:
        print(f"Error verifying credential {credential_id}: {str(e)}")
        return False

def get_contract():
    """
    Get the contract instance
    """
    web3 = Web3(Web3.HTTPProvider(os.getenv('ETHEREUM_NODE_URL')))
    contract_address = os.getenv('CONTRACT_ADDRESS')
    contract = web3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    return contract