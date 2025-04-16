# ProveIt Smart Contracts

This directory contains the Ethereum smart contracts for the ProveIt system.

## Contract Overview

The main contract is `ProveIt.sol`, which provides functionality for:

1. Registering file hashes on the blockchain
2. Verifying if a file hash has been registered
3. Retrieving registration details (owner, timestamp, metadata)

## Contract Design

The contract is intentionally simple to minimize gas costs and attack surface:

- A mapping stores file hashes and their registration details
- Registration details include owner address, timestamp, and optional metadata
- Helper functions provide easy access to specific registration details
- Events are emitted for off-chain tracking and indexing

## Development Setup

### Prerequisites

- [Node.js](https://nodejs.org/) (v16+)
- [Hardhat](https://hardhat.org/)

### Installation

```bash
# Install dependencies
npm install
```

### Compilation

```bash
# Compile contracts
npx hardhat compile
```

## Testing

```bash
# Run tests
npx hardhat test
```

## Deployment

### Local Development

```bash
# Start local Ethereum node
npx hardhat node

# Deploy to local node
npx hardhat run scripts/deploy.js --network localhost
```

### Testnet Deployment

```bash
# Deploy to Goerli testnet
npx hardhat run scripts/deploy.js --network goerli
```

### Production Deployment

```bash
# Deploy to Polygon (recommended for lower gas costs)
npx hardhat run scripts/deploy.js --network polygon

# Or deploy to Ethereum mainnet
npx hardhat run scripts/deploy.js --network mainnet
```

## Contract Addresses

After deployment, contract addresses will be available in the `deployments` directory:

- Goerli (testnet): TBD
- Polygon: TBD
- Mainnet: TBD

## Gas Optimization

The contract has been optimized for gas efficiency:

- Minimal storage usage
- Efficient data structures
- No unnecessary operations

## Security Considerations

The contract follows best practices for security:

- Simple, auditable code
- No external calls
- No complex access control
- No upgradability to minimize attack surface

## License

MIT
