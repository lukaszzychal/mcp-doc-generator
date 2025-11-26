# How the MCP Server Works - Step by Step Explanation

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## 📋 Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Server Startup](#server-startup)
4. [Tool Registration](#tool-registration)
5. [Request Processing](#request-processing)
6. [Data Flow Example](#data-flow-example)
7. [Tool Implementation Details](#tool-implementation-details)

---

## Introduction

The MCP (Model Context Protocol) server is a server that communicates via the stdio (standard input/output) protocol, providing tools for generating technical documentation with diagrams.

### What is MCP?
MCP is a communication protocol between AI (e.g., Cursor) and external tools. The server listens on stdin and responds through stdout using JSON-RPC format.

---

## System Architecture

### 1. Docker Components

The system consists of **2 Docker containers**:

![Docker Architecture Diagram](../output/docs_architecture_diagram.png)

#### Container 1: `plantuml`
- **Image**: `plantuml/plantuml-server:jetty`
- **Port**: 8080
- **Function**: Renders PlantUML diagrams to PNG/SVG
- **Endpoint**: `http://localhost:8080/png` or `/svg`

#### Container 2: `mcp-server`
- **Image**: Built from `Dockerfile`
- **Function**: Main MCP server
- **Volumes**:
  - `./src` → `/app/src` (source code, read-only)
  - `./output` → `/app/output` (output directory, writable)
  - `./src/templates` → `/app/src/templates` (templates, read-only)
- **Dependencies**: Waits for `plantuml` to be healthy (healthcheck)

---

## Server Startup

### Step 1: Start Docker Containers

```bash
docker compose up -d
```

**What happens:**
1. Docker starts the `plantuml` container on port 8080
2. Docker checks the healthcheck of the `plantuml` container (curl to http://localhost:8080/)
3. When `plantuml` is healthy, it starts the `mcp-server` container
4. The `mcp-server` container runs the `src/server.py` script

### Step 2: MCP Server Initialization

In the `src/server.py` file:

```python
# Line 20: Create MCP server instance
app = Server("mcp-documentation-server")

# Line 429-440: Main startup function
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,      # stdin - read requests
            write_stream,     # stdout - send responses
            app.create_initialization_options()
        )
```

**What happens:**
1. The MCP server creates a stdio connection (stdin/stdout)
2. Listens for JSON-RPC requests coming through stdin
3. Sends responses through stdout

---

## Tool Registration

### Step 3: List Available Tools

When a client (e.g., Cursor) asks for available tools, the `list_tools()` function is called:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available documentation generation tools."""
    tools = []
    
    # Add PlantUML tools
    tools.extend([...])
    
    # Add Mermaid tools
    tools.extend([...])
    
    # Add Graphviz tools
    tools.append(...)
    
    # Add draw.io tools
    tools.append(...)
    
    # Add export tools
    tools.extend([...])
    
    return tools
```

**What happens:**
1. Client sends a `tools/list` request through stdin
2. Server calls `list_tools()`
3. Server returns a list of all available tools with their schemas
4. Each tool has:
   - `name` - tool name
   - `description` - functionality description
   - `inputSchema` - JSON Schema defining input parameters

**Tool example:**
```python
Tool(
    name="generate_c4_diagram",
    description="Generate C4 architecture diagram...",
    inputSchema={
        "type": "object",
        "properties": {
            "diagram_type": {"type": "string", "enum": ["context", "container", ...]},
            "content": {"type": "string"},
            "output_path": {"type": "string"},
            "format": {"type": "string", "enum": ["png", "svg"], "default": "png"}
        },
        "required": ["diagram_type", "content", "output_path"]
    }
)
```

---

## Request Processing

### Step 4: Tool Call

When a client wants to use a tool, it sends a `tools/call` request:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_c4_diagram",
    "arguments": {
      "diagram_type": "context",
      "content": "Person(user, \"User\")...",
      "output_path": "output/diagram.png",
      "format": "png"
    }
  }
}
```

### Step 5: Routing to the Appropriate Tool

In the `src/server.py` file, the `call_tool()` function:

```python
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute the requested tool."""
    try:
        # PlantUML tools
        if name == "generate_c4_diagram":
            result = await plantuml.generate_c4_diagram(...)
        elif name == "generate_uml_diagram":
            result = await plantuml.generate_uml_diagram(...)
        # ... more tools
        
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

**What happens:**
1. Server receives a request with tool name and arguments
2. Checks the tool name (`name`)
3. Calls the appropriate function from the tool module
4. Returns the result as `TextContent`

---

## Data Flow Example

### Scenario: Generating C4 Context Diagram

![Data Flow Sequence Diagram](../output/docs_data_flow_diagram.png)

### Detailed Flow for `generate_c4_diagram`:

#### Step 1: Validation
```python
# plantuml.py, line 61-74
if not content or not content.strip():
    return "✗ Error: Content is empty..."

# Checks if it contains C4 keywords
c4_keywords = ["Person", "System", "System_Ext", ...]
has_diagram_content = any(keyword in content for keyword in c4_keywords)
```

#### Step 2: Prepare PlantUML Code
```python
# plantuml.py, line 77-88
c4_includes = _get_c4_includes(diagram_type)  # Adds !include for C4
cleaned_content = re.sub(r'@startuml\s*', '', content)  # Cleans existing tags
full_content = f"@startuml\n{c4_includes}{cleaned_content}\n@enduml"
```

**Example resulting code:**
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "User")
System(ecommerce, "E-commerce System")
Rel(user, ecommerce, "Buys products")

@enduml
```

#### Step 3: Rendering via PlantUML Server
```python
# plantuml.py, line 168-183
endpoint = f"{PLANTUML_SERVER}/png"  # http://plantuml:8080/png

async with aiohttp.ClientSession() as session:
    async with session.post(
        endpoint,
        data=full_content.encode('utf-8'),
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    ) as response:
        image_data = await response.read()  # Receives binary PNG
        write_binary_file(output_path, image_data)  # Saves to file
```

#### Step 4: File Save
```python
# utils/file_manager.py
def write_binary_file(file_path: str, data: bytes):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)  # Creates directories
    path.write_bytes(data)  # Saves binary file
```

---

## Tool Implementation Details

### 1. PlantUML Tools (`src/tools/plantuml.py`)

**Available functions:**
- `generate_c4_diagram()` - C4 diagrams (context, container, component, code)
- `generate_uml_diagram()` - UML diagrams (class, component, deployment, etc.)
- `generate_sequence_diagram()` - Sequence diagrams

**Common function:** `_render_plantuml()`
- Sends PlantUML code to HTTP server
- Receives PNG/SVG image
- Saves to file

### 2. Mermaid Tools (`src/tools/mermaid.py`)

**Available functions:**
- `generate_flowchart()` - Flowcharts
- `generate_sequence()` - Sequence diagrams
- `generate_gantt()` - Gantt charts

**How it works:**
- Uses `mermaid.ink` library (online API) or local renderer
- Sends Mermaid code to API
- Receives PNG/SVG image

### 3. Graphviz Tools (`src/tools/graphviz.py`)

**Function:** `generate_graph()`
- Accepts DOT code (Graphviz)
- Uses local Graphviz (if available) or online API
- Renders to PNG/SVG/PDF

### 4. draw.io Tools (`src/tools/drawio.py`)

**Function:** `generate_diagram()`
- Accepts draw.io XML
- Converts to PNG/SVG/PDF image
- Uses `drawio` library or API

### 5. Export Tools (`src/tools/export.py`)

**Functions:**
- `export_to_pdf()` - Markdown → PDF (uses Pandoc)
- `export_to_docx()` - Markdown → DOCX (uses Pandoc)
- `create_from_template()` - Generates documents from templates

**Templates available in `src/templates/`:**
- `adr_template.md` - Architecture Decision Record
- `api_spec_template.md` - API Specification
- `c4_context_template.puml` - C4 Context Template
- `microservices_overview_template.md` - Microservices Overview

---

## JSON-RPC Communication

### Request Format

**List tools:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Call tool:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "generate_c4_diagram",
    "arguments": {
      "diagram_type": "context",
      "content": "...",
      "output_path": "output/diagram.png"
    }
  }
}
```

### Response Format

**Success:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✓ C4 context diagram generated successfully: /app/output/diagram.png"
      }
    ]
  }
}
```

**Error:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "Error: PlantUML server error: ..."
  }
}
```

---

## Error Handling

### Error Handling Levels:

1. **Input Validation** (in `call_tool()`)
   - Checks if tool exists
   - Returns `"Unknown tool: {name}"` if not

2. **Tool Validation** (e.g., in `plantuml.py`)
   - Checks if content is not empty
   - Checks if it contains required elements

3. **Network Exception Handling** (in `_render_plantuml()`)
   - `aiohttp.ClientError` - connection problem
   - Returns readable error message

4. **General Exception Handling** (in `call_tool()`)
   - Catches all exceptions
   - Returns `"Error: {str(e)}"`

---

## Environment Variables

### In `mcp-server` container:

- `PLANTUML_SERVER=http://plantuml:8080` - PlantUML server URL
- `PYTHONPATH=/app` - Python path
- `PYTHONUNBUFFERED=1` - Disables output buffering (for logs)

### In `plantuml` container:

- `PLANTUML_LIMIT_SIZE=8192` - Maximum diagram size

---

## Summary

### Key Points:

1. **MCP Server** communicates via stdio using JSON-RPC
2. **Two Docker containers** - PlantUML server and MCP server
3. **11 tools** available through MCP protocol
4. **Modular architecture** - each diagram type in a separate module
5. **UTF-8 support** - all tools support UTF-8 characters
6. **Multi-level error handling**

### Typical Request Flow:

![Request Flow Diagram](../output/docs_request_flow_diagram.png)

---

## Further Reading

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - How to use the server
- [QUICKSTART.md](QUICKSTART.md) - Quick start
- [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - Project structure
- [DOCKER_CONTAINERS_EXPLAINED.md](DOCKER_CONTAINERS_EXPLAINED.md) - Docker containers details

---

<a name="polski"></a>
# Polski

## 📋 Spis treści
1. [Wprowadzenie](#wprowadzenie-polski)
2. [Architektura systemu](#architektura-systemu-polski)
3. [Uruchomienie serwera](#uruchomienie-serwera-polski)
4. [Rejestracja narzędzi](#rejestracja-narzędzi-polski)
5. [Przetwarzanie żądań](#przetwarzanie-żądań-polski)
6. [Przykład przepływu danych](#przykład-przepływu-danych-polski)
7. [Szczegóły implementacji narzędzi](#szczegóły-implementacji-narzędzi-polski)

---

<a name="wprowadzenie-polski"></a>
## Wprowadzenie

Serwer MCP (Model Context Protocol) to serwer komunikujący się przez protokół stdio (standard input/output), który udostępnia narzędzia do generowania dokumentacji technicznej z diagramami.

### Co to jest MCP?
MCP to protokół komunikacji między AI (np. Cursor) a zewnętrznymi narzędziami. Serwer nasłuchuje na stdin i odpowiada przez stdout używając formatu JSON-RPC.

---

<a name="architektura-systemu-polski"></a>
## Architektura systemu

### 1. Komponenty Docker

System składa się z **2 kontenerów Docker**:

![Diagram Architektury Docker](../output/docs_architecture_diagram.png)

#### Kontener 1: `plantuml`
- **Obraz**: `plantuml/plantuml-server:jetty`
- **Port**: 8080
- **Funkcja**: Renderuje diagramy PlantUML do PNG/SVG
- **Endpoint**: `http://localhost:8080/png` lub `/svg`

#### Kontener 2: `mcp-server`
- **Obraz**: Budowany z `Dockerfile`
- **Funkcja**: Główny serwer MCP
- **Volumes**:
  - `./src` → `/app/src` (kod źródłowy, tylko do odczytu)
  - `./output` → `/app/output` (katalog wyjściowy, zapisywalny)
  - `./src/templates` → `/app/src/templates` (szablony, tylko do odczytu)
- **Zależności**: Czeka aż `plantuml` będzie zdrowy (healthcheck)

---

<a name="uruchomienie-serwera-polski"></a>
## Uruchomienie serwera

### Krok 1: Start kontenerów Docker

```bash
docker compose up -d
```

**Co się dzieje:**
1. Docker uruchamia kontener `plantuml` na porcie 8080
2. Docker sprawdza healthcheck kontenera `plantuml` (curl do http://localhost:8080/)
3. Gdy `plantuml` jest zdrowy, uruchamia kontener `mcp-server`
4. Kontener `mcp-server` uruchamia skrypt `src/server.py`

### Krok 2: Inicjalizacja serwera MCP

W pliku `src/server.py`:

```python
# Linia 20: Tworzenie instancji serwera MCP
app = Server("mcp-documentation-server")

# Linia 429-440: Główna funkcja uruchamiająca
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,      # stdin - odczyt żądań
            write_stream,     # stdout - wysyłanie odpowiedzi
            app.create_initialization_options()
        )
```

**Co się dzieje:**
1. Serwer MCP tworzy połączenie stdio (stdin/stdout)
2. Nasłuchuje na żądania JSON-RPC przychodzące przez stdin
3. Wysyła odpowiedzi przez stdout

---

<a name="rejestracja-narzędzi-polski"></a>
## Rejestracja narzędzi

### Krok 3: Lista dostępnych narzędzi

Gdy klient (np. Cursor) pyta o dostępne narzędzia, wywoływana jest funkcja `list_tools()`:

```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available documentation generation tools."""
    tools = []
    
    # Dodawanie narzędzi PlantUML
    tools.extend([...])
    
    # Dodawanie narzędzi Mermaid
    tools.extend([...])
    
    # Dodawanie narzędzi Graphviz
    tools.append(...)
    
    # Dodawanie narzędzi draw.io
    tools.append(...)
    
    # Dodawanie narzędzi eksportu
    tools.extend([...])
    
    return tools
```

**Co się dzieje:**
1. Klient wysyła żądanie `tools/list` przez stdin
2. Serwer wywołuje `list_tools()`
3. Serwer zwraca listę wszystkich dostępnych narzędzi z ich schematami
4. Każde narzędzie ma:
   - `name` - nazwa narzędzia
   - `description` - opis funkcjonalności
   - `inputSchema` - JSON Schema definiujący parametry wejściowe

**Przykład narzędzia:**
```python
Tool(
    name="generate_c4_diagram",
    description="Generate C4 architecture diagram...",
    inputSchema={
        "type": "object",
        "properties": {
            "diagram_type": {"type": "string", "enum": ["context", "container", ...]},
            "content": {"type": "string"},
            "output_path": {"type": "string"},
            "format": {"type": "string", "enum": ["png", "svg"], "default": "png"}
        },
        "required": ["diagram_type", "content", "output_path"]
    }
)
```

---

<a name="przetwarzanie-żądań-polski"></a>
## Przetwarzanie żądań

### Krok 4: Wywołanie narzędzia

Gdy klient chce użyć narzędzia, wysyła żądanie `tools/call`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "generate_c4_diagram",
    "arguments": {
      "diagram_type": "context",
      "content": "Person(user, \"Użytkownik\")...",
      "output_path": "output/diagram.png",
      "format": "png"
    }
  }
}
```

### Krok 5: Routing do odpowiedniego narzędzia

W pliku `src/server.py`, funkcja `call_tool()`:

```python
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute the requested tool."""
    try:
        # PlantUML tools
        if name == "generate_c4_diagram":
            result = await plantuml.generate_c4_diagram(...)
        elif name == "generate_uml_diagram":
            result = await plantuml.generate_uml_diagram(...)
        # ... więcej narzędzi
        
        return [TextContent(type="text", text=result)]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
```

**Co się dzieje:**
1. Serwer otrzymuje żądanie z nazwą narzędzia i argumentami
2. Sprawdza nazwę narzędzia (`name`)
3. Wywołuje odpowiednią funkcję z modułu narzędziowego
4. Zwraca wynik jako `TextContent`

---

<a name="przykład-przepływu-danych-polski"></a>
## Przykład przepływu danych

### Scenariusz: Generowanie diagramu C4 Context

![Diagram Przepływu Danych](../output/docs_data_flow_diagram.png)

### Szczegółowy przepływ dla `generate_c4_diagram`:

#### Krok 1: Walidacja
```python
# plantuml.py, linia 61-74
if not content or not content.strip():
    return "✗ Error: Content is empty..."

# Sprawdza czy zawiera słowa kluczowe C4
c4_keywords = ["Person", "System", "System_Ext", ...]
has_diagram_content = any(keyword in content for keyword in c4_keywords)
```

#### Krok 2: Przygotowanie kodu PlantUML
```python
# plantuml.py, linia 77-88
c4_includes = _get_c4_includes(diagram_type)  # Dodaje !include dla C4
cleaned_content = re.sub(r'@startuml\s*', '', content)  # Czyści istniejące tagi
full_content = f"@startuml\n{c4_includes}{cleaned_content}\n@enduml"
```

**Przykład wynikowego kodu:**
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "Użytkownik")
System(ecommerce, "System E-commerce")
Rel(user, ecommerce, "Kupuje produkty")

@enduml
```

#### Krok 3: Renderowanie przez PlantUML Server
```python
# plantuml.py, linia 168-183
endpoint = f"{PLANTUML_SERVER}/png"  # http://plantuml:8080/png

async with aiohttp.ClientSession() as session:
    async with session.post(
        endpoint,
        data=full_content.encode('utf-8'),
        headers={'Content-Type': 'text/plain; charset=utf-8'}
    ) as response:
        image_data = await response.read()  # Otrzymuje binarny PNG
        write_binary_file(output_path, image_data)  # Zapisuje do pliku
```

#### Krok 4: Zapis pliku
```python
# utils/file_manager.py
def write_binary_file(file_path: str, data: bytes):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)  # Tworzy katalogi
    path.write_bytes(data)  # Zapisuje binarny plik
```

---

<a name="szczegóły-implementacji-narzędzi-polski"></a>
## Szczegóły implementacji narzędzi

### 1. Narzędzia PlantUML (`src/tools/plantuml.py`)

**Dostępne funkcje:**
- `generate_c4_diagram()` - Diagramy C4 (context, container, component, code)
- `generate_uml_diagram()` - Diagramy UML (class, component, deployment, etc.)
- `generate_sequence_diagram()` - Diagramy sekwencji

**Wspólna funkcja:** `_render_plantuml()`
- Wysyła kod PlantUML do serwera HTTP
- Otrzymuje obraz PNG/SVG
- Zapisuje do pliku

### 2. Narzędzia Mermaid (`src/tools/mermaid.py`)

**Dostępne funkcje:**
- `generate_flowchart()` - Flowcharty
- `generate_sequence()` - Diagramy sekwencji
- `generate_gantt()` - Wykresy Gantta

**Jak działa:**
- Używa biblioteki `mermaid.ink` (API online) lub lokalnego renderera
- Wysyła kod Mermaid do API
- Otrzymuje obraz PNG/SVG

### 3. Narzędzia Graphviz (`src/tools/graphviz.py`)

**Funkcja:** `generate_graph()`
- Przyjmuje kod DOT (Graphviz)
- Używa lokalnego Graphviz (jeśli dostępny) lub API online
- Renderuje do PNG/SVG/PDF

### 4. Narzędzia draw.io (`src/tools/drawio.py`)

**Funkcja:** `generate_diagram()`
- Przyjmuje XML draw.io
- Konwertuje do obrazu PNG/SVG/PDF
- Używa biblioteki `drawio` lub API

### 5. Narzędzia eksportu (`src/tools/export.py`)

**Funkcje:**
- `export_to_pdf()` - Markdown → PDF (używa Pandoc)
- `export_to_docx()` - Markdown → DOCX (używa Pandoc)
- `create_from_template()` - Generuje dokumenty z szablonów

**Szablony dostępne w `src/templates/`:**
- `adr_template.md` - Architecture Decision Record
- `api_spec_template.md` - Specyfikacja API
- `c4_context_template.puml` - Szablon C4 Context
- `microservices_overview_template.md` - Przegląd mikrousług

---

## Komunikacja JSON-RPC

### Format żądań

**Lista narzędzi:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Wywołanie narzędzia:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "generate_c4_diagram",
    "arguments": {
      "diagram_type": "context",
      "content": "...",
      "output_path": "output/diagram.png"
    }
  }
}
```

### Format odpowiedzi

**Sukces:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "✓ C4 context diagram generated successfully: /app/output/diagram.png"
      }
    ]
  }
}
```

**Błąd:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "error": {
    "code": -32603,
    "message": "Internal error",
    "data": "Error: PlantUML server error: ..."
  }
}
```

---

## Obsługa błędów

### Poziomy obsługi błędów:

1. **Walidacja wejścia** (w `call_tool()`)
   - Sprawdza czy narzędzie istnieje
   - Zwraca `"Unknown tool: {name}"` jeśli nie

2. **Walidacja w narzędziach** (np. w `plantuml.py`)
   - Sprawdza czy content nie jest pusty
   - Sprawdza czy zawiera wymagane elementy

3. **Obsługa wyjątków sieciowych** (w `_render_plantuml()`)
   - `aiohttp.ClientError` - problem z połączeniem
   - Zwraca czytelny komunikat błędu

4. **Ogólna obsługa wyjątków** (w `call_tool()`)
   - Łapie wszystkie wyjątki
   - Zwraca `"Error: {str(e)}"`

---

## Zmienne środowiskowe

### W kontenerze `mcp-server`:

- `PLANTUML_SERVER=http://plantuml:8080` - URL serwera PlantUML
- `PYTHONPATH=/app` - Ścieżka Pythona
- `PYTHONUNBUFFERED=1` - Wyłącza buforowanie wyjścia (dla logów)

### W kontenerze `plantuml`:

- `PLANTUML_LIMIT_SIZE=8192` - Maksymalny rozmiar diagramu

---

## Podsumowanie

### Kluczowe punkty:

1. **Serwer MCP** komunikuje się przez stdio używając JSON-RPC
2. **Dwa kontenery Docker** - PlantUML server i MCP server
3. **11 narzędzi** dostępnych przez protokół MCP
4. **Modularna architektura** - każdy typ diagramu w osobnym module
5. **Obsługa polskich znaków** - wszystkie narzędzia wspierają UTF-8
6. **Obsługa błędów** na wielu poziomach

### Przepływ typowego żądania:

![Diagram Przepływu Żądania](../output/docs_request_flow_diagram.png)

---

## Dalsze czytanie

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - Jak używać serwera
- [QUICKSTART.md](QUICKSTART.md) - Szybki start
- [PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md) - Struktura projektu
- [DOCKER_CONTAINERS_EXPLAINED.md](DOCKER_CONTAINERS_EXPLAINED.md) - Szczegóły kontenerów Docker
