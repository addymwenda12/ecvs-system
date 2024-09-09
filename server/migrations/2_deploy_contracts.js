const CredentialContract = artifacts.require("CredentialContract");

module.exports = function(deployer) {
    deployer.deploy(CredentialContract)
        .then(() => CredentialContract.deployed())
        .then(instance => {
            console.log("Contract deployed at:", instance.address);
        });
};