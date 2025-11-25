#!/bin/bash
# Test integracji MCP z Cursor

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "================================================"
echo "  Test integracji MCP z Cursor"
echo "================================================"
echo ""

# Sprawdź czy kontenery Docker działają
echo "1. Sprawdzanie kontenerów Docker..."
if docker ps | grep -q "mcp-documentation-server"; then
    echo -e "${GREEN}✓ MCP documentation server działa${NC}"
else
    echo -e "${RED}✗ MCP documentation server NIE działa${NC}"
    echo "  Uruchom: docker compose up -d"
    exit 1
fi

if docker ps | grep -q "mcp-plantuml-server"; then
    echo -e "${GREEN}✓ PlantUML server działa${NC}"
else
    echo -e "${RED}✗ PlantUML server NIE działa${NC}"
    exit 1
fi

echo ""

# Sprawdź konfigurację Cursor
echo "2. Sprawdzanie konfiguracji Cursor..."

CURSOR_CONFIG_DIR="$HOME/Library/Application Support/Cursor"
CURSOR_USER_DIR="$CURSOR_CONFIG_DIR/User"

if [ -d "$CURSOR_CONFIG_DIR" ]; then
    echo -e "${GREEN}✓ Katalog Cursor istnieje${NC}"
    
    # Sprawdź logi MCP
    if [ -d "$CURSOR_CONFIG_DIR/logs" ]; then
        echo -e "${GREEN}✓ Katalog logów istnieje${NC}"
        
        # Znajdź najnowsze logi
        LATEST_LOG=$(find "$CURSOR_CONFIG_DIR/logs" -type d -name "*" | sort -r | head -1)
        if [ -n "$LATEST_LOG" ]; then
            echo "  Najnowsze logi: $LATEST_LOG"
            
            # Sprawdź logi MCP
            MCP_LOGS=$(find "$LATEST_LOG" -name "*mcp*" -type f 2>/dev/null | head -5)
            if [ -n "$MCP_LOGS" ]; then
                echo -e "${GREEN}✓ Znaleziono logi MCP${NC}"
                echo "  Logi MCP:"
                echo "$MCP_LOGS" | while read log; do
                    echo "    - $log"
                done
            else
                echo -e "${YELLOW}⚠ Nie znaleziono logów MCP${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}⚠ Katalog logów nie istnieje${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Katalog Cursor nie istnieje${NC}"
    echo "  Cursor może nie być zainstalowany lub używa innej lokalizacji"
fi

echo ""

# Sprawdź czy MCP server odpowiada
echo "3. Test połączenia z MCP server..."

# Test przez docker exec
if docker exec mcp-documentation-server python -c "import sys; sys.path.insert(0, '/app/src'); from server import app; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✓ MCP server odpowiada${NC}"
else
    echo -e "${RED}✗ MCP server nie odpowiada${NC}"
fi

echo ""

# Lista wszystkich narzędzi
echo "4. Lista dostępnych narzędzi MCP:"
echo ""
echo "Następujące narzędzia powinny być dostępne w Cursor:"
echo ""
echo "  1. generate_c4_diagram"
echo "     - Typy: context, container, component, code"
echo "     - Formaty: png, svg"
echo ""
echo "  2. generate_uml_diagram"
echo "     - Typy: class, component, deployment, package, activity, usecase"
echo "     - Formaty: png, svg"
echo ""
echo "  3. generate_sequence_diagram"
echo "     - Formaty: png, svg"
echo ""
echo "  4. generate_flowchart"
echo "     - Formaty: png, svg"
echo ""
echo "  5. generate_mermaid_sequence"
echo "     - Formaty: png, svg"
echo ""
echo "  6. generate_gantt"
echo "     - Formaty: png, svg"
echo ""
echo "  7. generate_dependency_graph"
echo "     - Layouty: dot, neato, fdp, circo, twopi"
echo "     - Formaty: png, svg, pdf"
echo ""
echo "  8. generate_cloud_diagram"
echo "     - Formaty: png, svg, pdf"
echo ""
echo "  9. export_to_pdf"
echo "     - Eksport markdown do PDF"
echo ""
echo "  10. export_to_docx"
echo "     - Eksport markdown do DOCX"
echo ""
echo "  11. create_document_from_template"
echo "     - Szablony: adr, api_spec, c4_context, microservices_overview"
echo ""

echo "5. Instrukcje testowania w Cursor:"
echo ""
echo "Aby przetestować narzędzia w Cursor:"
echo ""
echo "  1. Upewnij się, że kontenery Docker działają:"
echo "     docker compose ps"
echo ""
echo "  2. W Cursor, otwórz nową konwersację"
echo ""
echo "  3. Spróbuj użyć narzędzia MCP, np.:"
echo "     'Wygeneruj C4 Context Diagram dla systemu e-commerce'"
echo ""
echo "  4. Sprawdź czy narzędzie jest dostępne i działa"
echo ""
echo "  5. Sprawdź czy pliki są tworzone w katalogu output/"
echo ""
echo "  6. Jeśli narzędzie nie działa, sprawdź logi Cursor:"
echo "     $CURSOR_CONFIG_DIR/logs/"
echo ""

echo "6. Test ręczny - sprawdź czy narzędzia są widoczne:"
echo ""
echo "W Cursor, sprawdź czy widzisz narzędzia MCP w:"
echo "  - Ustawieniach (Settings)"
echo "  - Lista dostępnych narzędzi w konwersacji"
echo ""

echo "================================================"
echo "  Test zakończony"
echo "================================================"

