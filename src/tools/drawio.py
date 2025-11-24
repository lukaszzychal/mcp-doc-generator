"""draw.io cloud architecture diagram generation tools."""

import asyncio
import tempfile
import os
import base64
import aiohttp
from typing import Literal
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_binary_file


async def generate_diagram(
    content: str,
    output_path: str,
    format: Literal["png", "svg", "pdf"] = "png"
) -> str:
    """
    Generate cloud architecture diagram using draw.io.
    Uses draw.io online export API as fallback.
    
    Args:
        content: draw.io XML diagram definition
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message
    """
    try:
        # Ensure output directory exists
        ensure_output_directory(output_path)
        abs_output = Path(output_path).absolute()
        
        # Save draw.io XML file (can be opened with draw.io desktop or online)
        # Note: Direct export API is not publicly available
        
        # For now, save as .drawio file (user can export manually)
        # Future: Implement headless Chrome export or use draw.io desktop CLI
        
        if format == "svg":
            # SVG can be embedded in draw.io XML
            drawio_output = str(abs_output).replace('.svg', '.drawio')
        else:
            drawio_output = str(abs_output).replace(f'.{format}', '.drawio')
        
        # Write draw.io XML
        with open(drawio_output, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Return info message
        return f"✓ draw.io XML saved: {drawio_output}\n" \
               f"   To export to {format.upper()}: Open in draw.io desktop/online and export.\n" \
               f"   Alternative: Use draw.io desktop CLI: drawio -x -f {format} -o {abs_output} {drawio_output}"
    
    except aiohttp.ClientError as e:
        return f"✗ Error: Could not connect to draw.io export API.\n" \
               f"Details: {str(e)}\n" \
               f"Alternative: Install draw.io desktop and use CLI export."
    except Exception as e:
        return f"✗ Error generating cloud diagram: {str(e)}"

