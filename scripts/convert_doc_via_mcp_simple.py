#!/usr/bin/env python3
"""
External client script to convert markdown document to PDF using MCP server.

NOTE: This is an external helper script. The actual PDF conversion functionality
is part of the MCP server (export_to_pdf tool). This script is just a test client
that demonstrates how to call the MCP server programmatically.

For production use, call export_to_pdf directly through MCP protocol (e.g., via Cursor).
"""

import json
import subprocess
import sys
from pathlib import Path


def send_mcp_request(method: str, params: dict = None, request_id: int = 1):
    """Send JSON-RPC request to MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    if params:
        request["params"] = params
    
    return json.dumps(request) + "\n"


def convert_doc_to_pdf(doc_path: str = None, output_path: str = None):
    """
    Convert document to PDF using MCP server.
    
    Args:
        doc_path: Path to markdown file (default: docs/JAK_DZIALA_SERWER_MCP.md)
        output_path: Output PDF path (default: output/JAK_DZIALA_SERWER_MCP.pdf)
    """
    if doc_path is None:
        doc_path = Path(__file__).parent.parent / "docs" / "JAK_DZIALA_SERWER_MCP.md"
    else:
        doc_path = Path(doc_path)
    
    if output_path is None:
        output_path = "output/JAK_DZIALA_SERWER_MCP.pdf"
    
    # Use absolute path - user must mount the directory if needed
    # For files in project root, use /app/ prefix
    # For external files, user should mount them or use absolute host path
    if doc_path.is_absolute():
        # Absolute path - assume it's accessible in container or user will mount it
        doc_path_container = str(doc_path)
    else:
        # Relative path - convert to container path
        # Note: User must mount the directory containing the file
        doc_path_container = f"/app/{doc_path.relative_to(Path(__file__).parent.parent)}"
    
    output_path_container = f"/app/{output_path}" if not Path(output_path).is_absolute() else output_path
    
    print(f"Converting document via MCP server...")
    print(f"  Source: {doc_path}")
    print(f"  Output: {output_path}")
    print(f"  Container source: {doc_path_container}")
    print(f"  Container output: {output_path_container}")
    print(f"\n  NOTE: Make sure the source directory is mounted in docker-compose.yml")
    print(f"        if using files outside /app/src or /app/output")
    
    # Prepare commands
    docker_cmd = [
        "docker", "exec", "-i", "mcp-documentation-server",
        "sh", "-c", "cd /app/src && PYTHONPATH=/app/src python server.py"
    ]
    
    # Start process
    process = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Initialize
        init_request = send_mcp_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "convert-script", "version": "1.0"}
        }, 1)
        
        process.stdin.write(init_request)
        process.stdin.flush()
        
        # Read initialize response
        init_response = process.stdout.readline()
        print(f"Initialize response: {init_response[:100]}...")
        
        # Send initialized notification
        initialized = send_mcp_request("notifications/initialized", None, None)
        process.stdin.write(initialized)
        process.stdin.flush()
        
        # Call export_to_pdf tool
        tool_request = send_mcp_request("tools/call", {
            "name": "export_to_pdf",
            "arguments": {
                "markdown_file_path": doc_path_container,
                "output_path": output_path_container,
                "title": "How the MCP Server Works - Step by Step Explanation",
                "author": "MCP Documentation Server",
                "include_toc": True
            }
        }, 2)
        
        process.stdin.write(tool_request)
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        result = json.loads(response)
        
        if "result" in result:
            if "content" in result["result"]:
                for content in result["result"]["content"]:
                    if "text" in content:
                        print(content["text"])
        elif "error" in result:
            print(f"✗ Error: {result['error']}")
            sys.exit(1)
        
        print(f"\n✓ PDF generated successfully!")
        print(f"  Location: {Path(output_path).absolute()}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        process.stdin.close()
        process.wait()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert markdown to PDF via MCP server")
    parser.add_argument("--input", "-i", help="Input markdown file path")
    parser.add_argument("--output", "-o", help="Output PDF file path")
    args = parser.parse_args()
    
    convert_doc_to_pdf(args.input, args.output)

