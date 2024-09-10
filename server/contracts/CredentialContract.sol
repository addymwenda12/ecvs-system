// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CredentialContract {
    struct Credential {
        string credentialId;
        bytes32 hashValue;
        bool isVerified;
    }

    mapping(string => Credential) private credentials;

    event CredentialIssued(string credentialId, bytes32 hashValue);
    event CredentialVerified(string credentialId, bool isVerified);

    function issueCredential(string memory credentialId, bytes32 hashValue) public {
        require(credentials[credentialId].hashValue == bytes32(0), "Credential already exists");
        credentials[credentialId] = Credential(credentialId, hashValue, true);
        emit CredentialIssued(credentialId, hashValue);
    }

    function verifyCredential(string memory credentialId) public view returns (bool) {
        Credential memory credential = credentials[credentialId];
        return credential.isVerified;
    }

    function revokeCredential(string memory credentialId) public {
        require(credentials[credentialId].hashValue != bytes32(0), "Credential does not exist");
        credentials[credentialId].isVerified = false;
        emit CredentialVerified(credentialId, false);
    }
}