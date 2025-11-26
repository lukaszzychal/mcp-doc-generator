#!/bin/bash
# Script to run MCP tests locally with Docker containers

set -e

echo "🧪 MCP Test Runner - Local Testing"
echo "===================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if containers are running
if ! docker ps | grep -q "mcp-documentation-server"; then
    echo "📦 Starting Docker containers..."
    docker compose up -d
    
    echo "⏳ Waiting for containers to be ready..."
    sleep 5
    
    # Wait for PlantUML server
    echo "⏳ Waiting for PlantUML server..."
    timeout=60
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if curl -f -s http://localhost:8080/ > /dev/null 2>&1; then
            echo "✅ PlantUML server is ready!"
            break
        fi
        echo "   Waiting... ($elapsed/$timeout seconds)"
        sleep 2
        elapsed=$((elapsed + 2))
    done
    
    if [ $elapsed -ge $timeout ]; then
        echo "❌ PlantUML server failed to start"
        docker compose logs plantuml
        exit 1
    fi
    
    # Wait for MCP server container
    echo "⏳ Waiting for MCP server container..."
    timeout=30
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        if docker ps | grep -q "mcp-documentation-server"; then
            echo "✅ MCP server container is running!"
            sleep 2
            break
        fi
        echo "   Waiting... ($elapsed/$timeout seconds)"
        sleep 2
        elapsed=$((elapsed + 2))
    done
else
    echo "✅ Containers are already running"
fi

echo ""
echo "🧪 Running tests..."
echo ""

# Test mode: full, quick, or custom
TEST_MODE="${1:-full}"

case "$TEST_MODE" in
    "full")
        echo "📋 Running FULL test (all formats and types)..."
        python3 tests/test_mcp_local.py
        ;;
    "quick")
        echo "📋 Running QUICK test (PNG only, dot layout)..."
        TEST_FORMATS=png TEST_LAYOUTS=dot python3 tests/test_mcp_local.py
        ;;
    "debug")
        echo "📋 Running test with DEBUG logging..."
        TEST_DEBUG=true python3 tests/test_mcp_local.py
        ;;
    *)
        echo "📋 Running custom test with: $*"
        "$@"
        python3 tests/test_mcp_local.py
        ;;
esac

TEST_EXIT_CODE=$?

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed (exit code: $TEST_EXIT_CODE)"
    echo ""
    echo "📋 Container logs:"
    docker compose logs mcp-server --tail 50
fi

exit $TEST_EXIT_CODE

