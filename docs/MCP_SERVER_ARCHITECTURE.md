# MCP Server Architecture - Technical Details

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Server vs External Scripts

### What is part of the MCP server?

The **MCP server** (`src/server.py`) provides these tools through the MCP protocol:

1. **Diagram generation tools** (PlantUML, Mermaid, Graphviz, draw.io)
2. **Export tools** (`export_to_pdf`, `export_to_docx`) - **These are part of the server**
3. **Template tools** (`create_document_from_template`)

### What are external scripts?

Scripts in `scripts/` directory are **external helper tools** that:
- Call the MCP server programmatically
- Demonstrate how to use MCP tools
- Provide convenience wrappers for common tasks

**Examples:**
- `scripts/convert_doc_via_mcp_simple.py` - External client that calls `export_to_pdf` tool
- `scripts/mcp_client.py` - General-purpose MCP client
- `scripts/generate_examples.py` - Example generator

**Important:** The actual PDF conversion functionality is **inside the MCP server** (`src/tools/export.py`). The scripts are just clients that call it.

## Docker Volume Mounts

### Standard mounts (always present):

```yaml
volumes:
  - ./src:/app/src:ro              # Server source code
  - ./output:/app/output            # Output directory (writable)
  - ./src/templates:/app/src/templates:ro  # Templates
```

### Optional mounts (user-specific):

If you need to access additional directories (e.g., `docs/`), mount them explicitly:

```yaml
volumes:
  # ... standard mounts ...
  - ./docs:/app/docs:ro             # Optional: mount docs directory
  - /path/to/your/files:/app/data:ro # Optional: mount custom directory
```

**Why not mount `docs/` by default?**
- Keeps the server universal - works with any file structure
- Users can mount only what they need
- Avoids hardcoding project-specific paths

## Using export_to_pdf Tool

### Via MCP Protocol (recommended):

**In Cursor:**
```
Convert docs/myfile.md to PDF: output/myfile.pdf
```

**Programmatically:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "export_to_pdf",
    "arguments": {
      "markdown_file_path": "/app/docs/myfile.md",
      "output_path": "/app/output/myfile.pdf",
      "title": "My Document",
      "include_toc": true
    }
  }
}
```

### Via External Script (for testing):

```bash
# Using default file (requires docs/ mount)
python3 scripts/convert_doc_via_mcp_simple.py

# Using custom file
python3 scripts/convert_doc_via_mcp_simple.py -i /path/to/file.md -o output.pdf
```

**Note:** The script is just a convenience wrapper. The actual conversion happens in the MCP server.

---

<a name="polski"></a>
# Polski

## Serwer vs Skrypty Zewnętrzne

### Co jest częścią serwera MCP?

**Serwer MCP** (`src/server.py`) udostępnia te narzędzia przez protokół MCP:

1. **Narzędzia generowania diagramów** (PlantUML, Mermaid, Graphviz, draw.io)
2. **Narzędzia eksportu** (`export_to_pdf`, `export_to_docx`) - **To jest część serwera**
3. **Narzędzia szablonów** (`create_document_from_template`)

### Co to są skrypty zewnętrzne?

Skrypty w katalogu `scripts/` to **zewnętrzne narzędzia pomocnicze**, które:
- Wywołują serwer MCP programatycznie
- Pokazują jak używać narzędzi MCP
- Dostarczają wygodne opakowania dla typowych zadań

**Przykłady:**
- `scripts/convert_doc_via_mcp_simple.py` - Zewnętrzny klient wywołujący narzędzie `export_to_pdf`
- `scripts/mcp_client.py` - Ogólny klient MCP
- `scripts/generate_examples.py` - Generator przykładów

**Ważne:** Rzeczywista funkcjonalność konwersji PDF jest **wewnątrz serwera MCP** (`src/tools/export.py`). Skrypty to tylko klienci, które go wywołują.

## Mounty Wolumenów Docker

### Standardowe mounty (zawsze obecne):

```yaml
volumes:
  - ./src:/app/src:ro              # Kod źródłowy serwera
  - ./output:/app/output            # Katalog wyjściowy (zapisywalny)
  - ./src/templates:/app/src/templates:ro  # Szablony
```

### Opcjonalne mounty (specyficzne dla użytkownika):

Jeśli potrzebujesz dostępu do dodatkowych katalogów (np. `docs/`), zmountuj je jawnie:

```yaml
volumes:
  # ... standardowe mounty ...
  - ./docs:/app/docs:ro             # Opcjonalnie: zmountuj katalog docs
  - /ścieżka/do/plików:/app/data:ro # Opcjonalnie: zmountuj własny katalog
```

**Dlaczego nie mountować `docs/` domyślnie?**
- Zachowuje uniwersalność serwera - działa z dowolną strukturą plików
- Użytkownicy mogą zmountować tylko to, czego potrzebują
- Unika hardkodowania ścieżek specyficznych dla projektu

## Używanie narzędzia export_to_pdf

### Przez protokół MCP (zalecane):

**W Cursor:**
```
Konwertuj docs/myfile.md do PDF: output/myfile.pdf
```

**Programatycznie:**
```json
{
  "method": "tools/call",
  "params": {
    "name": "export_to_pdf",
    "arguments": {
      "markdown_file_path": "/app/docs/myfile.md",
      "output_path": "/app/output/myfile.pdf",
      "title": "Mój Dokument",
      "include_toc": true
    }
  }
}
```

### Przez skrypt zewnętrzny (do testowania):

```bash
# Używając domyślnego pliku (wymaga mount docs/)
python3 scripts/convert_doc_via_mcp_simple.py

# Używając własnego pliku
python3 scripts/convert_doc_via_mcp_simple.py -i /ścieżka/do/pliku.md -o output.pdf
```

**Uwaga:** Skrypt to tylko wygodne opakowanie. Rzeczywista konwersja odbywa się w serwerze MCP.

