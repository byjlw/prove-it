#!/bin/bash
# ProveIt Setup Script

# Exit on error
set -e

# Print commands
set -x

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Please install Node.js and try again."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is required but not installed. Please install npm and try again."
    exit 1
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r python/requirements-dev.txt
pip install -e python/

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

# Compile smart contracts
echo "Compiling smart contracts..."
npx hardhat compile

# Run tests
echo "Running tests..."
python -m unittest discover -s python/proveit/tests
npx hardhat test

# Deploy to local network (optional)
read -p "Do you want to deploy to a local Hardhat network? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Start local Hardhat network in the background
    echo "Starting local Hardhat network..."
    npx hardhat node &
    HARDHAT_PID=$!
    
    # Wait for the network to start
    sleep 5
    
    # Deploy contracts
    echo "Deploying contracts to local network..."
    npx hardhat run scripts/deploy.js --network localhost
    
    # Kill the Hardhat network
    kill $HARDHAT_PID
fi

# Setup complete
echo "Setup complete! You can now use ProveIt."
echo "To start the web interface: proveit serve"
echo "To register a file: proveit register path/to/file.pdf"
echo "To verify a file: proveit verify path/to/file.pdf"
