# ProveIt - Usage Guide

This document provides detailed instructions for using the ProveIt system to register and verify intellectual property on the Ethereum blockchain.

## Table of Contents

1. [Web Interface](#web-interface)
2. [Python Package](#python-package)
3. [Python Library](#python-library)
4. [Smart Contract Direct Interaction](#smart-contract-direct-interaction)
5. [Troubleshooting](#troubleshooting)

## Web Interface

The web interface provides the most user-friendly way to interact with ProveIt.

### Accessing the Web Interface

- **Hosted Version**: Visit [https://proveit.example.com](https://proveit.example.com)
- **Local Version**: After installing the Python package, run `proveit serve` to start a local server

### Registering Intellectual Property

1. Click on the "Register" tab
2. Upload your file using the drag-and-drop area or file browser
3. Wait for the file to be hashed (this happens locally on your device)
4. Connect your wallet by clicking the "Connect Wallet" button
   - Supported wallets: MetaMask, Rabby, WalletConnect
5. (Optional) Add metadata such as title, description, or creation date
6. Click "Register on Blockchain"
7. Confirm the transaction in your wallet
8. Wait for the transaction to be mined
9. Download your registration certificate

### Verifying Intellectual Property

1. Click on the "Verify" tab
2. Upload the file you want to verify
3. Wait for the file to be hashed
4. The system will automatically check if the hash exists on the blockchain
5. View the verification results, including:
   - Registration status
   - Owner address
   - Registration timestamp
   - Any associated metadata
6. (Optional) Download a verification certificate

## Python Package

The Python package provides both a command-line interface and a Python library.

### Installation

```bash
pip install proveit
```

### CLI Commands

#### Configuration

```bash
# Set up your configuration (interactive)
proveit config

# Set specific configuration options
proveit config --network polygon --wallet-type metamask
```

#### Registration

```bash
# Basic registration
proveit register path/to/file.pdf

# With metadata
proveit register path/to/file.pdf --metadata "Title: My Thesis, Author: John Doe"

# Specify network
proveit register path/to/file.pdf --network polygon
```

#### Verification

```bash
# Basic verification
proveit verify path/to/file.pdf

# Specify network
proveit verify path/to/file.pdf --network polygon

# Export verification result
proveit verify path/to/file.pdf --output verification_result.json
```

#### Local Web Interface

```bash
# Start local web server on default port (8000)
proveit serve

# Specify port
proveit serve --port 3000
```

### Configuration File

The CLI uses a configuration file located at `~/.proveit/config.json`:

```json
{
  "network": "polygon",
  "wallet_type": "metamask",
  "gas_price_strategy": "medium",
  "contract_addresses": {
    "mainnet": "0x1234...",
    "polygon": "0xabcd...",
    "goerli": "0x5678..."
  }
}
```

You can edit this file directly or use the `proveit config` command.

## Python Library

The Python library provides programmatic access to ProveIt functionality.

### Basic Usage

```python
from proveit import ProveIt

# Initialize with default settings
prover = ProveIt()

# Register a file
result = prover.register_file('path/to/document.pdf')
print(f"File registered with hash: {result.hash}")
print(f"Transaction: {result.tx_hash}")

# Verify a file
verification = prover.verify_file('path/to/document.pdf')
if verification.is_registered:
    print(f"Registered by {verification.owner} on {verification.timestamp}")
else:
    print("File not registered")
```

### Advanced Usage

```python
from proveit import ProveIt, NetworkType

# Initialize with specific settings
prover = ProveIt(
    network=NetworkType.POLYGON,
    wallet_provider='rabby',
    gas_price_strategy='fast'
)

# Register with metadata
metadata = {
    "title": "Engineering Design",
    "author": "Jane Smith",
    "creation_date": "2025-04-01",
    "description": "Mechanical component design for project X"
}

result = prover.register_file(
    file_path='path/to/design.png',
    metadata=json.dumps(metadata)
)

# Generate certificate
certificate = prover.generate_certificate(result.hash)
certificate.save('registration_certificate.pdf')

# Batch verification
files = ['file1.pdf', 'file2.jpg', 'file3.png']
results = prover.batch_verify_files(files)
for file_path, verification in zip(files, results):
    print(f"{file_path}: {'Registered' if verification.is_registered else 'Not registered'}")
```

### Custom Hashing

```python
from proveit import ProveIt, hash_file, hash_content

# Hash a file manually
file_hash = hash_file('path/to/document.pdf')

# Hash content directly
content = "This is the content I want to hash"
content_hash = hash_content(content)

# Use pre-computed hash
prover = ProveIt()
result = prover.register_hash(file_hash)
```

## Smart Contract Direct Interaction

For advanced users who want to interact directly with the smart contract:

### Contract Addresses

- Mainnet: `0x1234...` (placeholder)
- Polygon: `0xabcd...` (placeholder)
- Goerli (testnet): `0x5678...` (placeholder)

### Contract ABI

```json
[
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "fileHash",
        "type": "bytes32"
      },
      {
        "internalType": "string",
        "name": "metadata",
        "type": "string"
      }
    ],
    "name": "register",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "fileHash",
        "type": "bytes32"
      }
    ],
    "name": "verify",
    "outputs": [
      {
        "components": [
          {
            "internalType": "address",
            "name": "owner",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "metadata",
            "type": "string"
          }
        ],
        "internalType": "struct ProveIt.Registration",
        "name": "",
        "type": "tuple"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
```

### Example with Web3.js

```javascript
const Web3 = require('web3');
const web3 = new Web3(window.ethereum);
const contractABI = [...]; // ABI from above
const contractAddress = '0xabcd...'; // Address for your network

const proveItContract = new web3.eth.Contract(contractABI, contractAddress);

// Register a hash
async function registerHash(hash, metadata) {
  const accounts = await web3.eth.requestAccounts();
  return proveItContract.methods.register(hash, metadata).send({
    from: accounts[0]
  });
}

// Verify a hash
async function verifyHash(hash) {
  return proveItContract.methods.verify(hash).call();
}
```

## Troubleshooting

### Common Issues

#### "Transaction Failed" Error

- **Cause**: Insufficient gas, network congestion, or wallet issues
- **Solution**: Try increasing gas price, wait for network congestion to decrease, or check wallet connection

#### "File Too Large" Warning

- **Cause**: Files over 100MB may cause browser performance issues
- **Solution**: Use the CLI for large files, or consider hashing a compressed version of the file

#### "Hash Already Registered" Message

- **Cause**: The exact file has already been registered on the blockchain
- **Solution**: Verify the file to see who registered it and when

#### Wallet Connection Issues

- **Cause**: Browser permissions, wallet extension problems
- **Solution**: Ensure wallet extension is installed and up to date, check browser permissions

### Getting Help

- **GitHub Issues**: Report bugs or request features on our [GitHub repository](https://github.com/example/proveit)
- **Documentation**: Check the latest documentation at [docs.proveit.example.com](https://docs.proveit.example.com)
- **Community Forum**: Ask questions on our [community forum](https://forum.proveit.example.com)

## Legal Considerations

Remember that ProveIt provides evidence of file existence at a specific time but does not constitute legal copyright registration. For legal protection, consult with an intellectual property attorney and consider formal copyright registration through appropriate government channels.
