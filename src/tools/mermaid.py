"""Mermaid diagram generation tools."""

import os
import asyncio
import tempfile
import aiohttp
import base64
from typing import Literal
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_file, write_binary_file


# Check if mermaid-cli is available
MMDC_PATH = os.getenv("MMDC_PATH", "mmdc")
# Use mermaid.ink API as fallback
USE_MERMAID_INK_API = os.getenv("USE_MERMAID_INK_API", "true").lower() == "true"


async def generate_flowchart(
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate flowchart using Mermaid.
    
    Args:
        content: Mermaid flowchart code
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message
    """
    # Wrap content if needed
    if not content.strip().startswith("flowchart") and not content.strip().startswith("graph"):
        full_content = f"flowchart TD\n{content}"
    else:
        full_content = content
    
    return await _render_mermaid(full_content, output_path, format, "Flowchart")


async def generate_sequence(
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate sequence diagram using Mermaid.
    
    Args:
        content: Mermaid sequence diagram code
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message
    """
    # Wrap content if needed
    if not content.strip().startswith("sequenceDiagram"):
        full_content = f"sequenceDiagram\n{content}"
    else:
        full_content = content
    
    return await _render_mermaid(full_content, output_path, format, "Sequence diagram")


async def generate_gantt(
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate Gantt chart using Mermaid.
    
    Args:
        content: Mermaid Gantt diagram code
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message
    """
    # Wrap content if needed
    if not content.strip().startswith("gantt"):
        full_content = f"gantt\n{content}"
    else:
        full_content = content
    
    return await _render_mermaid(full_content, output_path, format, "Gantt chart")


async def _render_mermaid(
    content: str,
    output_path: str,
    format: Literal["png", "svg"],
    diagram_name: str
) -> str:
    """
    Render Mermaid diagram using mermaid.ink API (fallback to CLI if needed).
    
    Args:
        content: Mermaid diagram code
        output_path: Output file path
        format: Output format
        diagram_name: Name for logging
        
    Returns:
        Success message
    """
    try:
        # Ensure output directory exists
        ensure_output_directory(output_path)
        abs_output = Path(output_path).absolute()
        
        # Try using mermaid.ink API first (no Puppeteer issues)
        if USE_MERMAID_INK_API:
            try:
                # Encode diagram for URL
                encoded = base64.urlsafe_b64encode(content.encode('utf-8')).decode('ascii')
                
                # mermaid.ink API endpoints
                if format == "svg":
                    url = f"https://mermaid.ink/svg/{encoded}"
                else:  # png
                    url = f"https://mermaid.ink/img/{encoded}"
                
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=30) as response:
                        if response.status == 200:
                            image_data = await response.read()
                            write_binary_file(str(abs_output), image_data)
                            return f"✓ {diagram_name} generated successfully: {abs_output} (via mermaid.ink)"
                        else:
                            # Fallback to CLI if API fails
                            raise Exception(f"mermaid.ink API returned HTTP {response.status}")
            
            except Exception as api_error:
                # Fallback to CLI
                print(f"Warning: mermaid.ink API failed ({api_error}), trying CLI...")
        
        # Fallback: Use mermaid-cli
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            cmd = [
                MMDC_PATH,
                "-i", tmp_path,
                "-o", str(abs_output),
                "-e", format,
                "-b", "transparent"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise Exception(f"Mermaid CLI error: {error_msg}")
            
            return f"✓ {diagram_name} generated successfully: {abs_output}"
        
        finally:
            os.unlink(tmp_path)
    
    except FileNotFoundError:
        return f"✗ Error: mermaid-cli (mmdc) not found and mermaid.ink API unavailable.\n" \
               f"Install it with: npm install -g @mermaid-js/mermaid-cli"
    except Exception as e:
        return f"✗ Error generating {diagram_name}: {str(e)}"

