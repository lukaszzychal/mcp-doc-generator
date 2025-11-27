# Cursor Configuration with npx

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

This guide explains how to configure Cursor to use the MCP documentation server via npx installation.

## Configuration

### Step 1: Open Cursor Settings

1. Open Cursor
2. Go to **Settings** (or press `Cmd+,` on macOS / `Ctrl+,` on Windows/Linux)
3. Navigate to **Features** → **Model Context Protocol** (or search for "MCP")

### Step 2: Add MCP Server Configuration

Add the following configuration to your Cursor MCP settings:

#### Option 1: Latest version from branch

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator"
      ]
    }
  }
}
```

#### Option 2: Specific version (tag) - Recommended for production

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.3"
      ]
    }
  }
}
```

#### Option 3: Specific branch

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation"
      ]
    }
  }
}
```

### Step 3: Environment Variables (Optional)

If you need to set environment variables (e.g., custom PlantUML server):

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.3"
      ],
      "env": {
        "PLANTUML_SERVER": "http://localhost:8080",
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

### Step 4: Restart Cursor

After adding the configuration, restart Cursor to apply changes.

### Step 5: Verify Installation

1. Open a new conversation in Cursor
2. Check if MCP tools are available
3. Try using a tool, e.g.:
   - "Generate C4 Context Diagram for e-commerce system"
   - "Create UML Class Diagram with User and Order classes"

## Requirements

Before using npx installation, ensure:

1. **Node.js** >= 14.0.0 is installed
   - Check: `node --version`
   - Install: https://nodejs.org/

2. **Python** >= 3.10 is installed
   - Check: `python3 --version`
   - Install: https://www.python.org/

3. **Python dependencies** are installed:
   ```bash
   pip install -r requirements.txt
   ```
   Or use Docker (recommended):
   ```bash
   docker compose up -d
   ```

## Troubleshooting

### Problem: npx cannot find package

**Solution:**
- Ensure you use the full path: `github:lukaszzychal/mcp-doc-generator`
- Check if repository is public
- Verify tag/branch exists

### Problem: "Python 3.10+ is required but not found"

**Solution:**
- Install Python 3.10 or newer
- Ensure Python is in PATH
- Check: `python3 --version`

### Problem: "ModuleNotFoundError: No module named 'mcp'"

**Solution:**
- Install dependencies: `pip install -r requirements.txt`
- Or use Docker: `docker compose up -d`

### Problem: MCP tools not visible in Cursor

**Solution:**
1. Check Cursor logs: `~/Library/Application Support/Cursor/logs/` (macOS)
2. Restart Cursor
3. Verify configuration syntax (valid JSON)
4. Check if npx is working: `npx --version`

## Alternative: Docker Configuration

If you prefer Docker (more reliable, includes all dependencies):

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
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

See [QUICKSTART.md](QUICKSTART.md) for Docker setup.

## See also

- [NPX_INSTALLATION.md](NPX_INSTALLATION.md) - Detailed npx installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start with Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Complete usage guide

---

<a name="polski"></a>
# Polski

## Przegląd

Ten przewodnik wyjaśnia jak skonfigurować Cursor do używania serwera MCP dokumentacji przez instalację npx.

## Konfiguracja

### Krok 1: Otwórz ustawienia Cursor

1. Otwórz Cursor
2. Przejdź do **Settings** (lub naciśnij `Cmd+,` na macOS / `Ctrl+,` na Windows/Linux)
3. Przejdź do **Features** → **Model Context Protocol** (lub wyszukaj "MCP")

### Krok 2: Dodaj konfigurację serwera MCP

Dodaj następującą konfigurację do ustawień MCP w Cursor:

#### Opcja 1: Najnowsza wersja z gałęzi

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator"
      ]
    }
  }
}
```

#### Opcja 2: Konkretna wersja (tag) - Zalecane dla produkcji

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.3"
      ]
    }
  }
}
```

#### Opcja 3: Konkretna gałąź

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation"
      ]
    }
  }
}
```

### Krok 3: Zmienne środowiskowe (Opcjonalne)

Jeśli potrzebujesz ustawić zmienne środowiskowe (np. niestandardowy serwer PlantUML):

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.3"
      ],
      "env": {
        "PLANTUML_SERVER": "http://localhost:8080",
        "PYTHONPATH": "/path/to/project"
      }
    }
  }
}
```

### Krok 4: Restart Cursor

Po dodaniu konfiguracji, zrestartuj Cursor aby zastosować zmiany.

### Krok 5: Weryfikacja instalacji

1. Otwórz nową konwersację w Cursor
2. Sprawdź czy narzędzia MCP są dostępne
3. Spróbuj użyć narzędzia, np.:
   - "Wygeneruj C4 Context Diagram dla systemu e-commerce"
   - "Utwórz UML Class Diagram z klasami User i Order"

## Wymagania

Przed użyciem instalacji npx, upewnij się że:

1. **Node.js** >= 14.0.0 jest zainstalowany
   - Sprawdź: `node --version`
   - Zainstaluj: https://nodejs.org/

2. **Python** >= 3.10 jest zainstalowany
   - Sprawdź: `python3 --version`
   - Zainstaluj: https://www.python.org/

3. **Zależności Python** są zainstalowane:
   ```bash
   pip install -r requirements.txt
   ```
   Lub użyj Docker (zalecane):
   ```bash
   docker compose up -d
   ```

## Rozwiązywanie problemów

### Problem: npx nie znajduje pakietu

**Rozwiązanie:**
- Upewnij się, że używasz pełnej ścieżki: `github:lukaszzychal/mcp-doc-generator`
- Sprawdź czy repozytorium jest publiczne
- Zweryfikuj czy tag/gałąź istnieje

### Problem: "Python 3.10+ is required but not found"

**Rozwiązanie:**
- Zainstaluj Python 3.10 lub nowszy
- Upewnij się, że Python jest w PATH
- Sprawdź: `python3 --version`

### Problem: "ModuleNotFoundError: No module named 'mcp'"

**Rozwiązanie:**
- Zainstaluj zależności: `pip install -r requirements.txt`
- Lub użyj Docker: `docker compose up -d`

### Problem: Narzędzia MCP nie są widoczne w Cursor

**Rozwiązanie:**
1. Sprawdź logi Cursor: `~/Library/Application Support/Cursor/logs/` (macOS)
2. Zrestartuj Cursor
3. Zweryfikuj składnię konfiguracji (poprawny JSON)
4. Sprawdź czy npx działa: `npx --version`

## Alternatywa: Konfiguracja Docker

Jeśli wolisz Docker (bardziej niezawodne, zawiera wszystkie zależności):

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
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

Zobacz [QUICKSTART.md](QUICKSTART.md) dla konfiguracji Docker.

## Zobacz także

- [NPX_INSTALLATION.md](NPX_INSTALLATION.md) - Szczegółowy przewodnik instalacji npx
- [QUICKSTART.md](QUICKSTART.md) - Szybki start z Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Kompletny przewodnik użycia

