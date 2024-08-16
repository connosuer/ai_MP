from solcx import compile_standard, install_solc
import json

# Install specific Solidity version
install_solc("0.8.0")

# Read the Solidity contract file
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

# Extract the contract ABI
abi = compiled_sol["contracts"]["AIModelMarketplace.sol"]["AIModelMarketplace"]["abi"]

# Save the ABI to a file
with open("contract_abi.json", "w") as file:
    json.dump(abi, file)

print("Contract compiled successfully. ABI saved to contract_abi.json")