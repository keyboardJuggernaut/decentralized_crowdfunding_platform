//SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

/// @title Crowdfunding platform
/// @author Riccardo Magni
/// @notice This contract was created for educational purpose, its reliability is not guaranteed
/// @dev All functions calls are currently implemented without side effects


import "./ERC20.sol";
import "./Governed.sol";
import "./ERC20Burnable.sol";
import "./SafeMath.sol";

/**
 * @title Crowd Token contract
 * @dev This is the implementation of the ERC20 CWD Token.
 *
 * The token is initially owned by the deployer address that can mint tokens to create the initial
 * distribution. For convenience, an initial supply can be passed in the constructor that will be
 * assigned to the deployer.
 *
 */
contract CWDToken is Governed, ERC20, ERC20Burnable {

    // -- State --
    mapping(address => bool) private _minters;
    mapping(address => uint256) public nonces;

    // -- Events --
    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);
    event Mint(address indexed minter, address indexed to, uint256 indexed amount);

    // -- Modifier --
    modifier onlyMinter() {
        require(isMinter(msg.sender), "Only minter can call");
        _;
    }

    /**
     * @dev Crowd Token Contract Constructor.
     * @param _initialSupply Initial supply of CWD
     */
    constructor(uint256 _initialSupply) ERC20("Crowd Token", "CWD") {
        Governed._initialize(msg.sender);

        // The Governor has the initial supply of tokens
        _mint(msg.sender, _initialSupply);

        // The Governor is the default minter
        _addMinter(msg.sender);

    }


    /**
     * @dev Add a new minter.
     * @param _account Address of the minter
     */
    function addMinter(address _account) external onlyGovernor {
        _addMinter(_account);
    }

    /**
     * @dev Remove a minter.
     * @param _account Address of the minter
     */
    function removeMinter(address _account) external onlyGovernor {
        _removeMinter(_account);
    }

    /**
     * @dev Renounce to be a minter.
     */
    function renounceMinter() external {
        _removeMinter(msg.sender);
    }

    /**
     * @dev Mint new tokens.
     * @param _to Address to send the newly minted tokens
     * @param _amount Amount of tokens to mint
     */
    function mint(address _to, uint256 _amount) external onlyMinter {
        _mint(_to, _amount);
        emit Mint(msg.sender, _to, _amount);
    }

    /**
     * @dev Return if the `_account` is a minter or not.
     * @param _account Address to check
     * @return True if the `_account` is minter
     */
    function isMinter(address _account) public view returns (bool) {
        return _minters[_account];
    }

    /**
     * @dev Add a new minter.
     * @param _account Address of the minter
     */
    function _addMinter(address _account) private {
        _minters[_account] = true;
        emit MinterAdded(_account);
    }

    /**
     * @dev Remove a minter.
     * @param _account Address of the minter
     */
    function _removeMinter(address _account) private {
        _minters[_account] = false;
        emit MinterRemoved(_account);
    }

}

/**
* @title Crowdfunding platform contract
* @dev This is the implementation of the the crowdfunding platform associated with CWD token.
*/

contract CrowdFunding is CWDToken {

    /// @dev Wrappers over Solidity's arithmetic operations with added overflow checks
    using SafeMath for uint;

    // -- State --
    struct Campaign {
        address payable beneficiary;
        string description;
        uint fundingGoal;
        uint deadline;
        uint numFunders;
        uint amount;
        mapping (address => uint) funders;
        bool completed;
    }

    uint public numCampaigns;
    mapping (uint => Campaign) public campaigns;

    uint public minPeriodOfDeadline;

    // -- Events --
    event NewCampaignCreated(uint indexed campaignID, address indexed beneficiary, uint indexed deadline, uint amount);
    event NewContribution(address indexed from, uint indexed campaignID, uint indexed amountFunded);
    event Refund(address indexed refunded, uint indexed amount, uint indexed campaignID);
    event GoalReached(uint indexed campaignID, uint indexed timestamp);
    event OfferReceived(address indexed from, uint indexed amount);

    /**
     * @dev Crowdfunding Contract Constructor.
     * @param _initialSupply Initial supply of CWD
     * @param _minPeriodOfDeadline Minimum period before the deadline of a campaign
     */
    constructor (uint _initialSupply, uint _minPeriodOfDeadline) CWDToken (_initialSupply) {

        // Set minPeriodOfDeadline to discourage creation of fake campaigns only to get token
        minPeriodOfDeadline = _minPeriodOfDeadline;

    }

    /**
     * @dev Add a new campaign
     * @param _beneficiary Beneficiary of the campaign
     * @param _description Description of the campaign
     * @param _goal Target of the campaign to be reached
     * @param _deadline Deadline of the campaign
     */
    function newCampaign(address payable _beneficiary, string memory _description, uint _goal, uint _deadline) public {

        require(_beneficiary != address(0), "Zero address entered!");
        require(_goal > 0, "Goal has to be a positive value");
        require(_deadline > block.timestamp, "Set a future deadline!");
        require(_deadline.sub(block.timestamp) > minPeriodOfDeadline, "Set a future deadline!");

        uint campaignID = numCampaigns++;
        Campaign storage c = campaigns[campaignID];
        c.beneficiary = _beneficiary;
        c.description = _description;
        c.fundingGoal = _goal;
        c.deadline = _deadline;

        emit NewCampaignCreated(campaignID, c.beneficiary, c.deadline, c.amount);
    }

    /**
     * @dev Contribute to a campaign
     * @param campaignID ID associated with the campaign
     */
    function contribute(uint campaignID) public payable {
        Campaign storage c = campaigns[campaignID];
        require(c.completed == false, "Campaign has been already completed!");
        require(c.fundingGoal > 0, "CampaingID is not correct!");
        require(c.deadline > block.timestamp, "Deadline has already been reached!");
        require(msg.value > 0, "Offer value has to be greater than zero");

        if(c.funders[msg.sender] == 0) {
            c.numFunders++;
        }

        c.funders[msg.sender] = c.funders[msg.sender].add(msg.value);
        c.amount = c.amount.add(msg.value);

        emit NewContribution(msg.sender, campaignID, msg.value);

        // Reward funder with CWD tokens
        ERC20._mint(msg.sender, msg.value);

        // Check if goal of the campaign has been reached
        // and if it happened, send amount to its beneficiary
        if(checkGoalReached(campaignID)) {
            uint amount = c.amount;
            c.amount = 0;
            c.completed = true;
            c.beneficiary.transfer(amount);

            // Reward funder who made the campaign reach the goal with further CWD tokens
            ERC20._mint(msg.sender, 1000);
        }
    }

    /**
     * @dev Check if the goal of the campaign has been reached
     * @param campaignID ID associated with the campaign
     * @return True if amount reached is more or equal to the goal of the campaign, otherwise false
     */
    function checkGoalReached(uint campaignID) public returns (bool) {
        Campaign storage c = campaigns[campaignID];
        if (c.completed == true) {
            return true;
        }
        else if (c.amount < c.fundingGoal) {
            return false;
        }
        else
        {
            emit GoalReached(campaignID, block.timestamp);
            return true;
        }

    }

    /**
     * @dev Refund contributors if the campaign has failed
     * @param campaignID ID associated with the campaign
     */
    function refund(uint campaignID) public {

        Campaign storage c = campaigns[campaignID];

        require(c.fundingGoal > 0, "CampaignID is not correct!");
        require(block.timestamp > c.deadline, "Campaign is still in progress!");
        require(c.completed == false, "Campaign has been successfully completed!");
        require(c.funders[msg.sender] > 0, "You have been already refunded or you are not a funder!");

        uint amountFunded = c.funders[msg.sender];
        c.funders[msg.sender] = 0;
        c.amount = c.amount.sub(amountFunded);
        payable(msg.sender).transfer(amountFunded);

        emit Refund(msg.sender, amountFunded, campaignID);
    }

    /**
     * @dev Permit the governor to transfer value stored in the contract
     * @param _recipient Recipient of sent value
     */
    function collect(address payable _recipient) public onlyGovernor {
        _recipient.transfer(address(this).balance);
    }

    /**
     * @dev Fallback function: hold sent value in the contract
     */
    receive() external payable {
        emit OfferReceived(msg.sender, msg.value);
    }

}
