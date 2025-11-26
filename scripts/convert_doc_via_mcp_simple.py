#!/usr/bin/env python3
"""
Script to convert markdown document to PDF using MCP server via JSON-RPC.
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


def convert_doc_to_pdf():
    """Convert document to PDF using MCP server."""
    doc_path = Path(__file__).parent.parent / "docs" / "JAK_DZIALA_SERWER_MCP.md"
    output_path = "output/JAK_DZIALA_SERWER_MCP.pdf"
    
    # Convert paths to container paths
    doc_path_container = f"/app/{doc_path.relative_to(Path(__file__).parent.parent)}"
    output_path_container = f"/app/{output_path}"
    
    print(f"Converting document via MCP server...")
    print(f"  Source: {doc_path}")
    print(f"  Output: {output_path}")
    
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
    convert_doc_to_pdf()

