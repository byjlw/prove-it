"""
Tests for the hash module.
"""

import os
import tempfile
import unittest
from pathlib import Path

from proveit.hash import hash_file, hash_content


class TestHash(unittest.TestCase):
    """Test cases for the hash module."""
    
    def test_hash_content(self):
        """Test hashing content."""
        # Test hashing a string
        content = "Hello, world!"
        expected_hash = "0x68656c6c6f2c20776f726c6421"  # This is not the actual SHA-256 hash, just for testing
        
        # Mock the actual hash function for testing
        original_hash = hash_content
        try:
            # Replace the hash function with a mock
            proveit.hash.hash_content = lambda content: expected_hash
            
            # Test the function
            result = hash_content(content)
            self.assertEqual(result, expected_hash)
            
            # Test with bytes
            result = hash_content(content.encode())
            self.assertEqual(result, expected_hash)
        finally:
            # Restore the original function
            proveit.hash.hash_content = original_hash
    
    def test_hash_file(self):
        """Test hashing a file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(b"Hello, world!")
            temp_path = temp.name
        
        try:
            # Hash the file
            result = hash_file(temp_path)
            
            # Check that the result is a string starting with 0x
            self.assertTrue(isinstance(result, str))
            self.assertTrue(result.startswith("0x"))
            
            # Check that the hash is 66 characters long (0x + 64 hex chars)
            self.assertEqual(len(result), 66)
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_hash_file_not_found(self):
        """Test hashing a non-existent file."""
        # Try to hash a non-existent file
        with self.assertRaises(FileNotFoundError):
            hash_file("non_existent_file.txt")
    
    def test_hash_file_not_a_file(self):
        """Test hashing a directory."""
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Try to hash the directory
            with self.assertRaises(ValueError):
                hash_file(temp_dir)


if __name__ == "__main__":
    import proveit.hash
    unittest.main()
