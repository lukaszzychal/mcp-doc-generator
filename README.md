# MCP Documentation Server

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![MCP](https://img.shields.io/badge/MCP-0.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Polish](https://img.shields.io/badge/language-Polski-red.svg)

📊 **MCP Server for automated technical documentation & architecture diagrams.** Generate C4, UML, Mermaid & Graphviz diagrams. Export to PDF/DOCX with full Unicode support. Templates for ADRs, API specs & microservices.

---

**Languages:** [🇬🇧 English](#english) | [🇵🇱 Polski](#polish)

---

## English

### 🎯 Features

#### Architecture Diagrams
- **PlantUML**: C4 Architecture (Context/Container/Component/Code), UML diagrams (class, component, deployment), sequence diagrams
- **Mermaid**: Flowcharts, sequence diagrams, Gantt charts
- **Graphviz**: Dependency graphs for microservices
- **draw.io**: Cloud architecture diagrams with AWS/Azure/GCP icons

#### Document Export
- **PDF**: With proper Unicode font support (including Polish characters: ąćęłńóśźż)
- **DOCX**: Microsoft Word documents with custom styles
- **Markdown**: Multi-file consolidation

#### Ready-made Templates
- **ADR** (Architecture Decision Record)
- **API Specification**
- **C4 Context Diagrams**
- **Microservices Overview**

### 🚀 Quick Start

#### Option 1: Automated Installation

```bash
chmod +x install.sh
./install.sh
```

The script will automatically:
- Check all dependencies
- Install required packages
- Build Docker containers
- Start services

#### Option 2: Docker (Recommended)

```bash
docker-compose up -d
```

#### Option 3: Manual Installation

**Prerequisites:**
- Python 3.10+
- PlantUML (Java required)
- Graphviz
- Mermaid CLI
- Pandoc (for PDF/DOCX export)

**Install dependencies:**

```bash
# macOS
brew install plantuml graphviz pandoc
npm install -g @mermaid-js/mermaid-cli

# Ubuntu/Debian
sudo apt-get install plantuml graphviz pandoc npm
npm install -g @mermaid-js/mermaid-cli

# Install Python packages
pip install -r requirements.txt
```

### 📖 Usage

#### Configure in Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "python",
      "args": ["/path/to/mcp-doc-generator/src/server.py"]
    }
  }
}
```

#### Available Tools

1. **generate_c4_diagram** - C4 architecture diagrams (Context/Container/Component/Code)
2. **generate_uml_diagram** - UML diagrams (class, component, deployment, package, activity)
3. **generate_sequence_diagram** - Sequence diagrams (PlantUML)
4. **generate_flowchart** - Flowcharts (Mermaid)
5. **generate_mermaid_sequence** - Sequence diagrams (Mermaid)
6. **generate_gantt** - Gantt charts for project timelines
7. **generate_dependency_graph** - Dependency graphs (Graphviz)
8. **generate_cloud_diagram** - Cloud architecture diagrams (draw.io)
9. **export_to_pdf** - Convert Markdown to PDF
10. **export_to_docx** - Convert Markdown to DOCX
11. **create_document_from_template** - Generate documents from templates

### 💡 Example Usage

```python
# In Claude Desktop, simply ask:
"Generate a C4 context diagram for an e-commerce system with users, 
web app, API gateway, and payment service. Export to PNG."

"Create an ADR document for switching from REST to GraphQL."

"Generate a Gantt chart for our Q1 2025 roadmap and export to PDF."
```

### 🏗️ Architecture

```
mcp-doc-generator/
├── src/
│   ├── server.py              # Main MCP server
│   ├── tools/                 # Tool implementations
│   │   ├── plantuml.py       # PlantUML integration
│   │   ├── mermaid.py        # Mermaid integration
│   │   ├── graphviz.py       # Graphviz integration
│   │   ├── drawio.py         # draw.io integration
│   │   └── export.py         # PDF/DOCX export
│   ├── utils/                 # Utilities
│   │   ├── file_manager.py   # File operations
│   │   └── polish_support.py # Polish language support
│   └── templates/             # Document templates
│       ├── adr_template.md
│       ├── api_spec_template.md
│       ├── c4_context_template.puml
│       └── microservices_overview_template.md
├── examples/                  # Usage examples
├── output/                    # Generated files
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

### 🐳 Docker Deployment

```bash
# Build
docker build -t mcp-doc-generator .

# Run
docker run -p 8000:8000 mcp-doc-generator

# Or use docker-compose
docker-compose up -d
```

### 🧪 Testing

```bash
# Run all tests
python test_all_tools.py

# Test specific tool
python -c "from src.tools import plantuml; print('PlantUML OK')"
```

### 🌍 Polish Language Support

Full support for Polish characters in:
- ✅ PDF exports (proper font rendering)
- ✅ DOCX documents
- ✅ Diagrams (labels, descriptions)
- ✅ Templates
- ✅ File names and paths

Example Polish characters: **ąćęłńóśźż ĄĆĘŁŃÓŚŹŻ**

### 📚 Use Cases

- **Software Architects**: Document system architecture with C4 diagrams
- **Tech Leads**: Maintain ADRs and technical decisions
- **Developers**: Generate API documentation automatically
- **Technical Writers**: Create professional documentation quickly
- **DevOps**: Document infrastructure and deployments
- **Project Managers**: Create Gantt charts and timelines

### 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙋 Support

- 📖 [Documentation](examples/example_usage.md)
- 🐛 [Report Issues](https://github.com/lukaszzychal/mcp-doc-generator/issues)
- 💬 [Discussions](https://github.com/lukaszzychal/mcp-doc-generator/discussions)

### 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

---

## Polish

### 🎯 Funkcje

#### Diagramy Architektoniczne
- **PlantUML**: Architektura C4 (Kontekst/Kontener/Komponent/Kod), diagramy UML (klasy, komponenty, deployment), diagramy sekwencji
- **Mermaid**: Flowcharty, diagramy sekwencji, wykresy Gantta
- **Graphviz**: Grafy zależności między mikrousługami
- **draw.io**: Diagramy architektury chmurowej z ikonami AWS/Azure/GCP

#### Eksport Dokumentów
- **PDF**: Z polskimi czcionkami i pełnym wsparciem UTF-8 (ąćęłńóśźż)
- **DOCX**: Dokumenty Microsoft Word z niestandardowymi stylami
- **Markdown**: Konsolidacja wielu plików

#### Gotowe Szablony
- **ADR** (Architecture Decision Record - Zapisy Decyzji Architektonicznych)
- **Specyfikacja API**
- **Diagramy Kontekstu C4**
- **Przegląd Mikrousług**

### 🚀 Szybki Start

#### Opcja 1: Automatyczna Instalacja

```bash
chmod +x install.sh
./install.sh
```

Skrypt automatycznie:
- Sprawdzi wszystkie zależności
- Zainstaluje wymagane pakiety
- Zbuduje kontenery Docker
- Uruchomi serwisy

#### Opcja 2: Docker (Zalecane)

```bash
docker-compose up -d
```

#### Opcja 3: Instalacja Manualna

**Wymagania:**
- Python 3.10+
- PlantUML (wymaga Java)
- Graphviz
- Mermaid CLI
- Pandoc (do eksportu PDF/DOCX)

**Instalacja zależności:**

```bash
# macOS
brew install plantuml graphviz pandoc
npm install -g @mermaid-js/mermaid-cli

# Ubuntu/Debian
sudo apt-get install plantuml graphviz pandoc npm
npm install -g @mermaid-js/mermaid-cli

# Zainstaluj pakiety Python
pip install -r requirements.txt
```

### 📖 Użycie

#### Konfiguracja w Claude Desktop

Dodaj do `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "documentation": {
      "command": "python",
      "args": ["/ścieżka/do/mcp-doc-generator/src/server.py"]
    }
  }
}
```

#### Dostępne Narzędzia

1. **generate_c4_diagram** - Diagramy architektury C4 (Kontekst/Kontener/Komponent/Kod)
2. **generate_uml_diagram** - Diagramy UML (klasy, komponenty, deployment, pakiety, aktywności)
3. **generate_sequence_diagram** - Diagramy sekwencji (PlantUML)
4. **generate_flowchart** - Schematy blokowe (Mermaid)
5. **generate_mermaid_sequence** - Diagramy sekwencji (Mermaid)
6. **generate_gantt** - Wykresy Gantta dla harmonogramów projektów
7. **generate_dependency_graph** - Grafy zależności (Graphviz)
8. **generate_cloud_diagram** - Diagramy architektury chmurowej (draw.io)
9. **export_to_pdf** - Konwersja Markdown do PDF
10. **export_to_docx** - Konwersja Markdown do DOCX
11. **create_document_from_template** - Generowanie dokumentów z szablonów

### 💡 Przykłady Użycia

```python
# W Claude Desktop, po prostu zapytaj:
"Wygeneruj diagram kontekstu C4 dla systemu e-commerce z użytkownikami, 
aplikacją webową, bramką API i serwisem płatności. Eksportuj do PNG."

"Stwórz dokument ADR dla przejścia z REST na GraphQL."

"Wygeneruj wykres Gantta dla naszej mapy drogowej Q1 2025 i wyeksportuj do PDF."
```

### 🏗️ Architektura

```
mcp-doc-generator/
├── src/
│   ├── server.py              # Główny serwer MCP
│   ├── tools/                 # Implementacje narzędzi
│   │   ├── plantuml.py       # Integracja PlantUML
│   │   ├── mermaid.py        # Integracja Mermaid
│   │   ├── graphviz.py       # Integracja Graphviz
│   │   ├── drawio.py         # Integracja draw.io
│   │   └── export.py         # Eksport PDF/DOCX
│   ├── utils/                 # Narzędzia pomocnicze
│   │   ├── file_manager.py   # Operacje na plikach
│   │   └── polish_support.py # Wsparcie języka polskiego
│   └── templates/             # Szablony dokumentów
│       ├── adr_template.md
│       ├── api_spec_template.md
│       ├── c4_context_template.puml
│       └── microservices_overview_template.md
├── examples/                  # Przykłady użycia
├── output/                    # Wygenerowane pliki
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

### 🐳 Wdrożenie Docker

```bash
# Budowanie
docker build -t mcp-doc-generator .

# Uruchomienie
docker run -p 8000:8000 mcp-doc-generator

# Lub użyj docker-compose
docker-compose up -d
```

### 🧪 Testowanie

```bash
# Uruchom wszystkie testy
python test_all_tools.py

# Testuj konkretne narzędzie
python -c "from src.tools import plantuml; print('PlantUML OK')"
```

### 🌍 Wsparcie Języka Polskiego

Pełne wsparcie polskich znaków w:
- ✅ Eksporcie PDF (prawidłowe renderowanie czcionek)
- ✅ Dokumentach DOCX
- ✅ Diagramach (etykiety, opisy)
- ✅ Szablonach
- ✅ Nazwach plików i ścieżkach

Przykładowe polskie znaki: **ąćęłńóśźż ĄĆĘŁŃÓŚŹŻ**

### 📚 Przypadki Użycia

- **Architekci Oprogramowania**: Dokumentuj architekturę systemu za pomocą diagramów C4
- **Tech Leadzi**: Prowadź ADR-y i decyzje techniczne
- **Deweloperzy**: Generuj dokumentację API automatycznie
- **Technical Writerzy**: Twórz profesjonalną dokumentację szybko
- **DevOps**: Dokumentuj infrastrukturę i wdrożenia
- **Project Managerowie**: Twórz wykresy Gantta i harmonogramy

### 🤝 Współpraca

Wkłady są mile widziane! Przeczytaj [CONTRIBUTING.md](CONTRIBUTING.md) aby uzyskać szczegóły.

1. Sforkuj repozytorium
2. Utwórz branch dla swojej funkcji (`git checkout -b feature/super-funkcja`)
3. Zatwierdź swoje zmiany (`git commit -m 'Dodaj super funkcję'`)
4. Wypchnij do brancha (`git push origin feature/super-funkcja`)
5. Otwórz Pull Request

### 📄 Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) po szczegóły.

### 🙋 Wsparcie

- 📖 [Dokumentacja](examples/example_usage.md)
- 🐛 [Zgłoś Problem](https://github.com/lukaszzychal/mcp-doc-generator/issues)
- 💬 [Dyskusje](https://github.com/lukaszzychal/mcp-doc-generator/discussions)

### 🌟 Historia Gwiazdek

Jeśli ten projekt jest dla Ciebie użyteczny, rozważ danie mu ⭐ na GitHubie!

---

**Made with ❤️ for developers who value good documentation**

**Stworzone z ❤️ dla deweloperów, którzy cenią dobrą dokumentację**
