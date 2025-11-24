"""
Template Mode - Pre-built diagram templates with variable substitution.

Provides easy-to-use templates for common architecture patterns.
Users just fill in the blanks instead of writing full code.
"""

import re
from pathlib import Path
from typing import Dict, Literal, Optional
from .plantuml import generate_c4_diagram, generate_uml_diagram
from .mermaid import generate_flowchart, generate_sequence, generate_gantt
from .graphviz import generate_graph


TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "diagram_templates"


def list_available_templates() -> Dict[str, list]:
    """
    List all available templates grouped by category.
    
    Returns:
        Dict with categories and their templates
    """
    templates = {
        "c4": [],
        "uml": [],
        "mermaid": [],
        "graphviz": []
    }
    
    if not TEMPLATES_DIR.exists():
        return templates
    
    for template_file in TEMPLATES_DIR.glob("*"):
        if template_file.is_file() and template_file.stem != "README":
            name = template_file.stem
            
            if name.startswith("c4_"):
                templates["c4"].append(name)
            elif name.startswith("uml_"):
                templates["uml"].append(name)
            elif name.startswith("mermaid_"):
                templates["mermaid"].append(name)
            elif name.startswith("graphviz_"):
                templates["graphviz"].append(name)
    
    return templates


def get_template_variables(template_name: str) -> list[str]:
    """
    Extract all variables ({{var}}) from a template.
    
    Args:
        template_name: Name of the template (without extension)
        
    Returns:
        List of variable names found in template
    """
    template_content = _load_template(template_name)
    if not template_content:
        return []
    
    # Find all {{variable}} patterns
    variables = re.findall(r'\{\{(\w+)\}\}', template_content)
    # Remove duplicates while preserving order
    return list(dict.fromkeys(variables))


def _load_template(template_name: str) -> Optional[str]:
    """
    Load template content from file.
    
    Args:
        template_name: Name of the template (without extension)
        
    Returns:
        Template content or None if not found
    """
    # Try different extensions
    for ext in ['.puml', '.mmd', '.dot']:
        template_path = TEMPLATES_DIR / f"{template_name}{ext}"
        if template_path.exists():
            return template_path.read_text(encoding='utf-8')
    
    return None


def _substitute_variables(template_content: str, variables: Dict[str, str]) -> str:
    """
    Replace {{variable}} placeholders with actual values.
    
    Args:
        template_content: Template string with {{var}} placeholders
        variables: Dict mapping variable names to values
        
    Returns:
        Content with substituted variables
    """
    result = template_content
    
    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"
        result = result.replace(placeholder, str(var_value))
    
    return result


def _detect_template_type(template_name: str) -> str:
    """
    Detect template type from name.
    
    Args:
        template_name: Template name
        
    Returns:
        Type: 'c4', 'uml', 'mermaid', or 'graphviz'
    """
    if template_name.startswith("c4_"):
        return "c4"
    elif template_name.startswith("uml_"):
        return "uml"
    elif template_name.startswith("mermaid_"):
        return "mermaid"
    elif template_name.startswith("graphviz_"):
        return "graphviz"
    else:
        # Try to detect by file extension
        for ext, type_ in [('.puml', 'c4'), ('.mmd', 'mermaid'), ('.dot', 'graphviz')]:
            if (TEMPLATES_DIR / f"{template_name}{ext}").exists():
                return type_
        
        return "unknown"


async def generate_from_template(
    template_name: str,
    variables: Dict[str, str],
    output_path: str,
    format: Literal["png", "svg", "pdf"] = "png"
) -> str:
    """
    Generate diagram from template with variable substitution.
    
    This is the main Template Mode function. Instead of writing full
    PlantUML/Mermaid code, users just:
    1. Choose a template
    2. Fill in variables
    3. Generate!
    
    Args:
        template_name: Name of template (e.g., "c4_ecommerce_basic")
        variables: Dict of variables to substitute (e.g., {"system_name": "My Shop"})
        output_path: Where to save the diagram
        format: Output format (png, svg, pdf)
        
    Returns:
        Success/error message
        
    Example:
        >>> await generate_from_template(
        ...     template_name="c4_ecommerce_basic",
        ...     variables={
        ...         "system_name": "My E-Shop",
        ...         "customer_label": "Customer",
        ...         "payment_provider": "Stripe"
        ...     },
        ...     output_path="output/my-shop.png"
        ... )
        "✓ Diagram generated from template: /path/to/output/my-shop.png"
    """
    try:
        # 1. Load template
        template_content = _load_template(template_name)
        if not template_content:
            available = list_available_templates()
            return f"✗ Template '{template_name}' not found.\n" \
                   f"   Available templates:\n" \
                   f"   C4: {', '.join(available['c4'])}\n" \
                   f"   UML: {', '.join(available['uml'])}\n" \
                   f"   Mermaid: {', '.join(available['mermaid'])}\n" \
                   f"   Graphviz: {', '.join(available['graphviz'])}"
        
        # 2. Substitute variables
        diagram_code = _substitute_variables(template_content, variables)
        
        # 3. Detect template type and call appropriate generator
        template_type = _detect_template_type(template_name)
        
        if template_type == "c4":
            # Determine diagram type from template name
            if "context" in template_name or "ecommerce" in template_name or "microservices" in template_name:
                diagram_type = "context"
            elif "container" in template_name or "api_gateway" in template_name or "event_driven" in template_name:
                diagram_type = "container"
            else:
                diagram_type = "context"  # default
            
            result = await generate_c4_diagram(
                diagram_type=diagram_type,
                content=diagram_code,
                output_path=output_path,
                format=format
            )
            return f"✓ Diagram generated from template '{template_name}'\n   {result}"
        
        elif template_type == "uml":
            result = await generate_uml_diagram(
                diagram_type="class",  # templates are mostly class diagrams
                content=diagram_code,
                output_path=output_path,
                format=format
            )
            return f"✓ Diagram generated from template '{template_name}'\n   {result}"
        
        elif template_type == "mermaid":
            # Determine Mermaid type from template name
            if "flowchart" in template_name:
                result = await generate_flowchart(
                    content=diagram_code,
                    output_path=output_path,
                    format=format
                )
            elif "sequence" in template_name:
                result = await generate_sequence(
                    content=diagram_code,
                    output_path=output_path,
                    format=format
                )
            elif "gantt" in template_name:
                result = await generate_gantt(
                    content=diagram_code,
                    output_path=output_path,
                    format=format
                )
            else:
                return f"✗ Unknown Mermaid template type for '{template_name}'"
            
            return f"✓ Diagram generated from template '{template_name}'\n   {result}"
        
        elif template_type == "graphviz":
            result = await generate_graph(
                content=diagram_code,
                output_path=output_path,
                format=format
            )
            return f"✓ Diagram generated from template '{template_name}'\n   {result}"
        
        else:
            return f"✗ Unknown template type for '{template_name}'"
    
    except Exception as e:
        return f"✗ Error generating from template '{template_name}': {str(e)}"


async def get_template_info(template_name: str) -> str:
    """
    Get information about a template including required variables.
    
    Args:
        template_name: Name of the template
        
    Returns:
        Formatted string with template info
    """
    try:
        # Check if template exists
        template_content = _load_template(template_name)
        if not template_content:
            return f"✗ Template '{template_name}' not found"
        
        # Get variables
        variables = get_template_variables(template_name)
        template_type = _detect_template_type(template_name)
        
        # Format output
        info = f"📋 Template: {template_name}\n"
        info += f"   Type: {template_type.upper()}\n"
        info += f"   Variables ({len(variables)}):\n"
        
        for var in variables:
            info += f"     - {var}\n"
        
        info += f"\n   Usage:\n"
        info += f"   generate_from_template(\n"
        info += f"       template_name=\"{template_name}\",\n"
        info += f"       variables={{\n"
        for var in variables[:3]:  # Show first 3 as example
            info += f"           \"{var}\": \"...\",\n"
        if len(variables) > 3:
            info += f"           # ... {len(variables) - 3} more variables\n"
        info += f"       }},\n"
        info += f"       output_path=\"output/diagram.png\"\n"
        info += f"   )"
        
        return info
    
    except Exception as e:
        return f"✗ Error getting template info: {str(e)}"

