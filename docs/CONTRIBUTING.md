# Contributing to MCP Documentation Server

Dziękujemy za zainteresowanie kontrybuowaniem do projektu! 🎉

## Jak zacząć

1. Fork repozytorium
2. Sklonuj swój fork lokalnie
3. Utwórz branch dla swojej funkcji: `git checkout -b feature/moja-funkcja`
4. Wprowadź zmiany
5. Przetestuj zmiany
6. Commit z opisowym message: `git commit -m "Add: nowa funkcja X"`
7. Push do swojego forka: `git push origin feature/moja-funkcja`
8. Utwórz Pull Request

## Standardy Kodu

### Python

- Używamy Python 3.10+
- Formatowanie: Black (line length: 100)
- Linting: Ruff
- Type hints dla wszystkich funkcji publicznych
- Docstrings w stylu Google

```python
def example_function(param: str, optional: int = 10) -> dict:
    """
    Short description of the function.
    
    Args:
        param: Description of param
        optional: Description of optional parameter
        
    Returns:
        Description of return value
    """
    return {"result": param}
```

### Commit Messages

Format: `<type>: <description>`

Types:
- `Add:` - nowa funkcjonalność
- `Fix:` - naprawa błędu
- `Update:` - aktualizacja istniejącej funkcji
- `Refactor:` - refaktoring kodu
- `Docs:` - zmiany w dokumentacji
- `Test:` - dodanie lub aktualizacja testów
- `Chore:` - maintenance (dependencies, config)

Przykłady:
```
Add: support for PDF bookmarks
Fix: Polish characters in DOCX export
Update: PlantUML server configuration
Docs: add examples for API documentation
```

## Testowanie

```bash
# Uruchom testy
pytest

# Z coverage
pytest --cov=src

# Tylko określone testy
pytest tests/test_plantuml.py
```

## Dodawanie Nowych Narzędzi

### 1. Utwórz moduł w `src/tools/`

```python
# src/tools/my_tool.py

async def my_tool_function(
    param: str,
    output_path: str,
    format: str = "png"
) -> str:
    """
    Description of what the tool does.
    
    Args:
        param: Description
        output_path: Output file path
        format: Output format
        
    Returns:
        Success message
    """
    try:
        # Implementation
        return f"✓ Tool completed: {output_path}"
    except Exception as e:
        return f"✗ Error: {str(e)}"
```

### 2. Dodaj do `server.py`

W `list_tools()`:
```python
Tool(
    name="my_tool",
    description="Description of the tool",
    inputSchema={
        "type": "object",
        "properties": {
            "param": {
                "type": "string",
                "description": "Parameter description"
            }
        },
        "required": ["param"]
    }
)
```

W `call_tool()`:
```python
elif name == "my_tool":
    result = await my_tool.my_tool_function(
        arguments["param"],
        arguments["output_path"]
    )
```

### 3. Dodaj testy

```python
# tests/test_my_tool.py

import pytest
from tools import my_tool

@pytest.mark.asyncio
async def test_my_tool():
    result = await my_tool.my_tool_function(
        "test",
        "output/test.png"
    )
    assert "✓" in result
```

### 4. Aktualizuj dokumentację

- README.md - dodaj sekcję o nowym narzędziu
- examples/ - dodaj przykład użycia

## Dodawanie Szablonów

1. Utwórz szablon w `src/templates/`
2. Użyj placeholder format: `{{variable_name}}`
3. Dodaj wsparcie w `export.py`
4. Dodaj przykład wypełnionego szablonu w `examples/`

## Review Process

1. Pull Request musi przejść CI checks
2. Minimum 1 approval od maintainera
3. Kod musi być sformatowany (black, ruff)
4. Testy muszą przechodzić
5. Dokumentacja musi być zaktualizowana

## Pytania?

- Otwórz [Issue](https://github.com/lukaszzychal/mcp-doc-generator/issues) z pytaniem
- Dołącz do [dyskusji](https://github.com/lukaszzychal/mcp-doc-generator/discussions) w istniejących Issues
- Skontaktuj się z maintainerami: lukasz.zychal.dev@gmail.com

## Kodeks Postępowania

- Bądź uprzejmy i szanuj innych
- Konstruktywna krytyka mile widziana
- Zero tolerancji dla harassment
- Pomóż innym rosnąć i uczyć się

## Licencja

Kontrybuując do tego projektu, zgadzasz się na licencję MIT.

