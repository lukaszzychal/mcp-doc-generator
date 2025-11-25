# Quick Start Guide - MCP Documentation Server

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
