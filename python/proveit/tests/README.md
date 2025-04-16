# ProveIt Tests

This directory contains tests for the ProveIt package.

## Running Tests

You can run the tests using the `unittest` module:

```bash
# Run all tests
python -m unittest discover -s python/proveit/tests

# Run a specific test file
python -m unittest python/proveit/tests/test_hash.py

# Run a specific test case
python -m unittest python/proveit/tests.test_hash.TestHash.test_hash_file
```

## Test Coverage

To run tests with coverage:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover -s python/proveit/tests

# Generate coverage report
coverage report -m
```

## Test Structure

The tests are organized by module:

- `test_hash.py`: Tests for the hash module
- `test_blockchain.py`: Tests for the blockchain module (requires mock blockchain)
- `test_core.py`: Tests for the core functionality
- `test_certificate.py`: Tests for certificate generation

## Writing Tests

When writing tests, follow these guidelines:

1. Each test file should focus on a single module
2. Use descriptive test method names
3. Include docstrings for test classes and methods
4. Use appropriate assertions for the type of test
5. Mock external dependencies (e.g., blockchain interactions)
6. Clean up any temporary files or resources

## Mocking Blockchain Interactions

For tests that involve blockchain interactions, use the `unittest.mock` module to mock the Web3 provider and contract calls. This allows testing without an actual blockchain connection.

Example:

```python
from unittest import mock
from proveit.blockchain import BlockchainConnector

# Mock the Web3 provider
with mock.patch('web3.Web3.HTTPProvider') as mock_provider:
    # Mock the contract call
    with mock.patch.object(BlockchainConnector, 'verify') as mock_verify:
        mock_verify.return_value = {
            'is_registered': True,
            'owner': '0x1234...',
            'timestamp': '2025-04-15T12:00:00Z'
        }
        
        # Test the function
        result = blockchain_connector.verify('0xabcd...')
        self.assertTrue(result['is_registered'])
