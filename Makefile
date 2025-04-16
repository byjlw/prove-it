# ProveIt Makefile

.PHONY: help setup install test lint format clean docs deploy-local deploy-testnet deploy-mainnet serve

help:
	@echo "ProveIt - Blockchain Intellectual Property Verification"
	@echo ""
	@echo "Usage:"
	@echo "  make setup         Setup the development environment"
	@echo "  make install       Install dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code"
	@echo "  make clean         Clean build artifacts"
	@echo "  make docs          Build documentation"
	@echo "  make deploy-local  Deploy to local network"
	@echo "  make deploy-testnet Deploy to testnet"
	@echo "  make deploy-mainnet Deploy to mainnet"
	@echo "  make serve         Start the web interface"

setup:
	@echo "Setting up development environment..."
	chmod +x setup.sh
	./setup.sh

install:
	@echo "Installing dependencies..."
	pip install -e python/
	pip install -r requirements-dev.txt
	npm install

test:
	@echo "Running tests..."
	python -m unittest discover -s python/proveit/tests
	npx hardhat test

lint:
	@echo "Running linters..."
	flake8 python/
	mypy python/
	npx eslint web/

format:
	@echo "Formatting code..."
	black python/
	isort python/
	npx prettier --write web/

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	rm -rf artifacts/
	rm -rf cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

docs:
	@echo "Building documentation..."
	cd docs && make html

deploy-local:
	@echo "Deploying to local network..."
	npx hardhat run scripts/deploy.js --network localhost

deploy-testnet:
	@echo "Deploying to testnet..."
	npx hardhat run scripts/deploy.js --network goerli

deploy-mainnet:
	@echo "Deploying to mainnet..."
	npx hardhat run scripts/deploy.js --network mainnet

serve:
	@echo "Starting web interface..."
	python -m proveit.cli serve
