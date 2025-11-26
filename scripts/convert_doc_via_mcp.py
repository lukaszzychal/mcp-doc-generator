#!/usr/bin/env python3
"""
Script to convert markdown document to PDF using MCP server.
Uses the export_to_pdf tool through MCP protocol.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def convert_doc_to_pdf():
    """Convert document to PDF using MCP server."""
    doc_path = Path(__file__).parent.parent / "docs" / "JAK_DZIALA_SERWER_MCP.md"
    output_path = "output/JAK_DZIALA_SERWER_MCP.pdf"
    
    # Convert paths to container paths
    doc_path_container = f"/app/{doc_path.relative_to(Path(__file__).parent.parent)}"
    output_path_container = f"/app/{output_path}"
    
    print(f"Converting document via MCP server...")
    print(f"  Source: {doc_path}")
    print(f"  Output: {output_path}")
    
    # Use docker exec to run MCP server
    server_params = StdioServerParameters(
        command="docker",
        args=[
            "exec",
            "-i",
            "mcp-documentation-server",
            "sh",
            "-c",
            "cd /app/src && PYTHONPATH=/app/src python server.py"
        ],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            
            # Call export_to_pdf tool
            result = await session.call_tool(
                "export_to_pdf",
                arguments={
                    "markdown_file_path": doc_path_container,
                    "output_path": output_path_container,
                    "title": "How the MCP Server Works - Step by Step Explanation",
                    "author": "MCP Documentation Server",
                    "include_toc": True
                }
            )
            
            # Print result
            if result.content:
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text)
                    else:
                        print(content)
            
            print(f"\n✓ PDF generated successfully!")
            print(f"  Location: {Path(output_path).absolute()}")


if __name__ == "__main__":
    try:
        asyncio.run(convert_doc_to_pdf())
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

