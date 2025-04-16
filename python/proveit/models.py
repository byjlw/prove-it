"""
Data models for the ProveIt package.
"""

from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


class NetworkType(Enum):
    """Enum representing different Ethereum networks."""
    MAINNET = "mainnet"
    GOERLI = "goerli"
    POLYGON = "polygon"
    POLYGON_MUMBAI = "polygonMumbai"
    LOCAL = "localhost"


@dataclass
class RegistrationResult:
    """Result of a file registration operation."""
    hash: str
    tx_hash: str
    owner: str
    timestamp: datetime
    network: NetworkType
    block_number: Optional[int] = None
    metadata: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the registration result to a dictionary."""
        return {
            "hash": self.hash,
            "tx_hash": self.tx_hash,
            "owner": self.owner,
            "timestamp": self.timestamp.isoformat(),
            "network": self.network.value,
            "block_number": self.block_number,
            "metadata": self.metadata
        }


@dataclass
class VerificationResult:
    """Result of a file verification operation."""
    hash: str
    is_registered: bool
    owner: Optional[str] = None
    timestamp: Optional[datetime] = None
    metadata: Optional[str] = None
    network: Optional[NetworkType] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the verification result to a dictionary."""
        result = {
            "hash": self.hash,
            "is_registered": self.is_registered
        }
        
        if self.is_registered:
            result.update({
                "owner": self.owner,
                "timestamp": self.timestamp.isoformat() if self.timestamp else None,
                "metadata": self.metadata,
                "network": self.network.value if self.network else None
            })
            
        return result


@dataclass
class Certificate:
    """Certificate of registration."""
    hash: str
    owner: str
    timestamp: datetime
    tx_hash: str
    network: NetworkType
    metadata: Optional[str] = None
    file_name: Optional[str] = None
    
    def save(self, output_path: str) -> str:
        """
        Save the certificate to a PDF file.
        
        Args:
            output_path: Path where the certificate should be saved
            
        Returns:
            The path to the saved certificate
        """
        # This is a placeholder. The actual implementation will be in certificate.py
        return output_path
