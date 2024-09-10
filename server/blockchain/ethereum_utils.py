from web3 import Web3
from dotenv import load_dotenv
import os
import json
from .contract_abi import CONTRACT_ABI
from tenacity import retry, stop_after_attempt, wait_fixed

load_dotenv()

# Connect to the Ethereum network (Ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

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

# Create contract instance
credential_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def estimate_gas_price():
    """
    Estimate the current gas price
    """
    return w3.eth.gas_price

def issue_credential(credential_id, hash_value):
    contract = w3.eth.contract(address=os.getenv('CONTRACT_ADDRESS'), abi=CONTRACT_ABI)

    from_account = os.getenv('ETHEREUM_ACCOUNT_ADDRESS')
    private_key = os.getenv('ETHEREUM_PRIVATE_KEY')
    
    # Convert the hash_value to bytes32
    hash_bytes32 = w3.to_bytes(hexstr=hash_value)
    
    try:
        # Estimate gas
        gas_estimate = contract.functions.issueCredential(credential_id, hash_bytes32).estimate_gas({'from': from_account})
        
        # Get the nonce
        nonce = w3.eth.get_transaction_count(from_account)
        
        # Build transaction
        transaction = contract.functions.issueCredential(credential_id, hash_bytes32).build_transaction({
            'from': from_account,
            'gas': gas_estimate,
            'nonce': nonce,
            'gasPrice': w3.eth.gas_price,
            'chainId': w3.eth.chain_id
        })
        
        # Sign and send transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt
    except Exception as e:
        raise Exception(f"Error issuing credential {credential_id}: {str(e)}")

def verify_credential(credential_id):
    """
    Verify a credential on the blockchain
    """
    try:
        print(f"Attempting to verify credential with ID: {credential_id}")
        print(f"Contract address: {credential_contract.address}")
        print(f"Connected to network: {w3.net.version}")
        is_verified = credential_contract.functions.verifyCredential(credential_id).call()
        print(f"Verification result for credential {credential_id}: {is_verified}")
        return is_verified
    except Exception as e:
        print(f"Error verifying credential {credential_id}: {str(e)}")
        print(f"Contract ABI: {contract_abi}")
        return False

def get_contract():
    """
    Get the contract instance
    """
    contract_address = os.getenv('CONTRACT_ADDRESS')
    contract = w3.eth.contract(address=contract_address, abi=CONTRACT_ABI)
    return contract

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def issue_credential_with_retry(credential_id, hash_value):
    return issue_credential(credential_id, hash_value)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def verify_credential_with_retry(credential_id):
    return verify_credential(credential_id)

def get_balance(address):
    """
    Get the balance of an Ethereum address
    """
    try:
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        return float(balance_eth)
    except Exception as e:
        print(f"Error getting balance for address {address}: {str(e)}")
        return 0.0

def generate_ethereum_address(private_key=None):
    """
    Generate a new Ethereum address from a private key or create a new one
    """
    if private_key:
        account = w3.eth.account.from_key(private_key)
    else:
        account = w3.eth.account.create()
    return account.address, account._private_key.hex()