# MCP Documentation Server

MCP (Model Context Protocol) server for generating technical documentation with diagrams.

> **📢 Status:** Serwer MCP jest obecnie testowany w pracy.

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

> **📢 Status:** The MCP server is currently being tested in production at work.

## 🚀 Quick Start

```bash
# 1. Start Docker containers
docker compose up -d

# 2. Use MCP client with your own prompt
python3 scripts/mcp_client.py -f examples/prompts/prompt.txt

# 3. Or use in Cursor - open conversation and use MCP tools
```

## 📦 Installation via npx

You can install and run the server directly via `npx` without cloning the repository:

```bash
# Latest version from main branch
npx github:lukaszzychal/mcp-doc-generator

# Specific version (tag)
npx github:lukaszzychal/mcp-doc-generator#v0.1.2

# Specific branch
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

**Requirements:**
- Node.js >= 14.0.0 (for npx)
- Python >= 3.10 (for the MCP server)
- Python dependencies installed (see [requirements.txt](requirements.txt))

For detailed instructions, see [NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md).

## 📦 Stable Release

**Latest stable version:** [v0.1.2](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.2)

For production use, we recommend using a tagged release:

```bash
# Clone specific version
git clone --branch v0.1.2 https://github.com/lukaszzychal/mcp-doc-generator.git

# Or checkout tag in existing repo
git checkout v0.1.2
```

**Available releases:**
- [v0.1.2](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.2) - CI/CD optimizations, Docker caching improvements
- [v0.1.1](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.1) - Previous stable release
- [v0.1.0](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.0) - Initial release

> **Note:** The `main` branch contains the latest development version. For production, use a tagged release.

### Alternative: Distroless Image (Smaller & More Secure)

For a smaller, more secure image (~300-500MB smaller):

```bash
docker compose -f docker-compose.distroless.yml up -d
```

See [DOCKER_BUILD_OPTIMIZATION.md](docs/DOCKER_BUILD_OPTIMIZATION.md) for details.

## 📚 Documentation

- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Complete usage guide (locally and with Cursor)
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Quick start in 5 minutes
- **[NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md)** - Installation via npx
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Project structure
- **[TEST_RESULTS_MCP.md](docs/TEST_RESULTS_MCP.md)** - Test results for all tools
- **[DOCKER_CONTAINERS_EXPLAINED.md](docs/DOCKER_CONTAINERS_EXPLAINED.md)** - Docker containers usage explained

## 🛠️ Available Tools

1. **generate_c4_diagram** - C4 architecture diagrams (context, container, component, code)
2. **generate_uml_diagram** - UML diagrams (class, component, deployment, package, activity, usecase)
3. **generate_sequence_diagram** - PlantUML sequence diagrams
4. **generate_flowchart** - Mermaid flowcharts
5. **generate_mermaid_sequence** - Mermaid sequence diagrams
6. **generate_gantt** - Gantt charts
7. **generate_dependency_graph** - Graphviz dependency graphs
8. **generate_cloud_diagram** - draw.io cloud architecture diagrams
9. **export_to_pdf** - Markdown to PDF export
10. **export_to_docx** - Markdown to DOCX export
11. **create_document_from_template** - Documents from templates (ADR, API Spec, C4, Microservices)

## 📁 Project Structure

```
MCPServer/
├── src/              # MCP server source code
├── scripts/          # Helper scripts (mcp_client.py, install.sh, generate_examples.py)
├── tests/            # Tests and test files
├── docs/             # Project documentation
├── examples/         # Usage examples
└── output/           # Output directory (mounted in Docker)
```

Details: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 💡 Usage Examples

### Locally (without Cursor)

```bash
# From file
python3 scripts/mcp_client.py -f examples/prompts/prompt.txt

# From command line
python3 scripts/mcp_client.py -p "Generate C4 context diagram for e-commerce. Save as output/diagram.png"

# From stdin
cat prompt.txt | python3 scripts/mcp_client.py
```

### With Cursor

1. Start containers: `docker compose up -d`
2. Open Cursor
3. Use MCP tools in conversation, e.g.:
   - "Generate C4 Context Diagram for e-commerce system"
   - "Create UML Class Diagram with User and Order classes"

## 🧪 Tests

```bash
# Tests for all MCP tools
python3 tests/test_mcp_local.py

# Cursor integration test
./tests/test_mcp_cursor_integration.sh
```

## 📖 More Information

- [Usage guide](docs/USAGE_GUIDE.md) - Detailed instructions
- [Quick start](docs/QUICKSTART.md) - Installation and configuration
- [Test results](docs/TEST_RESULTS_MCP.md) - Status of all tools
- [Examples](examples/example_usage.md) - Usage examples for each tool

## 🔧 Requirements

- Docker and Docker Compose (recommended)
- Python 3.10+ (required for MCP server)
- Node.js >= 14.0.0 (optional, for npx installation)
- Cursor (optional, for integration)

## 📝 License

See [LICENSE](LICENSE)

---

<a name="polski"></a>
# Polski

MCP (Model Context Protocol) server do generowania dokumentacji technicznej z diagramami.

> **📢 Status:** Serwer MCP jest obecnie testowany w pracy.

## 🚀 Szybki Start

```bash
# 1. Uruchom kontenery Docker
docker compose up -d

# 2. Użyj klienta MCP z własnym promptem
python3 scripts/mcp_client.py -f examples/prompts/prompt.txt

# 3. Lub użyj w Cursor - otwórz konwersację i użyj narzędzi MCP
```

## 📦 Instalacja przez npx

Możesz zainstalować i uruchomić serwer bezpośrednio przez `npx` bez klonowania repozytorium:

```bash
# Najnowsza wersja z gałęzi main
npx github:lukaszzychal/mcp-doc-generator

# Konkretna wersja (tag)
npx github:lukaszzychal/mcp-doc-generator#v0.1.2

# Konkretna gałąź
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

**Wymagania:**
- Node.js >= 14.0.0 (dla npx)
- Python >= 3.10 (dla serwera MCP)
- Zainstalowane zależności Python (zobacz [requirements.txt](requirements.txt))

Szczegółowe instrukcje: [NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md).

## 📦 Stabilna Wersja

**Najnowsza stabilna wersja:** [v0.1.2](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.2)

Do użycia produkcyjnego zalecamy użycie tagowanej wersji:

```bash
# Sklonuj konkretną wersję
git clone --branch v0.1.2 https://github.com/lukaszzychal/mcp-doc-generator.git

# Lub przełącz się na tag w istniejącym repo
git checkout v0.1.2
```

**Dostępne wydania:**
- [v0.1.2](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.2) - Optymalizacje CI/CD, ulepszenia cache Docker
- [v0.1.1](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.1) - Poprzednia stabilna wersja
- [v0.1.0](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.0) - Wersja początkowa

> **Uwaga:** Branch `main` zawiera najnowszą wersję deweloperską. Do produkcji używaj tagowanej wersji.

### Alternatywa: Obraz Distroless (Mniejszy i Bezpieczniejszy)

Dla mniejszego, bardziej bezpiecznego obrazu (~300-500MB mniej):

```bash
docker compose -f docker-compose.distroless.yml up -d
```

Zobacz [DOCKER_BUILD_OPTIMIZATION.md](docs/DOCKER_BUILD_OPTIMIZATION.md) dla szczegółów.

## 📚 Dokumentacja

- **[USAGE_GUIDE.md](docs/USAGE_GUIDE.md)** - Kompletny przewodnik użycia (lokalnie i z Cursor)
- **[QUICKSTART.md](docs/QUICKSTART.md)** - Szybki start w 5 minut
- **[NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md)** - Instalacja przez npx
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Struktura projektu
- **[TEST_RESULTS_MCP.md](docs/TEST_RESULTS_MCP.md)** - Wyniki testów wszystkich narzędzi

## 🛠️ Dostępne Narzędzia

1. **generate_c4_diagram** - Diagramy architektury C4 (context, container, component, code)
2. **generate_uml_diagram** - Diagramy UML (class, component, deployment, package, activity, usecase)
3. **generate_sequence_diagram** - Diagramy sekwencji PlantUML
4. **generate_flowchart** - Flowchart Mermaid
5. **generate_mermaid_sequence** - Diagramy sekwencji Mermaid
6. **generate_gantt** - Wykresy Gantta
7. **generate_dependency_graph** - Grafy zależności Graphviz
8. **generate_cloud_diagram** - Diagramy architektury chmurowej draw.io
9. **export_to_pdf** - Eksport markdown do PDF
10. **export_to_docx** - Eksport markdown do DOCX
11. **create_document_from_template** - Dokumenty z szablonów (ADR, API Spec, C4, Microservices)

## 📁 Struktura Projektu

```
MCPServer/
├── src/              # Kod źródłowy serwera MCP
├── scripts/          # Skrypty pomocnicze (mcp_client.py, install.sh)
├── tests/            # Testy i pliki testowe
├── docs/             # Dokumentacja projektu
├── examples/         # Przykłady użycia
└── output/           # Katalog wyjściowy (zmountowany w Docker)
```

Szczegóły: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## 💡 Przykłady Użycia

### Lokalnie (bez Cursor)

```bash
# Z pliku
python3 scripts/mcp_client.py -f examples/prompts/prompt.txt

# Z linii komend
python3 scripts/mcp_client.py -p "Generate C4 context diagram for e-commerce. Save as output/diagram.png"

# Z stdin
cat prompt.txt | python3 scripts/mcp_client.py
```

### Z Cursor

1. Uruchom kontenery: `docker compose up -d`
2. Otwórz Cursor
3. Użyj narzędzi MCP w konwersacji, np.:
   - "Wygeneruj C4 Context Diagram dla systemu e-commerce"
   - "Utwórz UML Class Diagram z klasami User i Order"

## 🧪 Testy

```bash
# Testy wszystkich narzędzi MCP
python3 tests/test_mcp_local.py

# Test integracji z Cursor
./tests/test_mcp_cursor_integration.sh

# Podstawowe testy systemu
./scripts/test.sh
```

## 📖 Więcej Informacji

- [Przewodnik użycia](docs/USAGE_GUIDE.md) - Szczegółowe instrukcje
- [Szybki start](docs/QUICKSTART.md) - Instalacja i konfiguracja
- [Wyniki testów](docs/TEST_RESULTS_MCP.md) - Status wszystkich narzędzi
- [Przykłady](examples/example_usage.md) - Przykłady użycia każdego narzędzia

## 🔧 Wymagania

- Docker i Docker Compose (zalecane)
- Python 3.10+ (wymagane dla serwera MCP)
- Node.js >= 14.0.0 (opcjonalnie, dla instalacji przez npx)
- Cursor (opcjonalnie, dla integracji)

## 📝 Licencja

Zobacz [LICENSE](LICENSE)
