"""
End-to-end integration tests for the ProveIt system.

These tests verify the complete functionality of the ProveIt system,
from wallet and PDF creation to blockchain registration and verification.
"""

import os
import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

from proveit import ProveIt
from proveit.models import NetworkType
from proveit.hash import hash_file, hash_content

# Import fixtures from conftest.py
# pylint: disable=unused-import
from tests.integration_tests.conftest import (
    assets_dir,
    test_wallet,
    test_pdf,
    network,
    cleanup,
    cleanup_assets
)


class TestEndToEnd:
    """End-to-end integration tests for the ProveIt system."""

    def test_wallet_creation(self, test_wallet):
        """Test that a wallet is created if it doesn't exist."""
        assert test_wallet is not None
        assert "address" in test_wallet
        assert "private_key" in test_wallet
        assert "network" in test_wallet
        
        # Verify the wallet address is valid
        assert test_wallet["address"].startswith("0x")
        assert len(test_wallet["address"]) == 42  # 0x + 40 hex chars
        
        # Verify the private key is valid
        assert test_wallet["private_key"].startswith("0x")
        assert len(test_wallet["private_key"]) == 66  # 0x + 64 hex chars

    def test_pdf_creation(self, test_pdf):
        """Test that a PDF is created if it doesn't exist."""
        assert test_pdf.exists()
        assert test_pdf.is_file()
        assert test_pdf.suffix == ".pdf"
        
        # Verify the file has content
        assert test_pdf.stat().st_size > 0

    def test_registration_and_verification(self, test_wallet, test_pdf, network):
        """
        Test the complete registration and verification flow.
        
        This test:
        1. Initializes the ProveIt system with the test wallet
        2. Registers the test PDF on the blockchain
        3. Verifies the registration was successful
        4. Verifies the PDF can be verified
        5. If the hash is already registered, creates a modified PDF in memory and registers that
        """
        # Skip if we're on a testnet and don't have funds
        if network != "hardhat":
            # TODO: Check if the wallet has funds on the testnet
            # For now, we'll just proceed and let it fail if there are no funds
            pass
        
        # Initialize ProveIt with the test wallet
        prover = ProveIt(
            network=network,
            private_key=test_wallet["private_key"]
        )
        
        # Get the file hash
        file_hash = hash_file(test_pdf)
        
        # Try to register the test PDF
        registration_result = None
        modified_registration_result = None
        
        try:
            # Try to register the original PDF
            registration_result = prover.register_file(test_pdf)
            
            # Verify the registration was successful
            assert registration_result is not None
            assert registration_result.hash is not None
            assert registration_result.tx_hash is not None
            assert registration_result.owner == test_wallet["address"]
            
            # The timestamp should be recent (within the last minute)
            now = datetime.now()
            assert registration_result.timestamp <= now
            assert registration_result.timestamp >= now - timedelta(minutes=1)
            
            # Verify the network is correct
            if network == "hardhat":
                assert registration_result.network == NetworkType.LOCAL
            elif network == "goerli":
                assert registration_result.network == NetworkType.GOERLI
            elif network == "polygon":
                assert registration_result.network == NetworkType.POLYGON
            elif network == "polygonMumbai":
                assert registration_result.network == NetworkType.POLYGON_MUMBAI
                
        except Exception as e:
            # If the hash is already registered, create a modified version
            if "Hash already registered" in str(e):
                print("Hash already registered, creating modified PDF in memory...")
                
                # Read the original PDF
                with open(test_pdf, 'rb') as f:
                    original_content = f.read()
                
                # Create a modified version with a timestamp to ensure a different hash
                import io
                import random
                modified_content = original_content + f"\n<!-- Modified: {datetime.now().isoformat()} Random: {random.randint(1, 1000000)} -->".encode('utf-8')
                
                # Register the modified content
                modified_hash = hash_content(modified_content)
                modified_registration_result = prover.register_content(modified_content)
                
                # Verify the modified registration was successful
                assert modified_registration_result is not None
                assert modified_registration_result.hash is not None
                assert modified_registration_result.tx_hash is not None
                assert modified_registration_result.owner == test_wallet["address"]
                
                # Verify the modified content
                modified_verification_result = prover.verify_content(modified_content)
                assert modified_verification_result.is_registered
                assert modified_verification_result.hash == modified_registration_result.hash
                assert modified_verification_result.owner == modified_registration_result.owner
                assert modified_verification_result.timestamp == modified_registration_result.timestamp
                
                print(f"Successfully registered modified PDF with hash: {modified_registration_result.hash}")
            else:
                # If it's a different error, raise it
                raise
        
        # Now verify the original PDF
        verification_result = prover.verify_file(test_pdf)
        
        # Verify the verification was successful
        assert verification_result is not None
        assert verification_result.is_registered
        
        # If we registered the hash in this test, verify the details match
        if registration_result is not None:
            assert verification_result.hash == registration_result.hash
            assert verification_result.owner == registration_result.owner
            assert verification_result.timestamp == registration_result.timestamp
        else:
            # Otherwise, just verify that the hash matches the file
            assert verification_result.hash == file_hash

    def test_certificate_generation(self, test_wallet, test_pdf, network, assets_dir):
        """
        Test certificate generation.
        
        This test:
        1. Initializes the ProveIt system with the test wallet
        2. Verifies the test PDF
        3. Generates a certificate for the registration
        4. Verifies the certificate contains the correct information
        """
        # Initialize ProveIt with the test wallet
        prover = ProveIt(
            network=network,
            private_key=test_wallet["private_key"]
        )
        
        # Verify the test PDF
        verification_result = prover.verify_file(test_pdf)
        
        # Skip if the PDF is not registered
        if not verification_result.is_registered:
            pytest.skip("PDF not registered, cannot generate certificate")
        
        # Generate a certificate
        certificate = prover.generate_certificate(verification_result.hash)
        
        # Verify the certificate contains the correct information
        assert certificate is not None
        assert certificate.hash == verification_result.hash
        assert certificate.owner == verification_result.owner
        assert certificate.timestamp == verification_result.timestamp
        
        # Save the certificate to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Save the certificate
            certificate_path = certificate.save(temp_path)
            
            # Verify the certificate file exists
            assert Path(certificate_path).exists()
            assert Path(certificate_path).is_file()
            assert Path(certificate_path).stat().st_size > 0
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])
