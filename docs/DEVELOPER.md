# ProveIt Developer Guide

This guide is intended for developers who want to contribute to the ProveIt project. It assumes you have experience with coding and git, but may be new to blockchain development.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Project Structure](#project-structure)
3. [Working with Testnets](#working-with-testnets)
4. [Getting Testnet Tokens](#getting-testnet-tokens)
5. [Smart Contract Development](#smart-contract-development)
6. [Testing Your Changes](#testing-your-changes)
7. [Deploying to Testnets](#deploying-to-testnets)
8. [Validating Your Changes](#validating-your-changes)
9. [Contribution Workflow](#contribution-workflow)
10. [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

- Node.js (v16+)
- Python 3.7+
- Git

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/example/proveit.git
   cd proveit
   ```

2. Install dependencies:
   ```bash
   # Install JavaScript dependencies
   npm install
   
   # Install Python dependencies
   pip install -r python/requirements-dev.txt
   pip install -e python/
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your own values (you'll set up testnet private keys later).

## Project Structure

The project is organized into several key components:

- `contracts/`: Solidity smart contracts
- `python/`: Python package
  - `proveit/`: Main package code
    - `blockchain.py`: Blockchain interaction
    - `core.py`: Core functionality
    - `web/`: Web interface
- `scripts/`: Deployment and utility scripts
- `test/`: Smart contract tests

## Working with Testnets

Testnets are separate blockchain networks designed for testing. They work just like the main networks (Ethereum mainnet, Polygon mainnet) but use tokens with no real value.

### Available Testnets

For this project, we support two main testnets:

1. **Goerli**: Ethereum testnet
2. **Mumbai**: Polygon testnet

### Why Use Testnets?

- Free to use (tokens have no real value)
- Identical behavior to mainnet
- Safe environment for testing
- No financial risk

### Setting Up Your Wallet for Testnets

1. Install a wallet like Rabby or MetaMask if you haven't already
2. Add the testnet networks to your wallet:

#### Adding Goerli Testnet to Rabby/MetaMask

1. Open your wallet
2. Go to Settings > Networks > Add Network
3. Enter the following details:
   - Network Name: `Goerli Test Network`
   - RPC URL: `https://goerli.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161`
   - Chain ID: `5`
   - Currency Symbol: `ETH`
   - Block Explorer URL: `https://goerli.etherscan.io`

#### Adding Mumbai Testnet to Rabby/MetaMask

1. Open your wallet
2. Go to Settings > Networks > Add Network
3. Enter the following details:
   - Network Name: `Mumbai Testnet`
   - RPC URL: `https://rpc-mumbai.maticvigil.com`
   - Chain ID: `80001`
   - Currency Symbol: `MATIC`
   - Block Explorer URL: `https://mumbai.polygonscan.com`

## Getting Testnet Tokens

To interact with testnets, you'll need testnet tokens. These have no real value but are necessary for transactions.

### Getting Goerli ETH

1. Go to [goerlifaucet.com](https://goerlifaucet.com/)
2. Connect with your Alchemy account (create one if needed)
3. Enter your wallet address
4. Click "Send Me ETH"

Alternative faucets:
- [faucet.paradigm.xyz](https://faucet.paradigm.xyz/)
- [goerli-faucet.pk910.de](https://goerli-faucet.pk910.de/)

### Getting Mumbai MATIC

1. Go to [faucet.polygon.technology](https://faucet.polygon.technology/)
2. Select "Mumbai"
3. Enter your wallet address
4. Click "Submit"

Alternative faucet:
- [mumbaifaucet.com](https://mumbaifaucet.com/)

### Creating a Development Account

For development, it's best to create a dedicated account:

1. Generate a new account in your wallet
2. Request testnet tokens for this account
3. Export the private key (keep it secure and never use it on mainnet)
4. Add this private key to your `.env` file:
   ```
   PRIVATE_KEY=your_private_key_without_0x_prefix
   ```

## Smart Contract Development

### Contract Structure

The main contract is `ProveIt.sol` in the `contracts/` directory. It handles:
- Registering file hashes
- Verifying file hashes
- Storing metadata

### Modifying the Contract

When modifying the contract:
1. Make your changes to `ProveIt.sol`
2. Compile the contract:
   ```bash
   npx hardhat compile
   ```
3. Run the tests:
   ```bash
   npx hardhat test
   ```

### Solidity Best Practices

- Keep functions simple and focused
- Use events for important state changes
- Add NatSpec comments to document your code
- Be mindful of gas costs
- Follow the checks-effects-interactions pattern

## Testing Your Changes

### Smart Contract Tests

Run the Solidity tests:
```bash
npx hardhat test
```

These tests use the Hardhat network, which is a local Ethereum network for testing.

### Python Package Tests

Run the Python tests:
```bash
python -m unittest discover -s python/proveit/tests
```

### End-to-End Testing

For a complete test of your changes:

1. Start a local Hardhat node:
   ```bash
   npx hardhat node
   ```

2. Deploy the contract to the local node:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```

3. Start the web interface:
   ```bash
   python -m proveit.cli serve
   ```

4. Test the functionality in your browser at `http://localhost:8000`

## Deploying to Testnets

### Deploying to Goerli

1. Ensure your `.env` file has your private key and an Infura API key
2. Run the deployment script:
   ```bash
   npx hardhat run scripts/deploy.js --network goerli
   ```
3. The contract address will be saved in `deployments/goerli/ProveIt.json`

### Deploying to Mumbai

1. Ensure your `.env` file has your private key and an Infura API key
2. Run the deployment script:
   ```bash
   npx hardhat run scripts/deploy.js --network polygonMumbai
   ```
3. The contract address will be saved in `deployments/polygonMumbai/ProveIt.json`

### Verifying the Contract on Etherscan/Polygonscan

After deployment, verify your contract so others can see the source code:

```bash
# For Goerli
npx hardhat verify --network goerli DEPLOYED_CONTRACT_ADDRESS

# For Mumbai
npx hardhat verify --network polygonMumbai DEPLOYED_CONTRACT_ADDRESS
```

## Validating Your Changes

After making changes, it's important to validate them thoroughly:

### 1. Local Validation

1. Run all tests:
   ```bash
   # Smart contract tests
   npx hardhat test
   
   # Python tests
   python -m unittest discover -s python/proveit/tests
   ```

2. Test the web interface locally:
   ```bash
   python -m proveit.cli serve
   ```
   
   Try registering and verifying files to ensure everything works.

### 2. Testnet Validation

1. Deploy to a testnet:
   ```bash
   npx hardhat run scripts/deploy.js --network goerli
   ```

2. Update your `.env` file with the new contract address:
   ```
   GOERLI_CONTRACT_ADDRESS=your_deployed_contract_address
   ```

3. Configure the Python package to use the testnet:
   ```bash
   python -m proveit.cli config --network goerli
   ```

4. Test the full flow:
   - Register a file: `python -m proveit.cli register path/to/file.pdf --network goerli`
   - Verify a file: `python -m proveit.cli verify path/to/file.pdf --network goerli`
   - Check the transaction on [Goerli Etherscan](https://goerli.etherscan.io)

### 3. Web Interface Validation

1. Start the web interface:
   ```bash
   python -m proveit.cli serve
   ```

2. Connect your wallet to the testnet
3. Register and verify files through the UI
4. Check for any console errors or UI issues

## Contribution Workflow

1. **Fork the repository** on GitHub
2. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** and commit them with clear messages:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
4. **Test your changes** thoroughly as described above
5. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Create a pull request** from your fork to the main repository
7. **Describe your changes** in the pull request, including:
   - What problem you're solving
   - How you tested your changes
   - Any testnet deployment addresses you used

## Troubleshooting

### Common Issues

#### "Nonce too high" Error

This happens when your wallet's transaction count doesn't match what the network expects.

**Solution**: Reset your account in MetaMask/Rabby:
1. Go to Settings > Advanced
2. Click "Reset Account"

#### Contract Deployment Fails

**Check**:
1. Do you have enough testnet tokens?
2. Is your private key correct in the `.env` file?
3. Is the Infura API key valid?

#### Transaction Reverted

**Check**:
1. Are you calling the contract correctly?
2. Look at the error message in the transaction details on Etherscan/Polygonscan
3. Try with higher gas limits

### Getting Help

If you're stuck:
1. Check the existing issues on GitHub
2. Look at the contract on Etherscan/Polygonscan
3. Create a new issue with:
   - What you were trying to do
   - The exact error message
   - Steps to reproduce

## Advanced Topics

### Gas Optimization

- Use the `--gas-report` flag with Hardhat tests to see gas usage:
  ```bash
  npx hardhat test --gas-report
  ```

### Contract Upgradeability

The current contract is not upgradeable. If you want to implement upgradeability:
1. Research proxy patterns (Transparent, UUPS)
2. Implement using OpenZeppelin's upgradeable contracts
3. Update deployment scripts

### Multi-Chain Support

To add support for additional EVM-compatible chains:
1. Add the network configuration to `hardhat.config.js`
2. Update the `BlockchainConnector` class in `python/proveit/blockchain.py`
3. Add the network to the web interface

## Security Considerations

When developing blockchain applications:

1. **Never commit private keys** to the repository
2. **Always use testnets** for development
3. **Consider having your contract audited** before mainnet deployment
4. **Test edge cases** thoroughly
5. **Be careful with user input** in the web interface

By following this guide, you should be able to contribute effectively to the ProveIt project, even if you're new to blockchain development.
