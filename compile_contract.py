from solcx import compile_standard, install_solc
import json

# Install specific Solidity version
install_solc("0.8.0")

with open("AIModelMarketPlace.sol", "r") as file:
    contract_source_code = file.read()

# Compile the contract
compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "AIModelMarketPlace.sol": {
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

# Extract the contract data
contract_data = compiled_sol['contracts']['AIModelMarketPlace.sol']['AIModelMarketplace']

# Save the ABI
with open("contract_abi.json", "w") as file:
    json.dump(contract_data["abi"], file)

# Save the bytecode
with open("contract_bytecode.json", "w") as file:
    json.dump(contract_data["evm"]["bytecode"]["object"], file)

print("Contract compiled successfully. ABI and bytecode saved.")