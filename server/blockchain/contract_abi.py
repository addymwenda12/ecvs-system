CONTRACT_ABI = [
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "credentialId",
          "type": "string"
        },
        {
          "internalType": "bytes32",
          "name": "hashValue",
          "type": "bytes32"
        }
      ],
      "name": "issueCredential",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "credentialId",
          "type": "string"
        }
      ],
      "name": "verifyCredential",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
]