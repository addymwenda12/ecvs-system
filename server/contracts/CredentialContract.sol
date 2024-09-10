pragma solidity ^0.8.0;

contract CredentialContract {
    struct Credential {
        string credentialId;
        bytes32 hashValue;
        string ipfsHash;
        bool isVerified;
    }

    mapping(string => Credential) private credentials;

    event CredentialIssued(string credentialId, bytes32 hashValue, string ipfsHash);
    event CredentialVerified(string credentialId, bool isVerified);

    function issueCredential(string memory credentialId, bytes32 hashValue, string memory ipfsHash) public {
        require(credentials[credentialId].hashValue == bytes32(0), "Credential already exists");
        credentials[credentialId] = Credential(credentialId, hashValue, ipfsHash, true);
        emit CredentialIssued(credentialId, hashValue, ipfsHash);
    }

    function verifyCredential(string memory credentialId) public view returns (bool, string memory) {
        Credential memory credential = credentials[credentialId];
        return (credential.isVerified, credential.ipfsHash);
    }

    function revokeCredential(string memory credentialId) public {
        require(credentials[credentialId].hashValue != bytes32(0), "Credential does not exist");
        credentials[credentialId].isVerified = false;
        emit CredentialVerified(credentialId, false);
    }
}