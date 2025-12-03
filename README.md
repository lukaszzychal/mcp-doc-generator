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
npx github:lukaszzychal/mcp-doc-generator#v0.1.7

# Specific branch
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

**Requirements:**
- Node.js >= 14.0.0 (for npx)
- Docker and Docker Compose (automatically managed by wrapper)
- Docker daemon must be running

**No local Python, Graphviz, Pandoc, or other tools required!** Everything runs in Docker containers.

For detailed instructions, see [NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md).

### OpenAI Image Generation (Optional)

To use AI image generation tools (`generate_image_openai`, `generate_icon_openai`, `generate_illustration_openai`):

1. **Set environment variable:**
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

2. **Get API key:** [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

3. **Pricing:** $0.04-0.12 per image (see [ROADMAP.md](docs/ROADMAP.md) for details)

**Note:** OpenAI tools are optional. All other tools work without API key. If API key is not configured, you'll receive a helpful error message with setup instructions.

#### Automatic Polish Text Translation

The OpenAI image generation tools automatically detect and translate Polish words to English for better text rendering in generated images. DALL-E 3 has limited support for non-English text, especially with diacritics.

##### Why PL→EN Translation is Required

**DALL-E 3 Limitations:**
- **Poor Polish text rendering**: DALL-E 3 struggles with Polish characters (ą, ć, ę, ł, ń, ó, ś, ź, ż), often producing misspellings like:
  - "Struktura" → "Strutira" or "STRUTIRA"
  - "Elastyczny" → "Elastncy" or "ELASTNCY"
  - "DOBRY KOD" → "DOBBRY KOD" or "GODE CODE"
- **Diacritics not supported**: Polish diacritics are frequently omitted or replaced with incorrect characters
- **English-first training**: DALL-E 3 was primarily trained on English text, resulting in much better accuracy for English
- **Text rendering quality**: English text in images is significantly more accurate and readable

**Why We Don't Support Direct Polish:**
1. **Technical limitation**: This is a DALL-E 3 model limitation, not a bug in our code
2. **Quality assurance**: English text ensures professional, readable diagrams
3. **User experience**: Automatic translation provides the best results without user intervention
4. **Future-proof**: If OpenAI improves Polish support, we can easily adjust the translation logic

**Our Solution:**
Instead of fighting DALL-E 3's limitations, we automatically translate Polish to English before image generation, ensuring:
- ✅ Accurate text rendering
- ✅ Professional-looking diagrams
- ✅ No manual translation needed
- ✅ Seamless user experience (you can still use Polish prompts!)

**How it works (Hybrid Approach):**
1. **DALL-E 3 generates graphics without text** - Visual elements only (shapes, icons, colors)
2. **Text labels are extracted** from your prompt automatically
3. **PIL/Pillow adds text overlay** - Perfect text rendering with precise positioning
4. **Result**: Beautiful graphics from DALL-E 3 + perfect text from PIL

**Benefits:**
- ✅ **100% accurate text** - No misspellings or errors
- ✅ **Supports all languages** - Polish with diacritics works perfectly
- ✅ **Professional quality** - Clean, readable labels
- ✅ **Consistent results** - Same text every time

**Technical details:**
- Automatically detects Polish words and translates for prompt clarity
- Extracts text labels (titles, acronyms, labels) from your prompt
- Uses DejaVu Sans font (supports Polish characters)
- Positions text intelligently (central labels, branch labels for mind maps)

**Example:**
- Input prompt: `"Diagram z tytułem 'DOBRY KOD' pokazujący Struktura SOLID"`
- Enhanced prompt: `"Diagram with title 'GOOD CODE' showing Structure SOLID"` + instruction for English text rendering

You can use Polish in your prompts - the system will automatically handle translation for text that appears in the image.

#### Usage Examples

**In Cursor (Recommended):**
Simply describe what you want in natural language:
```
Wygeneruj ilustrację mapy myśli "Zasady dobrego kodu" z centralnym węzłem 
"Dobry kod = prosty, elastyczny, odporny" i 5 gałęziami: SOLID, DRY, KISS, GRASP, CUPID.
Zapisz jako output/mindmap.png
```

Cursor automatically:
1. Recognizes this is an illustration request
2. Calls `generate_illustration_openai` via MCP protocol
3. Translates Polish text to English automatically
4. Generates the image

**Using mcp_client.py:**
```bash
# Set API key
export OPENAI_API_KEY=sk-...

# Generate illustration from prompt
python3 scripts/mcp_client.py -p "Wygeneruj ilustrację plakatu z zasadami programowania. Zapisz jako output/poster.png"

# Or from file
python3 scripts/mcp_client.py -f prompt.txt
```

**No Python code needed!** Just describe what you want - the MCP server handles everything automatically.

## 📦 Stable Release

**Latest stable version:** [v0.1.7](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.7)

For production use, we recommend using a tagged release:

```bash
# Clone specific version
git clone --branch v0.1.7 https://github.com/lukaszzychal/mcp-doc-generator.git

# Or checkout tag in existing repo
git checkout v0.1.7
```

**Available releases:**
- [v0.1.7](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.7) - Update version to 0.1.7 and add contact information
- [v0.1.6](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.6) - Fix npx installation (include Docker files)
- [v0.1.5](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.5) - Docker-based automatic container management
- [v0.1.4](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.4) - Commit message rules and validation hooks
- [v0.1.3](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.3) - npx installation support, Cursor rules
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
- **[CURSOR_NPX_SETUP.md](docs/CURSOR_NPX_SETUP.md)** - Cursor configuration guide (npx and Docker)
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
9. **generate_image_openai** - AI image generation using DALL-E 3 (requires OPENAI_API_KEY)
10. **generate_icon_openai** - AI icon generation using DALL-E 3 (requires OPENAI_API_KEY)
11. **generate_illustration_openai** - AI illustration generation using DALL-E 3 (requires OPENAI_API_KEY)
12. **export_to_pdf** - Markdown to PDF export
13. **export_to_docx** - Markdown to DOCX export
14. **create_document_from_template** - Documents from templates (ADR, API Spec, C4, Microservices)

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

Two installation methods are available:

#### Method 1: Docker (Recommended for Production)

1. Start containers: `docker compose up -d`
2. Configure Cursor MCP settings:
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
3. Restart Cursor
4. Use MCP tools in conversation, e.g.:
   - "Generate C4 Context Diagram for e-commerce system"
   - "Create UML Class Diagram with User and Order classes"

#### Method 2: npx (Recommended - Automatic Docker Management)

1. Make sure Docker is installed and running
2. Configure Cursor MCP settings:
   ```json
   {
     "mcpServers": {
       "mcp-doc-generator": {
         "command": "npx",
         "args": [
           "github:lukaszzychal/mcp-doc-generator#v0.1.7"
         ]
       }
     }
   }
   ```
3. Restart Cursor
4. The wrapper automatically manages Docker containers - no manual setup needed!
5. Use MCP tools in conversation

**See [CURSOR_NPX_SETUP.md](docs/CURSOR_NPX_SETUP.md) for detailed configuration instructions.**

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

### For npx Installation (Recommended)
- **Node.js** >= 14.0.0 (for npx)
- **Docker** and **Docker Compose** (automatically managed)
- **Docker daemon** must be running

### For Direct Docker Installation
- **Docker** and **Docker Compose**
- Manual container management

### Optional
- **Cursor** (for IDE integration)

## 📝 License

See [LICENSE](LICENSE)

## 💬 Community & Support

- **Discussions:** [GitHub Discussions](https://github.com/lukaszzychal/mcp-doc-generator/discussions)
- **Issues:** [GitHub Issues](https://github.com/lukaszzychal/mcp-doc-generator/issues)
- **Contact:** lukasz.zychal.dev@gmail.com

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
npx github:lukaszzychal/mcp-doc-generator#v0.1.7

# Konkretna gałąź
npx github:lukaszzychal/mcp-doc-generator#feat/test-npx-installation
```

**Wymagania:**
- Node.js >= 14.0.0 (dla npx)
- Docker i Docker Compose (automatycznie zarządzane przez wrapper)
- Docker demon musi być uruchomiony

**Nie trzeba instalować Pythona, Graphviz, Pandoc ani innych narzędzi lokalnie!** Wszystko działa w kontenerach Docker.

Szczegółowe instrukcje: [NPX_INSTALLATION.md](docs/NPX_INSTALLATION.md).

### Generowanie Obrazów OpenAI (Opcjonalne)

Aby używać narzędzi generowania obrazów AI (`generate_image_openai`, `generate_icon_openai`, `generate_illustration_openai`):

1. **Ustaw zmienną środowiskową:**
   ```bash
   export OPENAI_API_KEY=sk-...
   ```

2. **Pobierz klucz API:** [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)

3. **Cennik:** $0.04-0.12 za obraz (zobacz [ROADMAP.md](docs/ROADMAP.md) dla szczegółów)

**Uwaga:** Narzędzia OpenAI są opcjonalne. Wszystkie inne narzędzia działają bez klucza API. Jeśli klucz API nie jest skonfigurowany, otrzymasz pomocny komunikat błędu z instrukcjami konfiguracji.

#### Automatyczne Tłumaczenie Polskiego Tekstu

Narzędzia generowania obrazów OpenAI automatycznie wykrywają i tłumaczą polskie słowa na angielski, aby zapewnić lepsze renderowanie tekstu w generowanych obrazach. DALL-E 3 ma ograniczone wsparcie dla tekstu w językach innych niż angielski, szczególnie dla znaków diakrytycznych.

##### Dlaczego Mapowanie PL→EN jest Wymagane

**Ograniczenia DALL-E 3:**
- **Słabe renderowanie polskiego tekstu**: DALL-E 3 ma problemy z polskimi znakami (ą, ć, ę, ł, ń, ó, ś, ź, ż), często generując błędy ortograficzne jak:
  - "Struktura" → "Strutira" lub "STRUTIRA"
  - "Elastyczny" → "Elastncy" lub "ELASTNCY"
  - "DOBRY KOD" → "DOBBRY KOD" lub "GODE CODE"
- **Brak wsparcia dla znaków diakrytycznych**: Polskie znaki diakrytyczne są często pomijane lub zastępowane nieprawidłowymi znakami
- **Trening głównie na angielskim**: DALL-E 3 był głównie trenowany na tekście angielskim, co daje znacznie lepszą dokładność dla angielskiego
- **Jakość renderowania tekstu**: Tekst angielski w obrazach jest znacznie bardziej dokładny i czytelny

**Dlaczego Nie Obsługujemy Bezpośrednio Polskiego:**
1. **Ograniczenie techniczne**: To jest ograniczenie modelu DALL-E 3, a nie błąd w naszym kodzie
2. **Zapewnienie jakości**: Tekst angielski zapewnia profesjonalne, czytelne diagramy
3. **Doświadczenie użytkownika**: Automatyczne tłumaczenie zapewnia najlepsze wyniki bez interwencji użytkownika
4. **Przyszłościowość**: Jeśli OpenAI poprawi wsparcie dla polskiego, możemy łatwo dostosować logikę tłumaczenia

**Nasze Rozwiązanie:**
Zamiast walczyć z ograniczeniami DALL-E 3, automatycznie tłumaczymy polski na angielski przed generowaniem obrazu, zapewniając:
- ✅ Dokładne renderowanie tekstu
- ✅ Profesjonalnie wyglądające diagramy
- ✅ Brak potrzeby ręcznego tłumaczenia
- ✅ Płynne doświadczenie użytkownika (możesz nadal używać polskich promptów!)

**Jak to działa (Podejście Hybrydowe):**
1. **DALL-E 3 generuje grafikę bez tekstu** - Tylko elementy wizualne (kształty, ikony, kolory)
2. **Etykiety tekstowe są wyodrębniane** z Twojego promptu automatycznie
3. **PIL/Pillow dodaje nakładkę tekstową** - Doskonałe renderowanie tekstu z precyzyjnym pozycjonowaniem
4. **Wynik**: Piękna grafika z DALL-E 3 + doskonały tekst z PIL

**Zalety:**
- ✅ **100% dokładny tekst** - Brak błędów ortograficznych
- ✅ **Obsługuje wszystkie języki** - Polski z diakrytykami działa doskonale
- ✅ **Profesjonalna jakość** - Czyste, czytelne etykiety
- ✅ **Spójne wyniki** - Ten sam tekst za każdym razem

**Szczegóły techniczne:**
- Automatycznie wykrywa polskie słowa i tłumaczy dla jasności promptu
- Wyodrębnia etykiety tekstowe (tytuły, akronimy, etykiety) z Twojego promptu
- Używa czcionki DejaVu Sans (obsługuje polskie znaki)
- Inteligentnie pozycjonuje tekst (etykiety centralne, etykiety gałęzi dla map myśli)

**Przykład:**
- Prompt wejściowy: `"Diagram z tytułem 'DOBRY KOD' pokazujący Struktura SOLID"`
- Prompt ulepszony: `"Diagram with title 'GOOD CODE' showing Structure SOLID"` + instrukcja renderowania tekstu po angielsku

Możesz używać polskiego w swoich promptach - system automatycznie obsłuży tłumaczenie dla tekstu, który pojawia się na obrazie.

#### Przykłady Użycia

**W Cursor (Zalecane):**
Po prostu opisz co chcesz w języku naturalnym:
```
Wygeneruj ilustrację mapy myśli "Zasady dobrego kodu" z centralnym węzłem 
"Dobry kod = prosty, elastyczny, odporny" i 5 gałęziami: SOLID, DRY, KISS, GRASP, CUPID.
Zapisz jako output/mindmap.png
```

Cursor automatycznie:
1. Rozpoznaje, że to prośba o ilustrację
2. Wywołuje `generate_illustration_openai` przez protokół MCP
3. Tłumaczy polski tekst na angielski automatycznie
4. Generuje obraz

**Używając mcp_client.py:**
```bash
# Ustaw klucz API
export OPENAI_API_KEY=sk-...

# Wygeneruj ilustrację z promptu
python3 scripts/mcp_client.py -p "Wygeneruj ilustrację plakatu z zasadami programowania. Zapisz jako output/poster.png"

# Lub z pliku
python3 scripts/mcp_client.py -f prompt.txt
```

**Nie trzeba pisać kodu Python!** Wystarczy opisać co chcesz - serwer MCP obsługuje wszystko automatycznie.

## 📦 Stabilna Wersja

**Najnowsza stabilna wersja:** [v0.1.7](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.7)

Do użycia produkcyjnego zalecamy użycie tagowanej wersji:

```bash
# Sklonuj konkretną wersję
git clone --branch v0.1.7 https://github.com/lukaszzychal/mcp-doc-generator.git

# Lub przełącz się na tag w istniejącym repo
git checkout v0.1.7
```

**Dostępne wydania:**
- [v0.1.7](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.7) - Aktualizacja wersji do 0.1.7 i dodanie informacji kontaktowej
- [v0.1.6](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.6) - Naprawa instalacji npx (zawiera pliki Docker)
- [v0.1.5](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.5) - Automatyczne zarządzanie kontenerami Docker
- [v0.1.4](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.4) - Reguły commitów i hooki walidacji
- [v0.1.3](https://github.com/lukaszzychal/mcp-doc-generator/releases/tag/v0.1.3) - Wsparcie instalacji npx, reguły Cursor
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
- **[CURSOR_NPX_SETUP.md](docs/CURSOR_NPX_SETUP.md)** - Przewodnik konfiguracji Cursor (npx i Docker)
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

Dostępne są dwie metody instalacji:

#### Metoda 1: Docker (Zalecane dla produkcji)

1. Uruchom kontenery: `docker compose up -d`
2. Skonfiguruj ustawienia MCP w Cursor:
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
3. Zrestartuj Cursor
4. Użyj narzędzi MCP w konwersacji, np.:
   - "Wygeneruj C4 Context Diagram dla systemu e-commerce"
   - "Utwórz UML Class Diagram z klasami User i Order"

#### Metoda 2: npx (Zalecane - Automatyczne zarządzanie Dockerem)

1. Upewnij się, że Docker jest zainstalowany i uruchomiony
2. Skonfiguruj ustawienia MCP w Cursor:
   ```json
   {
     "mcpServers": {
       "mcp-doc-generator": {
         "command": "npx",
         "args": [
           "github:lukaszzychal/mcp-doc-generator#v0.1.7"
         ]
       }
     }
   }
   ```
3. Zrestartuj Cursor
4. Wrapper automatycznie zarządza kontenerami Docker - brak ręcznej konfiguracji!
5. Użyj narzędzi MCP w konwersacji

**Zobacz [CURSOR_NPX_SETUP.md](docs/CURSOR_NPX_SETUP.md) dla szczegółowych instrukcji konfiguracji.**

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

### Dla instalacji npx (Zalecane)
- **Node.js** >= 14.0.0 (dla npx)
- **Docker** i **Docker Compose** (automatycznie zarządzane)
- **Docker demon** musi być uruchomiony

### Dla bezpośredniej instalacji Docker
- **Docker** i **Docker Compose**
- Ręczne zarządzanie kontenerami

### Opcjonalne
- **Cursor** (dla integracji z IDE)

## 📝 Licencja

Zobacz [LICENSE](LICENSE)

## 💬 Społeczność i Wsparcie

- **Dyskusje:** [GitHub Discussions](https://github.com/lukaszzychal/mcp-doc-generator/discussions)
- **Zgłoszenia:** [GitHub Issues](https://github.com/lukaszzychal/mcp-doc-generator/issues)
- **Kontakt:** lukasz.zychal.dev@gmail.com
