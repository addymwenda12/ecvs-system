pragma solidity ^0.8.0;

contract CredentialContract {
    mapping(string => bytes32) private credentialHashes;
    mapping(string => string) private credentialIPFSHashes;

    function issueCredential(string memory credentialId, bytes32 hashValue, string memory ipfsHash) public {
        credentialHashes[credentialId] = hashValue;
        credentialIPFSHashes[credentialId] = ipfsHash;
    }

    function verifyCredential(string memory credentialId) public view returns (bool, string memory) {
        return (credentialHashes[credentialId] != bytes32(0), credentialIPFSHashes[credentialId]);
    }
}