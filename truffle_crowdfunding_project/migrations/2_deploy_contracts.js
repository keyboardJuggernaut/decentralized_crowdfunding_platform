const Crowdfunding = artifacts.require('Crowdfunding.sol');

module.exports = function(deployer) {
    deployer.deploy(Crowdfunding, 1000, 30);
};