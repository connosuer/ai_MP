# AI Model Marketplace

## Overview
AI Model Marketplace is a decentralized platform for buying and selling AI models. It leverages blockchain technology for secure transactions and IPFS for decentralized storage.

**Note:** This project is currently under active development. While core functionalities are in place, some features may be incomplete or subject to change. Still a lacking and a little buggy.

## Features
- List AI models for sale
- Browse available models
- Purchase models using cryptocurrency (ETH)
- Decentralized file storage with IPFS (currently defaulting to local storage)

## Prerequisites
- Python 3.8+
- Flask
- Web3.py
- IPFS (optional, fallback to local storage available)
- Ganache (for local blockchain testing)

## Quick Start
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-model-marketplace.git
   cd ai-model-marketplace
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start Ganache for a local Ethereum blockchain.

4. Compile and deploy the smart contract:
   ```
   python compile_contract.py
   python deploy_contract.py
   ```
   Note: Make sure Ganache is running before deploying the contract.

5. Start the Flask application:
   ```
   python app.py
   ```

6. Open a web browser and navigate to `http://localhost:5000`.

## Current Status
- Basic model listing and viewing implemented
- Local storage fallback when IPFS is unavailable
- Smart contract integration for transactions (testing required)
- User interface for listing and browsing models

