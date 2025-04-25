"""
Pytest configuration and fixtures for integration tests.

This module provides fixtures for setting up and tearing down the test environment,
including creating test assets (wallet and PDF) if they don't exist.
"""

import os
import json
import shutil
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Try to import reportlab for PDF generation
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# Try to import web3 for wallet creation
try:
    from web3 import Web3
    from eth_account import Account
    WEB3_AVAILABLE = True
except ImportError:
    WEB3_AVAILABLE = False


# Constants
ASSETS_DIR = Path(__file__).parent / "assets"
TEST_WALLET_PATH = ASSETS_DIR / "test_wallet.json"
TEST_PDF_PATH = ASSETS_DIR / "test_document.pdf"
DEFAULT_NETWORK = "hardhat"


def pytest_addoption(parser):
    """Add command-line options for integration tests."""
    parser.addoption(
        "--network",
        action="store",
        default=DEFAULT_NETWORK,
        help="Network to use for testing: hardhat or goerli"
    )
    parser.addoption(
        "--cleanup",
        action="store_true",
        default=False,
        help="Clean up test assets after tests"
    )


@pytest.fixture(scope="session")
def network(request) -> str:
    """Get the network to use for testing."""
    # Check command line option first
    network = request.config.getoption("--network")
    
    # Fall back to environment variable
    if not network:
        network = os.environ.get("PROVEIT_TEST_NETWORK", DEFAULT_NETWORK)
    
    # Validate network
    if network not in ["hardhat", "goerli", "polygon", "polygonMumbai"]:
        pytest.skip(f"Unsupported network: {network}")
    
    return network


@pytest.fixture(scope="session")
def cleanup(request) -> bool:
    """Determine if test assets should be cleaned up after tests."""
    return request.config.getoption("--cleanup")


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    """Get the directory for test assets."""
    # Create the assets directory if it doesn't exist
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    return ASSETS_DIR


@pytest.fixture(scope="session")
def test_wallet(assets_dir: Path, network: str) -> Dict[str, Any]:
    """
    Create a test wallet if it doesn't exist.
    
    Returns:
        Dict with wallet information (address, private_key)
    """
    if not WEB3_AVAILABLE:
        pytest.skip("web3 and eth_account are required for wallet creation")
    
    wallet_path = TEST_WALLET_PATH
    
    # If wallet exists, load it
    if wallet_path.exists():
        with open(wallet_path, 'r') as f:
            wallet = json.load(f)
        return wallet
    
    # Create a new wallet
    if network == "hardhat":
        # For hardhat, use a deterministic private key
        # This is the first account from the default hardhat mnemonic
        private_key = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
        account = Account.from_key(private_key)
    else:
        # For testnets, create a random account
        account = Account.create()
        private_key = account.key.hex()
    
    # Create wallet info
    wallet = {
        "address": account.address,
        "private_key": private_key,
        "network": network
    }
    
    # Save wallet to file
    with open(wallet_path, 'w') as f:
        json.dump(wallet, f, indent=2)
    
    return wallet


@pytest.fixture(scope="session")
def test_pdf(assets_dir: Path) -> Path:
    """
    Create a test PDF if it doesn't exist.
    
    Returns:
        Path to the test PDF
    """
    if not REPORTLAB_AVAILABLE:
        pytest.skip("reportlab is required for PDF creation")
    
    pdf_path = TEST_PDF_PATH
    
    # If PDF exists, return its path
    if pdf_path.exists():
        return pdf_path
    
    # Create a new PDF
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Add title
    c.drawString(100, 750, "ProveIt Test Document")
    
    # Add content
    c.drawString(100, 700, "This is a test document for the ProveIt system.")
    c.drawString(100, 680, "It contains static content for consistent hashing.")
    c.drawString(100, 660, f"Created for testing on network: {os.environ.get('PROVEIT_TEST_NETWORK', DEFAULT_NETWORK)}")
    c.drawString(100, 640, f"Timestamp: {os.environ.get('PROVEIT_TEST_TIMESTAMP', '2025-04-19')}")
    
    # Add a unique identifier
    c.drawString(100, 100, "Document ID: PROVEIT-TEST-DOC-2025")
    
    c.save()
    
    return pdf_path


@pytest.fixture(scope="session")
def cleanup_assets(cleanup: bool, assets_dir: Path):
    """
    Fixture to clean up test assets after tests if cleanup is enabled.
    
    This fixture is automatically used at the end of the session.
    """
    # This code runs before the tests
    yield
    
    # This code runs after the tests
    if cleanup:
        # Clean up test assets
        if TEST_WALLET_PATH.exists():
            TEST_WALLET_PATH.unlink()
        
        if TEST_PDF_PATH.exists():
            TEST_PDF_PATH.unlink()
