"""PlantUML diagram generation tools."""

import os
import re
import asyncio
import aiohttp
from typing import Literal
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_binary_file


# PlantUML server URL (will use Docker container)
PLANTUML_SERVER = os.getenv("PLANTUML_SERVER", "http://localhost:8080")


def _get_c4_includes(diagram_type: Literal["context", "container", "component", "code"]) -> str:
    """
    Get appropriate C4-PlantUML includes for the given diagram type.
    
    Args:
        diagram_type: Type of C4 diagram
        
    Returns:
        String with appropriate !include statements
    """
    base_url = "https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/"
    
    if diagram_type == "context":
        return f"!include {base_url}C4_Context.puml\n"
    elif diagram_type == "container":
        return f"!include {base_url}C4_Context.puml\n!include {base_url}C4_Container.puml\n"
    elif diagram_type == "component":
        return f"!include {base_url}C4_Context.puml\n!include {base_url}C4_Container.puml\n!include {base_url}C4_Component.puml\n"
    elif diagram_type == "code":
        # Code level requires all previous levels plus C4_Component.puml (which includes code elements)
        return f"!include {base_url}C4_Context.puml\n!include {base_url}C4_Container.puml\n!include {base_url}C4_Component.puml\n"
    else:
        # Default to context if unknown type
        return f"!include {base_url}C4_Context.puml\n"


async def generate_c4_diagram(
    diagram_type: Literal["context", "container", "component", "code"],
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate C4 architecture diagram.
    
    Args:
        diagram_type: Type of C4 diagram
        content: PlantUML/C4 diagram code
        output_path: Output file path
        format: Output format (png or svg)
        
    Returns:
        Success message with output path
    """
    # Validate content is not empty
    if not content or not content.strip():
        return f"✗ Error: Content is empty. Please provide PlantUML/C4 diagram code."
    
    # Check if content contains actual diagram definitions
    # C4 diagrams typically contain: Person, System, System_Ext, Rel, etc.
    c4_keywords = ["Person", "System", "System_Ext", "SystemDb", "SystemQueue", 
                   "Rel", "Rel_", "Lay_R", "Lay_U", "Lay_D", "Lay_L",
                   "Container", "ContainerDb", "ContainerQueue", "Component"]
    has_diagram_content = any(keyword in content for keyword in c4_keywords)
    
    if not has_diagram_content:
        return f"✗ Error: Content does not contain valid C4 diagram definitions. " \
               f"Expected keywords: Person, System, System_Ext, Rel, Container, Component, etc."
    
    # Get appropriate includes for diagram type
    c4_includes = _get_c4_includes(diagram_type)
    
    # Clean content: remove existing @startuml and @enduml if present
    cleaned_content = content.strip()
    
    # Remove @startuml if present (case insensitive, with optional whitespace)
    cleaned_content = re.sub(r'@startuml\s*', '', cleaned_content, flags=re.IGNORECASE)
    cleaned_content = re.sub(r'@enduml\s*', '', cleaned_content, flags=re.IGNORECASE)
    cleaned_content = cleaned_content.strip()
    
    # Build complete PlantUML code: @startuml + includes + content + @enduml
    full_content = f"@startuml\n{c4_includes}{cleaned_content}\n@enduml"
    
    return await _render_plantuml(full_content, output_path, format, f"C4 {diagram_type}")


async def generate_uml_diagram(
    diagram_type: Literal["class", "component", "deployment", "package", "activity", "usecase"],
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate UML diagram.
    
    Args:
        diagram_type: Type of UML diagram
        content: PlantUML diagram code
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message with output path
    """
    # Wrap content if needed
    if "@startuml" not in content:
        full_content = f"@startuml\n{content}\n@enduml"
    else:
        full_content = content
    
    return await _render_plantuml(full_content, output_path, format, f"UML {diagram_type}")


async def generate_sequence_diagram(
    content: str,
    output_path: str,
    format: Literal["png", "svg"] = "png"
) -> str:
    """
    Generate sequence diagram using PlantUML.
    
    Args:
        content: PlantUML sequence diagram code
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message with output path
    """
    # Wrap content if needed
    if "@startuml" not in content:
        full_content = f"@startuml\n{content}\n@enduml"
    else:
        full_content = content
    
    return await _render_plantuml(full_content, output_path, format, "Sequence diagram")


async def _render_plantuml(
    content: str,
    output_path: str,
    format: Literal["png", "svg"],
    diagram_name: str
) -> str:
    """
    Render PlantUML diagram using PlantUML server.
    
    Args:
        content: Complete PlantUML code
        output_path: Output file path
        format: Output format
        diagram_name: Name for logging
        
    Returns:
        Success message
    """
    try:
        # Ensure output directory exists
        ensure_output_directory(output_path)
        
        # Determine endpoint based on format
        endpoint = f"{PLANTUML_SERVER}/{format}"
        
        # Send request to PlantUML server
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                data=content.encode('utf-8'),
                headers={'Content-Type': 'text/plain; charset=utf-8'}
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"PlantUML server error: {error_text}")
                
                # Save the generated image
                image_data = await response.read()
                write_binary_file(output_path, image_data)
        
        abs_path = Path(output_path).absolute()
        return f"✓ {diagram_name} generated successfully: {abs_path}"
    
    except aiohttp.ClientError as e:
        return f"✗ Error connecting to PlantUML server: {str(e)}\n" \
               f"Make sure PlantUML server is running (docker-compose up)"
    except Exception as e:
        return f"✗ Error generating {diagram_name}: {str(e)}"

