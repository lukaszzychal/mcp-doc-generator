#!/usr/bin/env python3
"""
Test MCP server lokalnie przez Docker (docker exec).
Testuje wszystkie 11 narzędzi z wszystkimi dostępnymi opcjami.
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Kolory dla outputu
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
NC = '\033[0m'  # No Color

class MCPTester:
    def __init__(self):
        self.process = None
        self.request_id = 0
        self.results = []
        
    def start_server(self):
        """Uruchom MCP server przez docker exec"""
        cmd = [
            "docker", "exec", "-i", "mcp-documentation-server",
            "python", "src/server.py"
        ]
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        time.sleep(1)  # Czekaj na inicjalizację
        
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Wyślij żądanie JSON-RPC do MCP server"""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params:
            request["params"] = params
            
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Odczytaj odpowiedź - może być kilka linii
        response_line = ""
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            response_line += line
            if line.strip():
                try:
                    return json.loads(response_line.strip())
                except json.JSONDecodeError:
                    # Może być więcej linii do odczytania
                    continue
                    
        if response_line.strip():
            try:
                return json.loads(response_line.strip())
            except json.JSONDecodeError:
                return {"error": {"message": f"Invalid JSON response: {response_line[:100]}"}}
        return None
        
    def initialize(self) -> bool:
        """Inicjalizuj połączenie MCP"""
        print(f"{YELLOW}Inicjalizacja MCP...{NC}")
        response = self.send_request("initialize", {
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
            
    def list_tools(self) -> List[Dict[str, Any]]:
        """Pobierz listę dostępnych narzędzi"""
        print(f"{YELLOW}Pobieranie listy narzędzi...{NC}")
        response = self.send_request("tools/list")
        
        if response and "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"{GREEN}✓ Znaleziono {len(tools)} narzędzi{NC}")
            return tools
        else:
            print(f"{RED}✗ Błąd pobierania narzędzi: {response}{NC}")
            return []
            
    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Tuple[bool, str]:
        """Wywołaj narzędzie MCP"""
        try:
            response = self.send_request("tools/call", {
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
        
    def test_c4_diagram(self):
        """Test generate_c4_diagram - wszystkie typy i formaty"""
        print(f"\n{YELLOW}=== Test: generate_c4_diagram ==={NC}")
        
        types = ["context", "container", "component", "code"]
        formats = ["png", "svg"]
        
        for diagram_type in types:
            for fmt in formats:
                output_path = f"output/test_c4_{diagram_type}.{fmt}"
                content = f"""@startuml
Person(user, "User")
System(system, "System")
Rel(user, system, "Uses")
@enduml"""
                
                success, result = self.call_tool("generate_c4_diagram", {
                    "diagram_type": diagram_type,
                    "content": content,
                    "output_path": output_path,
                    "format": fmt
                })
                
                status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
                print(f"  {status} {diagram_type} ({fmt}): {result[:80]}")
                
                # Sprawdź czy plik istnieje
                if success:
                    file_path = Path(output_path)
                    if file_path.exists() and file_path.stat().st_size > 0:
                        print(f"    {GREEN}✓ Plik utworzony: {file_path.stat().st_size} bytes{NC}")
                    else:
                        print(f"    {RED}✗ Plik nie istnieje lub jest pusty{NC}")
                        
                self.results.append({
                    "tool": "generate_c4_diagram",
                    "type": diagram_type,
                    "format": fmt,
                    "success": success,
                    "result": result
                })
                
    def test_uml_diagram(self):
        """Test generate_uml_diagram - wszystkie typy i formaty"""
        print(f"\n{YELLOW}=== Test: generate_uml_diagram ==={NC}")
        
        types = ["class", "component", "deployment", "package", "activity", "usecase"]
        formats = ["png", "svg"]
        
        for diagram_type in types:
            for fmt in formats:
                output_path = f"output/test_uml_{diagram_type}.{fmt}"
                content = f"""class User {{
  +name: string
}}
class Order {{
  +id: int
}}
User --> Order"""
                
                success, result = self.call_tool("generate_uml_diagram", {
                    "diagram_type": diagram_type,
                    "content": content,
                    "output_path": output_path,
                    "format": fmt
                })
                
                status = f"{GREEN}✓{NC}" if success else f"{RED}✗{NC}"
                print(f"  {status} {diagram_type} ({fmt}): {result[:80]}")
                
                if success:
                    file_path = Path(output_path)
                    if file_path.exists() and file_path.stat().st_size > 0:
                        print(f"    {GREEN}✓ Plik utworzony: {file_path.stat().st_size} bytes{NC}")
                    else:
                        print(f"    {RED}✗ Plik nie istnieje{NC}")
                        
                self.results.append({
                    "tool": "generate_uml_diagram",
                    "type": diagram_type,
                    "format": fmt,
                    "success": success,
                    "result": result
                })
                
    def test_sequence_diagram(self):
        """Test generate_sequence_diagram"""
        print(f"\n{YELLOW}=== Test: generate_sequence_diagram ==={NC}")
        
        formats = ["png", "svg"]
        content = """Alice -> Bob: Hello
Bob --> Alice: Hi"""
        
        for fmt in formats:
            output_path = f"output/test_sequence.{fmt}"
            success, result = self.call_tool("generate_sequence_diagram", {
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
                    
            self.results.append({
                "tool": "generate_sequence_diagram",
                "format": fmt,
                "success": success,
                "result": result
            })
            
    def test_flowchart(self):
        """Test generate_flowchart"""
        print(f"\n{YELLOW}=== Test: generate_flowchart ==={NC}")
        
        formats = ["png", "svg"]
        content = """flowchart TD
    Start --> Check{Valid?}
    Check -->|Yes| Process
    Check -->|No| Error
    Process --> End"""
        
        for fmt in formats:
            output_path = f"output/test_flowchart.{fmt}"
            success, result = self.call_tool("generate_flowchart", {
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
                    
            self.results.append({
                "tool": "generate_flowchart",
                "format": fmt,
                "success": success,
                "result": result
            })
            
    def test_mermaid_sequence(self):
        """Test generate_mermaid_sequence"""
        print(f"\n{YELLOW}=== Test: generate_mermaid_sequence ==={NC}")
        
        formats = ["png", "svg"]
        content = """sequenceDiagram
    User->>API: Request
    API->>DB: Query
    DB-->>API: Data
    API-->>User: Response"""
        
        for fmt in formats:
            output_path = f"output/test_mermaid_sequence.{fmt}"
            success, result = self.call_tool("generate_mermaid_sequence", {
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
                    
            self.results.append({
                "tool": "generate_mermaid_sequence",
                "format": fmt,
                "success": success,
                "result": result
            })
            
    def test_gantt(self):
        """Test generate_gantt"""
        print(f"\n{YELLOW}=== Test: generate_gantt ==={NC}")
        
        formats = ["png", "svg"]
        content = """gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    section Phase 1
    Task 1 :a1, 2024-01-01, 30d
    Task 2 :a2, after a1, 20d
    section Phase 2
    Task 3 :a3, 2024-02-01, 15d"""
        
        for fmt in formats:
            output_path = f"output/test_gantt.{fmt}"
            success, result = self.call_tool("generate_gantt", {
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
                    
            self.results.append({
                "tool": "generate_gantt",
                "format": fmt,
                "success": success,
                "result": result
            })
            
    def test_dependency_graph(self):
        """Test generate_dependency_graph - wszystkie layouty i formaty"""
        print(f"\n{YELLOW}=== Test: generate_dependency_graph ==={NC}")
        
        layouts = ["dot", "neato", "fdp", "circo", "twopi"]
        formats = ["png", "svg", "pdf"]
        
        content = """digraph G {
    A -> B
    B -> C
    C -> A
}"""
        
        for layout in layouts:
            for fmt in formats:
                output_path = f"output/test_dependency_{layout}.{fmt}"
                success, result = self.call_tool("generate_dependency_graph", {
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
                        
                self.results.append({
                    "tool": "generate_dependency_graph",
                    "layout": layout,
                    "format": fmt,
                    "success": success,
                    "result": result
                })
                
    def test_cloud_diagram(self):
        """Test generate_cloud_diagram"""
        print(f"\n{YELLOW}=== Test: generate_cloud_diagram ==={NC}")
        
        formats = ["png", "svg", "pdf"]
        # Minimalny draw.io XML
        content = """<mxfile><diagram name="Page-1"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/><mxCell id="2" value="Cloud" style="shape=cloud" vertex="1" parent="1"><mxGeometry x="100" y="100" width="100" height="60" as="geometry"/></mxCell></root></mxGraphModel></diagram></mxfile>"""
        
        for fmt in formats:
            output_path = f"output/test_cloud.{fmt}"
            success, result = self.call_tool("generate_cloud_diagram", {
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
                    
            self.results.append({
                "tool": "generate_cloud_diagram",
                "format": fmt,
                "success": success,
                "result": result
            })
            
    def test_export_to_pdf(self):
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
        success, result = self.call_tool("export_to_pdf", {
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
        
    def test_export_to_docx(self):
        """Test export_to_docx"""
        print(f"\n{YELLOW}=== Test: export_to_docx ==={NC}")
        
        markdown_content = """# Test Document

This is a test document for DOCX export.
"""
        
        output_path = "output/test_export.docx"
        success, result = self.call_tool("export_to_docx", {
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
        
    def test_create_document_from_template(self):
        """Test create_document_from_template - wszystkie szablony"""
        print(f"\n{YELLOW}=== Test: create_document_from_template ==={NC}")
        
        templates = ["adr", "api_spec", "c4_context", "microservices_overview"]
        
        for template_type in templates:
            output_path = f"output/test_template_{template_type}.md"
            variables = {
                "title": f"Test {template_type}",
                "author": "Test Author",
                "date": "2024-01-01"
            }
            
            success, result = self.call_tool("create_document_from_template", {
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
                    
            self.results.append({
                "tool": "create_document_from_template",
                "template": template_type,
                "success": success,
                "result": result
            })
            
    def run_all_tests(self):
        """Uruchom wszystkie testy"""
        print(f"{YELLOW}{'='*60}{NC}")
        print(f"{YELLOW}Test MCP Server - Wszystkie narzędzia{NC}")
        print(f"{YELLOW}{'='*60}{NC}\n")
        
        try:
            self.start_server()
            
            if not self.initialize():
                print(f"{RED}Nie można zainicjalizować MCP server{NC}")
                return
                
            tools = self.list_tools()
            print(f"\n{GREEN}Dostępne narzędzia:{NC}")
            for tool in tools:
                print(f"  - {tool['name']}")
                
            # Uruchom wszystkie testy
            self.test_c4_diagram()
            self.test_uml_diagram()
            self.test_sequence_diagram()
            self.test_flowchart()
            self.test_mermaid_sequence()
            self.test_gantt()
            self.test_dependency_graph()
            self.test_cloud_diagram()
            self.test_export_to_pdf()
            self.test_export_to_docx()
            self.test_create_document_from_template()
            
            # Raport
            self.print_report()
            
        finally:
            if self.process:
                self.process.terminate()
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


if __name__ == "__main__":
    tester = MCPTester()
    tester.run_all_tests()

