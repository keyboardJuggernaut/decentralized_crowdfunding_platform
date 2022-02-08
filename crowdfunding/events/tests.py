from web3 import Web3
import json
import time
from pprint import pprint

# connect to a node
providerUrl = 'https://ropsten.infura.io/v3/77f3d31d6304460580a326ac5bd0a948'
web3 = Web3(Web3.HTTPProvider(providerUrl))

# check for establoshed connection
if web3.isConnected():
    # set default account

    account = web3.eth.account.privateKeyToAccount('0xb2bda96fda35ff35cad5ccd2389539d2572ca96d40af48e2c9da5742a32215fa')

    # reference to deployed crowdfunding smart contract
    contractAddress = '0x86D219D65452b013912B2af7b2E65E903fa3777d'
    contractAbi = json.loads('[{"inputs":[{"internalType":"uint256","name":"_initialSupply","type":"uint256"},{"internalType":"uint256","name":"_minPeriodOfDeadline","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"campaignID","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"timestamp","type":"uint256"}],"name":"GoalReached","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"minter","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"}],"name":"MinterAdded","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"account","type":"address"}],"name":"MinterRemoved","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"campaignID","type":"uint256"},{"indexed":true,"internalType":"address","name":"beneficiary","type":"address"},{"indexed":true,"internalType":"uint256","name":"deadline","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"NewCampaignCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"campaignID","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"amountFunded","type":"uint256"}],"name":"NewContribution","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"NewOwnership","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"NewPendingOwnership","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"OfferReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"refunded","type":"address"},{"indexed":true,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":true,"internalType":"uint256","name":"campaignID","type":"uint256"}],"name":"Refund","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"acceptOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"addMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"campaigns","outputs":[{"internalType":"address payable","name":"beneficiary","type":"address"},{"internalType":"string","name":"description","type":"string"},{"internalType":"uint256","name":"fundingGoal","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint256","name":"numFunders","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"bool","name":"completed","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"campaignID","type":"uint256"}],"name":"checkGoalReached","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_recipient","type":"address"}],"name":"collect","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"campaignID","type":"uint256"}],"name":"contribute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"governor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"isMinter","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minPeriodOfDeadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address payable","name":"_beneficiary","type":"address"},{"internalType":"string","name":"_description","type":"string"},{"internalType":"uint256","name":"_goal","type":"uint256"},{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"newCampaign","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"numCampaigns","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pendingGovernor","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"campaignID","type":"uint256"}],"name":"refund","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"removeMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceMinter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_newGovernor","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]');
    contract = web3.eth.contract(address=contractAddress, abi=contractAbi)

    ## testing routine

    print(f'Initial contributor\'s CWD token balance: {contract.functions.balanceOf(account.address).call()}')

    # create a new campaign
    beneficiaryAddress = account.address
    balance = web3.eth.get_balance(beneficiaryAddress)
    convBalance = web3.fromWei(balance, 'ether')
    print(f'Initial beneficiary\'s balance: {convBalance}\n')
    description = '*** Animal shelter, taking care of abandoned animals ***'
    goal = 10000
    deadline = int(time.time()*1000.0 + contract.functions.minPeriodOfDeadline().call() * 1000.0)

    gasprice = web3.toWei(20, 'gwei')

    tx = contract.functions.newCampaign(beneficiaryAddress, description, goal, deadline).buildTransaction()
    tx.update({
    'from': account.address,
    'nonce': web3.eth.get_transaction_count(account.address),
    'gas': 300000
    })
    signedTx = account.sign_transaction(tx)
    txHash = web3.eth.send_raw_transaction(signedTx.rawTransaction)
    txReceipt = web3.eth.wait_for_transaction_receipt(txHash)
    print('Transaction receipt for newCampaign method:')
    pprint(dict(txReceipt))

    # contribute to the campaign
    campaignID = contract.functions.numCampaigns().call() - 1
    tx = contract.functions.contribute(campaignID).buildTransaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 3000000,
        'value': 5000
    })
    signedTx = account.sign_transaction(tx)
    web3.eth.send_raw_transaction(signedTx.rawTransaction)

    txReceipt = web3.eth.wait_for_transaction_receipt(txHash)
    print('Transaction receipt for first Contribute method:')
    pprint(dict(txReceipt))

    time.sleep(5*60)
    tx = contract.functions.contribute(campaignID).buildTransaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 3000000,
        'value': 5000
    })
    signedTx = account.sign_transaction(tx)
    web3.eth.send_raw_transaction(signedTx.rawTransaction)

    txReceipt = web3.eth.wait_for_transaction_receipt(txHash)
    print('Transaction receipt for second Contribute method:')
    pprint(dict(txReceipt))

    print('\n*************\n')
    print(f'Final contributor\'s CWD token balance {contract.functions.balanceOf(account.address).call()}')
    balance = web3.eth.get_balance(beneficiaryAddress)
    convBalance = web3.fromWei(balance, 'ether')
    print(f'Initial beneficiary\'s balance: {convBalance}')

else:
    print('Connection failed. Test routine failed...')