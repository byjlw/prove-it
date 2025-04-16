# Contributing to ProveIt

Thank you for considering contributing to ProveIt! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and considerate of others.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with the following information:

1. A clear, descriptive title
2. A detailed description of the issue
3. Steps to reproduce the bug
4. Expected behavior
5. Actual behavior
6. Screenshots (if applicable)
7. Environment information (OS, Python version, Node.js version, etc.)

### Suggesting Enhancements

If you have an idea for an enhancement, please create an issue with the following information:

1. A clear, descriptive title
2. A detailed description of the enhancement
3. The motivation behind the enhancement
4. Any potential implementation details

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Create a new Pull Request

## Development Setup

1. Clone the repository
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Project Structure

- `contracts/`: Solidity smart contracts
- `python/`: Python package
  - `proveit/`: Main package code
    - `__init__.py`: Package initialization
    - `core.py`: Core functionality
    - `hash.py`: Hashing utilities
    - `blockchain.py`: Blockchain interaction
    - `certificate.py`: Certificate generation
    - `cli.py`: Command-line interface
    - `web/`: Web interface
    - `tests/`: Tests
- `web/`: Web interface
- `docs/`: Documentation
- `scripts/`: Deployment and utility scripts

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions, classes, and modules
- Keep files under 400 lines of code
- Use meaningful variable and function names

### Solidity

- Follow the Solidity style guide
- Keep contracts simple and focused
- Document functions with NatSpec comments
- Use appropriate visibility modifiers
- Follow security best practices

### JavaScript/TypeScript

- Follow the StandardJS style guide
- Use modern ES6+ features
- Document functions and components
- Use meaningful variable and function names

## Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a pull request
- Aim for high test coverage

### Running Tests

```bash
# Python tests
python -m unittest discover -s python/proveit/tests

# Smart contract tests
npx hardhat test
```

## Documentation

- Update documentation for all new features and changes
- Keep the README.md up to date
- Document API changes in the appropriate files

## Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in the present tense (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable

## Versioning

We use [Semantic Versioning](https://semver.org/) for versioning.

## License

By contributing to ProveIt, you agree that your contributions will be licensed under the project's MIT license.
