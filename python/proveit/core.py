"""
Core functionality for the ProveIt package.

This module provides the main ProveIt class, which is the primary interface for
interacting with the ProveIt system.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

from .blockchain import BlockchainConnector
from .hash import hash_file, hash_content
from .models import RegistrationResult, VerificationResult, Certificate, NetworkType


class ProveIt:
    """
    Main class for interacting with the ProveIt system.
    """
    
    def __init__(
        self,
        network: Union[str, NetworkType] = NetworkType.POLYGON,
        wallet_provider: str = "metamask",
        contract_address: Optional[str] = None,
        rpc_endpoint: Optional[str] = None,
        private_key: Optional[str] = None,
        infura_api_key: Optional[str] = None,
        gas_price_strategy: str = "medium"
    ):
        """
        Initialize the ProveIt instance.
        
        Args:
            network: Network to connect to (default: polygon)
            wallet_provider: Wallet provider to use (default: metamask)
            contract_address: Address of the ProveIt contract (default: use predefined address for network)
            rpc_endpoint: RPC endpoint to connect to (default: use predefined endpoint for network)
            private_key: Private key for signing transactions (default: use from environment)
            infura_api_key: Infura API key (default: use from environment)
            gas_price_strategy: Gas price strategy to use (default: medium)
        """
        self.network = network
        self.wallet_provider = wallet_provider
        self.gas_price_strategy = gas_price_strategy
        
        # Initialize blockchain connector
        self.blockchain = BlockchainConnector(
            network=network,
            contract_address=contract_address,
            rpc_endpoint=rpc_endpoint,
            private_key=private_key,
            infura_api_key=infura_api_key
        )
        
        # Load configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from the config file.
        
        Returns:
            Configuration dictionary
        """
        config_path = Path.home() / ".proveit" / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Return default configuration if file doesn't exist or is invalid
        return {
            "network": self.network.value if isinstance(self.network, NetworkType) else self.network,
            "wallet_type": self.wallet_provider,
            "gas_price_strategy": self.gas_price_strategy
        }
    
    def register_file(self, file_path: Union[str, Path], metadata: str = "") -> RegistrationResult:
        """
        Register a file on the blockchain.
        
        Args:
            file_path: Path to the file to register
            metadata: Optional metadata to associate with the file
            
        Returns:
            RegistrationResult object with registration details
            
        Raises:
            FileNotFoundError: If the file does not exist
            ValueError: If no account is available for signing transactions
        """
        # Calculate the file hash
        file_hash = hash_file(file_path)
        
        # Register the hash on the blockchain
        result = self.blockchain.register(file_hash, metadata)
        
        # Create and return a RegistrationResult object
        return RegistrationResult(
            hash=result["hash"],
            tx_hash=result["tx_hash"],
            owner=result["owner"],
            timestamp=result["timestamp"],
            network=NetworkType(result["network"]),
            block_number=result.get("block_number"),
            metadata=result.get("metadata")
        )
    
    def register_hash(self, file_hash: str, metadata: str = "") -> RegistrationResult:
        """
        Register a pre-computed hash on the blockchain.
        
        Args:
            file_hash: Hash to register
            metadata: Optional metadata to associate with the hash
            
        Returns:
            RegistrationResult object with registration details
            
        Raises:
            ValueError: If no account is available for signing transactions
        """
        # Register the hash on the blockchain
        result = self.blockchain.register(file_hash, metadata)
        
        # Create and return a RegistrationResult object
        return RegistrationResult(
            hash=result["hash"],
            tx_hash=result["tx_hash"],
            owner=result["owner"],
            timestamp=result["timestamp"],
            network=NetworkType(result["network"]),
            block_number=result.get("block_number"),
            metadata=result.get("metadata")
        )
    
    def register_content(self, content: Union[str, bytes], metadata: str = "") -> RegistrationResult:
        """
        Register content on the blockchain.
        
        Args:
            content: Content to register
            metadata: Optional metadata to associate with the content
            
        Returns:
            RegistrationResult object with registration details
            
        Raises:
            ValueError: If no account is available for signing transactions
        """
        # Calculate the content hash
        content_hash = hash_content(content)
        
        # Register the hash on the blockchain
        return self.register_hash(content_hash, metadata)
    
    def verify_file(self, file_path: Union[str, Path]) -> VerificationResult:
        """
        Verify if a file is registered on the blockchain.
        
        Args:
            file_path: Path to the file to verify
            
        Returns:
            VerificationResult object with verification details
            
        Raises:
            FileNotFoundError: If the file does not exist
        """
        # Calculate the file hash
        file_hash = hash_file(file_path)
        
        # Verify the hash on the blockchain
        return self.verify_hash(file_hash)
    
    def verify_hash(self, file_hash: str) -> VerificationResult:
        """
        Verify if a hash is registered on the blockchain.
        
        Args:
            file_hash: Hash to verify
            
        Returns:
            VerificationResult object with verification details
        """
        # Verify the hash on the blockchain
        result = self.blockchain.verify(file_hash)
        
        # Create and return a VerificationResult object
        if result["is_registered"]:
            return VerificationResult(
                hash=result["hash"],
                is_registered=True,
                owner=result["owner"],
                timestamp=result["timestamp"],
                metadata=result.get("metadata"),
                network=NetworkType(result["network"]) if "network" in result else None
            )
        else:
            return VerificationResult(
                hash=result["hash"],
                is_registered=False
            )
    
    def verify_content(self, content: Union[str, bytes]) -> VerificationResult:
        """
        Verify if content is registered on the blockchain.
        
        Args:
            content: Content to verify
            
        Returns:
            VerificationResult object with verification details
        """
        # Calculate the content hash
        content_hash = hash_content(content)
        
        # Verify the hash on the blockchain
        return self.verify_hash(content_hash)
    
    def batch_verify_files(self, file_paths: List[Union[str, Path]]) -> List[VerificationResult]:
        """
        Verify multiple files in batch.
        
        Args:
            file_paths: List of paths to files to verify
            
        Returns:
            List of VerificationResult objects with verification details
        """
        results = []
        
        for file_path in file_paths:
            try:
                result = self.verify_file(file_path)
                results.append(result)
            except FileNotFoundError:
                # Create a "not found" result
                results.append(VerificationResult(
                    hash="",
                    is_registered=False
                ))
        
        return results
    
    def generate_certificate(self, registration_result: Union[RegistrationResult, str]) -> Certificate:
        """
        Generate a certificate for a registration.
        
        Args:
            registration_result: RegistrationResult object or hash of a registered file
            
        Returns:
            Certificate object
            
        Raises:
            ValueError: If the hash is not registered
        """
        # If a hash is provided, verify it first
        if isinstance(registration_result, str):
            verification = self.verify_hash(registration_result)
            
            if not verification.is_registered:
                raise ValueError(f"Hash not registered: {registration_result}")
            
            # Create a certificate from the verification result
            return Certificate(
                hash=verification.hash,
                owner=verification.owner,
                timestamp=verification.timestamp,
                tx_hash="",  # Transaction hash not available from verification
                network=verification.network,
                metadata=verification.metadata
            )
        else:
            # Create a certificate from the registration result
            return Certificate(
                hash=registration_result.hash,
                owner=registration_result.owner,
                timestamp=registration_result.timestamp,
                tx_hash=registration_result.tx_hash,
                network=registration_result.network,
                metadata=registration_result.metadata
            )
