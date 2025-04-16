"""
ProveIt - A blockchain-based intellectual property verification system.

This package provides tools for registering and verifying intellectual property
on the Ethereum blockchain.
"""

from .core import ProveIt
from .hash import hash_file, hash_content
from .models import RegistrationResult, VerificationResult, NetworkType
from .certificate import generate_certificate

__version__ = "0.1.0"
__all__ = [
    "ProveIt",
    "hash_file",
    "hash_content",
    "RegistrationResult",
    "VerificationResult",
    "NetworkType",
    "generate_certificate",
]
