"""
Routes for the ProveIt web interface.

This module defines the routes for the Flask web application.
"""

import os
import json
import tempfile
from pathlib import Path
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for, jsonify, send_file, current_app
)
from werkzeug.utils import secure_filename

from ..core import ProveIt
from ..models import NetworkType

# Create blueprint
bp = Blueprint('proveit', __name__)


@bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@bp.route('/register')
def register_page():
    """Render the registration page."""
    return render_template('register.html')


@bp.route('/verify')
def verify_page():
    """Render the verification page."""
    return render_template('verify.html')


@bp.route('/api/hash', methods=['POST'])
def hash_file():
    """
    Hash a file.
    
    This endpoint accepts a file upload and returns the hash of the file.
    """
    from ..hash import hash_file as hash_file_func
    
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'Empty file'}), 400
    
    # Save the file to a temporary location
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, secure_filename(file.filename))
    file.save(temp_path)
    
    try:
        # Hash the file
        file_hash = hash_file_func(temp_path)
        
        # Return the hash
        return jsonify({
            'hash': file_hash,
            'filename': file.filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up the temporary file
        os.unlink(temp_path)
        os.rmdir(temp_dir)


@bp.route('/api/register', methods=['POST'])
def register_hash():
    """
    Register a hash on the blockchain.
    
    This endpoint accepts a hash and optional metadata and registers it on the blockchain.
    """
    # Get the request data
    data = request.json
    
    if not data or 'hash' not in data:
        return jsonify({'error': 'No hash provided'}), 400
    
    file_hash = data['hash']
    metadata = data.get('metadata', '')
    network = data.get('network', 'polygon')
    
    try:
        # Initialize ProveIt
        prover = ProveIt(network=network)
        
        # Register the hash
        result = prover.register_hash(file_hash, metadata)
        
        # Return the result
        return jsonify({
            'success': True,
            'hash': result.hash,
            'tx_hash': result.tx_hash,
            'owner': result.owner,
            'timestamp': result.timestamp.isoformat(),
            'network': result.network.value,
            'metadata': result.metadata
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/verify', methods=['POST'])
def verify_hash():
    """
    Verify a hash on the blockchain.
    
    This endpoint accepts a hash and checks if it is registered on the blockchain.
    """
    # Get the request data
    data = request.json
    
    if not data or 'hash' not in data:
        return jsonify({'error': 'No hash provided'}), 400
    
    file_hash = data['hash']
    network = data.get('network', 'polygon')
    
    try:
        # Initialize ProveIt
        prover = ProveIt(network=network)
        
        # Verify the hash
        result = prover.verify_hash(file_hash)
        
        # Return the result
        if result.is_registered:
            return jsonify({
                'is_registered': True,
                'hash': result.hash,
                'owner': result.owner,
                'timestamp': result.timestamp.isoformat(),
                'network': result.network.value,
                'metadata': result.metadata
            })
        else:
            return jsonify({
                'is_registered': False,
                'hash': result.hash
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/certificate', methods=['POST'])
def generate_certificate():
    """
    Generate a certificate for a registered hash.
    
    This endpoint accepts a hash and generates a certificate for it.
    """
    # Get the request data
    data = request.json
    
    if not data or 'hash' not in data:
        return jsonify({'error': 'No hash provided'}), 400
    
    file_hash = data['hash']
    network = data.get('network', 'polygon')
    file_name = data.get('filename')
    format_type = data.get('format', 'pdf')
    
    try:
        # Initialize ProveIt
        prover = ProveIt(network=network)
        
        # Generate the certificate
        certificate = prover.generate_certificate(file_hash)
        
        if file_name:
            certificate.file_name = file_name
        
        # Create a temporary file for the certificate
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, f"certificate.{format_type.lower()}")
        
        # Save the certificate
        certificate.save(temp_path)
        
        # Send the file
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f"proveit_certificate_{file_hash[:8]}.{format_type.lower()}",
            mimetype='application/pdf' if format_type.lower() == 'pdf' else 'application/json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/api/networks', methods=['GET'])
def get_networks():
    """
    Get the list of available networks.
    
    This endpoint returns the list of available networks.
    """
    networks = [network.value for network in NetworkType]
    return jsonify(networks)
