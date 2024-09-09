const CredentialContract = artifacts.require("CredentialContract");

module.exports = function (deployer) {
    deployer.deploy(CredentialContract);
};