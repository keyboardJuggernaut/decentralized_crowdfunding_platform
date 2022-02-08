const { assert } = require("console");

// get the considered contract
const Crowdfunding = artifacts.require('Crowdfunding');

contract('CrowdfundingContract', () => {

    let crowdfundingContract = null;
    let accounts = null;

    // execute before each testing block
    before(async () => {

        // reference to the deployed contract
        crowdfundingContract = await Crowdfunding.deployed();

        // load network accounts 
        accounts = await web3.eth.getAccounts();
    })

    it('Deploying and initializing contract properly', async () => {
        
        // check if contract was deployed successfully
        assert(crowdfundingContract.address != '', 'Contract address is empty');

        // check for governor (contract owner)
        const governor = await crowdfundingContract.governor();
        assert(governor == accounts[0], 'Governor is not the address deployed the contract');

        // check for constructor initilized properly
        const totalSupply = await crowdfundingContract.totalSupply();
        assert(totalSupply.toNumber() == 1000, 'Initial supply is different from passed value');

        const minPeriodOfDeadline = await crowdfundingContract.minPeriodOfDeadline();
        assert(minPeriodOfDeadline.toNumber() == 30, 'Minimum period of deadline is different from passed value');

        const tokenName = await crowdfundingContract.name();
        assert(tokenName == 'Crowd Token', 'Token name is not correct');

        const tokenSymbol = await crowdfundingContract.symbol();
        assert(tokenSymbol == 'CWD', 'Token symbol is not correct');
        
    });

    // pretend a campaign
    it('Creating and successfully completing a campaign', async () => {

        // set a future deadline 
        const deadline = Date.now() + 30;

        // create a new campaign
        await crowdfundingContract.newCampaign(accounts[2], 'Animal shelter', 1000, deadline, {from: accounts[1]});

        // get campaign
        let campaign = await crowdfundingContract.campaigns(0);

        // check for campaign attributes
        assert(campaign.beneficiary == accounts[2], 'Beneficiary was not set correctly');
        assert(campaign.description == 'Animal shelter', 'Description was not set correctly');
        assert(campaign.fundingGoal.toNumber() == 1000, 'Funding goal was not set correctly');
        assert(campaign.deadline.toNumber() == deadline, 'Deadline was not set correctly');

        // get beneficiary balance before campaign conclusion
        const beneficiaryBalanceBefore = await web3.eth.getBalance(campaign.beneficiary);

        // contribute to the campaign, reaching the target
        await crowdfundingContract.contribute(0, {from: accounts[0], value: 1000});

        // get campaign
        campaign = await crowdfundingContract.campaigns(0);

        // check for campaign conclusion
        assert(campaign.completed == true, 'State of campaign is not correct');
        assert(campaign.numFunders.toNumber() == 1, 'Number of funders is not correct');
        const numCampaigns = await crowdfundingContract.numCampaigns();
        assert(numCampaigns.toNumber() == 1, 'Number of campaigns is not correct');

        // check for correct issuance of tokens
        const balance = await crowdfundingContract.balanceOf(accounts[0]);
        const totalSupply = await crowdfundingContract.totalSupply();
        assert(balance.toNumber() == (1000 + 1000 + 1000), 'Issuing of tokens did not occur correctly');
        assert(totalSupply.toNumber() == 3000, 'Total supply is not correct');

        // get beneficiary balance after campaign conclusion
        const beneficiaryBalanceAfter = await web3.eth.getBalance(campaign.beneficiary);

        // check for transfer of funded amount to the beneficiary
        assert(beneficiaryBalanceAfter > beneficiaryBalanceBefore, 'Amount funded was not sent to the beneficiary');
    });

    it('Testing token functionalities', async () => {

        // check for initialized variables
        let totalSupply = await crowdfundingContract.totalSupply();
        assert(totalSupply.toNumber() == 3000, 'Initial supply is different from passed value');
        const governor = await crowdfundingContract.governor();
        let balanceOfGovernor = await crowdfundingContract.balanceOf(governor);
        assert(balanceOfGovernor.toNumber() == totalSupply.toNumber(), 'Initial variables are not correct');
        const governorIsMinter = await crowdfundingContract.isMinter(governor);
        assert(governorIsMinter == true, 'Governor is not a minter');

        // check for transfer functionality
        const recipient = accounts[1];
        await crowdfundingContract.transfer(recipient, 200, {from: governor});
        let balanceOfRecipient = await crowdfundingContract.balanceOf(recipient);
        assert(balanceOfRecipient.toNumber() == 200, 'Recipient\'s balance is not correct');
        balanceOfGovernor = await crowdfundingContract.balanceOf(governor);
        assert(balanceOfGovernor.toNumber() == 2800, 'Governor\'s balance is not correct');
        totalSupply = await crowdfundingContract.totalSupply();
        assert(totalSupply.toNumber() == 3000, 'Total supply is different from expected value');

        // check for burn functionality
        await crowdfundingContract.burn(200, {from: recipient});
        balanceOfRecipient = await crowdfundingContract.balanceOf(recipient);
        assert(balanceOfRecipient.toNumber() == 0, 'Burn function did not work properly');
        

        // check for allowance system
        await crowdfundingContract.approve(recipient, 500, {from: governor});
        const allowance = await crowdfundingContract.allowance(governor, recipient);
        assert(allowance.toNumber() == 500, 'Approve function did not work properly');
        await crowdfundingContract.transferFrom(governor, accounts[2], 500, {from: recipient});
        const balanceOfSecondRecipient = await crowdfundingContract.balanceOf(accounts[2]);
        balanceOfGovernor = await crowdfundingContract.balanceOf(governor);
        const allowanceFirstRecipient = await crowdfundingContract.allowance(governor, recipient);
        assert(balanceOfSecondRecipient.toNumber() == 500, 'TansferFrom did not work properly');
        assert(balanceOfGovernor.toNumber() == 2300, 'Governor balance is not empty');
        assert(allowanceFirstRecipient.toNumber() == 0, 'Allowance did not work properly');

    });

    // testing owner handling
    it('Transferring contract ownership', async () => {
        let governor = await crowdfundingContract.governor();
        const newGovernor = accounts[1];

        // propose new governor
        await crowdfundingContract.transferOwnership(newGovernor, {from: governor}); 
        const pendingGovernor = await crowdfundingContract.pendingGovernor();
        assert(newGovernor == pendingGovernor, 'Pending governor was not set properly');

        // accept proposal and change ownership
        await crowdfundingContract.acceptOwnership({from: newGovernor});
        governor = await crowdfundingContract.governor();
        assert(governor == newGovernor, 'New governor was not set correctly');
    });

});