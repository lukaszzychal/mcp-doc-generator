# Cursor Configuration with npx

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

This guide explains how to configure Cursor to use the MCP documentation server. Two installation methods are available:

1. **npx installation** (Recommended) - Easy, automatic Docker management, no local dependencies
2. **Docker installation** - Manual Docker setup, full control

## Configuration

### Step 1: Open Cursor Settings

1. Open Cursor
2. Go to **Settings** (or press `Cmd+,` on macOS / `Ctrl+,` on Windows/Linux)
3. Navigate to **Features** → **Model Context Protocol** (or search for "MCP")

### Step 2: Choose Installation Method

Choose one of the following installation methods:

## Method 1: npx Installation (Recommended)

The npx installation automatically manages Docker containers. You only need Docker installed and running - no Python, Graphviz, Pandoc, or other tools required!

### npx Configuration Options

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

### How npx Installation Works

When you use npx, the wrapper automatically:

1. Checks if Docker is installed and running
2. Builds Docker images if they don't exist
3. Starts Docker containers if they're not running
4. Runs the MCP server inside the Docker container

**No manual setup required!** Everything is handled automatically.

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

2. **Docker** and **Docker Compose** are installed
   - Check: `docker --version` and `docker compose version`
   - Install: https://docs.docker.com/get-docker/

3. **Docker daemon is running**
   - macOS/Windows: Start Docker Desktop application
   - Linux: `sudo systemctl start docker`
   - Verify: `docker info`

**That's it!** No Python, Graphviz, Pandoc, or other tools need to be installed locally. Everything runs in Docker containers.

## Troubleshooting

### Problem: npx cannot find package

**Solution:**
- Ensure you use the full path: `github:lukaszzychal/mcp-doc-generator`
- Check if repository is public
- Verify tag/branch exists

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
- Check if port 8080 is already in use
- Stop conflicting services on port 8080
- Check Docker logs: `docker compose logs`
- Try manually: `docker compose up -d`

### Problem: MCP tools not visible in Cursor

**Solution:**
1. Check Cursor logs: `~/Library/Application Support/Cursor/logs/` (macOS)
2. Restart Cursor
3. Verify configuration syntax (valid JSON)
4. Check if npx is working: `npx --version`

## Method 2: Docker Installation (Manual Setup)

This method requires manual Docker setup. Use this if you prefer full control over Docker containers or if npx installation doesn't work for you.

### Prerequisites

1. **Docker and Docker Compose** must be installed
2. **Start Docker containers:**
   ```bash
   docker compose up -d
   ```

### Docker Configuration

Add the following configuration to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "Documentation": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-documentation-server",
        "sh",
        "-c",
        "cd /app/src && PYTHONPATH=/app/src python server.py"
      ],
      "env": {
        "PYTHONPATH": "/app/src"
      }
    }
  }
}
```

**Alternative simpler Docker configuration:**

```json
{
  "mcpServers": {
    "Documentation": {
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

See [QUICKSTART.md](QUICKSTART.md) for detailed Docker setup instructions.

## See also

- [NPX_INSTALLATION.md](NPX_INSTALLATION.md) - Detailed npx installation guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start with Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Complete usage guide

---

<a name="polski"></a>
# Polski

## Przegląd

Ten przewodnik wyjaśnia jak skonfigurować Cursor do używania serwera MCP dokumentacji. Dostępne są dwie metody instalacji:

1. **Instalacja npx** (Zalecane) - Łatwa, automatyczne zarządzanie Dockerem, brak lokalnych zależności
2. **Instalacja Docker** - Ręczna konfiguracja Dockera, pełna kontrola

## Konfiguracja

### Krok 1: Otwórz ustawienia Cursor

1. Otwórz Cursor
2. Przejdź do **Settings** (lub naciśnij `Cmd+,` na macOS / `Ctrl+,` na Windows/Linux)
3. Przejdź do **Features** → **Model Context Protocol** (lub wyszukaj "MCP")

### Krok 2: Wybierz metodę instalacji

Wybierz jedną z następujących metod instalacji:

## Metoda 1: Instalacja npx (Zalecane)

Instalacja przez npx automatycznie zarządza kontenerami Docker. Potrzebujesz tylko zainstalowanego i uruchomionego Dockera - nie potrzebujesz Pythona, Graphviz, Pandoc ani innych narzędzi!

### Opcje konfiguracji npx

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

### Jak działa instalacja npx

Gdy używasz npx, wrapper automatycznie:

1. Sprawdza czy Docker jest zainstalowany i uruchomiony
2. Buduje obrazy Docker jeśli nie istnieją
3. Uruchamia kontenery Docker jeśli nie są uruchomione
4. Uruchamia serwer MCP wewnątrz kontenera Docker

**Brak ręcznej konfiguracji!** Wszystko jest obsługiwane automatycznie.

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

2. **Docker** i **Docker Compose** są zainstalowane
   - Sprawdź: `docker --version` i `docker compose version`
   - Zainstaluj: https://docs.docker.com/get-docker/

3. **Docker demon jest uruchomiony**
   - macOS/Windows: Uruchom aplikację Docker Desktop
   - Linux: `sudo systemctl start docker`
   - Zweryfikuj: `docker info`

**To wszystko!** Nie trzeba instalować Pythona, Graphviz, Pandoc ani innych narzędzi lokalnie. Wszystko działa w kontenerach Docker.

## Rozwiązywanie problemów

### Problem: npx nie znajduje pakietu

**Rozwiązanie:**
- Upewnij się, że używasz pełnej ścieżki: `github:lukaszzychal/mcp-doc-generator`
- Sprawdź czy repozytorium jest publiczne
- Zweryfikuj czy tag/gałąź istnieje

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
- Sprawdź czy port 8080 nie jest zajęty
- Zatrzymaj konfliktujące serwisy na porcie 8080
- Sprawdź logi Docker: `docker compose logs`
- Spróbuj ręcznie: `docker compose up -d`

### Problem: Narzędzia MCP nie są widoczne w Cursor

**Rozwiązanie:**
1. Sprawdź logi Cursor: `~/Library/Application Support/Cursor/logs/` (macOS)
2. Zrestartuj Cursor
3. Zweryfikuj składnię konfiguracji (poprawny JSON)
4. Sprawdź czy npx działa: `npx --version`

## Metoda 2: Instalacja Docker (Ręczna konfiguracja)

Ta metoda wymaga ręcznej konfiguracji Dockera. Użyj jej jeśli preferujesz pełną kontrolę nad kontenerami Docker lub jeśli instalacja przez npx nie działa.

### Wymagania wstępne

1. **Docker i Docker Compose** muszą być zainstalowane
2. **Uruchom kontenery Docker:**
   ```bash
   docker compose up -d
   ```

### Konfiguracja Docker

Dodaj następującą konfigurację do ustawień MCP w Cursor:

```json
{
  "mcpServers": {
    "Documentation": {
      "command": "docker",
      "args": [
        "exec",
        "-i",
        "mcp-documentation-server",
        "sh",
        "-c",
        "cd /app/src && PYTHONPATH=/app/src python server.py"
      ],
      "env": {
        "PYTHONPATH": "/app/src"
      }
    }
  }
}
```

**Alternatywna prostsza konfiguracja Docker:**

```json
{
  "mcpServers": {
    "Documentation": {
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

Zobacz [QUICKSTART.md](QUICKSTART.md) dla szczegółowych instrukcji konfiguracji Docker.

## Zobacz także

- [NPX_INSTALLATION.md](NPX_INSTALLATION.md) - Szczegółowy przewodnik instalacji npx
- [QUICKSTART.md](QUICKSTART.md) - Szybki start z Docker
- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Kompletny przewodnik użycia

