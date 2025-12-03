#!/usr/bin/env python3
"""
MCP Documentation Server
Generates technical documentation with diagrams (PlantUML, Mermaid, Graphviz, draw.io)
and exports to PDF/DOCX with full Polish language support.
"""

import asyncio
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import all tool modules
from tools import plantuml, mermaid, graphviz, drawio, export as export_tools, openai_images

# Create MCP server instance
app = Server("mcp-documentation-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available documentation generation tools."""
    tools = []
    
    # PlantUML tools
    tools.extend([
        Tool(
            name="generate_c4_diagram",
            description="Generate C4 architecture diagram (Context/Container/Component/Code). "
                       "Supports Polish language. Output: PNG or SVG file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "diagram_type": {
                        "type": "string",
                        "enum": ["context", "container", "component", "code"],
                        "description": "Type of C4 diagram"
                    },
                    "content": {
                        "type": "string",
                        "description": "PlantUML/C4 diagram code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path (e.g., 'output/architecture.png')"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png",
                        "description": "Output format"
                    }
                },
                "required": ["diagram_type", "content", "output_path"]
            }
        ),
        Tool(
            name="generate_uml_diagram",
            description="Generate UML diagram (class, component, deployment, package, activity). "
                       "Supports Polish language.",
            inputSchema={
                "type": "object",
                "properties": {
                    "diagram_type": {
                        "type": "string",
                        "enum": ["class", "component", "deployment", "package", "activity", "usecase"],
                        "description": "Type of UML diagram"
                    },
                    "content": {
                        "type": "string",
                        "description": "PlantUML diagram code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png"
                    }
                },
                "required": ["diagram_type", "content", "output_path"]
            }
        ),
        Tool(
            name="generate_sequence_diagram",
            description="Generate sequence diagram using PlantUML. Shows interactions between components.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "PlantUML sequence diagram code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png"
                    }
                },
                "required": ["content", "output_path"]
            }
        ),
    ])
    
    # Mermaid tools
    tools.extend([
        Tool(
            name="generate_flowchart",
            description="Generate flowchart using Mermaid. Perfect for process flows.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Mermaid flowchart code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png"
                    }
                },
                "required": ["content", "output_path"]
            }
        ),
        Tool(
            name="generate_mermaid_sequence",
            description="Generate sequence diagram using Mermaid. Alternative to PlantUML sequences.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Mermaid sequence diagram code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png"
                    }
                },
                "required": ["content", "output_path"]
            }
        ),
        Tool(
            name="generate_gantt",
            description="Generate Gantt chart using Mermaid. Perfect for project timelines.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "Mermaid Gantt diagram code"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg"],
                        "default": "png"
                    }
                },
                "required": ["content", "output_path"]
            }
        ),
    ])
    
    # Graphviz tools
    tools.append(
        Tool(
            name="generate_dependency_graph",
            description="Generate dependency graph using Graphviz. Perfect for microservices dependencies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "DOT language graph definition"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg", "pdf"],
                        "default": "png"
                    },
                    "layout": {
                        "type": "string",
                        "enum": ["dot", "neato", "fdp", "circo", "twopi"],
                        "default": "dot",
                        "description": "Graph layout algorithm"
                    }
                },
                "required": ["content", "output_path"]
            }
        )
    )
    
    # draw.io tools
    tools.append(
        Tool(
            name="generate_cloud_diagram",
            description="Generate cloud architecture diagram with AWS/Azure/GCP icons using draw.io.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "draw.io XML diagram definition"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["png", "svg", "pdf"],
                        "default": "png"
                    }
                },
                "required": ["content", "output_path"]
            }
        )
    )
    
    # Export tools
    tools.extend([
        Tool(
            name="export_to_pdf",
            description="Convert Markdown to PDF using Pandoc. Accepts either markdown content string or file path. Full Polish language support.",
            inputSchema={
                "type": "object",
                "properties": {
                    "markdown_content": {
                        "type": "string",
                        "description": "Markdown content to convert (optional if markdown_file_path is provided)"
                    },
                    "markdown_file_path": {
                        "type": "string",
                        "description": "Path to markdown file to convert (optional if markdown_content is provided)"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output PDF file path"
                    },
                    "title": {
                        "type": "string",
                        "description": "Document title (optional)"
                    },
                    "author": {
                        "type": "string",
                        "description": "Document author (optional)"
                    },
                    "include_toc": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include table of contents"
                    }
                },
                "required": ["output_path"]
            }
        ),
        Tool(
            name="export_to_docx",
            description="Convert Markdown to DOCX (Word) using Pandoc. Full Polish language support.",
            inputSchema={
                "type": "object",
                "properties": {
                    "markdown_content": {
                        "type": "string",
                        "description": "Markdown content to convert"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output DOCX file path"
                    },
                    "title": {
                        "type": "string",
                        "description": "Document title (optional)"
                    },
                    "author": {
                        "type": "string",
                        "description": "Document author (optional)"
                    }
                },
                "required": ["markdown_content", "output_path"]
            }
        ),
        Tool(
            name="create_document_from_template",
            description="Generate document from template (ADR, API Spec, C4, Microservices Overview).",
            inputSchema={
                "type": "object",
                "properties": {
                    "template_type": {
                        "type": "string",
                        "enum": ["adr", "api_spec", "c4_context", "microservices_overview"],
                        "description": "Type of template to use"
                    },
                    "variables": {
                        "type": "object",
                        "description": "Variables to fill in the template",
                        "additionalProperties": {"type": "string"}
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path (markdown)"
                    }
                },
                "required": ["template_type", "variables", "output_path"]
            }
        ),
    ])
    
    # OpenAI image generation tools
    tools.extend([
        Tool(
            name="generate_image_openai",
            description="Generate image using OpenAI DALL-E 3. Supports Polish prompts. "
                       "Requires OPENAI_API_KEY environment variable. "
                       "If API key is not configured, returns helpful error message.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Image description prompt (supports Polish, e.g., 'Kolorowy zając w stylu kreskówki')"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path (e.g., 'output/rabbit.png')"
                    },
                    "size": {
                        "type": "string",
                        "enum": ["1024x1024", "1024x1792", "1792x1024"],
                        "default": "1024x1024",
                        "description": "Image size"
                    },
                    "quality": {
                        "type": "string",
                        "enum": ["standard", "hd"],
                        "default": "standard",
                        "description": "Image quality (standard or hd)"
                    }
                },
                "required": ["prompt", "output_path"]
            }
        ),
        Tool(
            name="generate_icon_openai",
            description="Generate icon using OpenAI DALL-E 3. Optimized for icon generation. "
                       "Requires OPENAI_API_KEY environment variable.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Icon description (e.g., 'server icon', 'database icon')"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "style": {
                        "type": "string",
                        "default": "flat design, minimalist, simple",
                        "description": "Additional style description"
                    }
                },
                "required": ["prompt", "output_path"]
            }
        ),
        Tool(
            name="generate_illustration_openai",
            description="Generate illustration using OpenAI DALL-E 3. Optimized for concept illustrations. "
                       "Requires OPENAI_API_KEY environment variable.",
            inputSchema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Illustration description (e.g., 'Architecture diagram of microservices')"
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Output file path"
                    },
                    "style": {
                        "type": "string",
                        "default": "professional, technical illustration",
                        "description": "Additional style description"
                    }
                },
                "required": ["prompt", "output_path"]
            }
        ),
    ])
    
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute the requested tool."""
    try:
        # PlantUML tools
        if name == "generate_c4_diagram":
            result = await plantuml.generate_c4_diagram(
                arguments["diagram_type"],
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        elif name == "generate_uml_diagram":
            result = await plantuml.generate_uml_diagram(
                arguments["diagram_type"],
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        elif name == "generate_sequence_diagram":
            result = await plantuml.generate_sequence_diagram(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        
        # Mermaid tools
        elif name == "generate_flowchart":
            result = await mermaid.generate_flowchart(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        elif name == "generate_mermaid_sequence":
            result = await mermaid.generate_sequence(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        elif name == "generate_gantt":
            result = await mermaid.generate_gantt(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        
        # Graphviz tools
        elif name == "generate_dependency_graph":
            result = await graphviz.generate_graph(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png"),
                arguments.get("layout", "dot")
            )
        
        # draw.io tools
        elif name == "generate_cloud_diagram":
            result = await drawio.generate_diagram(
                arguments["content"],
                arguments["output_path"],
                arguments.get("format", "png")
            )
        
        # Export tools
        elif name == "export_to_pdf":
            result = await export_tools.export_to_pdf(
                markdown_content=arguments.get("markdown_content"),
                markdown_file_path=arguments.get("markdown_file_path"),
                output_path=arguments["output_path"],
                title=arguments.get("title"),
                author=arguments.get("author"),
                include_toc=arguments.get("include_toc", True)
            )
        elif name == "export_to_docx":
            result = await export_tools.export_to_docx(
                arguments["markdown_content"],
                arguments["output_path"],
                arguments.get("title"),
                arguments.get("author")
            )
        elif name == "create_document_from_template":
            result = await export_tools.create_from_template(
                arguments["template_type"],
                arguments["variables"],
                arguments["output_path"]
            )
        
        # OpenAI image generation tools
        elif name == "generate_image_openai":
            result = await openai_images.generate_image_openai(
                arguments["prompt"],
                arguments["output_path"],
                arguments.get("size", "1024x1024"),
                arguments.get("quality", "standard")
            )
        elif name == "generate_icon_openai":
            result = await openai_images.generate_icon_openai(
                arguments["prompt"],
                arguments["output_path"],
                arguments.get("style", "flat design, minimalist, simple")
            )
        elif name == "generate_illustration_openai":
            result = await openai_images.generate_illustration_openai(
                arguments["prompt"],
                arguments["output_path"],
                arguments.get("style", "professional, technical illustration")
            )
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        return [TextContent(type="text", text=result)]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

