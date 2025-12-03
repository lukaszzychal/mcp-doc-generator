# Configuration Files Explained / Wyjaśnienie Plików Konfiguracyjnych

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

This document explains the configuration files in the project root that are used for deployment and package management.

## Files

### 1. `railway.toml` - Railway Deployment Configuration

**What is Railway?**
Railway is a cloud platform (similar to Heroku) that makes it easy to deploy applications. You connect your GitHub repo, and Railway automatically builds and deploys your app.

**What does this file do?**
```toml
[build]
builder = "DOCKERFILE"              # Use Dockerfile to build the app
dockerfilePath = "Dockerfile"        # Location of Dockerfile

[deploy]
startCommand = "python src/server.py"  # Command to start the server
# Note: healthcheckPath removed - MCP server uses stdio protocol, not HTTP
# Railway monitors process health via process status instead
restartPolicyType = "ON_FAILURE"     # Restart if app crashes
restartPolicyMaxRetries = 10         # Try 10 times before giving up
```

**Important Note about Stdio Servers:**
This MCP server communicates via stdio (stdin/stdout), not HTTP. Therefore:
- ❌ No HTTP healthcheck endpoints (removed `healthcheckPath`)
- ✅ Railway monitors process health via process status
- ✅ Process-based restart policies work correctly
- ⚠️ MCP servers are typically used locally; Railway deployment is for specific use cases

**When is it used?**
- When you deploy to Railway platform
- Railway reads this file to know how to build and run your app
- You don't need to manually configure anything in Railway dashboard

**Example workflow:**
1. Push code to GitHub
2. Connect repo to Railway
3. Railway reads `railway.toml`
4. Railway builds Docker image
5. Railway runs `python src/server.py`
6. Your app is live!

---

### 2. `fly.toml` - Fly.io Deployment Configuration

**What is Fly.io?**
Fly.io is another cloud platform that runs apps close to users (edge computing). Good for global applications.

**What does this file do?**
```toml
app = "mcp-documentation-server"    # App name on Fly.io
primary_region = "waw"                # Warsaw, Poland (closest to you)

[build]
  dockerfile = "Dockerfile"         # Use Dockerfile

[env]
  PLANTUML_SERVER = "http://localhost:8080"  # Environment variables
  PYTHONPATH = "/app"
  PYTHONUNBUFFERED = "1"

[[services]]
  internal_port = 8080              # Port inside container
  protocol = "tcp"

  [[services.ports]]
    port = 80                        # HTTP port
    handlers = ["http"]
    force_https = true              # Redirect HTTP to HTTPS

  [[services.ports]]
    port = 443                       # HTTPS port
    handlers = ["tls", "http"]

[[vm]]
  cpu_kind = "shared"               # Shared CPU (cheaper)
  cpus = 1                          # 1 CPU core
  memory_mb = 1024                  # 1GB RAM

[mounts]
  source = "output_data"            # Persistent storage
  destination = "/app/output"       # Where to mount it
```

**When is it used?**
- When you deploy to Fly.io platform
- Fly.io uses this to configure networking, resources, and storage

**Key differences from Railway:**
- More detailed configuration (networking, CPU, memory)
- Can specify region (Warsaw)
- Persistent storage configuration
- More control over infrastructure

---

### 3. `pyproject.toml` - Python Project Configuration

**What is pyproject.toml?**
Modern Python standard for project configuration. Replaces `setup.py` and `requirements.txt` in one file.

**What does this file do?**

#### Project Metadata
```toml
[project]
name = "mcp-documentation-server"    # Package name
version = "0.1.0"                    # Version number
description = "MCP Server for generating technical documentation with diagrams"
authors = [{name = "Lukasz Zychal"}]
readme = "README.md"
requires-python = ">=3.10"          # Minimum Python version
```

#### Dependencies
```toml
dependencies = [
    "mcp>=0.9.0",                    # MCP protocol library
    "requests>=2.31.0",              # HTTP requests
    "aiohttp>=3.9.0",                # Async HTTP
    "python-multipart>=0.0.6",       # File uploads
    "pydantic>=2.5.0",               # Data validation
]
```

#### Development Dependencies
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",                # Testing framework
    "pytest-asyncio>=0.21.0",       # Async testing
    "black>=23.0.0",                 # Code formatter
    "ruff>=0.1.0",                   # Linter
]
```

#### Build System
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"
```

#### Code Quality Tools
```toml
[tool.black]
line-length = 100                   # Max line length
target-version = ['py310']          # Python 3.10+

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F"]                 # Error and failure checks
```

**When is it used?**
- When installing the package: `pip install .`
- When building the package: `python -m build`
- When running linters/formatters: `black .`, `ruff check .`
- Modern Python tools read this automatically

**Benefits:**
- ✅ One file instead of multiple (`setup.py`, `requirements.txt`, `setup.cfg`)
- ✅ Standard format (PEP 518, PEP 621)
- ✅ Tool configuration in one place
- ✅ Better dependency management

---

## Comparison Table

| File | Purpose | When Used | Platform |
|------|---------|-----------|----------|
| `railway.toml` | Railway deployment config | Deploying to Railway | Railway.app |
| `fly.toml` | Fly.io deployment config | Deploying to Fly.io | Fly.io |
| `pyproject.toml` | Python package config | Installing/building package | Local/PyPI |

---

## Do You Need All Three?

**Short answer:** No, but they serve different purposes.

- **`pyproject.toml`** - Always needed (Python project standard)
- **`railway.toml`** - Only if deploying to Railway
- **`fly.toml`** - Only if deploying to Fly.io

You can have both deployment configs and choose which platform to use, or remove the one you don't need.

---

<a name="polski"></a>
# Polski

## Przegląd

Ten dokument wyjaśnia pliki konfiguracyjne w głównym katalogu projektu, które są używane do wdrożenia i zarządzania pakietami.

## Pliki

### 1. `railway.toml` - Konfiguracja Wdrożenia Railway

**Czym jest Railway?**
Railway to platforma chmurowa (podobna do Heroku), która ułatwia wdrażanie aplikacji. Łączysz repozytorium GitHub, a Railway automatycznie buduje i wdraża aplikację.

**Co robi ten plik?**
```toml
[build]
builder = "DOCKERFILE"              # Użyj Dockerfile do budowania
dockerfilePath = "Dockerfile"        # Lokalizacja Dockerfile

[deploy]
startCommand = "python src/server.py"  # Komenda uruchomienia serwera
# Uwaga: healthcheckPath usunięty - serwer MCP używa protokołu stdio, nie HTTP
# Railway monitoruje zdrowie procesu przez status procesu
restartPolicyType = "ON_FAILURE"     # Restart przy awarii
restartPolicyMaxRetries = 10         # Spróbuj 10 razy przed rezygnacją
```

**Ważna Uwaga o Serwerach Stdio:**
Ten serwer MCP komunikuje się przez stdio (stdin/stdout), nie przez HTTP. Dlatego:
- ❌ Brak endpointów HTTP healthcheck (usunięto `healthcheckPath`)
- ✅ Railway monitoruje zdrowie procesu przez status procesu
- ✅ Polityki restartu oparte na procesach działają poprawnie
- ⚠️ Serwery MCP są zazwyczaj używane lokalnie; wdrożenie na Railway jest dla specyficznych przypadków użycia

**Kiedy jest używany?**
- Przy wdrażaniu na platformę Railway
- Railway czyta ten plik, aby wiedzieć jak zbudować i uruchomić aplikację
- Nie musisz ręcznie konfigurować niczego w panelu Railway

**Przykładowy workflow:**
1. Wypchnij kod do GitHub
2. Połącz repo z Railway
3. Railway czyta `railway.toml`
4. Railway buduje obraz Docker
5. Railway uruchamia `python src/server.py`
6. Aplikacja działa!

---

### 2. `fly.toml` - Konfiguracja Wdrożenia Fly.io

**Czym jest Fly.io?**
Fly.io to kolejna platforma chmurowa, która uruchamia aplikacje blisko użytkowników (edge computing). Dobre dla globalnych aplikacji.

**Co robi ten plik?**
```toml
app = "mcp-documentation-server"    # Nazwa aplikacji na Fly.io
primary_region = "waw"                # Warszawa, Polska (najbliżej Ciebie)

[build]
  dockerfile = "Dockerfile"         # Użyj Dockerfile

[env]
  PLANTUML_SERVER = "http://localhost:8080"  # Zmienne środowiskowe
  PYTHONPATH = "/app"
  PYTHONUNBUFFERED = "1"

[[services]]
  internal_port = 8080              # Port wewnątrz kontenera
  protocol = "tcp"

  [[services.ports]]
    port = 80                        # Port HTTP
    handlers = ["http"]
    force_https = true              # Przekieruj HTTP na HTTPS

  [[services.ports]]
    port = 443                       # Port HTTPS
    handlers = ["tls", "http"]

[[vm]]
  cpu_kind = "shared"               # Współdzielony CPU (tańszy)
  cpus = 1                          # 1 rdzeń CPU
  memory_mb = 1024                  # 1GB RAM

[mounts]
  source = "output_data"            # Trwałe przechowywanie
  destination = "/app/output"       # Gdzie zamontować
```

**Kiedy jest używany?**
- Przy wdrażaniu na platformę Fly.io
- Fly.io używa tego do konfiguracji sieci, zasobów i przechowywania

**Kluczowe różnice od Railway:**
- Bardziej szczegółowa konfiguracja (sieć, CPU, pamięć)
- Można określić region (Warszawa)
- Konfiguracja trwałego przechowywania
- Więcej kontroli nad infrastrukturą

---

### 3. `pyproject.toml` - Konfiguracja Projektu Python

**Czym jest pyproject.toml?**
Nowoczesny standard Pythona dla konfiguracji projektu. Zastępuje `setup.py` i `requirements.txt` w jednym pliku.

**Co robi ten plik?**

#### Metadane Projektu
```toml
[project]
name = "mcp-documentation-server"    # Nazwa pakietu
version = "0.1.0"                    # Numer wersji
description = "MCP Server for generating technical documentation with diagrams"
authors = [{name = "Lukasz Zychal"}]
readme = "README.md"
requires-python = ">=3.10"          # Minimalna wersja Pythona
```

#### Zależności
```toml
dependencies = [
    "mcp>=0.9.0",                    # Biblioteka protokołu MCP
    "requests>=2.31.0",              # Zapytania HTTP
    "aiohttp>=3.9.0",                # Async HTTP
    "python-multipart>=0.0.6",       # Upload plików
    "pydantic>=2.5.0",               # Walidacja danych
]
```

#### Zależności Deweloperskie
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",                # Framework testowy
    "pytest-asyncio>=0.21.0",       # Testy async
    "black>=23.0.0",                 # Formatowanie kodu
    "ruff>=0.1.0",                   # Linter
]
```

#### System Budowania
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"
```

#### Narzędzia Jakości Kodu
```toml
[tool.black]
line-length = 100                   # Maksymalna długość linii
target-version = ['py310']          # Python 3.10+

[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F"]                 # Sprawdzanie błędów i niepowodzeń
```

**Kiedy jest używany?**
- Przy instalacji pakietu: `pip install .`
- Przy budowaniu pakietu: `python -m build`
- Przy uruchamianiu linterów/formatterów: `black .`, `ruff check .`
- Nowoczesne narzędzia Pythona czytają to automatycznie

**Korzyści:**
- ✅ Jeden plik zamiast wielu (`setup.py`, `requirements.txt`, `setup.cfg`)
- ✅ Standardowy format (PEP 518, PEP 621)
- ✅ Konfiguracja narzędzi w jednym miejscu
- ✅ Lepsze zarządzanie zależnościami

---

## Tabela Porównawcza

| Plik | Cel | Kiedy Używany | Platforma |
|------|-----|---------------|-----------|
| `railway.toml` | Konfiguracja wdrożenia Railway | Wdrażanie na Railway | Railway.app |
| `fly.toml` | Konfiguracja wdrożenia Fly.io | Wdrażanie na Fly.io | Fly.io |
| `pyproject.toml` | Konfiguracja pakietu Python | Instalacja/budowanie pakietu | Lokalnie/PyPI |

---

## Czy Potrzebujesz Wszystkich Trzech?

**Krótka odpowiedź:** Nie, ale służą różnym celom.

- **`pyproject.toml`** - Zawsze potrzebny (standard projektu Python)
- **`railway.toml`** - Tylko jeśli wdrażasz na Railway
- **`fly.toml`** - Tylko jeśli wdrażasz na Fly.io

Możesz mieć obie konfiguracje wdrożenia i wybrać którą platformę użyć, lub usunąć tę której nie potrzebujesz.

---

**Ostatnia aktualizacja:** 2025-01-24

