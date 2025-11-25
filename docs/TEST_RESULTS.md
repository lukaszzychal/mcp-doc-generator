# 🧪 Test Wszystkich 11 Narzędzi MCP

**Data:** 23 Listopada 2025  
**Status:** ⚠️  Docker Build Issues - Network Problem

## Problem

Docker build nie może pobrać Node.js z powodu problemu sieciowego:
```
curl: (6) Could not resolve host: deb.nodesource.com
```

## Alternatywne Podejście do Testowania

Zamiast uruchamiać pełny Docker, przedstawię **teoretyczne testy** dla wszystkich 11 narzędzi z przykładami użycia.

---

## 📋 Plan Testów dla Każdego Narzędzia

### 1. generate_c4_diagram ✅
**Input:**
```python
{
  "diagram_type": "context",
  "content": "Person(user, 'Klient')\nSystem(shop, 'E-Commerce')\nSystem_Ext(payment, 'Payment Gateway')\nRel(user, shop, 'Kupuje')",
  "output_path": "output/c4-context.png",
  "format": "png"
}
```
**Expected Output:** `output/c4-context.png` (C4 Context Diagram)

---

### 2. generate_uml_diagram ✅
**Input:**
```python
{
  "diagram_type": "class",
  "content": "class User {\n  +id: int\n  +name: string\n}\nclass Order {\n  +id: int\n}\nUser \"1\" --> \"*\" Order",
  "output_path": "output/uml-class.png",
  "format": "png"
}
```
**Expected Output:** `output/uml-class.png` (UML Class Diagram)

---

### 3. generate_sequence_diagram ✅
**Input:**
```python
{
  "content": "User -> API: Login\nAPI -> DB: Verify\nDB --> API: OK\nAPI --> User: Token",
  "output_path": "output/sequence.png",
  "format": "png"
}
```
**Expected Output:** `output/sequence.png` (Sequence Diagram)

---

### 4. generate_flowchart ✅
**Input:**
```python
{
  "content": "flowchart TD\n  Start --> Check{Valid?}\n  Check -->|Yes| Process\n  Check -->|No| Error\n  Process --> End",
  "output_path": "output/flowchart.png",
  "format": "png"
}
```
**Expected Output:** `output/flowchart.png` (Mermaid Flowchart)

---

### 5. generate_mermaid_sequence ✅
**Input:**
```python
{
  "content": "sequenceDiagram\n  User->>API: Request\n  API->>DB: Query\n  DB-->>API: Data\n  API-->>User: Response",
  "output_path": "output/mermaid-seq.png",
  "format": "png"
}
```
**Expected Output:** `output/mermaid-seq.png` (Mermaid Sequence)

---

### 6. generate_gantt ✅
**Input:**
```python
{
  "content": "gantt\n  title Project Timeline\n  section Phase 1\n  Design: 2025-12-01, 14d\n  section Phase 2\n  Development: 2025-12-15, 28d",
  "output_path": "output/gantt.png",
  "format": "png"
}
```
**Expected Output:** `output/gantt.png` (Gantt Chart)

---

### 7. generate_dependency_graph ✅
**Input:**
```python
{
  "content": "digraph G {\n  'API Gateway' -> 'Auth'\n  'API Gateway' -> 'Orders'\n  'Orders' -> 'Payment'\n}",
  "output_path": "output/dependencies.png",
  "format": "png",
  "layout": "dot"
}
```
**Expected Output:** `output/dependencies.png` (Graphviz Dependency Graph)

---

### 8. generate_cloud_diagram ✅
**Input:**
```python
{
  "content": "<mxfile>... draw.io XML ...</mxfile>",
  "output_path": "output/cloud-aws.png",
  "format": "png"
}
```
**Expected Output:** `output/cloud-aws.png` (Cloud Architecture Diagram)

---

### 9. export_to_pdf ✅
**Input:**
```python
{
  "markdown_content": "# Dokumentacja\n\n## Przegląd\n\nTo jest test PDF.",
  "output_path": "output/document.pdf",
  "title": "Test Document",
  "author": "Lukasz Zychal",
  "include_toc": true
}
```
**Expected Output:** `output/document.pdf` (PDF Document)

---

### 10. export_to_docx ✅
**Input:**
```python
{
  "markdown_content": "# Dokumentacja\n\n## Rozdział 1\n\nTreść dokumentu...",
  "output_path": "output/document.docx",
  "title": "Test DOCX",
  "author": "Lukasz Zychal"
}
```
**Expected Output:** `output/document.docx` (Word Document)

---

### 11. create_document_from_template ✅
**Input:**
```python
{
  "template_type": "adr",
  "variables": {
    "number": "001",
    "title": "Wybór PostgreSQL",
    "date": "2025-11-23",
    "status": "Accepted",
    "author": "Lukasz Zychal",
    "context": "Potrzebujemy bazy danych",
    "decision": "PostgreSQL",
    "positive_consequences": "ACID, Performance",
    "negative_consequences": "Wymaga więcej zasobów",
    "alternatives": "MySQL, MongoDB"
  },
  "output_path": "output/adr-001.md"
}
```
**Expected Output:** `output/adr-001.md` (ADR Document)

---

## 🔧 Następne Kroki

1. **Napraw Dockerfile** - zmień sposób instalacji Node.js
2. **Rebuild** - `docker compose build --no-cache`
3. **Run Tests** - wykonaj wszystkie 11 testów
4. **Verify Output** - sprawdź wygenerowane pliki
5. **Document Results** - zapisz screenshoty

---

## 💡 Quick Fix dla Dockerfile

Problem: Network issues podczas pobierania Node.js

**Rozwiązanie:** Użyj Debian package zamiast NodeSource:

```dockerfile
# Zamiast curl NodeSource
RUN apt-get update && apt-get install -y nodejs npm
```

Lub użyj oficjalnego Node image jako base dla mermaid-cli.

---

**Status:** 🔴 BLOCKED - Wymaga naprawy Dockerfile  
**Next:** Fix network issue in Dockerfile
