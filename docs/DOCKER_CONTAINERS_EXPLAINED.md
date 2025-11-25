# Docker Containers Usage Explained / Użycie Kontenerów Docker

## English

### Question: Does `python3 scripts/generate_examples.py` use both containers?

**Answer: YES** ✅

When you run `python3 scripts/generate_examples.py`, it uses **both Docker containers**:

1. **MCP Documentation Server container** (`mcp-documentation-server`)
   - The script uses `MCPClient()` which executes: `docker exec -i mcp-documentation-server python src/server.py`
   - This runs the MCP server inside the Docker container

2. **PlantUML Server container** (`mcp-plantuml-server`)
   - The MCP server inside the container has environment variable: `PLANTUML_SERVER=http://plantuml:8080`
   - When generating PlantUML diagrams (C4, UML, Sequence), the MCP server makes HTTP requests to `http://plantuml:8080`
   - This uses Docker's internal network to communicate between containers

### How it works:

```
Host Machine
    │
    ├─> python3 scripts/generate_examples.py
    │       │
    │       └─> MCPClient.start_server()
    │               │
    │               └─> docker exec -i mcp-documentation-server python src/server.py
    │                       │
    │                       └─> MCP Server (inside container)
    │                               │
    │                               └─> HTTP request to http://plantuml:8080
    │                                       │
    │                                       └─> PlantUML Server (inside container)
    │                                               │
    │                                               └─> Returns PNG/SVG
    │                                                       │
    │                                                       └─> Saved to output/ (mounted volume)
```

### Requirements:

Both containers must be running:
```bash
docker compose up -d
```

This starts:
- `mcp-plantuml-server` on port 8080
- `mcp-documentation-server` (MCP server)

---

## Polski

### Pytanie: Czy `python3 scripts/generate_examples.py` używa obu kontenerów?

**Odpowiedź: TAK** ✅

Gdy uruchamiasz `python3 scripts/generate_examples.py`, używa **obu kontenerów Docker**:

1. **Kontener MCP Documentation Server** (`mcp-documentation-server`)
   - Skrypt używa `MCPClient()`, który wykonuje: `docker exec -i mcp-documentation-server python src/server.py`
   - To uruchamia serwer MCP wewnątrz kontenera Docker

2. **Kontener PlantUML Server** (`mcp-plantuml-server`)
   - Serwer MCP wewnątrz kontenera ma zmienną środowiskową: `PLANTUML_SERVER=http://plantuml:8080`
   - Podczas generowania diagramów PlantUML (C4, UML, Sequence), serwer MCP wysyła żądania HTTP do `http://plantuml:8080`
   - To używa wewnętrznej sieci Docker do komunikacji między kontenerami

### Jak to działa:

```
Maszyna Host
    │
    ├─> python3 scripts/generate_examples.py
    │       │
    │       └─> MCPClient.start_server()
    │               │
    │               └─> docker exec -i mcp-documentation-server python src/server.py
    │                       │
    │                       └─> Serwer MCP (wewnątrz kontenera)
    │                               │
    │                               └─> Żądanie HTTP do http://plantuml:8080
    │                                       │
    │                                       └─> Serwer PlantUML (wewnątrz kontenera)
    │                                               │
    │                                               └─> Zwraca PNG/SVG
    │                                                       │
    │                                                       └─> Zapisane do output/ (zmountowany wolumen)
```

### Wymagania:

Oba kontenery muszą być uruchomione:
```bash
docker compose up -d
```

To uruchamia:
- `mcp-plantuml-server` na porcie 8080
- `mcp-documentation-server` (serwer MCP)

