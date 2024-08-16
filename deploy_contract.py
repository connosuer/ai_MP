from web3 import Web3
from solcx import compile_standard, install_solc
import json

# Install specific Solidity version
install_solc("0.8.0")

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set the default account (the first account in Ganache)
w3.eth.default_account = w3.eth.accounts[0]

# Load the contract source code
with open("AIModelMarketplace.sol", "r") as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "AIModelMarketplace.sol": {
            "content": contract_source_code
        }
    },
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
}, solc_version="0.8.0")

# Get contract binary
contract_bytecode = compiled_sol['contracts']['AIModelMarketplace.sol']['AIModelMarketplace']['evm']['bytecode']['object']

# Get contract ABI
contract_abi = compiled_sol['contracts']['AIModelMarketplace.sol']['AIModelMarketplace']['abi']

# Save the ABI to a file
with open("contract_abi.json", "w") as file:
    json.dump(contract_abi, file)

# Create contract instance
Contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Deploy the contract
tx_hash = Contract.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")

# Save the contract address
with open("contract_address.txt", "w") as file:
    file.write(tx_receipt.contractAddress)