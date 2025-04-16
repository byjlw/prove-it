"""
Command-line interface for the ProveIt package.

This module provides a command-line interface for interacting with the ProveIt system.
"""

import os
import sys
import json
import click
from pathlib import Path
from datetime import datetime
from typing import Optional

from .core import ProveIt
from .models import NetworkType
from .hash import hash_file


@click.group()
@click.version_option()
def main():
    """
    ProveIt - A blockchain-based intellectual property verification system.
    
    This tool allows you to register and verify intellectual property on the Ethereum blockchain.
    """
    pass


@main.command()
@click.argument('file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('--metadata', '-m', help='Optional metadata to associate with the file')
@click.option('--network', '-n', help='Network to use (mainnet, goerli, polygon, polygonMumbai, localhost)')
@click.option('--output', '-o', help='Output file for the registration certificate')
def register(file_path: str, metadata: Optional[str] = None, network: Optional[str] = None, output: Optional[str] = None):
    """
    Register a file on the blockchain.
    
    This command calculates the hash of the specified file and registers it on the blockchain.
    """
    try:
        # Initialize ProveIt with the specified network if provided
        prover = ProveIt(network=network) if network else ProveIt()
        
        # Register the file
        click.echo(f"Registering file: {file_path}")
        result = prover.register_file(file_path, metadata or "")
        
        # Display the result
        click.echo(f"File registered successfully!")
        click.echo(f"Hash: {result.hash}")
        click.echo(f"Transaction: {result.tx_hash}")
        click.echo(f"Owner: {result.owner}")
        click.echo(f"Timestamp: {result.timestamp.isoformat()}")
        click.echo(f"Network: {result.network.value}")
        
        # Generate a certificate if requested
        if output:
            certificate = prover.generate_certificate(result)
            certificate.file_name = Path(file_path).name
            certificate_path = certificate.save(output)
            click.echo(f"Certificate saved to: {certificate_path}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.argument('file_path', type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.option('--network', '-n', help='Network to use (mainnet, goerli, polygon, polygonMumbai, localhost)')
@click.option('--output', '-o', help='Output file for the verification result')
def verify(file_path: str, network: Optional[str] = None, output: Optional[str] = None):
    """
    Verify if a file is registered on the blockchain.
    
    This command calculates the hash of the specified file and checks if it is registered on the blockchain.
    """
    try:
        # Initialize ProveIt with the specified network if provided
        prover = ProveIt(network=network) if network else ProveIt()
        
        # Verify the file
        click.echo(f"Verifying file: {file_path}")
        result = prover.verify_file(file_path)
        
        # Display the result
        if result.is_registered:
            click.echo(f"File is registered!")
            click.echo(f"Hash: {result.hash}")
            click.echo(f"Owner: {result.owner}")
            click.echo(f"Timestamp: {result.timestamp.isoformat()}")
            click.echo(f"Network: {result.network.value}")
            if result.metadata:
                click.echo(f"Metadata: {result.metadata}")
            
            # Generate a certificate if requested
            if output:
                certificate = prover.generate_certificate(result.hash)
                certificate.file_name = Path(file_path).name
                certificate_path = certificate.save(output)
                click.echo(f"Certificate saved to: {certificate_path}")
        else:
            click.echo(f"File is not registered.")
            click.echo(f"Hash: {result.hash}")
        
        # Save the result to a file if requested
        if output and not output.endswith(('.pdf', '.json')):
            with open(output, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            click.echo(f"Verification result saved to: {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--hash', '-h', required=True, help='Hash to verify')
@click.option('--network', '-n', help='Network to use (mainnet, goerli, polygon, polygonMumbai, localhost)')
@click.option('--output', '-o', help='Output file for the verification result')
def verify_hash(hash: str, network: Optional[str] = None, output: Optional[str] = None):
    """
    Verify if a hash is registered on the blockchain.
    
    This command checks if the specified hash is registered on the blockchain.
    """
    try:
        # Initialize ProveIt with the specified network if provided
        prover = ProveIt(network=network) if network else ProveIt()
        
        # Verify the hash
        click.echo(f"Verifying hash: {hash}")
        result = prover.verify_hash(hash)
        
        # Display the result
        if result.is_registered:
            click.echo(f"Hash is registered!")
            click.echo(f"Owner: {result.owner}")
            click.echo(f"Timestamp: {result.timestamp.isoformat()}")
            click.echo(f"Network: {result.network.value}")
            if result.metadata:
                click.echo(f"Metadata: {result.metadata}")
            
            # Generate a certificate if requested
            if output and (output.endswith('.pdf') or output.endswith('.json')):
                certificate = prover.generate_certificate(hash)
                certificate_path = certificate.save(output)
                click.echo(f"Certificate saved to: {certificate_path}")
        else:
            click.echo(f"Hash is not registered.")
        
        # Save the result to a file if requested
        if output and not output.endswith(('.pdf', '.json')):
            with open(output, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
            click.echo(f"Verification result saved to: {output}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--port', '-p', default=8000, help='Port to run the server on')
@click.option('--host', '-h', default='127.0.0.1', help='Host to run the server on')
def serve(port: int, host: str):
    """
    Start a local web server for the ProveIt web interface.
    
    This command starts a Flask server that serves the ProveIt web interface.
    """
    try:
        from .web import create_app
        
        click.echo(f"Starting ProveIt web server on http://{host}:{port}")
        app = create_app()
        app.run(host=host, port=port)
        
    except ImportError:
        click.echo("Error: Flask is required for the web interface. Install it with: pip install flask", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option('--network', help='Default network to use (mainnet, goerli, polygon, polygonMumbai, localhost)')
@click.option('--wallet-type', help='Default wallet type to use (metamask, rabby, walletconnect)')
@click.option('--gas-price-strategy', help='Default gas price strategy to use (slow, medium, fast)')
def config(network: Optional[str] = None, wallet_type: Optional[str] = None, gas_price_strategy: Optional[str] = None):
    """
    Configure ProveIt settings.
    
    This command allows you to configure default settings for ProveIt.
    """
    # Get the config directory
    config_dir = Path.home() / ".proveit"
    config_file = config_dir / "config.json"
    
    # Create the config directory if it doesn't exist
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
    
    # Load existing config if it exists
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            config = {}
    else:
        config = {}
    
    # Update config with provided values
    if network:
        try:
            # Validate network
            NetworkType(network)
            config["network"] = network
            click.echo(f"Default network set to: {network}")
        except ValueError:
            click.echo(f"Error: Invalid network: {network}", err=True)
            click.echo("Valid networks: mainnet, goerli, polygon, polygonMumbai, localhost")
            sys.exit(1)
    
    if wallet_type:
        valid_wallet_types = ["metamask", "rabby", "walletconnect"]
        if wallet_type.lower() in valid_wallet_types:
            config["wallet_type"] = wallet_type.lower()
            click.echo(f"Default wallet type set to: {wallet_type.lower()}")
        else:
            click.echo(f"Error: Invalid wallet type: {wallet_type}", err=True)
            click.echo(f"Valid wallet types: {', '.join(valid_wallet_types)}")
            sys.exit(1)
    
    if gas_price_strategy:
        valid_strategies = ["slow", "medium", "fast"]
        if gas_price_strategy.lower() in valid_strategies:
            config["gas_price_strategy"] = gas_price_strategy.lower()
            click.echo(f"Default gas price strategy set to: {gas_price_strategy.lower()}")
        else:
            click.echo(f"Error: Invalid gas price strategy: {gas_price_strategy}", err=True)
            click.echo(f"Valid strategies: {', '.join(valid_strategies)}")
            sys.exit(1)
    
    # If no options were provided, display current config
    if not any([network, wallet_type, gas_price_strategy]):
        click.echo("Current configuration:")
        for key, value in config.items():
            click.echo(f"{key}: {value}")
        
        # If no config exists, show help
        if not config:
            click.echo("No configuration found. Use --network, --wallet-type, or --gas-price-strategy to set defaults.")
    
    # Save the config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)


if __name__ == '__main__':
    main()
