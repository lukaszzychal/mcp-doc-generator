# 🖥️ Claude Desktop Setup - MCP Documentation Server

## 📋 Quick Setup Guide

### Step 1: Verify Docker is Running

```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer
docker compose ps

# Expected output:
# mcp-documentation-server   Up
# mcp-plantuml-server        Up (healthy)
```

If not running:
```bash
docker compose up -d
```

---

### Step 2: Configure Claude Desktop

**Config file location:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Recommended configuration (Docker):**
```json
{
  "mcpServers": {
    "documentation": {
      "command": "docker",
      "args": [
        "compose",
        "-f",
        "/Users/lukaszzychal/PhpstormProjects/MCPServer/docker-compose.yml",
        "exec",
        "-T",
        "mcp-server",
        "python",
        "src/server.py"
      ],
      "env": {
        "PYTHONPATH": "/app"
      }
    }
  }
}
```

**Alternative: Local Python (requires Python 3.10+):**
```json
{
  "mcpServers": {
    "documentation": {
      "command": "python3",
      "args": ["/Users/lukaszzychal/PhpstormProjects/MCPServer/src/server.py"],
      "env": {
        "PLANTUML_SERVER": "http://localhost:8080",
        "PYTHONPATH": "/Users/lukaszzychal/PhpstormProjects/MCPServer"
      }
    }
  }
}
```

---

### Step 3: Restart Claude Desktop

1. **Quit Claude Desktop** completely (⌘+Q)
2. **Reopen Claude Desktop**
3. **Check MCP status:** Look for "documentation" server in settings

---

### Step 4: Test with Sample Prompts

Open a new conversation in Claude Desktop and try:

#### Test 1: C4 Context Diagram
```
Generate a C4 context diagram for an e-commerce system with:
- Users (external)
- Web App (system boundary)
- API Gateway (system boundary)
- Payment Service (external)
- Database (internal)

Save as: test-server/c4-ecommerce.png
```

#### Test 2: ADR Document
```
Create an ADR (Architecture Decision Record) document about 
switching from REST to GraphQL API. Include:
- Context: Current REST API limitations
- Decision: Move to GraphQL
- Consequences: Pros and cons
- Alternatives considered

Save as: test-server/adr-rest-graphql.md
```

#### Test 3: Gantt Chart
```
Generate a Gantt chart for Q1 2025 roadmap:
- January 1-31: Planning & Design
- February 1-28: Development Sprint 1
- February 15-28: Development Sprint 2
- March 1-15: Testing & QA
- March 16-31: Launch & Deployment

Save as: test-server/q1-2025-roadmap.png
```

---

## 🔍 Verification

### Check if MCP Server is Connected

In Claude Desktop conversation, ask:
```
What MCP tools do you have access to?
```

Expected response should list:
- generate_c4_diagram
- generate_uml_diagram
- generate_sequence_diagram
- generate_flowchart
- generate_gantt
- generate_dependency_graph
- generate_cloud_diagram
- export_to_pdf
- export_to_docx
- create_document_from_template

---

### Check Generated Files

```bash
ls -lh test-server/

# Expected:
# c4-ecommerce.png
# adr-rest-graphql.md
# q1-2025-roadmap.png
```

---

## 🐛 Troubleshooting

### Issue 1: "MCP server not found"

**Symptoms:** Claude says it doesn't have documentation tools

**Solutions:**
1. Check config file exists:
   ```bash
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. Verify JSON syntax (no trailing commas!)

3. Restart Claude Desktop (⌘+Q, then reopen)

---

### Issue 2: "Docker container not responding"

**Symptoms:** Tools timeout or error

**Solutions:**
```bash
# Check container status
docker compose ps

# View logs
docker compose logs mcp-server
docker compose logs plantuml

# Restart if needed
docker compose restart
```

---

### Issue 3: "Permission denied on output file"

**Symptoms:** Cannot write to test-server/

**Solutions:**
```bash
# Fix permissions
chmod 755 test-server/

# Or use absolute path
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/output.png
```

---

### Issue 4: "PlantUML server not reachable"

**Symptoms:** C4/UML diagrams fail

**Solutions:**
```bash
# Check PlantUML health
curl http://localhost:8080/

# Should return HTML page
# If not, restart:
docker compose restart plantuml
```

---

### Issue 5: "Python version error"

**Symptoms:** MCP SDK import errors

**Solutions:**
- ✅ **Use Docker** (recommended - has Python 3.11)
- OR upgrade system Python to 3.10+:
  ```bash
  brew install python@3.11
  ```

---

## 📊 Configuration Comparison

| Method | Pros | Cons | When to Use |
|--------|------|------|-------------|
| **Docker** | ✅ No Python setup<br>✅ Always works<br>✅ Isolated | ❌ Slower startup | **RECOMMENDED** |
| **Local Python** | ✅ Faster<br>✅ Direct access | ❌ Requires Python 3.10+<br>❌ Dependency conflicts | Advanced users |

---

## 🧪 Advanced Configuration

### With Environment Variables

```json
{
  "mcpServers": {
    "documentation": {
      "command": "docker",
      "args": ["compose", "-f", "/path/to/docker-compose.yml", "exec", "-T", "mcp-server", "python", "src/server.py"],
      "env": {
        "PLANTUML_SERVER": "http://plantuml:8080",
        "OUTPUT_DIR": "/app/test-server",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

### With Multiple Servers

```json
{
  "mcpServers": {
    "documentation": {
      "command": "docker",
      "args": ["..."]
    },
    "other-server": {
      "command": "python",
      "args": ["/path/to/other/server.py"]
    }
  }
}
```

---

## 📚 Full Example Session

### 1. Start conversation in Claude Desktop:

**You:** "I need to document our microservices architecture"

**Claude:** "I can help with that! I have access to documentation tools..."

---

### 2. Generate C4 diagram:

**You:** 
```
Create a C4 container diagram showing:
- API Gateway (Node.js)
- User Service (Python)
- Order Service (Java)
- Payment Service (Go)
- PostgreSQL database
- Redis cache

Save as: test-server/microservices-architecture.png
```

**Claude:** *Uses generate_c4_diagram tool*

---

### 3. Generate ADR:

**You:**
```
Create an ADR for choosing microservices over monolith.
Save as: test-server/adr-001-microservices.md
```

**Claude:** *Uses create_document_from_template tool*

---

### 4. Export to PDF:

**You:**
```
Convert the ADR to PDF.
Save as: test-server/adr-001-microservices.pdf
```

**Claude:** *Uses export_to_pdf tool*

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Claude mentions using "documentation tools"
2. ✅ Files appear in `test-server/` directory
3. ✅ PNG/SVG files are valid images
4. ✅ PDF/DOCX files open correctly
5. ✅ No timeout or connection errors

---

## 🚀 Next Steps

Once configured:

1. **Explore templates:** Ask Claude about available templates
2. **Try different diagrams:** UML, flowcharts, Gantt charts
3. **Combine tools:** Generate diagram → export to PDF
4. **Automate workflows:** Create documentation sets

---

**Last Updated:** 25 Listopada 2025  
**Status:** ✅ Production Ready  
**Tested With:** Claude Desktop (latest), Docker 24.0+

