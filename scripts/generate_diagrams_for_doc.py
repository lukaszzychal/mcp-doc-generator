#!/usr/bin/env python3
"""
Script to generate diagrams for JAK_DZIALA_SERWER_MCP.md document.
Replaces ASCII diagrams with actual graphics.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tools import mermaid, plantuml


async def generate_architecture_diagram():
    """Generate Docker architecture diagram using Mermaid."""
    content = """
flowchart TB
    subgraph Docker["Docker Compose"]
        subgraph PlantUML["plantuml Container"]
            PU[PlantUML Server<br/>Port 8080<br/>Renders diagrams]
        end
        
        subgraph MCPServer["mcp-server Container"]
            MCP[MCP Server<br/>Python<br/>Main MCP Server]
        end
    end
    
    Client[Cursor / Client]
    
    Client -->|stdio<br/>JSON-RPC| MCP
    MCP -->|HTTP| PU
    
    style PlantUML fill:#e1f5ff
    style MCPServer fill:#fff4e1
    style Client fill:#e8f5e9
"""
    output_path = "output/docs_architecture_diagram.png"
    result = await mermaid.generate_flowchart(content, output_path, "png")
    print(result)
    return output_path


async def generate_data_flow_diagram():
    """Generate data flow sequence diagram using Mermaid."""
    content = """
sequenceDiagram
    participant C as Cursor
    participant MCP as MCP Server<br/>(server.py)
    participant PL as plantuml.py
    participant R as _render_plantuml()
    participant PU as PlantUML Server<br/>(Docker)
    participant FM as file_manager.py
    
    C->>MCP: 1. tools/list
    MCP-->>C: 2. Returns list of tools
    
    C->>MCP: 3. tools/call<br/>generate_c4_diagram
    MCP->>PL: 4. generate_c4_diagram()
    PL->>PL: Prepares PlantUML code
    PL->>R: 5. _render_plantuml()
    R->>PU: 6. POST http://plantuml:8080/png
    PU-->>R: 7. Returns PNG image
    R->>FM: 8. write_binary_file()
    FM->>FM: Saves to output/diagram.png
    FM-->>R: File saved
    R-->>PL: Success
    PL-->>MCP: Result message
    MCP-->>C: 8. "✓ C4 context generated..."
"""
    output_path = "output/docs_data_flow_diagram.png"
    result = await mermaid.generate_sequence(content, output_path, "png")
    print(result)
    return output_path


async def generate_request_flow_diagram():
    """Generate request flow diagram using Mermaid flowchart."""
    content = """
flowchart LR
    A[Cursor] -->|JSON-RPC| B[MCP Server]
    B --> C[Tool Module]
    C --> D[External Service<br/>PlantUML/Mermaid/etc.]
    D --> E[File Save]
    E --> F[Response]
    F --> A
    
    style A fill:#e8f5e9
    style B fill:#fff4e1
    style C fill:#e1f5ff
    style D fill:#f3e5f5
    style E fill:#fff9c4
    style F fill:#e8f5e9
"""
    output_path = "output/docs_request_flow_diagram.png"
    result = await mermaid.generate_flowchart(content, output_path, "png")
    print(result)
    return output_path


async def main():
    """Generate all diagrams."""
    print("Generating diagrams for documentation...")
    
    # Ensure output directory exists
    Path("output").mkdir(exist_ok=True)
    
    diagrams = {
        "architecture": await generate_architecture_diagram(),
        "data_flow": await generate_data_flow_diagram(),
        "request_flow": await generate_request_flow_diagram(),
    }
    
    print("\n✓ All diagrams generated successfully!")
    print("\nGenerated diagrams:")
    for name, path in diagrams.items():
        print(f"  - {name}: {path}")
    
    return diagrams


if __name__ == "__main__":
    asyncio.run(main())

