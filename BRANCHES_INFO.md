# 🌿 Full-Version Branch - Pełna Wersja

**Status:** ✅ Production Ready  
**Version:** Complete (Expert + Template + Smart Mode)

## 🎯 Co to jest?

Full-version branch zawiera **pełną wersję** MCP Documentation Server ze wszystkimi 3 trybami!

## ✅ Features (16 MCP Tools):

### 1. Expert Mode (11 tools):
**PlantUML:**
- generate_c4_diagram
- generate_uml_diagram
- generate_sequence_diagram

**Mermaid:**
- generate_flowchart
- generate_mermaid_sequence
- generate_gantt

**Graphviz:**
- generate_dependency_graph

**draw.io:**
- generate_cloud_diagram

**Export:**
- export_to_pdf
- export_to_docx
- create_document_from_template

### 2. Template Mode (+3 tools, FREE!):
- list_templates
- get_template_info
- generate_from_template

**10 Pre-built Templates:**
- 4 C4 Architecture (e-commerce, microservices, API gateway, event-driven)
- 2 UML (class diagrams, domain models)
- 3 Mermaid (flowcharts, sequences, gantt)
- 1 Graphviz (service dependencies)

### 3. Smart Mode (+2 tools, ~$0.02/diagram):
- get_smart_mode_status
- generate_smart (AI-powered!)

## 💰 Cost:
- **Expert Mode:** $0 (FREE!)
- **Template Mode:** $0 (FREE!)
- **Smart Mode:** ~$0.01-0.02/diagram (optional)

**Recommended:** 80% Template + 15% Expert + 5% Smart = ~$1-2/month

## 🚀 Quick Start:

```bash
./install.sh
docker compose up -d

# Optional: For Smart Mode
export OPENAI_API_KEY='sk-...'
```

## 🎨 Examples:

### Expert Mode (Full Control):
```python
generate_c4_diagram(
    diagram_type="context",
    content="Person(user, 'User')...",
    output_path="output/diagram.png"
)
```

### Template Mode (10x Faster!):
```python
generate_from_template(
    template_name="c4_ecommerce_basic",
    variables={"system_name": "My Shop", ...},
    output_path="output/shop.png"
)
```

### Smart Mode (AI Magic!):
```python
generate_smart(
    prompt="Create microservices with auth, user, product services",
    output_path="output/microservices.png"
)
```

## 📚 Documentation:

- `TEMPLATE_MODE_IMPLEMENTED.md` - Template Mode guide
- `SMART_MODE_IMPLEMENTED.md` - Smart Mode guide
- `HYBRID_MODES_COMPLETE.md` - Complete comparison
- `examples/template_mode_examples.md` - 8 examples
- `BRANCHES_INFO.md` - All branches comparison

## 🆚 vs Main Branch:

| Feature | main | full-version |
|---------|------|--------------|
| **Expert Mode** | ✅ 11 tools | ✅ 11 tools |
| **Template Mode** | ❌ | ✅ 3 tools, 10 templates |
| **Smart Mode** | ❌ | ✅ 2 tools (OpenAI) |
| **Total Tools** | 11 | **16** |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Ease** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Cost** | $0 | $0-2/month |

## 💡 Best For:
- Teams that want productivity boost
- Non-technical users (Template/Smart Mode)
- Quick prototyping
- Standardized documentation
- When speed matters

## 🔄 Switch to Basic Version?

```bash
git checkout main
```

Main = Expert Mode only (11 tools, FREE)

---

**Date:** 24 Listopada 2025  
**Status:** ✅ Production Ready  
**Cost:** $0-2/month (depending on Smart Mode usage)

