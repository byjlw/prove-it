"""
Certificate generation utilities for the ProveIt package.

This module provides functionality for generating certificates of registration.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from .models import Certificate


def generate_certificate(
    hash_value: str,
    owner: str,
    timestamp: datetime,
    tx_hash: str,
    network: str,
    metadata: Optional[str] = None,
    file_name: Optional[str] = None
) -> Certificate:
    """
    Generate a certificate of registration.
    
    Args:
        hash_value: Hash of the registered file
        owner: Address of the owner
        timestamp: Timestamp of registration
        tx_hash: Transaction hash
        network: Network where the hash is registered
        metadata: Optional metadata associated with the hash
        file_name: Optional name of the registered file
        
    Returns:
        Certificate object
    """
    return Certificate(
        hash=hash_value,
        owner=owner,
        timestamp=timestamp,
        tx_hash=tx_hash,
        network=network,
        metadata=metadata,
        file_name=file_name
    )


def _create_certificate_pdf(certificate: Certificate, output_path: str) -> str:
    """
    Create a PDF certificate.
    
    Args:
        certificate: Certificate object
        output_path: Path where the certificate should be saved
        
    Returns:
        The path to the saved certificate
        
    Raises:
        ImportError: If reportlab is not installed
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError(
            "reportlab is required for PDF certificate generation. "
            "Install it with: pip install reportlab"
        )
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["Normal"]
    
    # Create custom style for monospace text
    mono_style = ParagraphStyle(
        "MonoStyle",
        parent=normal_style,
        fontName="Courier",
        fontSize=8,
        leading=10
    )
    
    # Create the content
    content = []
    
    # Title
    content.append(Paragraph("Certificate of Registration", title_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Introduction
    intro_text = (
        "This certificate verifies that the following file hash was registered "
        "on the blockchain at the specified time. This provides evidence of the "
        "file's existence at that point in time."
    )
    content.append(Paragraph(intro_text, normal_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # File information
    content.append(Paragraph("File Information", heading_style))
    content.append(Spacer(1, 0.1 * inch))
    
    # File hash
    content.append(Paragraph("Hash (SHA-256):", normal_style))
    content.append(Paragraph(certificate.hash, mono_style))
    content.append(Spacer(1, 0.1 * inch))
    
    # File name if available
    if certificate.file_name:
        content.append(Paragraph("File Name:", normal_style))
        content.append(Paragraph(certificate.file_name, normal_style))
        content.append(Spacer(1, 0.1 * inch))
    
    # Registration information
    content.append(Paragraph("Registration Details", heading_style))
    content.append(Spacer(1, 0.1 * inch))
    
    # Create a table for registration details
    data = [
        ["Owner Address:", certificate.owner],
        ["Registration Date:", certificate.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")],
        ["Network:", certificate.network.value if hasattr(certificate.network, "value") else str(certificate.network)],
        ["Transaction Hash:", certificate.tx_hash]
    ]
    
    # Add metadata if available
    if certificate.metadata:
        data.append(["Metadata:", certificate.metadata])
    
    # Create the table
    table = Table(data, colWidths=[1.5 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Courier'),
        ('FONTSIZE', (1, 0), (1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    content.append(table)
    content.append(Spacer(1, 0.25 * inch))
    
    # Verification instructions
    content.append(Paragraph("Verification", heading_style))
    content.append(Spacer(1, 0.1 * inch))
    
    verification_text = (
        "To verify this registration, you can use the ProveIt tool to check "
        "the file hash against the blockchain record. Visit https://proveit.example.com "
        "or use the ProveIt command-line tool."
    )
    content.append(Paragraph(verification_text, normal_style))
    content.append(Spacer(1, 0.1 * inch))
    
    verification_command = f"proveit verify --hash {certificate.hash}"
    content.append(Paragraph("Command:", normal_style))
    content.append(Paragraph(verification_command, mono_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Legal disclaimer
    disclaimer_style = ParagraphStyle(
        "Disclaimer",
        parent=normal_style,
        fontSize=8,
        leading=10,
        textColor=colors.gray
    )
    
    disclaimer_text = (
        "DISCLAIMER: This certificate provides evidence of file existence at a specific time. "
        "It does not constitute copyright registration or legal protection. For legal protection, "
        "consult with an intellectual property attorney and consider formal copyright registration "
        "through appropriate government channels."
    )
    content.append(Paragraph(disclaimer_text, disclaimer_style))
    
    # Build the PDF
    doc.build(content)
    
    return output_path


def _create_certificate_json(certificate: Certificate, output_path: str) -> str:
    """
    Create a JSON certificate.
    
    Args:
        certificate: Certificate object
        output_path: Path where the certificate should be saved
        
    Returns:
        The path to the saved certificate
    """
    # Create certificate data
    data = {
        "hash": certificate.hash,
        "owner": certificate.owner,
        "timestamp": certificate.timestamp.isoformat(),
        "tx_hash": certificate.tx_hash,
        "network": certificate.network.value if hasattr(certificate.network, "value") else str(certificate.network)
    }
    
    # Add optional fields if available
    if certificate.metadata:
        data["metadata"] = certificate.metadata
    
    if certificate.file_name:
        data["file_name"] = certificate.file_name
    
    # Write to file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    return output_path


# Monkey patch the Certificate.save method
def _save_certificate(self, output_path: str) -> str:
    """
    Save the certificate to a file.
    
    Args:
        output_path: Path where the certificate should be saved
        
    Returns:
        The path to the saved certificate
    """
    # Determine the file format based on the extension
    output_path = Path(output_path)
    
    if output_path.suffix.lower() == '.pdf':
        return _create_certificate_pdf(self, str(output_path))
    elif output_path.suffix.lower() == '.json':
        return _create_certificate_json(self, str(output_path))
    else:
        # Default to PDF
        if not output_path.suffix:
            output_path = output_path.with_suffix('.pdf')
        return _create_certificate_pdf(self, str(output_path))


# Apply the monkey patch
Certificate.save = _save_certificate
