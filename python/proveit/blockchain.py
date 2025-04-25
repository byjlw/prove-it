"""
Blockchain interaction utilities for the ProveIt package.

This module provides functionality for interacting with the Ethereum blockchain
and the ProveIt smart contract.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union

# Use a more modern approach with web3.py
from web3 import Web3
from web3.exceptions import ContractLogicError

from .models import NetworkType


class BlockchainConnector:
    """
    Connector for interacting with the Ethereum blockchain and the ProveIt contract.
    """
    
    # Default contract addresses (to be updated after deployment)
    DEFAULT_CONTRACT_ADDRESSES = {
        NetworkType.MAINNET.value: "0x1234567890123456789012345678901234567890",  # Placeholder
        NetworkType.GOERLI.value: "0x1234567890123456789012345678901234567890",   # Placeholder
        NetworkType.POLYGON.value: "0x1234567890123456789012345678901234567890",  # Placeholder
        NetworkType.POLYGON_MUMBAI.value: "0x1234567890123456789012345678901234567890",  # Placeholder
        NetworkType.LOCAL.value: "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Default Hardhat deployment address
    }
    
    # Default RPC endpoints
    DEFAULT_RPC_ENDPOINTS = {
        NetworkType.MAINNET.value: "https://mainnet.infura.io/v3/",
        NetworkType.GOERLI.value: "https://goerli.infura.io/v3/",
        NetworkType.POLYGON.value: "https://polygon-mainnet.infura.io/v3/",
        NetworkType.POLYGON_MUMBAI.value: "https://polygon-mumbai.infura.io/v3/",
        NetworkType.LOCAL.value: "http://localhost:8545"
    }
    
    def __init__(
        self, 
        network: Union[str, NetworkType] = NetworkType.POLYGON,
        contract_address: Optional[str] = None,
        rpc_endpoint: Optional[str] = None,
        private_key: Optional[str] = None,
        infura_api_key: Optional[str] = None
    ):
        """
        Initialize the blockchain connector.
        
        Args:
            network: Network to connect to (default: polygon)
            contract_address: Address of the ProveIt contract (default: use predefined address for network)
            rpc_endpoint: RPC endpoint to connect to (default: use predefined endpoint for network)
            private_key: Private key for signing transactions (default: use from environment)
            infura_api_key: Infura API key (default: use from environment)
        """
        # Convert string network to NetworkType if needed
        if isinstance(network, str):
            try:
                # Handle "hardhat" as a special case for LOCAL network
                if network.lower() == "hardhat":
                    self.network = NetworkType.LOCAL
                else:
                    self.network = NetworkType(network)
            except ValueError:
                raise ValueError(f"Invalid network: {network}")
        else:
            self.network = network
        
        # Get Infura API key from environment if not provided
        if not infura_api_key and "INFURA_API_KEY" in os.environ:
            infura_api_key = os.environ["INFURA_API_KEY"]
        
        # Set up RPC endpoint
        if not rpc_endpoint:
            if self.network.value in self.DEFAULT_RPC_ENDPOINTS:
                rpc_endpoint = self.DEFAULT_RPC_ENDPOINTS[self.network.value]
                # Add Infura API key if needed and available
                if infura_api_key and "infura.io" in rpc_endpoint and not rpc_endpoint.endswith("/"):
                    rpc_endpoint += infura_api_key
            else:
                raise ValueError(f"No default RPC endpoint for network: {self.network.value}")
        
        # Connect to the blockchain
        self.web3 = Web3(Web3.HTTPProvider(rpc_endpoint))
        
        # Configure the web3 instance for the network
        if self.network in [NetworkType.GOERLI, NetworkType.POLYGON, NetworkType.POLYGON_MUMBAI]:
            # For PoA networks, we need to handle chain ID and gas price differently
            # This approach works with all versions of web3.py
            pass  # No middleware needed for basic functionality
        
        # Set up contract address
        if not contract_address:
            # Try to load from deployments directory first
            contract_address = self._load_contract_address_from_deployments()
            
            # Fall back to default if not found
            if not contract_address:
                if self.network.value in self.DEFAULT_CONTRACT_ADDRESSES:
                    contract_address = self.DEFAULT_CONTRACT_ADDRESSES[self.network.value]
                else:
                    raise ValueError(f"No default contract address for network: {self.network.value}")
        
        # Load contract ABI
        contract_abi = self._load_contract_abi()
        
        # Initialize contract
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
        
        # Set up account for transactions if private key is provided
        self.account = None
        if private_key:
            if private_key.startswith("0x"):
                private_key = private_key[2:]
            self.account = self.web3.eth.account.from_key(private_key)
        elif "PRIVATE_KEY" in os.environ:
            private_key = os.environ["PRIVATE_KEY"]
            if private_key.startswith("0x"):
                private_key = private_key[2:]
            self.account = self.web3.eth.account.from_key(private_key)
    
    def _load_contract_abi(self) -> list:
        """
        Load the contract ABI from the artifacts directory.
        
        Returns:
            The contract ABI as a list
        """
        # Try to find the ABI in the artifacts directory
        project_root = Path(__file__).parent.parent.parent
        artifact_path = project_root / "artifacts" / "contracts" / "ProveIt.sol" / "ProveIt.json"
        
        if artifact_path.exists():
            with open(artifact_path, 'r') as f:
                artifact = json.load(f)
                return artifact["abi"]
        
        # Fall back to embedded ABI if artifact not found
        return [
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
            },
            {
                "inputs": [
                    {
                        "internalType": "bytes32",
                        "name": "fileHash",
                        "type": "bytes32"
                    }
                ],
                "name": "isRegistered",
                "outputs": [
                    {
                        "internalType": "bool",
                        "name": "",
                        "type": "bool"
                    }
                ],
                "stateMutability": "view",
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
                "name": "getOwner",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
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
                "name": "getTimestamp",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
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
                "name": "getMetadata",
                "outputs": [
                    {
                        "internalType": "string",
                        "name": "",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {
                        "indexed": True,
                        "internalType": "bytes32",
                        "name": "hash",
                        "type": "bytes32"
                    },
                    {
                        "indexed": True,
                        "internalType": "address",
                        "name": "owner",
                        "type": "address"
                    },
                    {
                        "indexed": False,
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    },
                    {
                        "indexed": False,
                        "internalType": "string",
                        "name": "metadata",
                        "type": "string"
                    }
                ],
                "name": "HashRegistered",
                "type": "event"
            }
        ]
    
    def _load_contract_address_from_deployments(self) -> Optional[str]:
        """
        Load the contract address from the deployments directory.
        
        Returns:
            The contract address, or None if not found
        """
        project_root = Path(__file__).parent.parent.parent
        deployment_path = project_root / "deployments" / self.network.value / "ProveIt.json"
        
        if deployment_path.exists():
            try:
                with open(deployment_path, 'r') as f:
                    deployment = json.load(f)
                    return deployment.get("address")
            except (json.JSONDecodeError, KeyError):
                return None
        
        return None
    
    def register(self, file_hash: str, metadata: str = "") -> Dict[str, Any]:
        """
        Register a file hash on the blockchain.
        
        Args:
            file_hash: Hash of the file to register
            metadata: Optional metadata to associate with the hash
            
        Returns:
            Dictionary with transaction details
            
        Raises:
            ValueError: If no account is available for signing transactions
            ContractLogicError: If the hash is already registered
        """
        if not self.account:
            raise ValueError("No account available for signing transactions")
        
        # Ensure the hash is in the correct format
        if not file_hash.startswith("0x"):
            file_hash = "0x" + file_hash
        
        # Convert the hash to bytes32
        file_hash_bytes32 = bytes.fromhex(file_hash[2:])
        
        # Build the transaction
        tx = self.contract.functions.register(file_hash_bytes32, metadata).build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address),
            'gas': 200000,  # Adjust as needed
            'gasPrice': self.web3.eth.gas_price
        })
        
        # Sign and send the transaction
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # Wait for the transaction to be mined
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get the block timestamp
        block = self.web3.eth.get_block(tx_receipt.blockNumber)
        timestamp = datetime.fromtimestamp(block.timestamp)
        
        # Return transaction details
        return {
            "hash": file_hash,
            "tx_hash": tx_receipt.transactionHash.hex(),
            "owner": self.account.address,
            "timestamp": timestamp,
            "block_number": tx_receipt.blockNumber,
            "network": self.network.value,
            "metadata": metadata
        }
    
    def verify(self, file_hash: str) -> Dict[str, Any]:
        """
        Verify if a file hash is registered on the blockchain.
        
        Args:
            file_hash: Hash of the file to verify
            
        Returns:
            Dictionary with verification details
        """
        # Ensure the hash is in the correct format
        if not file_hash.startswith("0x"):
            file_hash = "0x" + file_hash
        
        # Convert the hash to bytes32
        file_hash_bytes32 = bytes.fromhex(file_hash[2:])
        
        # Call the verify function
        try:
            registration = self.contract.functions.verify(file_hash_bytes32).call()
            
            # Check if the hash is registered (owner is not zero address)
            is_registered = registration[0] != "0x0000000000000000000000000000000000000000"
            
            if is_registered:
                # Convert timestamp to datetime
                timestamp = datetime.fromtimestamp(registration[1])
                
                return {
                    "hash": file_hash,
                    "is_registered": True,
                    "owner": registration[0],
                    "timestamp": timestamp,
                    "metadata": registration[2],
                    "network": self.network.value
                }
            else:
                return {
                    "hash": file_hash,
                    "is_registered": False
                }
        except ContractLogicError:
            # Handle contract errors
            return {
                "hash": file_hash,
                "is_registered": False
            }
