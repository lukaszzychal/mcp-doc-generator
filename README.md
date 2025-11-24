# MCP Documentation Server

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-0.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Polish](https://img.shields.io/badge/język-Polski-red.svg)

📊 **MCP Server for automated technical documentation & architecture diagrams.** Generate C4, UML, Mermaid & Graphviz diagrams. Export to PDF/DOCX with full Unicode support. Templates for ADRs, API specs & microservices. 🇵🇱 Polish language ready.

---

🚀 Kompletny serwer MCP do automatycznego generowania dokumentacji technicznej z profesjonalnymi diagramami i eksportem do wielu formatów. Pełne wsparcie dla języka polskiego!

## 🎯 Funkcje

### Diagramy

- **PlantUML**: C4 Architecture, UML (klasy, komponenty, deployment), diagramy sekwencji
- **Mermaid**: Flowcharty, diagramy sekwencji, wykresy Gantta
- **Graphviz**: Grafy zależności między microservices
- **draw.io**: Diagramy cloud architecture z ikonami AWS/Azure/GCP

### Eksport Dokumentów

- **PDF**: Z polskimi czcionkami i pełnym wsparciem UTF-8
- **DOCX**: Dokumenty Word z customowymi stylami
- **Markdown**: Konsolidacja wielu plików

### Szablony Dokumentacji (Polski)

- **ADR** (Architecture Decision Record)
- **API Specification**
- **C4 Context Diagrams**
- **Microservices Overview**

## 📦 Szybki Start

### 1. Instalacja Automatyczna

```bash
chmod +x install.sh
./install.sh
```

Skrypt automatycznie:
- Sprawdzi wszystkie zależności
- Zainstaluje wymagane pakiety
- Zbuduje kontenery Docker
- Uruchomi serwisy

### 2. Instalacja Manualna

#### Wymagania

- Python 3.10+
- Docker & Docker Compose
- Node.js 18+ (opcjonalne, dla mermaid-cli)

#### Krok po kroku

```bash
# 1. Zainstaluj zależności Python
pip install -r requirements.txt

# 2. Zainstaluj mermaid-cli (opcjonalne)
npm install -g @mermaid-js/mermaid-cli

# 3. Utwórz katalogi
mkdir -p output

# 4. Uruchom Docker Compose
docker compose up -d

# 5. Sprawdź status
docker compose ps
```

## 🔧 Konfiguracja MCP w Claude Desktop

### macOS

Edytuj plik: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Linux

Edytuj plik: `~/.config/Claude/claude_desktop_config.json`

### Konfiguracja

```json
{
  "mcpServers": {
    "documentation": {
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

Po zapisaniu **zrestartuj Claude Desktop**.

## 🛠️ Dostępne Narzędzia

### 1. `generate_c4_diagram`

Generuje diagramy C4 Architecture (Context/Container/Component/Code).

**Parametry:**
- `diagram_type`: "context", "container", "component", lub "code"
- `content`: Kod PlantUML/C4
- `output_path`: Ścieżka do pliku wyjściowego
- `format`: "png" lub "svg" (domyślnie: "png")

**Przykład:**

```
Wygeneruj C4 Context Diagram dla systemu e-commerce z użytkownikiem, systemem zamówień i bazą danych.
```

### 2. `generate_uml_diagram`

Generuje diagramy UML (klasy, komponenty, deployment).

**Parametry:**
- `diagram_type`: "class", "component", "deployment", "package", "activity", "usecase"
- `content`: Kod PlantUML
- `output_path`: Ścieżka do pliku
- `format`: "png" lub "svg"

**Przykład:**

```
Utwórz diagram klas UML dla systemu zarządzania użytkownikami z klasami User, Role, Permission.
```

### 3. `generate_flowchart`

Generuje flowchart używając Mermaid.

**Parametry:**
- `content`: Kod Mermaid
- `output_path`: Ścieżka do pliku
- `format`: "png" lub "svg"

**Przykład:**

```
Stwórz flowchart procesu rejestracji użytkownika: start -> walidacja email -> zapis do bazy -> wysłanie email -> koniec.
```

### 4. `generate_gantt`

Generuje wykres Gantta dla timeline projektu.

**Parametry:**
- `content`: Kod Mermaid Gantt
- `output_path`: Ścieżka do pliku
- `format`: "png" lub "svg"

**Przykład:**

```
Utwórz wykres Gantta dla projektu z fazami: analiza (2 tygodnie), development (4 tygodnie), testing (2 tygodnie).
```

### 5. `generate_dependency_graph`

Generuje graf zależności używając Graphviz.

**Parametry:**
- `content`: Kod DOT
- `output_path`: Ścieżka do pliku
- `format`: "png", "svg", lub "pdf"
- `layout`: "dot", "neato", "fdp", "circo", "twopi" (domyślnie: "dot")

**Przykład:**

```
Stwórz graf zależności między microservices: API Gateway -> Auth Service, Order Service, Payment Service. Order Service zależy od Inventory Service.
```

### 6. `generate_cloud_diagram`

Generuje diagram cloud architecture z ikonami AWS/Azure/GCP.

**Parametry:**
- `content`: XML draw.io
- `output_path`: Ścieżka do pliku
- `format`: "png", "svg", lub "pdf"

### 7. `export_to_pdf`

Konwertuje Markdown na PDF z pełnym wsparciem dla polskiego.

**Parametry:**
- `markdown_content`: Treść Markdown
- `output_path`: Ścieżka do PDF
- `title`: Tytuł dokumentu (opcjonalne)
- `author`: Autor (opcjonalne)
- `include_toc`: Czy dodać spis treści (domyślnie: true)

**Przykład:**

```
Przekonwertuj ten dokument do PDF z tytułem "Dokumentacja Architektury" i autorem "Jan Kowalski".
```

### 8. `export_to_docx`

Konwertuje Markdown na DOCX (Word).

**Parametry:**
- `markdown_content`: Treść Markdown
- `output_path`: Ścieżka do DOCX
- `title`: Tytuł (opcjonalne)
- `author`: Autor (opcjonalne)

### 9. `create_document_from_template`

Generuje dokument z szablonu.

**Parametry:**
- `template_type`: "adr", "api_spec", "c4_context", "microservices_overview"
- `variables`: Słownik zmiennych do wypełnienia
- `output_path`: Ścieżka do pliku Markdown

**Przykład:**

```
Utwórz ADR z tytułem "Wybór bazy danych" używając szablonu ADR.
```

## 📝 Przykłady Użycia

### Przykład 1: Kompletna Dokumentacja Microservices

```
Potrzebuję kompletnej dokumentacji dla systemu microservices e-commerce:

1. C4 Context Diagram pokazujący użytkownika, system e-commerce, payment gateway i email service
2. Diagram sekwencji dla procesu składania zamówienia
3. Graf zależności między wszystkimi serwisami
4. ADR dokumentujący wybór Message Queue (RabbitMQ vs Kafka)
5. Wszystko wyeksportuj do PDF z tytułem "Architektura E-Commerce"
```

### Przykład 2: API Documentation

```
Wygeneruj dokumentację API dla mojego REST API:

1. Użyj szablonu API Spec
2. Dodaj diagramy sekwencji dla kluczowych endpointów
3. Wyeksportuj do PDF i DOCX
```

### Przykład 3: ADR z Diagramami

```
Utwórz ADR dokumentujący migrację z monolitu do microservices:

1. Diagram "before" (aktualny monolit)
2. Diagram "after" (docelowe microservices)
3. Graf zależności między nowymi serwisami
4. Wyeksportuj wszystko do PDF
```

## 🐳 Docker Commands

```bash
# Uruchom serwisy
docker compose up -d

# Zatrzymaj serwisy
docker compose down

# Zobacz logi
docker compose logs -f

# Zobacz logi tylko MCP server
docker compose logs -f mcp-server

# Przebuduj kontenery
docker compose build --no-cache

# Sprawdź status
docker compose ps
```

## ☁️ Deployment do Chmury

### Fly.io (Rekomendowane)

```bash
# 1. Zainstaluj Fly CLI
curl -L https://fly.io/install.sh | sh

# 2. Zaloguj się
fly auth login

# 3. Uruchom aplikację
fly launch

# 4. Deploy
fly deploy

# 5. Sprawdź status
fly status

# 6. Zobacz logi
fly logs
```

### Railway

```bash
# 1. Zainstaluj Railway CLI
npm i -g @railway/cli

# 2. Zaloguj się
railway login

# 3. Inicjalizuj projekt
railway init

# 4. Deploy
railway up

# 5. Status
railway status
```

## 📂 Struktura Projektu

```
mcp-documentation-server/
├── src/
│   ├── server.py              # Główny MCP server
│   ├── tools/
│   │   ├── plantuml.py       # PlantUML diagrams
│   │   ├── mermaid.py        # Mermaid diagrams
│   │   ├── graphviz.py       # Graphviz graphs
│   │   ├── drawio.py         # draw.io diagrams
│   │   └── export.py         # PDF/DOCX export
│   ├── templates/            # Polskie szablony
│   │   ├── adr_template.md
│   │   ├── api_spec_template.md
│   │   ├── c4_context_template.puml
│   │   └── microservices_overview_template.md
│   └── utils/
│       ├── file_manager.py   # File operations
│       └── polish_support.py # Polish language support
├── output/                    # Generated files
├── docker-compose.yml
├── Dockerfile
├── fly.toml                   # Fly.io config
├── railway.toml              # Railway config
├── install.sh                # Auto-installer
└── README.md
```

## 🔍 Troubleshooting

### PlantUML server nie działa

```bash
# Sprawdź czy kontener działa
docker compose ps

# Zrestartuj serwis
docker compose restart plantuml

# Sprawdź czy port 8080 jest wolny
lsof -i :8080
```

### Błąd "mermaid-cli not found"

```bash
# Zainstaluj globalnie
npm install -g @mermaid-js/mermaid-cli

# Lub użyj wersji z Docker (już zainstalowana)
docker compose exec mcp-server mmdc --version
```

### Błąd z polskimi znakami w PDF

Upewnij się, że masz zainstalowane:
- `texlive-xetex`
- `fonts-dejavu`

```bash
# macOS
brew install --cask mactex
brew install --cask font-dejavu

# Linux (Ubuntu/Debian)
sudo apt-get install texlive-xetex fonts-dejavu
```

## 🤝 Contributing

Zgłaszaj issues i pull requesty na GitHubie!

## 📄 Licencja

MIT License - Zobacz plik LICENSE

## 🎓 Dokumentacja Dodatkowa

- [PlantUML Guide](https://plantuml.com/)
- [C4 Model](https://c4model.com/)
- [Mermaid Documentation](https://mermaid.js.org/)
- [Graphviz Documentation](https://graphviz.org/)
- [Pandoc Manual](https://pandoc.org/MANUAL.html)

## 💬 Wsparcie

W razie pytań lub problemów, utwórz issue na GitHubie.

---

**Autor:** Lukasz Zychal  
**Wersja:** 0.1.0  
**Data:** Listopad 2025

