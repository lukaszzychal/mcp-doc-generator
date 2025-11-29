# npx Installation

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

The MCP server `mcp-doc-generator` can be installed and run directly via `npx`, allowing easy installation without cloning the repository.

## Requirements

- **Node.js** >= 14.0.0 (for npx)
- **Docker** and **Docker Compose** (for running the server and all dependencies)
- Docker daemon must be running

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
npx github:lukaszzychal/mcp-doc-generator#v0.1.6
```

### Option 3: Specific branch

```bash
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

## How it works?

1. `npx` downloads the repository from GitHub
2. Detects `package.json` with `bin` configuration
3. Runs Node.js wrapper (`bin/mcp-doc-generator.js`)
4. Wrapper automatically:
   - Checks if Docker is installed and running
   - Builds Docker images if they don't exist
   - Starts Docker containers if they're not running
   - Runs Python server in Docker container (`docker exec -i mcp-documentation-server python src/server.py`)
5. Server runs in stdio mode (stdin/stdout) according to MCP protocol

**No local installation required!** All dependencies (Python, Graphviz, Pandoc, PlantUML, Mermaid CLI) are included in Docker containers.

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
        "github:lukaszzychal/mcp-doc-generator#v0.1.6"
      ]
    }
  }
}
```

## Environment Requirements

### Docker Setup

The wrapper automatically manages Docker containers. You only need to:

1. **Install Docker** (if not already installed):
   - macOS: [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
   - Windows: [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

2. **Start Docker daemon**:
   - macOS/Windows: Start Docker Desktop application
   - Linux: `sudo systemctl start docker`

3. **Run npx** - the wrapper will automatically:
   - Check Docker availability
   - Build images if needed
   - Start containers if needed
   - Run the server

**No Python, Graphviz, Pandoc, or other tools need to be installed locally!** Everything runs in Docker containers.

### Environment variables

The server inside Docker container uses:
- `PLANTUML_SERVER=http://plantuml:8080` - PlantUML server (internal Docker network)
- `PYTHONPATH=/app` - Python path in container
- `PYTHONUNBUFFERED=1` - for better logging

These are automatically configured in the Docker container. You don't need to set them manually.

## Local Testing

To test installation locally:

```bash
# From project directory
npx .

# Or use test script
./tests/test_npx_installation.sh
```

## Troubleshooting

### Problem: "Docker is not installed or not found in PATH"

**Solution:**
- Install Docker Desktop (macOS/Windows) or Docker Engine (Linux)
- Make sure Docker is in PATH
- Check: `docker --version`

### Problem: "Docker daemon is not running"

**Solution:**
- macOS/Windows: Start Docker Desktop application
- Linux: `sudo systemctl start docker`
- Verify: `docker info`

### Problem: "Failed to build Docker images"

**Solution:**
- Check Docker daemon is running: `docker info`
- Check internet connection (needs to download base images)
- Check disk space: `docker system df`
- Try manually: `docker compose build`

### Problem: "Failed to start Docker containers"

**Solution:**
- Check if port 8080 is already in use: `lsof -i :8080` (macOS/Linux)
- Stop conflicting services on port 8080
- Check Docker logs: `docker compose logs`
- Try manually: `docker compose up -d`

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
| **npx** | Easy installation, automatic updates, no local dependencies | Requires Node.js and Docker |
| **Docker (direct)** | Full control, isolated environment | Requires manual setup |
| **Local installation** | Full control, no Docker needed | Requires manual installation of all dependencies (Python, Graphviz, Pandoc, etc.) |

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
- **Docker** i **Docker Compose** (do uruchomienia serwera i wszystkich zależności)
- Docker demon musi być uruchomiony

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
npx github:lukaszzychal/mcp-doc-generator#v0.1.6
```

### Opcja 3: Konkretna gałąź

```bash
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

## Jak to działa?

1. `npx` pobiera repozytorium z GitHub
2. Wykrywa `package.json` z konfiguracją `bin`
3. Uruchamia wrapper Node.js (`bin/mcp-doc-generator.js`)
4. Wrapper automatycznie:
   - Sprawdza czy Docker jest zainstalowany i uruchomiony
   - Buduje obrazy Docker jeśli nie istnieją
   - Uruchamia kontenery Docker jeśli nie są uruchomione
   - Uruchamia serwer Python w kontenerze Docker (`docker exec -i mcp-documentation-server python src/server.py`)
5. Serwer działa w trybie stdio (stdin/stdout) zgodnie z protokołem MCP

**Brak lokalnej instalacji!** Wszystkie zależności (Python, Graphviz, Pandoc, PlantUML, Mermaid CLI) są zawarte w kontenerach Docker.

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
        "github:lukaszzychal/mcp-doc-generator#v0.1.6"
      ]
    }
  }
}
```

## Wymagania środowiskowe

### Konfiguracja Docker

Wrapper automatycznie zarządza kontenerami Docker. Musisz tylko:

1. **Zainstalować Docker** (jeśli nie jest zainstalowany):
   - macOS: [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
   - Windows: [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

2. **Uruchomić Docker demon**:
   - macOS/Windows: Uruchom aplikację Docker Desktop
   - Linux: `sudo systemctl start docker`

3. **Uruchomić npx** - wrapper automatycznie:
   - Sprawdzi dostępność Docker
   - Zbuduje obrazy jeśli potrzeba
   - Uruchomi kontenery jeśli potrzeba
   - Uruchomi serwer

**Nie trzeba instalować Pythona, Graphviz, Pandoc ani innych narzędzi lokalnie!** Wszystko działa w kontenerach Docker.

### Zmienne środowiskowe

Serwer wewnątrz kontenera Docker używa:
- `PLANTUML_SERVER=http://plantuml:8080` - serwer PlantUML (wewnętrzna sieć Docker)
- `PYTHONPATH=/app` - ścieżka Python w kontenerze
- `PYTHONUNBUFFERED=1` - dla lepszego logowania

Te zmienne są automatycznie skonfigurowane w kontenerze Docker. Nie musisz ich ustawiać ręcznie.

## Testowanie lokalne

Aby przetestować instalację lokalnie:

```bash
# Z katalogu projektu
npx .

# Lub użyj skryptu testowego
./tests/test_npx_installation.sh
```

## Rozwiązywanie problemów

### Problem: "Docker is not installed or not found in PATH"

**Rozwiązanie:**
- Zainstaluj Docker Desktop (macOS/Windows) lub Docker Engine (Linux)
- Upewnij się, że Docker jest w PATH
- Sprawdź: `docker --version`

### Problem: "Docker daemon is not running"

**Rozwiązanie:**
- macOS/Windows: Uruchom aplikację Docker Desktop
- Linux: `sudo systemctl start docker`
- Zweryfikuj: `docker info`

### Problem: "Failed to build Docker images"

**Rozwiązanie:**
- Sprawdź czy Docker demon działa: `docker info`
- Sprawdź połączenie z internetem (potrzebne do pobrania obrazów bazowych)
- Sprawdź miejsce na dysku: `docker system df`
- Spróbuj ręcznie: `docker compose build`

### Problem: "Failed to start Docker containers"

**Rozwiązanie:**
- Sprawdź czy port 8080 nie jest zajęty: `lsof -i :8080` (macOS/Linux)
- Zatrzymaj konfliktujące serwisy na porcie 8080
- Sprawdź logi Docker: `docker compose logs`
- Spróbuj ręcznie: `docker compose up -d`

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
| **npx** | Łatwa instalacja, automatyczne aktualizacje, brak lokalnych zależności | Wymaga Node.js i Docker |
| **Docker (bezpośrednio)** | Pełna kontrola, izolowane środowisko | Wymaga ręcznej konfiguracji |
| **Lokalna instalacja** | Pełna kontrola, brak Dockera | Wymaga ręcznej instalacji wszystkich zależności (Python, Graphviz, Pandoc, itp.) |

## Zobacz także

- [QUICKSTART.md](QUICKSTART.md) - Szybki start z Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Kompletny przewodnik użycia
- [README.md](../README.md) - Ogólna dokumentacja projektu
