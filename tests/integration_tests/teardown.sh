#!/bin/bash
# Teardown script for integration tests
# This script checks if Hardhat is running and stops it

# Function to check if Hardhat is running
check_hardhat_running() {
    if pgrep -f "hardhat node" > /dev/null; then
        return 0  # Hardhat is running
    else
        return 1  # Hardhat is not running
    fi
}

# Check if Hardhat is running
if check_hardhat_running; then
    echo "Hardhat is running. Stopping all Hardhat processes..."
    pkill -f "hardhat node" || true
    echo "Hardhat processes stopped."
else
    echo "No Hardhat processes found."
fi

echo "Teardown complete!"
