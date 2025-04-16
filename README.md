# ProveIt

A blockchain-based intellectual property verification system that makes it easy to establish who created a document, image, or other intellectual property first.

## Overview

ProveIt allows users to:

1. **Register Intellectual Property**: Hash a file and store the hash on the Ethereum blockchain
2. **Verify Intellectual Property**: Check if a file has been previously registered and by whom
3. **Generate Certificates**: Create verifiable proof of registration

## Features

- **Multiple Interfaces**: Web, CLI, and Python library
- **Blockchain Verification**: Immutable proof of existence on Ethereum
- **Privacy-Focused**: Files are hashed locally; only the hash is stored on-chain
- **Wallet Support**: Compatible with MetaMask, Rabby, and WalletConnect
- **Simple & Efficient**: Optimized for low gas costs and ease of use

## Use Cases

ProveIt can be used to verify the creation date and ownership of various types of intellectual property, such as:

- **Academic Work**: Thesis papers (PDF), research data (CSV, XLSX)
- **Creative Content**: Artwork (PNG, JPG), music compositions (MP3, WAV)
- **Technical Designs**: Engineering drawings (DWG, PNG), architectural plans (PDF)
- **Literary Works**: Manuscripts (DOCX, PDF), screenplays (PDF)
- **Software**: Source code (various formats), compiled applications (EXE, APP)

## Getting Started


### Python Package

```bash
# Install the package
pip install proveit

# Register a file
proveit register path/to/thesis.pdf

# Verify a file
proveit verify path/to/engineering_design.png

# Launch local web interface
proveit serve
```

### Python Library

```python
from proveit import ProveIt

# Initialize
prover = ProveIt()

# Register a file
result = prover.register_file('path/to/thesis.pdf')
print(f"File registered with hash: {result.hash}")
print(f"Transaction: {result.tx_hash}")

# Verify a file
verification = prover.verify_file('path/to/engineering_design.png')
if verification.is_registered:
    print(f"Registered by {verification.owner} on {verification.timestamp}")
else:
    print("File not registered")
```

## Documentation

- [Design Documentation](docs/DESIGN.md)
- [Usage Guide](docs/USAGE.md)
- [Smart Contract](contracts/README.md)

## Legal Disclaimer

This tool provides blockchain-based verification of file existence at a specific time. Registration through ProveIt does not constitute copyright registration or legal protection. It simply provides evidence that you possessed the file at the time of registration.

## License

MIT
