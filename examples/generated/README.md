# Przykładowe Pliki Wygenerowane przez MCP Server

Ten katalog zawiera przykładowe pliki wygenerowane przez wszystkie narzędzia MCP Documentation Server.

## 📊 Diagramy

### C4 Architecture Diagrams

- **example_c4_context.png** - C4 Context Diagram (system e-commerce)
- **example_c4_container.png** - C4 Container Diagram (platforma e-commerce)
- **example_c4_component.png** - C4 Component Diagram (Order Service)
- **example_c4_code.png** - C4 Code Diagram (OrderService class)

### UML Diagrams

- **example_uml_class.png** - UML Class Diagram (User, Order, Product)
- **example_uml_component.png** - UML Component Diagram (Web, API, Database)
- **example_uml_deployment.png** - UML Deployment Diagram (Server, Database Server)

### Sequence Diagrams

- **example_sequence.png** - PlantUML Sequence Diagram (login process)
- **example_mermaid_sequence.png** - Mermaid Sequence Diagram (API request flow)

### Flowcharts & Charts

- **example_flowchart.png** - Mermaid Flowchart (order processing)
- **example_gantt.png** - Gantt Chart (project timeline)

### Graphs & Architecture

- **example_dependency_graph.png** - Graphviz Dependency Graph (service dependencies)
- **example_cloud.png** - Cloud Architecture Diagram (AWS components)

## 📄 Dokumenty

### Exports

- **example_export.pdf** - PDF export z markdown
- **example_export.docx** - DOCX export z markdown

### Templates

- **example_adr.md** - ADR (Architecture Decision Record) z szablonu
- **example_api_spec.md** - API Specification z szablonu

## 🎯 Jak używać

Te pliki są przykładami pokazującymi możliwości każdego narzędzia MCP. Możesz:

1. **Otworzyć pliki** - zobacz jak wyglądają wygenerowane diagramy
2. **Użyć jako referencje** - zobacz format i strukturę
3. **Porównać** - sprawdź różnice między typami diagramów

## 🔧 Regeneracja

Aby wygenerować te pliki ponownie:

```bash
# Uruchom kontenery
docker compose up -d

# Wygeneruj wszystkie przykłady
python3 scripts/generate_examples.py
```

## 📝 Uwagi

- Wszystkie pliki są generowane przez dockerowy serwer PlantUML/MCP
- Pliki PNG/SVG są renderowane przez PlantUML server
- Pliki PDF/DOCX są generowane przez Pandoc
- Pliki .md są tworzone z szablonów

## 📦 Rozmiary plików

- Diagramy PNG: ~2-45 KB
- Diagramy SVG: ~2-20 KB  
- Dokumenty PDF: ~20-30 KB
- Dokumenty DOCX: ~10 KB
- Dokumenty Markdown: ~1-2 KB

---

**Wygenerowano:** 25 Listopada 2024  
**Narzędzie:** MCP Documentation Server  
**Status:** ✅ Wszystkie przykłady wygenerowane

