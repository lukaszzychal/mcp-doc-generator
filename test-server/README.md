# 🧪 Test Server - Output Directory

This directory is used for testing MCP Documentation Server through Claude Desktop.

## 📝 Usage Examples

### 1. C4 Context Diagram (E-commerce)

**Prompt for Claude Desktop:**
```
Generate a C4 context diagram for an e-commerce system with users, 
web app, API gateway, and payment service. Export to PNG.
Save to: test-server/c4-ecommerce-context.png
```

---

### 2. ADR Document (REST → GraphQL)

**Prompt for Claude Desktop:**
```
Create an ADR document for switching from REST to GraphQL.
Include pros/cons, decision rationale, and consequences.
Save to: test-server/adr-rest-to-graphql.md
```

---

### 3. Gantt Chart (Q1 2025 Roadmap)

**Prompt for Claude Desktop:**
```
Generate a Gantt chart for our Q1 2025 roadmap:
- January: Planning & Design
- February: Development Phase 1
- March: Testing & Launch
Export to PDF.
Save to: test-server/roadmap-q1-2025.pdf
```

---

## 📂 Expected Output Files

After running the examples above, you should see:

```
test-server/
├── c4-ecommerce-context.png          # C4 diagram
├── adr-rest-to-graphql.md            # ADR document
└── roadmap-q1-2025.pdf               # Gantt chart
```

---

## ⚙️ Configuration

Make sure your Claude Desktop is configured with MCP server:

**Location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

**Content:**
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
      ]
    }
  }
}
```

Or if running locally:
```json
{
  "mcpServers": {
    "documentation": {
      "command": "python",
      "args": ["/Users/lukaszzychal/PhpstormProjects/MCPServer/src/server.py"],
      "env": {
        "PLANTUML_SERVER": "http://localhost:8080"
      }
    }
  }
}
```

---

## 🧪 Testing

1. **Open Claude Desktop**
2. **Start a new conversation**
3. **Use the prompts above** (Claude will use MCP tools automatically)
4. **Check this directory** for generated files

---

## 📊 Available MCP Tools

| Tool | Description | Example Output |
|------|-------------|----------------|
| **generate_c4_diagram** | C4 Architecture diagrams | PNG/SVG |
| **generate_uml_diagram** | UML class/component diagrams | PNG/SVG |
| **generate_sequence_diagram** | Sequence diagrams | PNG/SVG |
| **generate_flowchart** | Flowcharts | PNG/SVG |
| **generate_gantt** | Gantt charts | PNG/SVG |
| **generate_dependency_graph** | Dependency graphs | PNG/SVG/PDF |
| **generate_cloud_diagram** | Cloud architecture | .drawio XML |
| **export_to_pdf** | Markdown → PDF | PDF |
| **export_to_docx** | Markdown → Word | DOCX |
| **create_document_from_template** | Template-based docs | MD |

---

## 🐛 Troubleshooting

### Issue: "MCP server not responding"
**Solution:**
```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer
docker compose ps  # Check if containers are running
docker compose up -d  # Start if needed
```

### Issue: "Permission denied"
**Solution:**
```bash
chmod 755 test-server/
```

### Issue: "Output file not created"
**Solution:** Check absolute paths. Use full path:
```
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/output.png
```

---

**Last Updated:** 25 Listopada 2025  
**Status:** ✅ Ready for testing

