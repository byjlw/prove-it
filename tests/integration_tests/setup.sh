#!/bin/bash
# Setup script for integration tests
# This script checks if Hardhat is running and the contract is deployed
# If not, it starts Hardhat and deploys the contract

# Function to check if a process is running on a specific port
check_port() {
    if command -v lsof > /dev/null; then
        lsof -i :$1 > /dev/null
        return $?
    elif command -v netstat > /dev/null; then
        netstat -tuln | grep $1 > /dev/null
        return $?
    else
        echo "Neither lsof nor netstat is available. Cannot check if port $1 is in use."
        return 1
    fi
}

# Function to check if the contract is deployed
check_contract_deployed() {
    # Use curl to check if the contract has code at the expected address
    result=$(curl -s -X POST -H "Content-Type: application/json" \
        --data '{"jsonrpc":"2.0","method":"eth_getCode","params":["0x5FbDB2315678afecb367f032d93F642f64180aa3", "latest"],"id":1}' \
        http://localhost:8545)
    
    # Check if the result contains code (more than just "0x")
    if [[ $result == *"\"result\":\"0x\""* || $result == *"\"result\":\"0x0\""* ]]; then
        return 1
    else
        return 0
    fi
}

# Check if Hardhat is already running on port 8545
echo "Checking if Hardhat is running..."
if check_port 8545; then
    echo "Hardhat is already running on port 8545"
else
    echo "Starting Hardhat node..."
    npx hardhat node > hardhat.log 2>&1 &
    echo "Hardhat started with PID: $!"
    echo "Waiting for Hardhat to initialize..."
    sleep 5
fi

# Check if the contract is already deployed
echo "Checking if contract is deployed..."
if check_contract_deployed; then
    echo "Contract is already deployed at 0x5FbDB2315678afecb367f032d93F642f64180aa3"
else
    echo "Deploying contract..."
    npx hardhat run scripts/deploy.js --network localhost
fi

echo "Setup complete!"
