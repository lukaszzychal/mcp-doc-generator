# Quick Start Guide - MCP Documentation Server

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## 🚀 Quick Start (5 minutes)

### Step 1: Installation

```bash
# Clone/navigate to project directory
cd /Users/lukaszzychal/PhpstormProjects/MCPServer

# Run automatic installer
./install.sh
```

### Step 2: Verify it works

```bash
# Run tests
./test.sh
```

### Step 3: Configure Claude Desktop

**macOS:**
```bash
# Open configuration file
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Add configuration:**
```json
{
  "mcpServers": {
    "documentation": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-documentation-server",
        "python",
        "src/server.py"
      ]
    }
  }
}
```

### Step 4: Restart Claude Desktop

Close and restart the Claude Desktop application.

### Step 5: Test!

Open a new conversation in Claude and try:

```
Generate C4 Context Diagram for e-commerce system with user, 
main system and payment gateway. Save as output/test-c4.png
```

## ✅ Verification

After configuration, Claude should have access to the following tools:

1. ✅ `generate_c4_diagram` - C4 Architecture diagrams
2. ✅ `generate_uml_diagram` - UML diagrams
3. ✅ `generate_sequence_diagram` - Sequence diagrams
4. ✅ `generate_flowchart` - Flowcharts
5. ✅ `generate_mermaid_sequence` - Mermaid sequences
6. ✅ `generate_gantt` - Gantt charts
7. ✅ `generate_dependency_graph` - Dependency graphs
8. ✅ `generate_cloud_diagram` - Cloud architecture
9. ✅ `export_to_pdf` - PDF export
10. ✅ `export_to_docx` - Word export
11. ✅ `create_document_from_template` - Template-based docs

## 🔧 Basic Docker Commands

```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f

# Stop
docker compose down

# Restart single service
docker compose restart mcp-server
```

## 📖 Next Steps

1. Review examples in `examples/example_usage.md`
2. Check templates in `src/templates/`
3. Read full documentation in `README.md`

## ❓ Troubleshooting

### PlantUML not working
```bash
docker compose restart plantuml
curl http://localhost:8080/
```

### MCP server not responding
```bash
docker compose logs mcp-server
docker compose restart mcp-server
```

### Polish character encoding issues
Make sure you're using UTF-8:
```bash
export LANG=en_US.UTF-8
```

## 🎉 Done!

Now you can generate professional technical documentation using Claude!

---

<a name="polski"></a>
# Polski

## 🚀 Szybki Start (5 minut)

### Krok 1: Instalacja

```bash
# Sklonuj/przejdź do katalogu projektu
cd /Users/lukaszzychal/PhpstormProjects/MCPServer

# Uruchom automatyczny instalator
./install.sh
```

### Krok 2: Sprawdź czy działa

```bash
# Uruchom testy
./test.sh
```

### Krok 3: Konfiguracja Claude Desktop

**macOS:**
```bash
# Otwórz plik konfiguracyjny
open ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Dodaj konfigurację:**
```json
{
  "mcpServers": {
    "documentation": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-documentation-server",
        "python",
        "src/server.py"
      ]
    }
  }
}
```

### Krok 4: Restart Claude Desktop

Zamknij i uruchom ponownie aplikację Claude Desktop.

### Krok 5: Testuj!

Otwórz nową konwersację w Claude i spróbuj:

```
Wygeneruj C4 Context Diagram dla systemu e-commerce z użytkownikiem, 
głównym systemem i payment gateway. Zapisz jako output/test-c4.png
```

## ✅ Weryfikacja

Po konfiguracji, Claude powinien mieć dostęp do następujących narzędzi:

1. ✅ `generate_c4_diagram` - C4 Architecture diagrams
2. ✅ `generate_uml_diagram` - UML diagrams
3. ✅ `generate_sequence_diagram` - Sequence diagrams
4. ✅ `generate_flowchart` - Flowcharts
5. ✅ `generate_mermaid_sequence` - Mermaid sequences
6. ✅ `generate_gantt` - Gantt charts
7. ✅ `generate_dependency_graph` - Dependency graphs
8. ✅ `generate_cloud_diagram` - Cloud architecture
9. ✅ `export_to_pdf` - PDF export
10. ✅ `export_to_docx` - Word export
11. ✅ `create_document_from_template` - Template-based docs

## 🔧 Podstawowe Komendy Docker

```bash
# Uruchom serwisy
docker compose up -d

# Sprawdź status
docker compose ps

# Zobacz logi
docker compose logs -f

# Zatrzymaj
docker compose down

# Restart pojedynczego serwisu
docker compose restart mcp-server
```

## 📖 Następne Kroki

1. Przejrzyj przykłady w `examples/example_usage.md`
2. Sprawdź szablony w `src/templates/`
3. Przeczytaj pełną dokumentację w `README.md`

## ❓ Problemy?

### PlantUML nie działa
```bash
docker compose restart plantuml
curl http://localhost:8080/
```

### MCP server nie odpowiada
```bash
docker compose logs mcp-server
docker compose restart mcp-server
```

### Błędy z polskimi znakami
Upewnij się, że używasz UTF-8:
```bash
export LANG=pl_PL.UTF-8
```

## 🎉 Gotowe!

Teraz możesz generować profesjonalną dokumentację techniczną używając Claude!
