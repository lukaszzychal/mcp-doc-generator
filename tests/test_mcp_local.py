#!/usr/bin/env python3
"""
Test MCP server lokalnie przez Docker (docker exec).
Testuje wszystkie 11 narzędzi z wszystkimi dostępnymi opcjami.
Zoptymalizowany z równoległym wykonywaniem testów.
"""

import json
import asyncio
import subprocess
import sys
import os
import time
import threading
import queue
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional

# Kolory dla outputu
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

# Konfiguracja przez zmienne środowiskowe
TEST_FORMATS = os.getenv("TEST_FORMATS", "png,svg").split(",")
TEST_LAYOUTS = os.getenv("TEST_LAYOUTS", "dot,neato,fdp,circo,twopi").split(",")
TEST_C4_TYPES = os.getenv("TEST_C4_TYPES", "context,container,component,code").split(",")
TEST_UML_TYPES = os.getenv("TEST_UML_TYPES", "class,component,deployment,package,activity,usecase").split(",")
TEST_PARALLEL = int(os.getenv("TEST_PARALLEL", "10"))


class MCPTester:
    def __init__(self):
        self.process = None
        self.request_id = 0
        self.results = []
        self.request_lock = threading.Lock()  # Lock dla request_id i pending_responses
        self.stdin_lock = threading.Lock()  # Lock tylko dla zapisu do stdin
        self.response_queue = queue.Queue()  # Thread-safe queue
        self.pending_responses = {}  # request_id -> {"event": asyncio.Event, "response": None}
        self.reader_thread = None
        self.shutdown_event = threading.Event()
        self.loop = None  # Will be set when async context starts
        
    async def start_server(self):
        """Uruchom MCP server przez docker exec"""
        cmd = [
            "docker", "exec", "-i", "mcp-documentation-server",
            "python", "src/server.py"
        ]
        try:
            # Użyj synchronicznego subprocess (działa lepiej z docker exec)
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            
            # Sprawdź czy proces się nie zakończył natychmiast
            time.sleep(0.1)
            if self.process.poll() is not None:
                stderr_output = self.process.stderr.read(1024) if self.process.stderr else ""
                raise Exception(f"Process exited immediately with code {self.process.returncode}. Stderr: {stderr_output}")
            
            # Start background reader thread
            self.reader_thread = threading.Thread(target=self._read_responses_thread, daemon=True)
            self.reader_thread.start()
            
            # Czekaj na inicjalizację
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"{RED}Error starting server: {e}{NC}")
            if self.process:
                try:
                    stderr_output = self.process.stderr.read(1024) if self.process.stderr else ""
                    if stderr_output:
                        print(f"{RED}Stderr: {stderr_output}{NC}")
                except:
                    pass
            raise
        
    def _read_responses_thread(self):
        """Czytaj odpowiedzi z serwera w tle (w osobnym wątku)"""
        try:
            while not self.shutdown_event.is_set():
                if self.process.poll() is not None:
                    # Proces się zakończył
                    break
                    
                try:
                    line = self.process.stdout.readline()
                    if not line:
                        # EOF - proces się zakończył
                        break
                    if line.strip():
                        try:
                            response = json.loads(line.strip())
                            response_id = response.get("id")
                            if response_id and response_id in self.pending_responses:
                                # Znaleziono odpowiedź dla oczekującego żądania
                                self.pending_responses[response_id]["response"] = response
                                # Użyj asyncio.run_coroutine_threadsafe do ustawienia eventu
                                if self.loop and self.loop.is_running():
                                    asyncio.run_coroutine_threadsafe(
                                        self.pending_responses[response_id]["event"].set(),
                                        self.loop
                                    )
                                else:
                                    # Fallback - ustaw bezpośrednio jeśli loop nie działa
                                    try:
                                        self.pending_responses[response_id]["event"].set()
                                    except:
                                        pass
                            else:
                                # Dodaj do kolejki ogólnej (thread-safe queue)
                                self.response_queue.put(response)
                        except json.JSONDecodeError:
                            # Ignoruj nieprawidłowe JSON
                            continue
                except Exception as e:
                    error_str = str(e).lower()
                    if any(err in error_str for err in ["broken pipe", "connection reset", "eof"]):
                        break
                    print(f"{RED}Error reading responses: {e}{NC}")
                    break
        except Exception as e:
            error_str = str(e).lower()
            if not any(err in error_str for err in ["broken pipe", "connection reset", "eof"]):
                print(f"{RED}Error in response reader: {e}{NC}")
        finally:
            # Oznacz wszystkie oczekujące żądania jako timeout
            for pending in self.pending_responses.values():
                if pending["response"] is None:
                    pending["response"] = {"error": {"message": "Connection closed"}}
                if self.loop and self.loop.is_running():
                    asyncio.run_coroutine_threadsafe(pending["event"].set(), self.loop)
                else:
                    try:
                        pending["event"].set()
                    except:
                        pass
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wyślij żądanie JSON-RPC do MCP server"""
        # Tylko lock dla request_id (żeby było unikalne)
        with self.request_lock:
            self.request_id += 1
            request_id = self.request_id
        
        # Przygotuj żądanie poza lockiem
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method
        }
        if params:
            request["params"] = params
            
        request_json = json.dumps(request) + "\n"
        
        # Utwórz event do oczekiwania na odpowiedź
        response_event = asyncio.Event()
        with self.request_lock:
            self.pending_responses[request_id] = {
                "event": response_event,
                "response": None
            }
        
        try:
            # Wyślij żądanie (synchronicznie, bo to subprocess.Popen)
            # Lock tylko dla zapisu do stdin (żeby nie mieszać danych)
            with self.stdin_lock:
                if self.process.poll() is not None:
                    return {"error": {"message": "Process has terminated"}}
                self.process.stdin.write(request_json)
                self.process.stdin.flush()
            
            # Czekaj na odpowiedź z timeoutem
            try:
                await asyncio.wait_for(response_event.wait(), timeout=60.0)
                response = self.pending_responses[request_id]["response"]
                if response:
                    return response
                else:
                    # Sprawdź w kolejce jako fallback (z timeoutem)
                    # Użyj thread-safe queue.get z timeoutem
                    try:
                        while True:
                            try:
                                queued_response = self.response_queue.get(timeout=0.1)
                                if queued_response.get("id") == request_id:
                                    return queued_response
                                # Jeśli to nie nasza odpowiedź, zwróć z powrotem
                                self.response_queue.put(queued_response)
                            except queue.Empty:
                                return {"error": {"message": "No response received"}}
                    except Exception:
                        return {"error": {"message": "No response received"}}
            except asyncio.TimeoutError:
                return {"error": {"message": "Request timeout"}}
        finally:
            # Usuń z pending_responses
            with self.request_lock:
                if request_id in self.pending_responses:
                    del self.pending_responses[request_id]
        
    async def initialize(self) -> bool:
        """Inicjalizuj połączenie MCP"""
        print(f"{YELLOW}Inicjalizacja MCP...{NC}")
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        if response and "result" in response:
            print(f"{GREEN}✓ Inicjalizacja zakończona sukcesem{NC}")
            return True
        else:
            print(f"{RED}✗ Błąd inicjalizacji: {response}{NC}")
            return False
            
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Pobierz listę dostępnych narzędzi"""
        print(f"{YELLOW}Pobieranie listy narzędzi...{NC}")
        response = await self.send_request("tools/list")
        
        if response and "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"{GREEN}✓ Znaleziono {len(tools)} narzędzi{NC}")
            return tools
        else:
            print(f"{RED}✗ Błąd pobierania narzędzi: {response}{NC}")
            return []
            
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Tuple[bool, str]:
        """Wywołaj narzędzie MCP"""
        try:
            response = await self.send_request("tools/call", {
                "name": name,
                "arguments": arguments
            })
            
            if not response:
                return False, "No response from server"
                
            if "result" in response:
                if "content" in response["result"]:
                    content = response["result"]["content"][0]
                    if "text" in content:
                        return True, content["text"]
            elif "error" in response:
                error_msg = response["error"].get("message", "Unknown error")
                return False, error_msg
                
            return False, f"Unexpected response format: {str(response)[:200]}"
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    async def _test_single_c4(self, diagram_type: str, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego C4 diagramu"""
        output_path = f"output/test_c4_{diagram_type}.{fmt}"
        content = f"""@startuml
Person(user, "User")
System(system, "System")
Rel(user, system, "Uses")
@enduml"""
        
        success, result = await self.call_tool("generate_c4_diagram", {
            "diagram_type": diagram_type,
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} {diagram_type} ({fmt}): {result[:80]}")
        
        # Sprawdź czy plik istnieje
        file_size = 0
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                file_size = file_path.stat().st_size
                print(f"    {GREEN}✓ Plik utworzony: {file_size} bytes{NC}")
            else:
                print(f"    {RED}✗ Plik nie istnieje lub jest pusty{NC}")
        
        return {
            "tool": "generate_c4_diagram",
            "type": diagram_type,
            "format": fmt,
            "success": success,
            "result": result
        }
        
    async def test_c4_diagram(self):
        """Test generate_c4_diagram - wszystkie typy i formaty (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_c4_diagram ==={NC}")
        
        types = [t for t in ["context", "container", "component", "code"] if t in TEST_C4_TYPES]
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        
        # Utwórz wszystkie zadania
        tasks = []
        for diagram_type in types:
            for fmt in formats:
                tasks.append(self._test_single_c4(diagram_type, fmt))
        
        # Wykonaj równolegle z limitem
        semaphore = asyncio.Semaphore(TEST_PARALLEL)
        
        async def run_with_semaphore(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[run_with_semaphore(task) for task in tasks])
        self.results.extend(results)
    
    async def _test_single_uml(self, diagram_type: str, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego UML diagramu"""
        output_path = f"output/test_uml_{diagram_type}.{fmt}"
        content = f"""class User {{
  +name: string
}}
class Order {{
  +id: int
}}
User --> Order"""
        
        success, result = await self.call_tool("generate_uml_diagram", {
            "diagram_type": diagram_type,
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} {diagram_type} ({fmt}): {result[:80]}")
        
        file_size = 0
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                file_size = file_path.stat().st_size
                print(f"    {GREEN}✓ Plik utworzony: {file_size} bytes{NC}")
            else:
                print(f"    {RED}✗ Plik nie istnieje{NC}")
        
        return {
            "tool": "generate_uml_diagram",
            "type": diagram_type,
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_uml_diagram(self):
        """Test generate_uml_diagram - wszystkie typy i formaty (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_uml_diagram ==={NC}")
        
        types = [t for t in ["class", "component", "deployment", "package", "activity", "usecase"] if t in TEST_UML_TYPES]
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        
        tasks = []
        for diagram_type in types:
            for fmt in formats:
                tasks.append(self._test_single_uml(diagram_type, fmt))
        
        semaphore = asyncio.Semaphore(TEST_PARALLEL)
        
        async def run_with_semaphore(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[run_with_semaphore(task) for task in tasks])
        self.results.extend(results)
    
    async def _test_single_sequence(self, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego sequence diagramu"""
        output_path = f"output/test_sequence.{fmt}"
        content = """Alice -> Bob: Hello
Bob --> Alice: Hi"""
        
        success, result = await self.call_tool("generate_sequence_diagram", {
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_sequence_diagram",
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_sequence_diagram(self):
        """Test generate_sequence_diagram (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_sequence_diagram ==={NC}")
        
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        tasks = [self._test_single_sequence(fmt) for fmt in formats]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def _test_single_flowchart(self, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego flowchart"""
        output_path = f"output/test_flowchart.{fmt}"
        content = """flowchart TD
    Start --> Check{Valid?}
    Check -->|Yes| Process
    Check -->|No| Error
    Process --> End"""
        
        success, result = await self.call_tool("generate_flowchart", {
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_flowchart",
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_flowchart(self):
        """Test generate_flowchart (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_flowchart ==={NC}")
        
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        tasks = [self._test_single_flowchart(fmt) for fmt in formats]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def _test_single_mermaid_sequence(self, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego mermaid sequence"""
        output_path = f"output/test_mermaid_sequence.{fmt}"
        content = """sequenceDiagram
    User->>API: Request
    API->>DB: Query
    DB-->>API: Data
    API-->>User: Response"""
        
        success, result = await self.call_tool("generate_mermaid_sequence", {
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_mermaid_sequence",
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_mermaid_sequence(self):
        """Test generate_mermaid_sequence (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_mermaid_sequence ==={NC}")
        
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        tasks = [self._test_single_mermaid_sequence(fmt) for fmt in formats]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def _test_single_gantt(self, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego gantt"""
        output_path = f"output/test_gantt.{fmt}"
        content = """gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Task 1 :a1, 2024-01-01, 30d
    Task 2 :a2, after a1, 20d
    section Phase 2
    Task 3 :a3, 2024-02-01, 15d"""
        
        success, result = await self.call_tool("generate_gantt", {
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_gantt",
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_gantt(self):
        """Test generate_gantt (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_gantt ==={NC}")
        
        formats = [f for f in ["png", "svg"] if f in TEST_FORMATS]
        tasks = [self._test_single_gantt(fmt) for fmt in formats]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def _test_single_dependency(self, layout: str, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego dependency graph"""
        output_path = f"output/test_dependency_{layout}.{fmt}"
        content = """digraph G {
    A -> B
    B -> C
    C -> A
}"""
        
        success, result = await self.call_tool("generate_dependency_graph", {
            "content": content,
            "output_path": output_path,
            "format": fmt,
            "layout": layout
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} {layout} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_dependency_graph",
            "layout": layout,
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_dependency_graph(self):
        """Test generate_dependency_graph - wszystkie layouty i formaty (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_dependency_graph ==={NC}")
        
        layouts = [l for l in ["dot", "neato", "fdp", "circo", "twopi"] if l in TEST_LAYOUTS]
        formats = [f for f in ["png", "svg", "pdf"] if f in TEST_FORMATS]
        
        tasks = []
        for layout in layouts:
            for fmt in formats:
                tasks.append(self._test_single_dependency(layout, fmt))
        
        semaphore = asyncio.Semaphore(TEST_PARALLEL)
        
        async def run_with_semaphore(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[run_with_semaphore(task) for task in tasks])
        self.results.extend(results)
    
    async def _test_single_cloud(self, fmt: str) -> Dict[str, Any]:
        """Test pojedynczego cloud diagram"""
        output_path = f"output/test_cloud.{fmt}"
        content = """<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="Cloud" style="shape=cloud" vertex="1" parent="1"><mxGeometry x="100" y="100" width="100" height="60" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>"""
        
        success, result = await self.call_tool("generate_cloud_diagram", {
            "content": content,
            "output_path": output_path,
            "format": fmt
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} ({fmt}): {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony{NC}")
        
        return {
            "tool": "generate_cloud_diagram",
            "format": fmt,
            "success": success,
            "result": result
        }
    
    async def test_cloud_diagram(self):
        """Test generate_cloud_diagram (równolegle)"""
        print(f"\n{YELLOW}=== Test: generate_cloud_diagram ==={NC}")
        
        formats = [f for f in ["png", "svg", "pdf"] if f in TEST_FORMATS]
        tasks = [self._test_single_cloud(fmt) for fmt in formats]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def test_export_to_pdf(self):
        """Test export_to_pdf"""
        print(f"\n{YELLOW}=== Test: export_to_pdf ==={NC}")
        
        markdown_content = """# Test Document

This is a test document.

## Section 1

Some content here.

## Section 2

More content.
"""
        
        output_path = "output/test_export.pdf"
        success, result = await self.call_tool("export_to_pdf", {
            "markdown_content": markdown_content,
            "output_path": output_path,
            "title": "Test Document",
            "author": "Test Author",
            "include_toc": True
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status}: {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony: {file_path.stat().st_size} bytes{NC}")
                
        self.results.append({
            "tool": "export_to_pdf",
            "success": success,
            "result": result
        })
    
    async def test_export_to_docx(self):
        """Test export_to_docx"""
        print(f"\n{YELLOW}=== Test: export_to_docx ==={NC}")
        
        markdown_content = """# Test Document

This is a test document for DOCX export.
"""
        
        output_path = "output/test_export.docx"
        success, result = await self.call_tool("export_to_docx", {
            "markdown_content": markdown_content,
            "output_path": output_path,
            "title": "Test Document",
            "author": "Test Author"
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status}: {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony: {file_path.stat().st_size} bytes{NC}")
                
        self.results.append({
            "tool": "export_to_docx",
            "success": success,
            "result": result
        })
    
    async def _test_single_template(self, template_type: str) -> Dict[str, Any]:
        """Test pojedynczego template"""
        output_path = f"output/test_template_{template_type}.md"
        variables = {
            "title": f"Test {template_type}",
            "author": "Test Author",
            "date": "2024-01-01"
        }
        
        success, result = await self.call_tool("create_document_from_template", {
            "template_type": template_type,
            "variables": variables,
            "output_path": output_path
        })
        
        status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
        print(f"  {status} {template_type}: {result[:80]}")
        
        if success:
            file_path = Path(output_path)
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    {GREEN}✓ Plik utworzony: {file_path.stat().st_size} bytes{NC}")
        
        return {
            "tool": "create_document_from_template",
            "template": template_type,
            "success": success,
            "result": result
        }
    
    async def test_create_document_from_template(self):
        """Test create_document_from_template - wszystkie szablony (równolegle)"""
        print(f"\n{YELLOW}=== Test: create_document_from_template ==={NC}")
        
        templates = ["adr", "api_spec", "c4_context", "microservices_overview"]
        tasks = [self._test_single_template(t) for t in templates]
        results = await asyncio.gather(*tasks)
        self.results.extend(results)
    
    async def run_all_tests(self):
        """Uruchom wszystkie testy"""
        # Zapisz event loop dla użycia w wątkach
        self.loop = asyncio.get_event_loop()
        
        print(f"{YELLOW}{'='*60}{NC}")
        print(f"{YELLOW}Test MCP Server - Wszystkie narzędzia (zoptymalizowany){NC}")
        print(f"{YELLOW}{'='*60}{NC}\n")
        
        # Wyświetl konfigurację
        print(f"{YELLOW}Konfiguracja:{NC}")
        print(f"  TEST_FORMATS: {','.join(TEST_FORMATS)}")
        print(f"  TEST_LAYOUTS: {','.join(TEST_LAYOUTS)}")
        print(f"  TEST_C4_TYPES: {','.join(TEST_C4_TYPES)}")
        print(f"  TEST_UML_TYPES: {','.join(TEST_UML_TYPES)}")
        print(f"  TEST_PARALLEL: {TEST_PARALLEL}")
        print()
        
        try:
            await self.start_server()
            
            if not await self.initialize():
                print(f"{RED}Nie można zainicjalizować MCP server{NC}")
                return
                
            tools = await self.list_tools()
            print(f"\n{GREEN}Dostępne narzędzia:{NC}")
            for tool in tools:
                print(f"  - {tool['name']}")
            
            # Uruchom wszystkie testy równolegle gdzie to możliwe
            start_time = time.perf_counter()
            
            await asyncio.gather(
                self.test_c4_diagram(),
                self.test_uml_diagram(),
                self.test_sequence_diagram(),
                self.test_flowchart(),
                self.test_mermaid_sequence(),
                self.test_gantt(),
                self.test_dependency_graph(),
                self.test_cloud_diagram(),
                self.test_export_to_pdf(),
                self.test_export_to_docx(),
                self.test_create_document_from_template(),
            )
            
            elapsed_time = time.perf_counter() - start_time
            print(f"\n{YELLOW}Czas wykonania: {elapsed_time:.2f} sekund{NC}\n")
            
            # Raport
            self.print_report()
            
        finally:
            # Zatrzymaj reader thread
            if self.reader_thread:
                self.shutdown_event.set()
                if self.reader_thread.is_alive():
                    self.reader_thread.join(timeout=2.0)
            
            if self.process:
                self.process.terminate()
                self.process.wait(timeout=5.0)
                if self.process.poll() is None:
                    self.process.kill()
                    self.process.wait()
                
    def print_report(self):
        """Wyświetl raport z testów"""
        print(f"\n{YELLOW}{'='*60}{NC}")
        print(f"{YELLOW}RAPORT Z TESTÓW{NC}")
        print(f"{YELLOW}{'='*60}{NC}\n")
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        failed = total - successful
        
        print(f"Łącznie testów: {total}")
        print(f"{GREEN}Udanych: {successful}{NC}")
        print(f"{RED}Nieudanych: {failed}{NC}\n")
        
        # Grupuj po narzędziach
        tools_summary = {}
        for result in self.results:
            tool = result["tool"]
            if tool not in tools_summary:
                tools_summary[tool] = {"total": 0, "success": 0}
            tools_summary[tool]["total"] += 1
            if result["success"]:
                tools_summary[tool]["success"] += 1
                
        print(f"{'Narzędzie':<35} {'Status':<15} {'Szczegóły'}")
        print("-" * 80)
        
        for tool, stats in tools_summary.items():
            status_icon = f"{GREEN}✓{NC}" if stats["success"] == stats["total"] else f"{RED}✗{NC}"
            status_text = f"{stats['success']}/{stats['total']}"
            print(f"{tool:<35} {status_icon} {status_text:<13} ", end="")
            
            # Pokaż szczegóły dla nieudanych
            failed_tests = [r for r in self.results if r["tool"] == tool and not r["success"]]
            if failed_tests:
                print(f"Błędy: {len(failed_tests)}")
            else:
                print("OK")
                
        print()


async def main():
    tester = MCPTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
