# MCP Documentation Server Usage Guide / Przewodnik Użycia MCP Documentation Server

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Quick Start

### Using your own prompt (fastest)

```bash
# 1. Start containers
docker compose up -d

# 2. Generate diagram from prompt
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md

# Or from console:
python3 scripts/mcp_client.py -p "Generate C4 context diagram with User and System. Save as output/test.png"

# Or from specific file lines:
sed -n '12,30p' examples/prompts/EXAMPLE_PROMPTS.md | python3 scripts/mcp_client.py
```

### Using with Cursor

```bash
docker compose up -d
# Open Cursor and use MCP tools in conversation
```

---

## Table of Contents

1. [Local usage without Cursor](#local-usage-without-cursor)
2. [Usage with Cursor](#usage-with-cursor)
3. [Available tools](#available-tools)
4. [Usage examples](#usage-examples)

---

## Local Usage Without Cursor

### Option 1: Direct Python usage (requires Python 3.10+)

**Note:** If you have Python 3.9.6 or older, use Option 2 (Docker).

#### Step 1: Start PlantUML server

```bash
cd /path/to/MCPServer
docker compose up -d plantuml
```

Check if it's running:
```bash
curl http://localhost:8080/
```

#### Step 2: Install Python dependencies

```bash
pip install -r requirements.txt
```

#### Step 3: Set environment variable

```bash
export PLANTUML_SERVER=http://localhost:8080
export PYTHONPATH=/path/to/MCPServer
```

#### Step 4: Run MCP server

```bash
python3 src/server.py
```

The server will run in stdio mode (waits for input via stdin).

#### Step 5: Use test script

```bash
python3 tests/test_mcp_local.py
```

This will run all tests and generate diagrams in the `output/` directory.

#### Step 6: Use your own prompt

**From file:**
```bash
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md
```

**From console:**
```bash
python3 scripts/mcp_client.py -p "Generate C4 context diagram with User and System. Save as output/test.png"
```

**From stdin (pipe):**
```bash
cat prompt.txt | python3 scripts/mcp_client.py
```

**From specific file lines:**
```bash
sed -n '12,30p' examples/prompts/EXAMPLE_PROMPTS.md | python3 scripts/mcp_client.py
```

---

### Option 2: Using Docker (recommended)

#### Step 1: Start all containers

```bash
cd /path/to/MCPServer
docker compose up -d
```

Check status:
```bash
docker compose ps
```

#### Step 2: Use test script

```bash
python3 tests/test_mcp_local.py
```

The script will automatically use `docker exec` to run the MCP server in the container.

#### Step 3: Direct usage via docker exec

You can also run the MCP server directly:

```bash
docker exec -i mcp-documentation-server python src/server.py
```

This will run the server in stdio mode - you can send JSON-RPC requests via stdin.

---

## Usage with Cursor

### Step 1: Start Docker containers

```bash
cd /path/to/MCPServer
docker compose up -d
```

### Step 2: Check Cursor configuration

Cursor automatically detects MCP servers. Check if containers are running:

```bash
docker compose ps
```

### Step 3: Check integration

Run the check script:

```bash
./tests/test_mcp_cursor_integration.sh
```

### Step 4: Use in Cursor

1. **Open Cursor**
2. **Open a new conversation**
3. **Use MCP tools** - Cursor will automatically detect available tools

#### Example commands in Cursor:

**C4 Context Diagram:**
```
Generate C4 Context Diagram for e-commerce system with:
- User (customer)
- E-Commerce System (main system)
- Payment Gateway (external payment system)
- Shipping Service (delivery service)

Save as output/ecommerce-context.png
```

**UML Class Diagram:**
```
Generate UML Class Diagram with classes:
- User (id, name, email)
- Order (id, total, status)
- Product (id, name, price)

With relationships: User has many Order, Order has many Product.

Save as output/uml-class.png
```

---

## Available Tools

### 1. generate_c4_diagram
- **Types:** context, container, component, code
- **Formats:** png, svg
- **Description:** Generates C4 architecture diagrams

### 2. generate_uml_diagram
- **Types:** class, component, deployment, package, activity, usecase
- **Formats:** png, svg
- **Description:** Generates UML diagrams

### 3. generate_sequence_diagram
- **Formats:** png, svg
- **Description:** Generates PlantUML sequence diagrams

### 4. generate_flowchart
- **Formats:** png, svg
- **Description:** Generates flowcharts using Mermaid

### 5. generate_mermaid_sequence
- **Formats:** png, svg
- **Description:** Generates sequence diagrams using Mermaid

### 6. generate_gantt
- **Formats:** png, svg
- **Description:** Generates Gantt charts

### 7. generate_dependency_graph
- **Layouts:** dot, neato, fdp, circo, twopi
- **Formats:** png, svg, pdf
- **Description:** Generates dependency graphs using Graphviz

### 8. generate_cloud_diagram
- **Formats:** png, svg, pdf
- **Description:** Generates cloud architecture diagrams using draw.io

### 9. export_to_pdf
- **Description:** Exports markdown to PDF using Pandoc

### 10. export_to_docx
- **Description:** Exports markdown to DOCX (Word) using Pandoc

### 11. create_document_from_template
- **Templates:** adr, api_spec, c4_context, microservices_overview
- **Description:** Creates documents from ready-made templates

---

## Requirements

- Docker and Docker Compose
- Python 3.10+ (for local usage without Docker)
- Cursor (optional, for integration)

---

<a name="polski"></a>
# Polski

## Szybki Start

### Użycie własnego promptu (najszybsze)

```bash
# 1. Uruchom kontenery
docker compose up -d

# 2. Wygeneruj diagram z promptu
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md

# Lub z konsoli:
python3 mcp_client.py -p "Generate C4 context diagram with User and System. Save as output/test.png"

# Lub z konkretnych linii pliku:
sed -n '12,30p' examples/prompts/EXAMPLE_PROMPTS.md | python3 scripts/mcp_client.py
```

### Użycie z Cursor

```bash
docker compose up -d
# Otwórz Cursor i użyj narzędzi MCP w konwersacji
```

---

## Spis treści

1. [Użycie lokalne bez Cursor](#użycie-lokalne-bez-cursor)
2. [Użycie z Cursor](#użycie-z-cursor)
3. [Dostępne narzędzia](#dostępne-narzędzia)
4. [Przykłady użycia](#przykłady-użycia)

---

## Użycie lokalne bez Cursor

### Opcja 1: Bezpośrednie użycie przez Python (wymaga Python 3.10+)

**Uwaga:** Jeśli masz Python 3.9.6 lub starszy, użyj Opcji 2 (Docker).

#### Krok 1: Uruchom PlantUML server

```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer
docker compose up -d plantuml
```

Sprawdź czy działa:
```bash
curl http://localhost:8080/
```

#### Krok 2: Zainstaluj zależności Python

```bash
pip install -r requirements.txt
```

#### Krok 3: Ustaw zmienną środowiskową

```bash
export PLANTUML_SERVER=http://localhost:8080
export PYTHONPATH=/Users/lukaszzychal/PhpstormProjects/MCPServer
```

#### Krok 4: Uruchom MCP server

```bash
python3 src/server.py
```

Serwer będzie działał w trybie stdio (czeka na dane wejściowe przez stdin).

#### Krok 5: Użyj skryptu testowego

```bash
python3 test_mcp_local.py
```

To uruchomi wszystkie testy i wygeneruje diagramy w katalogu `output/`.

#### Krok 6: Użyj własnego promptu

**Z pliku:**
```bash
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md
```

**Z konsoli:**
```bash
python3 mcp_client.py -p "Generate C4 context diagram with User and System. Save as output/test.png"
```

**Z stdin (pipe):**
```bash
cat prompt.txt | python3 mcp_client.py
```

**Z konkretnych linii pliku:**
```bash
sed -n '12,30p' examples/prompts/EXAMPLE_PROMPTS.md | python3 scripts/mcp_client.py
```

---

### Opcja 2: Użycie przez Docker (zalecane)

#### Krok 1: Uruchom wszystkie kontenery

```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer
docker compose up -d
```

Sprawdź status:
```bash
docker compose ps
```

#### Krok 2: Użyj skryptu testowego

```bash
python3 test_mcp_local.py
```

Skrypt automatycznie użyje `docker exec` do uruchomienia MCP server w kontenerze.

#### Krok 3: Bezpośrednie użycie przez docker exec

Możesz też uruchomić MCP server bezpośrednio:

```bash
docker exec -i mcp-documentation-server python src/server.py
```

To uruchomi serwer w trybie stdio - możesz wysyłać żądania JSON-RPC przez stdin.

---

### Użycie własnych promptów

Możesz użyć skryptu `mcp_client.py` do generowania diagramów z własnych promptów:

#### Opcja 1: Prompt z pliku

```bash
# Uruchom kontenery
docker compose up -d

# Wygeneruj diagram z promptu w pliku
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md
```

Lub użyj konkretnego fragmentu pliku:
```bash
# Wyciągnij prompt z pliku (linie 12-30)
sed -n '12,30p' examples/prompts/EXAMPLE_PROMPTS.md | python3 scripts/mcp_client.py
```

#### Opcja 2: Prompt z linii komend

```bash
python3 mcp_client.py -p "Generate a C4 context diagram for an e-commerce system with Users, Payment Gateway, and Web Application. Save as output/ecommerce.png"
```

#### Opcja 3: Prompt z stdin (pipe)

```bash
echo "Generate C4 context diagram with User and System. Save as output/test.png" | python3 mcp_client.py
```

#### Opcja 4: Tryb interaktywny

```bash
python3 mcp_client.py -i
# Wpisz prompt, naciśnij Ctrl+D aby zakończyć
```

#### Przykład z pliku EXAMPLE_PROMPTS.md

```bash
# Uruchom kontenery
docker compose up -d

# Wygeneruj diagram z przykładu
python3 mcp_client.py -f <(sed -n '12,30p' test-server/EXAMPLE_PROMPTS.md)
```

Lub bezpośrednio:
```bash
cat <<EOF | python3 mcp_client.py
Generate a C4 context diagram for an e-commerce system with the following components:

External Systems:
- Users (customers browsing and purchasing)
- Payment Gateway (Stripe/PayPal)
- Shipping Service (FedEx/UPS)

System Boundary - E-commerce Platform:
- Web Application (React frontend)
- Mobile App (iOS/Android)
- API Gateway (Node.js)
- Order Service
- Inventory Service
- Database (PostgreSQL)

Show relationships between all components with descriptions.

Save the diagram as PNG to:
output/c4-ecommerce-context.png
EOF
```

---

### Przykład użycia lokalnego - Python script (zaawansowany)

Utwórz plik `test_local_usage.py`:

```python
#!/usr/bin/env python3
import subprocess
import json
import sys

# Uruchom MCP server przez docker exec
process = subprocess.Popen(
    ["docker", "exec", "-i", "mcp-documentation-server", "python", "src/server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Inicjalizuj połączenie
init_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "local-client",
            "version": "1.0.0"
        }
    }
}

process.stdin.write(json.dumps(init_request) + "\n")
process.stdin.flush()

# Pobierz listę narzędzi
tools_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
}

process.stdin.write(json.dumps(tools_request) + "\n")
process.stdin.flush()

# Odczytaj odpowiedź
response = process.stdout.readline()
tools = json.loads(response)
print("Dostępne narzędzia:")
for tool in tools["result"]["tools"]:
    print(f"  - {tool['name']}")

# Wygeneruj diagram C4
c4_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
        "name": "generate_c4_diagram",
        "arguments": {
            "diagram_type": "context",
            "content": "@startuml\nPerson(user, 'User')\nSystem(system, 'System')\nRel(user, system, 'Uses')\n@enduml",
            "output_path": "output/test_local.png",
            "format": "png"
        }
    }
}

process.stdin.write(json.dumps(c4_request) + "\n")
process.stdin.flush()

response = process.stdout.readline()
result = json.loads(response)
print("\nWynik:")
print(result["result"]["content"][0]["text"])

process.terminate()
```

Uruchom:
```bash
python3 test_local_usage.py
```

---

## Użycie z Cursor

### Krok 1: Uruchom kontenery Docker

```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer
docker compose up -d
```

### Krok 2: Sprawdź konfigurację Cursor

Cursor automatycznie wykrywa MCP serwery. Sprawdź czy kontenery działają:

```bash
docker compose ps
```

### Krok 3: Sprawdź integrację

Uruchom skrypt sprawdzający:

```bash
./test_mcp_cursor_integration.sh
```

### Krok 4: Użyj w Cursor

1. **Otwórz Cursor**
2. **Otwórz nową konwersację**
3. **Użyj narzędzi MCP** - Cursor automatycznie wykryje dostępne narzędzia

#### Przykłady komend w Cursor:

**C4 Context Diagram:**
```
Wygeneruj C4 Context Diagram dla systemu e-commerce z:
- Użytkownik (klient)
- System E-Commerce (główny system)
- Payment Gateway (zewnętrzny system płatności)
- Shipping Service (serwis dostaw)

Zapisz jako output/ecommerce-context.png
```

**UML Class Diagram:**
```
Wygeneruj UML Class Diagram z klasami:
- User (id, name, email)
- Order (id, total, status)
- Product (id, name, price)

Z relacjami: User ma wiele Order, Order ma wiele Product.

Zapisz jako output/uml-class.png
```

**Sequence Diagram:**
```
Wygeneruj Sequence Diagram dla procesu logowania:
1. User -> API: Login request
2. API -> Database: Verify credentials
3. Database -> API: User data
4. API -> User: JWT token

Zapisz jako output/login-sequence.png
```

**Flowchart:**
```
Wygeneruj flowchart dla procesu zamówienia:
- Start
- Sprawdź dostępność produktu
- Jeśli dostępny -> Przetwórz zamówienie
- Jeśli niedostępny -> Wyświetl błąd
- Koniec

Zapisz jako output/order-flowchart.png
```

**Export do PDF:**
```
Wyeksportuj następujący markdown do PDF:

# Dokumentacja Systemu

## Wprowadzenie
System e-commerce do zarządzania zamówieniami.

## Architektura
System składa się z...

Zapisz jako output/documentation.pdf
```

**Template ADR:**
```
Utwórz ADR dokument z szablonu adr:
- Numer: 001
- Tytuł: Wybór PostgreSQL jako bazy danych
- Status: Accepted
- Autor: Jan Kowalski
- Kontekst: Potrzebujemy relacyjnej bazy danych
- Decyzja: PostgreSQL
- Pozytywne: ACID, JSON support
- Negatywne: Więcej zasobów niż MySQL

Zapisz jako output/adr-001.md
```

### Krok 5: Sprawdź wygenerowane pliki

Wszystkie pliki są zapisywane w katalogu `output/`:

```bash
ls -lh output/
```

---

## Dostępne narzędzia

### 1. generate_c4_diagram
- **Typy:** context, container, component, code
- **Formaty:** png, svg
- **Opis:** Generuje diagramy architektury C4

### 2. generate_uml_diagram
- **Typy:** class, component, deployment, package, activity, usecase
- **Formaty:** png, svg
- **Opis:** Generuje diagramy UML

### 3. generate_sequence_diagram
- **Formaty:** png, svg
- **Opis:** Generuje diagramy sekwencji PlantUML

### 4. generate_flowchart
- **Formaty:** png, svg
- **Opis:** Generuje flowchart używając Mermaid

### 5. generate_mermaid_sequence
- **Formaty:** png, svg
- **Opis:** Generuje diagramy sekwencji używając Mermaid

### 6. generate_gantt
- **Formaty:** png, svg
- **Opis:** Generuje wykresy Gantta

### 7. generate_dependency_graph
- **Layouty:** dot, neato, fdp, circo, twopi
- **Formaty:** png, svg, pdf
- **Opis:** Generuje grafy zależności używając Graphviz

### 8. generate_cloud_diagram
- **Formaty:** png, svg, pdf
- **Opis:** Generuje diagramy architektury chmurowej używając draw.io

### 9. export_to_pdf
- **Opis:** Eksportuje markdown do PDF używając Pandoc

### 10. export_to_docx
- **Opis:** Eksportuje markdown do DOCX (Word) używając Pandoc

### 11. create_document_from_template
- **Szablony:** adr, api_spec, c4_context, microservices_overview
- **Opis:** Tworzy dokumenty z gotowych szablonów

---

## Przykłady użycia

### Przykład 1: Użycie własnego promptu z pliku

```bash
# 1. Uruchom kontenery
docker compose up -d

# 2. Przygotuj prompt w pliku prompt.txt
cat > prompt.txt <<EOF
Generate a C4 context diagram for an e-commerce system with:
- Users (customers)
- Payment Gateway (Stripe)
- Web Application (React)
- API Gateway (Node.js)
- Database (PostgreSQL)

Save as output/my-diagram.png
EOF

# 3. Wygeneruj diagram
python3 mcp_client.py -f prompt.txt

# 4. Sprawdź wynik
ls -lh output/my-diagram.png
```

### Przykład 2: Prompt z konsoli

```bash
# Bezpośrednio z linii komend
python3 mcp_client.py -p "Generate UML class diagram with User and Order classes. Save as output/classes.png"
```

### Przykład 3: Pełny workflow lokalny

```bash
# 1. Uruchom kontenery
docker compose up -d

# 2. Sprawdź status
docker compose ps

# 3. Uruchom testy (wygeneruje przykładowe diagramy)
python3 test_mcp_local.py

# 4. Sprawdź wygenerowane pliki
ls -lh output/

# 5. Zatrzymaj kontenery
docker compose down
```

### Przykład 4: Użycie w Cursor

1. Uruchom kontenery: `docker compose up -d`
2. Otwórz Cursor
3. W konwersacji napisz: "Wygeneruj C4 Context Diagram dla systemu e-commerce"
4. Cursor automatycznie użyje narzędzia MCP
5. Sprawdź plik w `output/`

### Przykład 5: Wczytanie promptu z pliku i zapisanie do innej lokalizacji

```bash
# Wczytaj prompt z pliku, ale zmień ścieżkę wyjściową
python3 scripts/mcp_client.py -f examples/prompts/EXAMPLE_PROMPTS.md | \
  sed 's|examples/generated/c4-ecommerce-context.png|output/my-ecommerce.png|' | \
  python3 scripts/mcp_client.py
```

### Przykład 6: Testowanie konkretnego narzędzia

```bash
# Uruchom tylko PlantUML server
docker compose up -d plantuml

# Uruchom testy dla konkretnego narzędzia
python3 -c "
from test_mcp_local import MCPTester
tester = MCPTester()
tester.start_server()
tester.initialize()
tester.test_c4_diagram()  # Tylko C4 diagrams
"
```

---

## Rozwiązywanie problemów

### Problem: Kontenery nie startują

```bash
# Sprawdź logi
docker compose logs

# Zrestartuj kontenery
docker compose down
docker compose up -d
```

### Problem: MCP server nie odpowiada

```bash
# Sprawdź czy kontener działa
docker ps | grep mcp-documentation-server

# Sprawdź logi kontenera
docker logs mcp-documentation-server

# Zrestartuj kontener
docker compose restart mcp-server
```

### Problem: PlantUML server nie odpowiada

```bash
# Sprawdź czy działa
curl http://localhost:8080/

# Sprawdź logi
docker logs mcp-plantuml-server

# Zrestartuj
docker compose restart plantuml
```

### Problem: Cursor nie widzi narzędzi MCP

1. Sprawdź czy kontenery działają: `docker compose ps`
2. Sprawdź logi Cursor: `~/Library/Application Support/Cursor/logs/`
3. Zrestartuj Cursor
4. Sprawdź konfigurację MCP w Cursor (jeśli dostępna)

### Problem: Pliki nie są tworzone

```bash
# Sprawdź uprawnienia katalogu output
ls -la output/

# Sprawdź czy katalog istnieje
mkdir -p output

# Sprawdź logi kontenera
docker logs mcp-documentation-server
```

---

## Przydatne komendy

```bash
# Uruchom kontenery
docker compose up -d

# Zatrzymaj kontenery
docker compose down

# Sprawdź status
docker compose ps

# Zobacz logi
docker compose logs -f

# Zrestartuj kontenery
docker compose restart

# Uruchom testy
python3 test_mcp_local.py

# Użyj własnego promptu
python3 mcp_client.py -f twoj-plik.txt

# Sprawdź integrację z Cursor
./test_mcp_cursor_integration.sh

# Sprawdź wygenerowane pliki
ls -lh output/

# Wyczyść katalog output
rm -rf output/*
```

---

## Wymagania

- Docker i Docker Compose
- Python 3.10+ (dla lokalnego użycia bez Docker)
- Cursor (opcjonalnie, dla integracji)

---

## Wsparcie

Więcej informacji:
- `README.md` - Ogólna dokumentacja projektu
- `TEST_RESULTS_MCP.md` - Wyniki testów wszystkich narzędzi
- `examples/example_usage.md` - Przykłady użycia
- `test-server/EXAMPLE_PROMPTS.md` - Przykładowe prompty

