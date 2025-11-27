#!/bin/bash
# Test instalacji przez npx dla mcp-doc-generator

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Test instalacji przez npx"
echo "=========================================="
echo ""

# Test 1: Sprawdź czy package.json istnieje
echo "1. Sprawdzanie package.json..."
if [ -f "package.json" ]; then
    echo -e "${GREEN}✓ package.json istnieje${NC}"
    cat package.json | grep -q '"name"' && echo -e "${GREEN}✓ package.json zawiera 'name'${NC}"
    cat package.json | grep -q '"bin"' && echo -e "${GREEN}✓ package.json zawiera 'bin'${NC}"
else
    echo -e "${RED}✗ package.json nie istnieje${NC}"
    exit 1
fi

# Test 2: Sprawdź czy wrapper istnieje
echo ""
echo "2. Sprawdzanie wrappera Node.js..."
if [ -f "bin/mcp-doc-generator.js" ]; then
    echo -e "${GREEN}✓ bin/mcp-doc-generator.js istnieje${NC}"
    if [ -x "bin/mcp-doc-generator.js" ]; then
        echo -e "${GREEN}✓ Wrapper jest wykonywalny${NC}"
    else
        echo -e "${YELLOW}⚠ Wrapper nie jest wykonywalny, ustawiam uprawnienia...${NC}"
        chmod +x bin/mcp-doc-generator.js
    fi
else
    echo -e "${RED}✗ bin/mcp-doc-generator.js nie istnieje${NC}"
    exit 1
fi

# Test 3: Sprawdź czy npx jest dostępny
echo ""
echo "3. Sprawdzanie npx..."
if command -v npx &> /dev/null; then
    echo -e "${GREEN}✓ npx jest dostępny${NC}"
    npx --version
else
    echo -e "${RED}✗ npx nie jest dostępny${NC}"
    exit 1
fi

# Test 4: Sprawdź czy Python jest dostępny
echo ""
echo "4. Sprawdzanie Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Python3 jest dostępny: ${PYTHON_VERSION}${NC}"
    
    # Sprawdź wersję Python (wymagane >= 3.10)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
        echo -e "${GREEN}✓ Python wersja jest >= 3.10${NC}"
    else
        echo -e "${YELLOW}⚠ Python wersja ${PYTHON_VERSION} może być za stara (wymagane >= 3.10)${NC}"
    fi
else
    echo -e "${RED}✗ Python3 nie jest dostępny${NC}"
    exit 1
fi

# Test 5: Test lokalnego uruchomienia przez npx (timeout 5 sekund)
echo ""
echo "5. Test lokalnego uruchomienia przez npx..."
echo "   (Uruchomię serwer przez npx . i sprawdzę czy odpowiada)"
echo ""

# Uruchom serwer w tle z timeoutem
timeout 3 npx . < /dev/null > /tmp/npx_test_output.log 2>&1 &
NPX_PID=$!

# Poczekaj chwilę
sleep 1

# Sprawdź czy proces działa
if ps -p $NPX_PID > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Serwer uruchomił się przez npx${NC}"
    # Zabij proces
    kill $NPX_PID 2>/dev/null || true
    wait $NPX_PID 2>/dev/null || true
else
    echo -e "${YELLOW}⚠ Serwer nie uruchomił się lub zakończył się zbyt szybko${NC}"
    echo "   Sprawdzam logi..."
    cat /tmp/npx_test_output.log 2>/dev/null || echo "   Brak logów"
fi

# Test 6: Sprawdź czy można użyć npx z GitHub (tylko informacyjnie)
echo ""
echo "6. Informacje o instalacji z GitHub:"
echo "   Aby zainstalować z GitHub, użyj:"
echo "   ${GREEN}npx github:lukaszzychal/mcp-doc-generator${NC}"
echo "   Lub z konkretnym tagiem:"
echo "   ${GREEN}npx github:lukaszzychal/mcp-doc-generator#v0.1.0${NC}"

echo ""
echo "=========================================="
echo -e "${GREEN}Testy podstawowe zakończone${NC}"
echo "=========================================="
echo ""
echo "Aby przetestować pełną funkcjonalność:"
echo "1. Uruchom: ${GREEN}npx .${NC}"
echo "2. W innym terminalu użyj klienta MCP do testowania"
echo "3. Lub użyj: ${GREEN}python3 scripts/mcp_client.py${NC} (wymaga modyfikacji do użycia npx)"

