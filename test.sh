#!/bin/bash
set -e

echo "================================================"
echo "  MCP Documentation Server - Test Script"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

print_test() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $2"
    else
        echo -e "${RED}✗${NC} $2"
    fi
}

echo "Testing MCP Documentation Server components..."
echo ""

# Test 1: Check if Docker containers are running
echo "1. Docker Containers"
if docker ps | grep -q "mcp-plantuml-server"; then
    print_test 0 "PlantUML server is running"
else
    print_test 1 "PlantUML server is NOT running"
fi

if docker ps | grep -q "mcp-documentation-server"; then
    print_test 0 "MCP server is running"
else
    print_test 1 "MCP server is NOT running"
fi

echo ""

# Test 2: Check PlantUML server
echo "2. PlantUML Server Health"
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ | grep -q "200"; then
    print_test 0 "PlantUML server responds on http://localhost:8080"
else
    print_test 1 "PlantUML server not responding"
fi

echo ""

# Test 3: Check if output directory exists
echo "3. File System"
if [ -d "output" ]; then
    print_test 0 "Output directory exists"
else
    print_test 1 "Output directory missing"
    mkdir -p output
    echo "  Created output directory"
fi

echo ""

# Test 4: Check Python dependencies
echo "4. Python Dependencies"
if python3 -c "import mcp" 2>/dev/null; then
    print_test 0 "MCP package installed"
else
    print_test 1 "MCP package NOT installed"
fi

if python3 -c "import aiohttp" 2>/dev/null; then
    print_test 0 "aiohttp package installed"
else
    print_test 1 "aiohttp package NOT installed"
fi

echo ""

# Test 5: Check system tools
echo "5. System Tools"
if command -v mmdc >/dev/null 2>&1; then
    print_test 0 "mermaid-cli (mmdc) installed"
else
    print_test 1 "mermaid-cli (mmdc) NOT installed (will use Docker version)"
fi

if command -v pandoc >/dev/null 2>&1; then
    PANDOC_VERSION=$(pandoc --version | head -n1)
    print_test 0 "Pandoc installed: $PANDOC_VERSION"
else
    print_test 1 "Pandoc NOT installed (will use Docker version)"
fi

if command -v dot >/dev/null 2>&1; then
    print_test 0 "Graphviz installed"
else
    print_test 1 "Graphviz NOT installed (will use Docker version)"
fi

echo ""

# Test 6: Test PlantUML rendering (optional, requires server)
echo "6. Integration Test - PlantUML Rendering"
PLANTUML_TEST="@startuml\nAlice -> Bob: Hello\n@enduml"
if curl -s -X POST http://localhost:8080/png -d "$PLANTUML_TEST" -o /tmp/test_diagram.png 2>/dev/null; then
    if [ -f /tmp/test_diagram.png ] && [ -s /tmp/test_diagram.png ]; then
        print_test 0 "PlantUML rendering works"
        rm /tmp/test_diagram.png
    else
        print_test 1 "PlantUML rendering failed"
    fi
else
    print_test 1 "Could not connect to PlantUML server"
fi

echo ""
echo "================================================"
echo "  Test Summary"
echo "================================================"
echo ""
echo "If all tests pass, the server is ready to use!"
echo ""
echo "To use the server with Claude Desktop:"
echo "1. Configure claude_desktop_config.json"
echo "2. Restart Claude Desktop"
echo "3. Check if 'documentation' server appears"
echo ""

