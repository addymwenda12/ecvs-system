pragma solidity ^0.8.0;

contract CredentialContract {
    mapping(string => bytes32) private credentials;

    function issueCredential(string memory credentialId, bytes32 hashValue) public {
        credentials[credentialId] = hashValue;
    }

    function verifyCredential(string memory credentialId) public view returns (bool) {
        return credentials[credentialId] != bytes32(0);
    }
}