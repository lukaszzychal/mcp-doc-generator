"""
Smart Mode - AI-assisted diagram generation using OpenAI API.

Analyzes natural language prompts and generates appropriate diagram code.
User just describes what they want, AI does the rest!
"""

import os
from typing import Dict, Literal, Optional
from openai import AsyncOpenAI

from .plantuml import generate_c4_diagram, generate_uml_diagram, generate_sequence_diagram
from .mermaid import generate_flowchart, generate_sequence, generate_gantt
from .graphviz import generate_graph


# Initialize OpenAI client (API key from environment)
client = None


def init_openai_client():
    """Initialize OpenAI client with API key from environment."""
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False
    client = AsyncOpenAI(api_key=api_key)
    return True


async def analyze_prompt(prompt: str) -> Dict:
    """
    Analyze user prompt to determine:
    1. What type of diagram they want (C4, UML, flowchart, etc.)
    2. What elements/components should be included
    3. What relationships exist
    
    Args:
        prompt: Natural language description
        
    Returns:
        Dict with analysis results
        
    Example:
        >>> await analyze_prompt("Create a microservices architecture with auth, user, and product services")
        {
            "diagram_type": "c4_container",
            "elements": ["auth_service", "user_service", "product_service"],
            "relationships": [...],
            "suggested_template": "c4_microservices_basic"
        }
    """
    if not client:
        if not init_openai_client():
            return {
                "error": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
            }
    
    try:
        system_prompt = """You are an expert software architect assistant. Analyze the user's request and determine:
1. What type of diagram they want (c4_context, c4_container, c4_component, uml_class, sequence, flowchart, gantt, graph)
2. Key elements/components that should appear
3. Relationships between elements
4. Whether a template exists that matches (c4_ecommerce_basic, c4_microservices_basic, c4_api_gateway, etc.)

Return JSON with:
{
  "diagram_type": "c4_container | uml_class | sequence | flowchart | gantt | graph",
  "tool": "c4 | uml | mermaid | graphviz",
  "elements": ["element1", "element2", ...],
  "suggested_template": "template_name or null",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}"""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cost-effective
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3  # Lower = more consistent
        )
        
        import json
        analysis = json.loads(response.choices[0].message.content)
        return analysis
    
    except Exception as e:
        return {"error": f"Failed to analyze prompt: {str(e)}"}


async def generate_diagram_code(
    prompt: str,
    diagram_type: str,
    tool: str
) -> str:
    """
    Generate diagram code from natural language description.
    
    Args:
        prompt: What user wants to create
        diagram_type: Type of diagram (c4_context, uml_class, etc.)
        tool: Which tool to use (c4, uml, mermaid, graphviz)
        
    Returns:
        Generated code (PlantUML, Mermaid, or DOT)
        
    Example:
        >>> code = await generate_diagram_code(
        ...     "E-commerce with user, shop, and payment",
        ...     "c4_context",
        ...     "c4"
        ... )
        >>> print(code)
        Person(user, "User")
        System(shop, "E-commerce")
        System_Ext(payment, "Payment Gateway")
        ...
    """
    if not client:
        if not init_openai_client():
            return "Error: OpenAI API key not configured"
    
    try:
        # Build system prompt based on tool
        if tool == "c4":
            system_prompt = """You are an expert in C4 PlantUML diagrams. Generate ONLY the diagram code (no @startuml/@enduml, no includes).
Use proper C4-PlantUML syntax:
- Person(id, "Label", "Description")
- System(id, "Label", "Description")
- System_Ext(id, "External", "Description")
- Container(id, "Label", "Tech", "Description")
- Component(id, "Label", "Tech", "Description")
- Rel(from, to, "Label", "Protocol")

Generate clean, professional code that accurately represents the user's description."""

        elif tool == "uml":
            system_prompt = """You are an expert in UML PlantUML diagrams. Generate ONLY the diagram code (no @startuml/@enduml).
Use proper PlantUML syntax:
- class ClassName { fields; methods }
- interface InterfaceName
- enum EnumName
- ClassName "1" --> "*" OtherClass : relationship
- ClassName --|> ParentClass : inheritance

Generate clean, professional code."""

        elif tool == "mermaid":
            if "flowchart" in diagram_type:
                system_prompt = """You are an expert in Mermaid flowcharts. Generate ONLY the flowchart code.
Start with: flowchart TD
Use syntax:
- Node[Label]
- Node{Decision?}
- Node([Start/End])
- A --> B
- A -->|Label| B

Generate clear, logical flow."""

            elif "sequence" in diagram_type:
                system_prompt = """You are an expert in Mermaid sequence diagrams. Generate ONLY the sequence code.
Start with: sequenceDiagram
Use syntax:
- participant A as Label
- A->>B: Message
- B-->>A: Response
- alt/else/end for conditions
- Note over A,B: Note text

Generate clear interactions."""

            elif "gantt" in diagram_type:
                system_prompt = """You are an expert in Mermaid Gantt charts. Generate ONLY the gantt code.
Start with: gantt
Use syntax:
- title Project Name
- dateFormat YYYY-MM-DD
- section Phase
- Task name :done, 2024-01-01, 7d
- Another task :active, 2024-01-08, 3d

Generate realistic timeline."""

        elif tool == "graphviz":
            system_prompt = """You are an expert in Graphviz DOT language. Generate ONLY the graph code.
Use syntax:
- digraph Name { }
- node [shape=box, style=filled]
- A [label="Service A"]
- A -> B [label="depends on"]

Generate clear dependency graph."""

        else:
            system_prompt = "Generate diagram code based on user request."
        
        response = await client.chat.completions.create(
            model="gpt-4o",  # Better quality for code generation
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create diagram for: {prompt}\n\nGenerate ONLY the code, no explanations."}
            ],
            temperature=0.7  # Balanced creativity
        )
        
        code = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if code.startswith("```"):
            lines = code.split("\n")
            code = "\n".join(lines[1:-1]) if len(lines) > 2 else code
        
        return code
    
    except Exception as e:
        return f"Error generating code: {str(e)}"


async def generate_smart(
    prompt: str,
    output_path: str,
    format: Literal["png", "svg", "pdf"] = "png",
    force_type: Optional[str] = None
) -> str:
    """
    Smart Mode main function: Generate diagram from natural language.
    
    This is the magic function! User just describes what they want,
    and AI:
    1. Analyzes the prompt
    2. Determines best diagram type
    3. Generates the code
    4. Renders the diagram
    
    Args:
        prompt: Natural language description (e.g., "Create microservices architecture with 3 services")
        output_path: Where to save diagram
        format: Output format
        force_type: Optional - force specific diagram type (c4_context, flowchart, etc.)
        
    Returns:
        Success/error message
        
    Example:
        >>> result = await generate_smart(
        ...     "Create an e-commerce system with user, shop, payment, and email services",
        ...     "output/ecommerce.png"
        ... )
        "✓ Smart diagram generated: /path/to/output/ecommerce.png
           Type: C4 Context
           Cost: $0.015"
    """
    try:
        # Step 1: Analyze prompt (unless type is forced)
        if force_type:
            diagram_type = force_type
            tool = _detect_tool_from_type(diagram_type)
        else:
            analysis = await analyze_prompt(prompt)
            
            if "error" in analysis:
                return f"✗ {analysis['error']}"
            
            diagram_type = analysis.get("diagram_type", "c4_context")
            tool = analysis.get("tool", "c4")
            
            # Check if template exists and would be faster
            suggested_template = analysis.get("suggested_template")
            if suggested_template:
                return f"💡 Suggestion: Template '{suggested_template}' matches your request!\n" \
                       f"   Use Template Mode for faster generation (0 cost):\n" \
                       f"   generate_from_template('{suggested_template}', variables={{...}})\n" \
                       f"   \n" \
                       f"   Or continue with Smart Mode? (generates custom diagram, ~$0.02)"
        
        # Step 2: Generate code
        code = await generate_diagram_code(prompt, diagram_type, tool)
        
        if code.startswith("Error:"):
            return f"✗ {code}"
        
        # Step 3: Render diagram using appropriate tool
        if tool == "c4":
            # Determine C4 diagram level
            if "context" in diagram_type:
                c4_type = "context"
            elif "container" in diagram_type:
                c4_type = "container"
            elif "component" in diagram_type:
                c4_type = "component"
            else:
                c4_type = "context"
            
            result = await generate_c4_diagram(c4_type, code, output_path, format)
        
        elif tool == "uml":
            result = await generate_uml_diagram("class", code, output_path, format)
        
        elif tool == "mermaid":
            if "flowchart" in diagram_type:
                result = await generate_flowchart(code, output_path, format)
            elif "sequence" in diagram_type:
                result = await generate_sequence(code, output_path, format)
            elif "gantt" in diagram_type:
                result = await generate_gantt(code, output_path, format)
        
        elif tool == "graphviz":
            result = await generate_graph(code, output_path, format)
        
        else:
            return f"✗ Unknown tool type: {tool}"
        
        # Add Smart Mode badge to result
        return f"✨ SMART MODE GENERATED ✨\n" \
               f"   {result}\n" \
               f"   Type: {diagram_type}\n" \
               f"   Cost: ~$0.01-0.02\n" \
               f"   \n" \
               f"   💡 To edit: Use Expert Mode with the generated code"
    
    except Exception as e:
        return f"✗ Smart generation failed: {str(e)}"


def _detect_tool_from_type(diagram_type: str) -> str:
    """Helper to detect tool from diagram type."""
    if "c4_" in diagram_type or diagram_type in ["context", "container", "component"]:
        return "c4"
    elif "uml_" in diagram_type or diagram_type in ["class", "sequence_uml"]:
        return "uml"
    elif diagram_type in ["flowchart", "sequence", "gantt", "mermaid_"]:
        return "mermaid"
    elif diagram_type in ["graph", "dependency"]:
        return "graphviz"
    else:
        return "c4"  # default


async def get_smart_mode_status() -> str:
    """
    Check if Smart Mode is available and configured.
    
    Returns:
        Status message
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return """❌ Smart Mode NOT CONFIGURED

To enable Smart Mode:
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Set environment variable:
   export OPENAI_API_KEY='sk-...'
3. Restart MCP server

Smart Mode allows natural language diagram generation:
- Just describe what you want
- AI generates the code
- Cost: ~$0.01-0.02 per diagram

Alternative: Use Template Mode (FREE) for common patterns!"""
    
    if not client:
        init_openai_client()
    
    if client:
        return """✅ Smart Mode READY

You can now use natural language to generate diagrams!

Example:
  generate_smart(
      "Create microservices architecture with auth, user, and product services",
      "output/architecture.png"
  )

Cost: ~$0.01-0.02 per diagram
Models: GPT-4o-mini (analysis) + GPT-4o (generation)

💡 Tip: Use Template Mode (FREE) when possible!"""
    else:
        return "❌ Smart Mode: Failed to initialize OpenAI client"

