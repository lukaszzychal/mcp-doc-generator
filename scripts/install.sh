#!/bin/bash
set -e

echo "================================================"
echo "  MCP Documentation Server - Instalator"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on macOS or Linux
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM=Linux;;
    Darwin*)    PLATFORM=Mac;;
    *)          PLATFORM="UNKNOWN:${OS}"
esac

echo "Platforma: $PLATFORM"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "1. Sprawdzanie zależności..."
echo ""

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status 0 "Python 3 zainstalowany: $PYTHON_VERSION"
else
    print_status 1 "Python 3 nie znaleziony"
    echo "Zainstaluj Python 3.10+:"
    if [ "$PLATFORM" = "Mac" ]; then
        echo "  brew install python@3.11"
    else
        echo "  sudo apt-get install python3.11"
    fi
    exit 1
fi

# Check Docker
if command_exists docker; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    print_status 0 "Docker zainstalowany: $DOCKER_VERSION"
else
    print_status 1 "Docker nie znaleziony"
    echo "Zainstaluj Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
if command_exists docker-compose || docker compose version >/dev/null 2>&1; then
    print_status 0 "Docker Compose zainstalowany"
    COMPOSE_CMD="docker compose"
    if ! docker compose version >/dev/null 2>&1; then
        COMPOSE_CMD="docker-compose"
    fi
else
    print_status 1 "Docker Compose nie znaleziony"
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_status 0 "Node.js zainstalowany: $NODE_VERSION"
else
    print_warning "Node.js nie znaleziony (opcjonalne, dla mermaid-cli)"
    echo "Zainstaluj Node.js:"
    if [ "$PLATFORM" = "Mac" ]; then
        echo "  brew install node"
    else
        echo "  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -"
        echo "  sudo apt-get install -y nodejs"
    fi
fi

echo ""
echo "2. Instalowanie zależności Python..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
print_status $? "Zależności Python zainstalowane"

echo ""
echo "3. Instalowanie mermaid-cli (globalne)..."
if command_exists npm; then
    npm install -g @mermaid-js/mermaid-cli
    print_status $? "mermaid-cli zainstalowany"
else
    print_warning "npm nie znaleziony, pomijam instalację mermaid-cli"
    echo "Mermaid będzie dostępny tylko w kontenerze Docker"
fi

echo ""
echo "4. Sprawdzanie dodatkowych narzędzi..."

# Check Pandoc
if command_exists pandoc; then
    PANDOC_VERSION=$(pandoc --version | head -n1)
    print_status 0 "Pandoc zainstalowany: $PANDOC_VERSION"
else
    print_warning "Pandoc nie znaleziony (będzie dostępny w Docker)"
    if [ "$PLATFORM" = "Mac" ]; then
        echo "  Zainstaluj: brew install pandoc"
    else
        echo "  Zainstaluj: sudo apt-get install pandoc texlive-xetex"
    fi
fi

# Check Graphviz
if command_exists dot; then
    GRAPHVIZ_VERSION=$(dot -V 2>&1)
    print_status 0 "Graphviz zainstalowany: $GRAPHVIZ_VERSION"
else
    print_warning "Graphviz nie znaleziony (będzie dostępny w Docker)"
    if [ "$PLATFORM" = "Mac" ]; then
        echo "  Zainstaluj: brew install graphviz"
    else
        echo "  Zainstaluj: sudo apt-get install graphviz"
    fi
fi

echo ""
echo "5. Tworzenie katalogów..."
mkdir -p output
print_status 0 "Katalog output utworzony"

echo ""
echo "6. Kopiowanie plików konfiguracyjnych..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_status 0 "Plik .env utworzony"
else
    print_status 0 "Plik .env już istnieje"
fi

echo ""
echo "7. Budowanie kontenerów Docker..."
$COMPOSE_CMD build
print_status $? "Kontenery zbudowane"

echo ""
echo "8. Uruchamianie serwisów..."
$COMPOSE_CMD up -d
print_status $? "Serwisy uruchomione"

echo ""
echo "9. Czekanie na uruchomienie PlantUML server..."
sleep 5
if curl -s http://localhost:8080/ >/dev/null; then
    print_status 0 "PlantUML server działa"
else
    print_warning "PlantUML server może jeszcze się uruchamiać..."
fi

echo ""
echo "================================================"
echo "  Instalacja zakończona!"
echo "================================================"
echo ""
echo "Następne kroki:"
echo ""
echo "1. Skonfiguruj MCP w Claude Desktop:"
echo "   Edytuj plik konfiguracyjny Claude:"
if [ "$PLATFORM" = "Mac" ]; then
    echo "   ~/Library/Application Support/Claude/claude_desktop_config.json"
else
    echo "   ~/.config/Claude/claude_desktop_config.json"
fi
echo ""
echo "   Dodaj serwer:"
echo '   {'
echo '     "mcpServers": {'
echo '       "documentation": {'
echo '         "command": "docker",'
echo '         "args": ["exec", "-i", "mcp-documentation-server", "python", "src/server.py"]'
echo '       }'
echo '     }'
echo '   }'
echo ""
echo "2. Zrestartuj Claude Desktop"
echo ""
echo "3. Sprawdź dostępne narzędzia:"
echo "   - generate_c4_diagram"
echo "   - generate_uml_diagram"
echo "   - generate_flowchart"
echo "   - export_to_pdf"
echo "   - i wiele innych!"
echo ""
echo "Użycie:"
echo "  Uruchom: $COMPOSE_CMD up -d"
echo "  Zatrzymaj: $COMPOSE_CMD down"
echo "  Logi: $COMPOSE_CMD logs -f"
echo ""
echo "Deployment do chmury:"
echo "  Fly.io: fly launch && fly deploy"
echo "  Railway: railway up"
echo ""

