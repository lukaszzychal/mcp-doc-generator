# PDF Conversion Flow - Who Does What?

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Question: Who actually performs the PDF conversion?

**Answer: The MCP Server performs the conversion.**

## Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PDF Conversion Flow                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│ External Script │  (convert_doc_via_mcp_simple.py)
│  (Client)       │
└────────┬────────┘
         │ 1. Sends JSON-RPC request
         │    {"method": "tools/call", "name": "export_to_pdf"}
         │
         ▼
┌─────────────────┐
│  MCP Server     │  (src/server.py)
│  call_tool()    │
└────────┬────────┘
         │ 2. Routes to export_tools.export_to_pdf()
         │
         ▼
┌─────────────────┐
│ export_to_pdf() │  (src/tools/export.py)
│  - Reads file    │  ← THIS IS WHERE CONVERSION HAPPENS
│  - Fixes images  │
│  - Calls Pandoc  │
│  - Generates PDF │
└────────┬────────┘
         │ 3. Executes: pandoc file.md -o output.pdf
         │
         ▼
┌─────────────────┐
│     Pandoc      │  (Inside Docker container)
│  + xelatex      │
└────────┬────────┘
         │ 4. Generates PDF file
         │
         ▼
┌─────────────────┐
│  output/file.pdf│  (Saved to /app/output/)
└─────────────────┘
```

## Detailed Explanation

### 1. External Scripts (convert_doc_via_mcp*.py)

**Role:** External clients that call the MCP server

**What they do:**
- Send JSON-RPC requests to MCP server
- Handle communication protocol
- Display results

**What they DON'T do:**
- ❌ They do NOT perform PDF conversion
- ❌ They do NOT call Pandoc directly
- ❌ They do NOT process markdown files

**Code location:** `scripts/convert_doc_via_mcp_simple.py` (lines 103-113)

```python
# Script sends request to MCP server
tool_request = send_mcp_request("tools/call", {
    "name": "export_to_pdf",  # ← Calls MCP tool
    "arguments": {...}
})
```

### 2. MCP Server (src/server.py)

**Role:** Routes requests to appropriate tool functions

**What it does:**
- Receives JSON-RPC request
- Routes to `export_tools.export_to_pdf()`
- Returns result to client

**Code location:** `src/server.py` (lines 403-410)

```python
elif name == "export_to_pdf":
    result = await export_tools.export_to_pdf(  # ← Routes to tool
        markdown_file_path=arguments.get("markdown_file_path"),
        output_path=arguments["output_path"],
        ...
    )
```

### 3. Export Tool (src/tools/export.py)

**Role: ACTUALLY PERFORMS THE CONVERSION**

**What it does:**
- ✅ Reads markdown file
- ✅ Fixes image paths
- ✅ Prepares metadata
- ✅ **Calls Pandoc to convert to PDF** ← CONVERSION HAPPENS HERE
- ✅ Saves PDF file

**Code location:** `src/tools/export.py` (lines 61-186)

```python
async def export_to_pdf(...):
    # Read file
    markdown_content = read_file(str(file_path))
    
    # Fix image paths
    markdown_content = fix_image_paths(...)
    
    # Build Pandoc command
    cmd = ["pandoc", tmp_path, "-o", str(abs_output), ...]
    
    # Run Pandoc ← THIS IS THE ACTUAL CONVERSION
    process = await asyncio.create_subprocess_exec(*cmd, ...)
    
    # PDF is generated here!
```

## Summary

| Component | Role | Does Conversion? |
|-----------|------|------------------|
| `convert_doc_via_mcp_simple.py` | External client | ❌ No - just sends request |
| `src/server.py` | MCP server router | ❌ No - just routes request |
| `src/tools/export.py` | Export tool | ✅ **YES - performs conversion** |
| Pandoc (in container) | PDF engine | ✅ Yes - generates PDF |

## Verification

You can verify this by checking:

1. **Pandoc is in Docker container:**
   ```bash
   docker exec mcp-documentation-server which pandoc
   # Output: /usr/bin/pandoc
   ```

2. **Conversion happens in container:**
   - Check logs: `docker logs mcp-documentation-server`
   - PDF is created in `/app/output/` inside container

3. **Script only sends requests:**
   - Script has no Pandoc calls
   - Script only sends JSON-RPC messages

---

<a name="polski"></a>
# Polski

## Pytanie: Kto faktycznie wykonuje konwersję PDF?

**Odpowiedź: Serwer MCP wykonuje konwersję.**

## Diagram Przepływu

```
┌─────────────────────────────────────────────────────────────┐
│                    Przepływ Konwersji PDF                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│ Skrypt Zewnętrzny│  (convert_doc_via_mcp_simple.py)
│  (Klient)       │
└────────┬────────┘
         │ 1. Wysyła żądanie JSON-RPC
         │    {"method": "tools/call", "name": "export_to_pdf"}
         │
         ▼
┌─────────────────┐
│  Serwer MCP     │  (src/server.py)
│  call_tool()    │
└────────┬────────┘
         │ 2. Przekierowuje do export_tools.export_to_pdf()
         │
         ▼
┌─────────────────┐
│ export_to_pdf() │  (src/tools/export.py)
│  - Czyta plik   │  ← TUTAJ DZIEJE SIĘ KONWERSJA
│  - Naprawia img │
│  - Wywołuje Pandoc│
│  - Generuje PDF │
└────────┬────────┘
         │ 3. Wykonuje: pandoc file.md -o output.pdf
         │
         ▼
┌─────────────────┐
│     Pandoc      │  (Wewnątrz kontenera Docker)
│  + xelatex      │
└────────┬────────┘
         │ 4. Generuje plik PDF
         │
         ▼
┌─────────────────┐
│  output/file.pdf│  (Zapisany w /app/output/)
└─────────────────┘
```

## Szczegółowe Wyjaśnienie

### 1. Skrypty Zewnętrzne (convert_doc_via_mcp*.py)

**Rola:** Zewnętrzni klienci wywołujący serwer MCP

**Co robią:**
- Wysyłają żądania JSON-RPC do serwera MCP
- Obsługują protokół komunikacji
- Wyświetlają wyniki

**Czego NIE robią:**
- ❌ NIE wykonują konwersji PDF
- ❌ NIE wywołują Pandoc bezpośrednio
- ❌ NIE przetwarzają plików markdown

**Lokalizacja kodu:** `scripts/convert_doc_via_mcp_simple.py` (linie 103-113)

```python
# Skrypt wysyła żądanie do serwera MCP
tool_request = send_mcp_request("tools/call", {
    "name": "export_to_pdf",  # ← Wywołuje narzędzie MCP
    "arguments": {...}
})
```

### 2. Serwer MCP (src/server.py)

**Rola:** Przekierowuje żądania do odpowiednich funkcji narzędziowych

**Co robi:**
- Otrzymuje żądanie JSON-RPC
- Przekierowuje do `export_tools.export_to_pdf()`
- Zwraca wynik klientowi

**Lokalizacja kodu:** `src/server.py` (linie 403-410)

```python
elif name == "export_to_pdf":
    result = await export_tools.export_to_pdf(  # ← Przekierowuje do narzędzia
        markdown_file_path=arguments.get("markdown_file_path"),
        output_path=arguments["output_path"],
        ...
    )
```

### 3. Narzędzie Eksportu (src/tools/export.py)

**Rola: FAKTYCZNIE WYKONUJE KONWERSJĘ**

**Co robi:**
- ✅ Czyta plik markdown
- ✅ Naprawia ścieżki obrazków
- ✅ Przygotowuje metadane
- ✅ **Wywołuje Pandoc do konwersji na PDF** ← KONWERSJA DZIEJE SIĘ TUTAJ
- ✅ Zapisuje plik PDF

**Lokalizacja kodu:** `src/tools/export.py` (linie 61-186)

```python
async def export_to_pdf(...):
    # Czytanie pliku
    markdown_content = read_file(str(file_path))
    
    # Naprawianie ścieżek obrazków
    markdown_content = fix_image_paths(...)
    
    # Budowanie komendy Pandoc
    cmd = ["pandoc", tmp_path, "-o", str(abs_output), ...]
    
    # Uruchomienie Pandoc ← TO JEST RZECZYWISTA KONWERSJA
    process = await asyncio.create_subprocess_exec(*cmd, ...)
    
    # PDF jest generowany tutaj!
```

## Podsumowanie

| Komponent | Rola | Wykonuje Konwersję? |
|-----------|------|---------------------|
| `convert_doc_via_mcp_simple.py` | Zewnętrzny klient | ❌ Nie - tylko wysyła żądanie |
| `src/server.py` | Router serwera MCP | ❌ Nie - tylko przekierowuje żądanie |
| `src/tools/export.py` | Narzędzie eksportu | ✅ **TAK - wykonuje konwersję** |
| Pandoc (w kontenerze) | Silnik PDF | ✅ Tak - generuje PDF |

## Weryfikacja

Możesz to zweryfikować sprawdzając:

1. **Pandoc jest w kontenerze Docker:**
   ```bash
   docker exec mcp-documentation-server which pandoc
   # Wynik: /usr/bin/pandoc
   ```

2. **Konwersja dzieje się w kontenerze:**
   - Sprawdź logi: `docker logs mcp-documentation-server`
   - PDF jest tworzony w `/app/output/` wewnątrz kontenera

3. **Skrypt tylko wysyła żądania:**
   - Skrypt nie ma wywołań Pandoc
   - Skrypt tylko wysyła wiadomości JSON-RPC

