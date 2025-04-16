"""
Hashing utilities for the ProveIt package.

This module provides functions for hashing files and content using SHA-256.
"""

import hashlib
from pathlib import Path
from typing import Union, BinaryIO


def hash_file(file_path: Union[str, Path], chunk_size: int = 8192) -> str:
    """
    Calculate the SHA-256 hash of a file.
    
    Args:
        file_path: Path to the file to hash
        chunk_size: Size of chunks to read from the file (in bytes)
        
    Returns:
        The hexadecimal representation of the hash, prefixed with '0x'
    
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    hasher = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        return _hash_file_object(f, hasher, chunk_size)


def _hash_file_object(file_obj: BinaryIO, hasher: 'hashlib._Hash', chunk_size: int) -> str:
    """
    Hash a file object using the provided hasher.
    
    Args:
        file_obj: File object to hash
        hasher: Hasher to use
        chunk_size: Size of chunks to read from the file
        
    Returns:
        The hexadecimal representation of the hash, prefixed with '0x'
    """
    while True:
        chunk = file_obj.read(chunk_size)
        if not chunk:
            break
        hasher.update(chunk)
    
    return '0x' + hasher.hexdigest()


def hash_content(content: Union[str, bytes]) -> str:
    """
    Calculate the SHA-256 hash of content.
    
    Args:
        content: Content to hash (string or bytes)
        
    Returns:
        The hexadecimal representation of the hash, prefixed with '0x'
    """
    hasher = hashlib.sha256()
    
    if isinstance(content, str):
        content = content.encode('utf-8')
    
    hasher.update(content)
    return '0x' + hasher.hexdigest()
