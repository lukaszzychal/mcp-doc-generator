---
title: How I Built an MCP Server That Saves 40 Hours/Month on Documentation
published: false
description: Building a Python MCP server that automatically generates architecture diagrams and exports to PDF/DOCX with full Unicode support
tags: mcp, python, documentation, opensource
canonical_url: 
cover_image: 
series: Building MCP Servers
---

# How I Built an MCP Server That Saves 40 Hours/Month on Documentation

As a software architect, I have a confession: **I hate writing documentation.**

Not because it's not important—it absolutely is. But because it's:
- ⏰ Time-consuming (20-30% of my work time)
- 😴 Repetitive and boring
- 📉 Quickly becomes outdated
- 🎨 Formatting nightmares (especially with Polish characters: ąćęłńóśźż)

Last month, I spent **8 hours** creating a single C4 architecture diagram, exporting it to PDF, and writing an ADR (Architecture Decision Record) in Word. Eight. Hours.

I thought: *"There has to be a better way."*

Spoiler: There is. And I built it.

---

## 💡 The Problem: Documentation Hell

Let me paint you a picture of a typical documentation workflow:

```
Step 1: Draw architecture diagram
├─ Open draw.io or Lucidchart
├─ Drag boxes, connect arrows
├─ Fight with alignment
├─ Export to PNG (looks blurry)
└─ Time: 2-3 hours 😫

Step 2: Write documentation
├─ Open Word
├─ Copy-paste diagram (formatting breaks)
├─ Write text around it
├─ Polish characters don't display correctly
├─ Fight with styles
└─ Time: 2-3 hours 😤

Step 3: Export to PDF
├─ "Save as PDF"
├─ Fonts are wrong
├─ Polish characters: ��� (broken)
├─ Cry a little
└─ Time: 1 hour + therapy 😭

Total: 5-7 hours per document
```

And the worst part? **Next week you need to update it because requirements changed.**

---

## 🚀 The Solution: MCP Doc Generator

I recently discovered [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) from Anthropic—a way to extend Claude's capabilities with custom tools.

So I built an MCP server that does all of this automatically:

✅ Generate architecture diagrams (C4, UML, sequence, flowcharts)  
✅ Export to PDF/DOCX with perfect formatting  
✅ Full Unicode support (including Polish: ąćęłńóśźż)  
✅ Ready-made templates (ADR, API Spec, etc.)  
✅ Works directly in Claude Desktop  

**Result:** What took 8 hours now takes **5 minutes**. ⚡

---

## 🏗️ How It Works

The server integrates multiple diagram tools:

- **PlantUML** - for C4 architecture diagrams
- **Mermaid** - for flowcharts and Gantt charts
- **Graphviz** - for dependency graphs
- **draw.io** - for cloud architecture diagrams
- **Pandoc** - for PDF/DOCX export with proper fonts

Here's the magic: You just ask Claude in natural language, and it generates everything.

### Example Conversation:

**Me:** "Generate a C4 context diagram for an e-commerce system with users, web app, API gateway, payment service, and database. Export to PNG."

**Claude (using MCP server):** "Here's your diagram..."

[*Generated in 10 seconds*]

---

## 💻 Technical Deep Dive

### Architecture

The MCP server is built in Python and exposes 11 tools to Claude:

```python
# src/server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("mcp-documentation-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(name="generate_c4_diagram", ...),
        Tool(name="generate_uml_diagram", ...),
        Tool(name="export_to_pdf", ...),
        # ... 8 more tools
    ]
```

### Key Features

#### 1. PlantUML Integration

PlantUML is perfect for architecture diagrams but notoriously hard to set up. I wrapped it in a simple async function:

```python
# src/tools/plantuml.py
async def generate_c4_diagram(
    diagram_type: str,
    content: str,
    output_path: str,
    format: str = "png"
) -> str:
    """Generate C4 diagram using PlantUML."""
    
    # Add C4 includes
    if diagram_type == "context":
        puml_content = "@startuml\n"
        puml_content += "!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml\n"
        puml_content += content
        puml_content += "\n@enduml"
    
    # Generate diagram
    result = await run_plantuml(puml_content, output_path, format)
    return f"Diagram generated: {output_path}"
```

#### 2. Polish Language Support

This was critical for my use case. Many tools don't handle Polish characters (ąćęłńóśźż) correctly in PDFs.

Solution: Custom LaTeX templates with proper font configuration:

```python
# src/utils/polish_support.py
def get_latex_template() -> str:
    return r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[polish]{babel}
\usepackage{lmodern}  % Latin Modern font supports Polish
\usepackage{graphicx}
\usepackage{hyperref}

\begin{document}
$body$
\end{document}
"""
```

Now Polish characters work perfectly in PDFs! 🇵🇱

#### 3. Template System

I created reusable templates for common documents:

```markdown
# ADR Template (src/templates/adr_template.md)

# ADR-{number}: {title}

## Status
{status}

## Context
{context}

## Decision
{decision}

## Consequences
{consequences}

## Date
{date}
```

Claude fills in the variables, and the MCP server generates a beautiful PDF.

---

## 📦 Setup & Usage

### Installation

The easiest way is with Docker:

```bash
git clone https://github.com/lukaszzychal/mcp-doc-generator
cd mcp-doc-generator
docker-compose up -d
```

Or manually:

```bash
# Install dependencies
brew install plantuml graphviz pandoc
npm install -g @mermaid-js/mermaid-cli

# Install Python packages
pip install -r requirements.txt
```

### Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "python",
      "args": ["/path/to/mcp-doc-generator/src/server.py"]
    }
  }
}
```

Restart Claude Desktop, and you're done!

---

## 🎯 Real-World Examples

### Example 1: Architecture Diagram

**Prompt:** "Create a C4 container diagram for a microservices e-commerce platform with web frontend, API gateway, 5 services (user, product, order, payment, notification), and databases."

**Result:** Complete diagram in 15 seconds.

### Example 2: ADR Document

**Prompt:** "Create an ADR for switching from REST to GraphQL. Status: Accepted. Context: Multiple clients need different data shapes. Decision: Implement GraphQL with Apollo. Consequences: Better performance, but team needs training. Export to PDF."

**Result:** Professional PDF document ready to share.

### Example 3: API Documentation

**Prompt:** "Generate API specification document for a user management API with endpoints: POST /users, GET /users/{id}, PUT /users/{id}, DELETE /users/{id}. Export to DOCX."

**Result:** Word document with formatted API specs.

---

## 🔍 Challenges & Solutions

### Challenge 1: PlantUML Java Dependency

**Problem:** PlantUML requires Java, which is a heavy dependency.

**Solution:** Docker image with all dependencies pre-installed. One command deployment.

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    plantuml \
    graphviz \
    pandoc \
    default-jre-headless \
    npm

RUN npm install -g @mermaid-js/mermaid-cli

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "src/server.py"]
```

### Challenge 2: Async File Operations

**Problem:** Generating diagrams can take seconds. Don't want to block.

**Solution:** Everything is async with proper error handling:

```python
async def generate_diagram(content: str, output_path: str):
    try:
        # Create output directory
        await ensure_directory_exists(output_path)
        
        # Generate asynchronously
        result = await asyncio.create_subprocess_exec(
            "plantuml", "-tpng", input_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        await result.communicate()
        
        if result.returncode != 0:
            raise Exception(f"PlantUML failed: {stderr}")
            
        return f"Success: {output_path}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Challenge 3: Font Rendering in PDFs

**Problem:** Default Pandoc PDFs don't support Polish characters.

**Solution:** Custom LaTeX template with proper font encoding (see code above).

---

## 📊 Results & Impact

### Before vs After

| Task | Before | After | Time Saved |
|------|--------|-------|------------|
| C4 Diagram | 2-3 hours | 5 minutes | **97% faster** |
| ADR Document | 1-2 hours | 3 minutes | **95% faster** |
| API Spec | 3-4 hours | 5 minutes | **98% faster** |
| Full Architecture Doc | 8-10 hours | 15 minutes | **98% faster** |

### Real Numbers

- **40 hours/month** saved on documentation
- **$6,000/month** value (at $150/hour)
- **$72,000/year** in productivity gains

For a team of 5 architects? **$360,000/year** in saved time.

---

## 🌟 What's Next?

The project is open source and I'm actively developing it. Roadmap:

- [ ] AI-powered diagram generation from code
- [ ] Confluence/Notion integration
- [ ] Real-time collaboration
- [ ] Web UI (not just Claude Desktop)
- [ ] More templates (compliance, security)
- [ ] GitLab/GitHub Actions integration

---

## 🎁 Try It Yourself

The project is open source and available on GitHub:

**🔗 https://github.com/lukaszzychal/mcp-doc-generator**

⭐ **Star the repo** if you find it useful!

### Getting Started

```bash
# Clone the repo
git clone https://github.com/lukaszzychal/mcp-doc-generator

# Run with Docker
docker-compose up -d

# Configure Claude Desktop
# (see repo README for details)

# Start documenting!
```

---

## 🤝 Contributing

I'd love contributions! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests
- 📝 Documentation improvements
- 🔧 Pull requests

Check out [CONTRIBUTING.md](https://github.com/lukaszzychal/mcp-doc-generator/blob/main/CONTRIBUTING.md) in the repo.

---

## 💭 Final Thoughts

Documentation doesn't have to be painful. With the right tools (and a bit of automation), you can:

✅ Save hours of manual work  
✅ Maintain consistency  
✅ Keep docs up-to-date  
✅ Focus on what matters: building great software  

The MCP ecosystem is just getting started, and I'm excited to see what we'll build together.

**What repetitive tasks are you automating?** Let me know in the comments! 👇

---

## 🔗 Links

- 📦 [GitHub Repository](https://github.com/lukaszzychal/mcp-doc-generator)
- 📖 [MCP Documentation](https://modelcontextprotocol.io/)
- 🐦 [Follow me on Twitter](https://twitter.com/yourusername) (optional)
- 💼 [Connect on LinkedIn](https://linkedin.com/in/yourusername) (optional)

---

**Tags:** #mcp #python #documentation #opensource #automation #devtools #architecture #claude

---

*If you enjoyed this article, please ⭐ star the repo and share with your team!*

*Questions? Drop them in the comments below! 👇*


