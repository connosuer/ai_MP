from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set the default account (the first account in Ganache)
w3.eth.default_account = w3.eth.accounts[0]

# Load the contract ABI and bytecode
with open("contract_abi.json", "r") as file:
    contract_abi = json.load(file)

with open("contract_bytecode.json", "r") as file:
    contract_bytecode = json.load(file)

# Create contract instance
Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Deploy the contract
tx_hash = Contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")

# Save the contract address
with open("contract_address.txt", "w") as file:
    file.write(tx_receipt.contractAddress)