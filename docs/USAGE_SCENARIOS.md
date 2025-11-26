# Usage Scenarios - export_to_pdf Tool

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Will it work? Yes, with different approaches:

### ✅ Scenario 1: Using markdown_content (Most Common)

**How:** User provides markdown content as string

**Works:** ✅ Always works - no file access needed

**Example in Cursor:**
```
Convert this markdown to PDF:

# My Document
Content here...

Save as: output/my-doc.pdf
```

**MCP Call:**
```json
{
  "name": "export_to_pdf",
  "arguments": {
    "markdown_content": "# My Document\n\nContent...",
    "output_path": "/app/output/my-doc.pdf"
  }
}
```

### ⚠️ Scenario 2: Using markdown_file_path

**How:** User provides path to markdown file

**Works:** ✅ Works if file is accessible in container

**Options:**
1. **File in already mounted directory:**
   - `/app/src/templates/` - ✅ Always available
   - `/app/output/` - ✅ Always available
   - Any directory user mounts explicitly

2. **File in unmounted directory (e.g., docs/):**
   - ❌ Won't work unless user mounts it
   - User must add to docker-compose.yml:
     ```yaml
     volumes:
       - ./docs:/app/docs:ro
     ```

**Example:**
```json
{
  "name": "export_to_pdf",
  "arguments": {
    "markdown_file_path": "/app/docs/myfile.md",  # Requires mount
    "output_path": "/app/output/myfile.pdf"
  }
}
```

### 📝 Scenario 3: External Script Usage

**Default behavior (without mount):**
```bash
python3 scripts/convert_doc_via_mcp_simple.py
# ❌ Won't work - tries to access /app/docs/ which isn't mounted
```

**With custom file (in mounted directory):**
```bash
# Option 1: Mount docs/ first, then use default
# Edit docker-compose.yml to add: - ./docs:/app/docs:ro
python3 scripts/convert_doc_via_mcp_simple.py

# Option 2: Use file from already mounted directory
python3 scripts/convert_doc_via_mcp_simple.py -i /app/src/templates/some.md -o output.pdf

# Option 3: Use absolute path (if mounted)
python3 scripts/convert_doc_via_mcp_simple.py -i /app/docs/file.md -o output.pdf
```

## Summary

| Use Case | Works? | Notes |
|----------|--------|-------|
| Cursor + `markdown_content` | ✅ Yes | Always works - most common |
| Cursor + `markdown_file_path` (mounted dir) | ✅ Yes | Use files from /app/src, /app/output, or user-mounted dirs |
| Cursor + `markdown_file_path` (unmounted dir) | ❌ No | User must mount directory first |
| Script (default, no mount) | ❌ No | Requires docs/ mount or use -i parameter |
| Script (with -i parameter) | ✅ Yes | If file is in mounted directory |

## Recommendation

**For maximum compatibility:**
- Use `markdown_content` when possible (works everywhere)
- If using files, mount only what you need in docker-compose.yml
- Scripts are optional helpers - main functionality is in MCP server

---

<a name="polski"></a>
# Polski

## Czy będzie działać? Tak, z różnymi podejściami:

### ✅ Scenariusz 1: Używanie markdown_content (Najczęstsze)

**Jak:** Użytkownik podaje zawartość markdown jako string

**Działa:** ✅ Zawsze działa - nie wymaga dostępu do plików

**Przykład w Cursor:**
```
Konwertuj ten markdown do PDF:

# Mój Dokument
Treść tutaj...

Zapisz jako: output/my-doc.pdf
```

**Wywołanie MCP:**
```json
{
  "name": "export_to_pdf",
  "arguments": {
    "markdown_content": "# Mój Dokument\n\nTreść...",
    "output_path": "/app/output/my-doc.pdf"
  }
}
```

### ⚠️ Scenariusz 2: Używanie markdown_file_path

**Jak:** Użytkownik podaje ścieżkę do pliku markdown

**Działa:** ✅ Działa jeśli plik jest dostępny w kontenerze

**Opcje:**
1. **Plik w już zmountowanym katalogu:**
   - `/app/src/templates/` - ✅ Zawsze dostępne
   - `/app/output/` - ✅ Zawsze dostępne
   - Dowolny katalog zmountowany przez użytkownika

2. **Plik w niezmountowanym katalogu (np. docs/):**
   - ❌ Nie zadziała chyba że użytkownik go zmountuje
   - Użytkownik musi dodać do docker-compose.yml:
     ```yaml
     volumes:
       - ./docs:/app/docs:ro
     ```

**Przykład:**
```json
{
  "name": "export_to_pdf",
  "arguments": {
    "markdown_file_path": "/app/docs/myfile.md",  # Wymaga mountu
    "output_path": "/app/output/myfile.pdf"
  }
}
```

### 📝 Scenariusz 3: Użycie Skryptu Zewnętrznego

**Domyślne zachowanie (bez mountu):**
```bash
python3 scripts/convert_doc_via_mcp_simple.py
# ❌ Nie zadziała - próbuje dostać się do /app/docs/ który nie jest zmountowany
```

**Z własnym plikiem (w zmountowanym katalogu):**
```bash
# Opcja 1: Najpierw zmountuj docs/, potem użyj domyślnego
# Edytuj docker-compose.yml aby dodać: - ./docs:/app/docs:ro
python3 scripts/convert_doc_via_mcp_simple.py

# Opcja 2: Użyj pliku z już zmountowanego katalogu
python3 scripts/convert_doc_via_mcp_simple.py -i /app/src/templates/some.md -o output.pdf

# Opcja 3: Użyj bezwzględnej ścieżki (jeśli zmountowany)
python3 scripts/convert_doc_via_mcp_simple.py -i /app/docs/file.md -o output.pdf
```

## Podsumowanie

| Przypadek Użycia | Działa? | Uwagi |
|-------------------|---------|-------|
| Cursor + `markdown_content` | ✅ Tak | Zawsze działa - najczęstsze |
| Cursor + `markdown_file_path` (zmountowany katalog) | ✅ Tak | Użyj plików z /app/src, /app/output, lub zmountowanych przez użytkownika |
| Cursor + `markdown_file_path` (niezmountowany katalog) | ❌ Nie | Użytkownik musi najpierw zmountować katalog |
| Skrypt (domyślny, bez mountu) | ❌ Nie | Wymaga mountu docs/ lub użycia parametru -i |
| Skrypt (z parametrem -i) | ✅ Tak | Jeśli plik jest w zmountowanym katalogu |

## Rekomendacja

**Dla maksymalnej kompatybilności:**
- Używaj `markdown_content` gdy możliwe (działa wszędzie)
- Jeśli używasz plików, zmountuj tylko to, czego potrzebujesz w docker-compose.yml
- Skrypty to opcjonalne pomocniki - główna funkcjonalność jest w serwerze MCP

