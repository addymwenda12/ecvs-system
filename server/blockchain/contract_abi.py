import json
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
contract_path = os.path.join(current_dir, '..', 'build', 'contracts', 'CredentialContract.json')

with open(contract_path) as f:
    contract_json = json.load(f)

CONTRACT_ABI = contract_json['abi']