# ProveIt Integration Tests

This directory contains end-to-end integration tests for the ProveIt system. These tests verify the complete functionality of the system, from wallet and PDF creation to blockchain registration and verification.

## Test Structure

The integration tests are organized as follows:

- `conftest.py`: Contains pytest fixtures for setting up and tearing down the test environment
- `test_end_to_end.py`: Contains the actual test cases

## Test Assets

The tests create and use the following assets:

- A test wallet (Ethereum private key)
- A test PDF document

These assets are stored in the `assets` directory, which is excluded from version control via `.gitignore`.

## Running the Tests

### Prerequisites

Before running the tests, make sure you have the required dependencies installed:

```bash
pip install -e .  # Install the ProveIt package
pip install -r requirements-dev.txt  # Install development dependencies
```

### Running with Hardhat (Local Blockchain)

To run the tests with a local Hardhat node:

1. Start a Hardhat node in a separate terminal:

```bash
npx hardhat node
```

2. Deploy the contract to the local node:

```bash
npx hardhat run scripts/deploy.js --network localhost
```

3. Run the integration tests:

```bash
pytest -xvs tests/integration_tests/
```

### Running with Goerli Testnet

To run the tests with the Goerli testnet:

1. Make sure you have a `.env` file with your Infura API key and a funded wallet:

```
INFURA_API_KEY=your_infura_api_key
PRIVATE_KEY=your_private_key_without_0x_prefix
```

2. Run the integration tests with the `--network` option:

```bash
pytest -xvs tests/integration_tests/ --network goerli
```

### Cleaning Up Test Assets

By default, the tests keep the generated assets (wallet and PDF) for inspection and reuse. To clean up these assets after the tests, use the `--cleanup` option:

```bash
pytest -xvs tests/integration_tests/ --cleanup
```

## Test Cases

The integration tests verify the following functionality:

1. **Wallet Creation**: Tests that a wallet is created if it doesn't exist
2. **PDF Creation**: Tests that a PDF is created if it doesn't exist
3. **Registration and Verification**: Tests the complete registration and verification flow
4. **Certificate Generation**: Tests that a certificate can be generated for a registered file

## CI/CD Integration

These tests are designed to run in a CI/CD pipeline. When running in a CI environment, the tests automatically use the Hardhat network by default.

To run the tests in a GitHub Actions workflow, add the following to your workflow file:

```yaml
- name: Run integration tests
  run: |
    npx hardhat node &
    sleep 5
    npx hardhat run scripts/deploy.js --network localhost
    pytest -xvs tests/integration_tests/
```

## Troubleshooting

### Tests Fail with "No Funds" Error

If you're running the tests with a testnet and get an error about insufficient funds, make sure your wallet has enough testnet tokens. You can get Goerli ETH from a faucet like [goerlifaucet.com](https://goerlifaucet.com/).

### Tests Fail with "Contract Not Deployed" Error

If you're running the tests with a local Hardhat node and get an error about the contract not being deployed, make sure you've deployed the contract to the local node with `npx hardhat run scripts/deploy.js --network localhost`.
