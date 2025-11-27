# npx Installation

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

The MCP server `mcp-doc-generator` can be installed and run directly via `npx`, allowing easy installation without cloning the repository.

## Requirements

- **Node.js** >= 14.0.0 (for npx)
- **Python** >= 3.10 (for the MCP server)
- Python dependencies installed (see [requirements.txt](../requirements.txt))

## Installation

### Option 1: Latest version from main branch

```bash
npx github:lukaszzychal/mcp-doc-generator
```

Or shorter (if Cursor Store automatically maps):

```bash
npx lukaszzychal/mcp-doc-generator
```

### Option 2: Specific version (tag)

```bash
npx github:lukaszzychal/mcp-doc-generator#v0.1.0
```

### Option 3: Specific branch

```bash
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

## How it works?

1. `npx` downloads the repository from GitHub
2. Detects `package.json` with `bin` configuration
3. Runs Node.js wrapper (`bin/mcp-doc-generator.js`)
4. Wrapper runs Python server (`python src/server.py`)
5. Server runs in stdio mode (stdin/stdout) according to MCP protocol

## Configuration in Cursor

To use the server in Cursor via npx, add to MCP configuration:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator"
      ]
    }
  }
}
```

Or with a specific tag:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.0"
      ]
    }
  }
}
```

## Environment Requirements

### Python and dependencies

Before using via npx, make sure that:

1. Python 3.10+ is installed and available in PATH
2. Python dependencies are installed:

```bash
pip install -r requirements.txt
```

Or use Docker (recommended):

```bash
docker compose up -d
```

### Environment variables

Wrapper automatically sets:
- `PYTHONPATH` - points to project root directory
- `PYTHONUNBUFFERED=1` - for better logging
- `PLANTUML_SERVER` - defaults to `http://localhost:8080` (if not set)

You can override environment variables:

```bash
PLANTUML_SERVER=http://custom-server:8080 npx github:lukaszzychal/mcp-doc-generator
```

## Local Testing

To test installation locally:

```bash
# From project directory
npx .

# Or use test script
./tests/test_npx_installation.sh
```

## Troubleshooting

### Problem: "Python 3.10+ is required but not found"

**Solution:**
- Install Python 3.10 or newer
- Make sure Python is in PATH
- Check: `python3 --version`

### Problem: "ModuleNotFoundError: No module named 'mcp'"

**Solution:**
- Install dependencies: `pip install -r requirements.txt`
- Or use Docker: `docker compose up -d`

### Problem: npx cannot find package

**Solution:**
- Make sure you use full path: `npx github:lukaszzychal/mcp-doc-generator`
- Check if repository is public
- Check if tag/branch exists

### Problem: Wrapper is not executable

**Solution:**
```bash
chmod +x bin/mcp-doc-generator.js
```

## File Structure

```
mcp-doc-generator/
├── package.json              # npm/npx configuration
├── bin/
│   └── mcp-doc-generator.js # Node.js wrapper
├── src/
│   └── server.py            # MCP server (Python)
└── requirements.txt         # Python dependencies
```

## Installation Methods Comparison

| Method | Advantages | Disadvantages |
|--------|------------|---------------|
| **npx** | Easy installation, automatic updates | Requires Node.js and Python |
| **Docker** | Isolated environment, all dependencies | Requires Docker |
| **Local installation** | Full control | Requires manual dependency installation |

## See also

- [QUICKSTART.md](QUICKSTART.md) - Quick start with Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Complete usage guide
- [README.md](../README.md) - General project documentation

---

<a name="polski"></a>
# Polski

## Przegląd

Serwer MCP `mcp-doc-generator` może być zainstalowany i uruchomiony przez `npx`, co pozwala na łatwą instalację bez konieczności klonowania repozytorium.

## Wymagania

- **Node.js** >= 14.0.0 (dla npx)
- **Python** >= 3.10 (dla serwera MCP)
- Zainstalowane zależności Python (zobacz [requirements.txt](../requirements.txt))

## Instalacja

### Opcja 1: Najnowsza wersja z głównej gałęzi

```bash
npx github:lukaszzychal/mcp-doc-generator
```

Lub krócej (jeśli Cursor Store automatycznie mapuje):

```bash
npx lukaszzychal/mcp-doc-generator
```

### Opcja 2: Konkretna wersja (tag)

```bash
npx github:lukaszzychal/mcp-doc-generator#v0.1.0
```

### Opcja 3: Konkretna gałąź

```bash
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

## Jak to działa?

1. `npx` pobiera repozytorium z GitHub
2. Wykrywa `package.json` z konfiguracją `bin`
3. Uruchamia wrapper Node.js (`bin/mcp-doc-generator.js`)
4. Wrapper uruchamia serwer Python (`python src/server.py`)
5. Serwer działa w trybie stdio (stdin/stdout) zgodnie z protokołem MCP

## Konfiguracja w Cursor

Aby użyć serwera w Cursor przez npx, dodaj do konfiguracji MCP:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator"
      ]
    }
  }
}
```

Lub z konkretnym tagiem:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.0"
      ]
    }
  }
}
```

## Wymagania środowiskowe

### Python i zależności

Przed użyciem przez npx, upewnij się że:

1. Python 3.10+ jest zainstalowany i dostępny w PATH
2. Zależności Python są zainstalowane:

```bash
pip install -r requirements.txt
```

Lub użyj Docker (zalecane):

```bash
docker compose up -d
```

### Zmienne środowiskowe

Wrapper automatycznie ustawia:
- `PYTHONPATH` - wskazuje na katalog główny projektu
- `PYTHONUNBUFFERED=1` - dla lepszego logowania
- `PLANTUML_SERVER` - domyślnie `http://localhost:8080` (jeśli nie ustawione)

Możesz nadpisać zmienne środowiskowe:

```bash
PLANTUML_SERVER=http://custom-server:8080 npx github:lukaszzychal/mcp-doc-generator
```

## Testowanie lokalne

Aby przetestować instalację lokalnie:

```bash
# Z katalogu projektu
npx .

# Lub użyj skryptu testowego
./tests/test_npx_installation.sh
```

## Rozwiązywanie problemów

### Problem: "Python 3.10+ is required but not found"

**Rozwiązanie:**
- Zainstaluj Python 3.10 lub nowszy
- Upewnij się, że Python jest w PATH
- Sprawdź: `python3 --version`

### Problem: "ModuleNotFoundError: No module named 'mcp'"

**Rozwiązanie:**
- Zainstaluj zależności: `pip install -r requirements.txt`
- Lub użyj Docker: `docker compose up -d`

### Problem: npx nie znajduje pakietu

**Rozwiązanie:**
- Upewnij się, że używasz pełnej ścieżki: `npx github:lukaszzychal/mcp-doc-generator`
- Sprawdź czy repozytorium jest publiczne
- Sprawdź czy tag/gałąź istnieje

### Problem: Wrapper nie jest wykonywalny

**Rozwiązanie:**
```bash
chmod +x bin/mcp-doc-generator.js
```

## Struktura plików

```
mcp-doc-generator/
├── package.json              # Konfiguracja npm/npx
├── bin/
│   └── mcp-doc-generator.js # Wrapper Node.js
├── src/
│   └── server.py            # Serwer MCP (Python)
└── requirements.txt         # Zależności Python
```

## Porównanie metod instalacji

| Metoda | Zalety | Wady |
|--------|--------|------|
| **npx** | Łatwa instalacja, automatyczne aktualizacje | Wymaga Node.js i Python |
| **Docker** | Izolowane środowisko, wszystkie zależności | Wymaga Docker |
| **Lokalna instalacja** | Pełna kontrola | Wymaga ręcznej instalacji zależności |

## Zobacz także

- [QUICKSTART.md](QUICKSTART.md) - Szybki start z Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Kompletny przewodnik użycia
- [README.md](../README.md) - Ogólna dokumentacja projektu
