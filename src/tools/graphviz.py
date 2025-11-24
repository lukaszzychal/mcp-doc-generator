"""Graphviz dependency graph generation tools."""

import asyncio
import tempfile
import os
from typing import Literal
from pathlib import Path

from utils.file_manager import ensure_output_directory


async def generate_graph(
    content: str,
    output_path: str,
    format: Literal["png", "svg", "pdf"] = "png",
    layout: Literal["dot", "neato", "fdp", "circo", "twopi"] = "dot"
) -> str:
    """
    Generate dependency graph using Graphviz.
    
    Args:
        content: DOT language graph definition
        output_path: Output file path
        format: Output format
        layout: Graph layout algorithm
        
    Returns:
        Success message
    """
    try:
        # Ensure output directory exists
        ensure_output_directory(output_path)
        
        # Wrap content if needed (add digraph wrapper)
        if not content.strip().startswith("digraph") and not content.strip().startswith("graph"):
            full_content = f"digraph G {{\n{content}\n}}"
        else:
            full_content = content
        
        # Create temporary file for DOT input
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dot', delete=False, encoding='utf-8') as tmp:
            tmp.write(full_content)
            tmp_path = tmp.name
        
        try:
            abs_output = Path(output_path).absolute()
            
            # Run Graphviz
            cmd = [
                layout,  # dot, neato, fdp, circo, or twopi
                f"-T{format}",
                tmp_path,
                "-o", str(abs_output)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                raise Exception(f"Graphviz error: {error_msg}")
            
            return f"✓ Dependency graph generated successfully: {abs_output}"
        
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)
    
    except FileNotFoundError:
        return f"✗ Error: Graphviz ({layout}) not found.\n" \
               f"Install it with: brew install graphviz (macOS) or apt-get install graphviz (Linux)"
    except Exception as e:
        return f"✗ Error generating dependency graph: {str(e)}"

