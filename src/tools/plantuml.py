"""PlantUML diagram generation tools."""

import os
import asyncio
import aiohttp
from typing import Literal
from pathlib import Path

from utils.file_manager import ensure_output_directory, write_binary_file


# PlantUML server URL (will use Docker container)
PLANTUML_SERVER = os.getenv("PLANTUML_SERVER", "http://localhost:8080")


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
    # Add C4-PlantUML includes and wrapper
    c4_includes = """@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

"""
    
    # Wrap content if it doesn't have @startuml/@enduml
    if "@startuml" not in content:
        full_content = c4_includes + content + "\n@enduml"
    else:
        # Insert includes after @startuml
        full_content = content.replace("@startuml", c4_includes)
    
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

