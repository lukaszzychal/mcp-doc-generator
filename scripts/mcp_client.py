#!/usr/bin/env python3
"""
Interaktywny klient MCP do generowania diagramów z własnych promptów.
Może czytać prompt z konsoli lub z pliku.
"""

import json
import subprocess
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

class MCPClient:
    def __init__(self):
        self.process = None
        self.request_id = 0
        
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
        # Inicjalizuj połączenie
        self.initialize()
        
    def initialize(self):
        """Inicjalizuj połączenie MCP"""
        response = self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "mcp-client",
                "version": "1.0.0"
            }
        })
        return response is not None
        
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
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
        
        # Odczytaj odpowiedź
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
                    continue
                    
        if response_line.strip():
            try:
                return json.loads(response_line.strip())
            except json.JSONDecodeError:
                return None
        return None
        
    def list_tools(self):
        """Pobierz listę dostępnych narzędzi"""
        response = self.send_request("tools/list")
        if response and "result" in response and "tools" in response["result"]:
            return response["result"]["tools"]
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
                        # Sprawdź czy odpowiedź zawiera błąd
                        text = content["text"]
                        if "Error" in text or "error" in text.lower():
                            return False, text
                        return True, text
            elif "error" in response:
                error_msg = response["error"].get("message", "Unknown error")
                # Jeśli error ma też data, może zawierać więcej informacji
                if "data" in response["error"]:
                    error_msg += f" - {response['error']['data']}"
                return False, error_msg
                
            return False, f"Unexpected response: {str(response)[:200]}"
        except UnicodeDecodeError as e:
            return False, f"Encoding error - response may be binary: {str(e)}"
        except Exception as e:
            return False, f"Exception: {str(e)}"
            
    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Parsuje prompt użytkownika i zwraca parametry dla narzędzia MCP.
        Próbuje automatycznie rozpoznać typ diagramu z promptu.
        """
        prompt_lower = prompt.lower()
        
        # Sprawdź typ diagramu - sprawdź w kolejności od najbardziej specyficznego
        if "c4" in prompt_lower or "context" in prompt_lower or "container" in prompt_lower:
            # Sprawdź w kolejności: code, component, container, context
            if "code" in prompt_lower and "c4" in prompt_lower:
                diagram_type = "code"
            elif "component" in prompt_lower and "c4" in prompt_lower:
                diagram_type = "component"
            elif "container" in prompt_lower and "c4" in prompt_lower:
                diagram_type = "container"
            elif "context" in prompt_lower:
                diagram_type = "context"
            else:
                # Domyślnie context dla C4
                diagram_type = "context"
                
            # Wygeneruj PlantUML kod z promptu (przekaż diagram_type)
            content = self.generate_c4_from_prompt(prompt, diagram_type)
            return {
                "tool": "generate_c4_diagram",
                "arguments": {
                    "diagram_type": diagram_type,
                    "content": content,
                    "output_path": self.extract_output_path(prompt) or "output/diagram.png",
                    "format": "png" if ".png" in prompt.lower() else "svg"
                }
            }
        elif "uml" in prompt_lower or "class diagram" in prompt_lower:
            diagram_type = "class"
            if "component" in prompt_lower:
                diagram_type = "component"
            elif "deployment" in prompt_lower:
                diagram_type = "deployment"
            elif "package" in prompt_lower:
                diagram_type = "package"
            elif "activity" in prompt_lower:
                diagram_type = "activity"
            elif "usecase" in prompt_lower or "use case" in prompt_lower:
                diagram_type = "usecase"
                
            content = self.generate_uml_from_prompt(prompt)
            return {
                "tool": "generate_uml_diagram",
                "arguments": {
                    "diagram_type": diagram_type,
                    "content": content,
                    "output_path": self.extract_output_path(prompt) or "output/uml.png",
                    "format": "png" if ".png" in prompt.lower() else "svg"
                }
            }
        elif "sequence" in prompt_lower or "sequencja" in prompt_lower:
            content = self.generate_sequence_from_prompt(prompt)
            return {
                "tool": "generate_sequence_diagram",
                "arguments": {
                    "content": content,
                    "output_path": self.extract_output_path(prompt) or "output/sequence.png",
                    "format": "png" if ".png" in prompt.lower() else "svg"
                }
            }
        elif "flowchart" in prompt_lower or "flow chart" in prompt_lower or "schemat" in prompt_lower:
            content = self.generate_flowchart_from_prompt(prompt)
            return {
                "tool": "generate_flowchart",
                "arguments": {
                    "content": content,
                    "output_path": self.extract_output_path(prompt) or "output/flowchart.png",
                    "format": "png" if ".png" in prompt.lower() else "svg"
                }
            }
        else:
            # Domyślnie C4 context
            content = self.generate_c4_from_prompt(prompt, "context")
            return {
                "tool": "generate_c4_diagram",
                "arguments": {
                    "diagram_type": "context",
                    "content": content,
                    "output_path": self.extract_output_path(prompt) or "output/diagram.png",
                    "format": "png"
                }
            }
            
    def extract_output_path(self, prompt: str) -> Optional[str]:
        """Wyciągnij ścieżkę wyjściową z promptu"""
        lines = prompt.split('\n')
        for line in lines:
            if "save" in line.lower() or "zapisz" in line.lower() or "output" in line.lower():
                # Szukaj ścieżki w linii
                if "/" in line or "output/" in line.lower():
                    # Wyciągnij ścieżkę
                    parts = line.split()
                    for part in parts:
                        if "/" in part or part.endswith(".png") or part.endswith(".svg"):
                            return part.strip('"\'')
        return None
        
    def generate_c4_from_prompt(self, prompt: str, diagram_type: str = "context") -> str:
        """Generuje kod PlantUML C4 z promptu"""
        lines = prompt.split('\n')
        
        # Użyj set do unikania duplikatów
        components_set = set()
        components_list = []
        relationships = []
        
        # Flagi do śledzenia sekcji
        in_external = False
        in_system_boundary = False
        
        # Najpierw spróbuj parsować z listy (linie z "-")
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            line_lower = line.lower()
            
            # Wykryj sekcje
            if "external systems" in line_lower or "external system" in line_lower:
                in_external = True
                in_system_boundary = False
                continue
            elif "system boundary" in line_lower or "platform" in line_lower or "e-commerce platform" in line_lower:
                in_external = False
                in_system_boundary = True
                continue
            elif "save" in line_lower or "zapisz" in line_lower:
                break  # Koniec promptu
                
            # Parsuj komponenty z listy (linie z "-")
            if line.startswith("-"):
                name = line.replace("-", "").strip()
                if not name:
                    continue
                    
                # External Systems
                if in_external or "external" in line_lower:
                    if "user" in name.lower() or "customer" in name.lower():
                        comp = 'Person(customer, "Customer", "Users browsing and purchasing")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "payment" in name.lower() or "stripe" in name.lower() or "paypal" in name.lower():
                        comp = f'System_Ext(payment, "{name}", "Payment Gateway")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "shipping" in name.lower() or "fedex" in name.lower() or "ups" in name.lower():
                        comp = f'System_Ext(shipping, "{name}", "Shipping Service")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    else:
                        clean_id = name.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
                        comp = f'System_Ext({clean_id}, "{name}", "External System")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                            
                # System Boundary (containers)
                elif in_system_boundary:
                    if "web" in name.lower() or "react" in name.lower() or ("application" in name.lower() and "frontend" in name.lower()):
                        comp = f'Container(webapp, "{name}", "React", "Web Application")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "mobile" in name.lower() or "ios" in name.lower() or "android" in name.lower():
                        comp = f'Container(mobile, "{name}", "iOS/Android", "Mobile App")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "api" in name.lower() and "gateway" in name.lower():
                        comp = f'Container(api, "{name}", "Node.js", "API Gateway")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "order" in name.lower() and "service" in name.lower():
                        comp = f'Container(orders, "{name}", "Microservice", "Order Service")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "inventory" in name.lower() and "service" in name.lower():
                        comp = f'Container(inventory, "{name}", "Microservice", "Inventory Service")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
                    elif "database" in name.lower() or "postgres" in name.lower():
                        comp = f'ContainerDb(db, "{name}", "PostgreSQL", "Database")'
                        if comp not in components_set:
                            components_set.add(comp)
                            components_list.append(comp)
        
        # Jeśli nie znaleziono komponentów z listy, parsuj z całego promptu
        if len(components_list) <= 1:  # Tylko customer
            prompt_lower = prompt.lower()
            
            # Sprawdź typ diagramu (przekazany jako parametr)
            
            # Szukaj komponentów w tekście
            if "user" in prompt_lower or "customer" in prompt_lower:
                customer_comp = 'Person(customer, "Customer", "Users browsing and purchasing")'
                if customer_comp not in components_set:
                    components_list.insert(0, customer_comp)
                    components_set.add(customer_comp)
                    
            if "payment" in prompt_lower and ("gateway" in prompt_lower or "stripe" in prompt_lower or "paypal" in prompt_lower):
                comp = 'System_Ext(payment, "Payment Gateway", "Payment Gateway")'
                if comp not in components_set:
                    components_set.add(comp)
                    components_list.append(comp)
                    
            if "shipping" in prompt_lower or "fedex" in prompt_lower or "ups" in prompt_lower:
                comp = 'System_Ext(shipping, "Shipping Service", "Shipping Service")'
                if comp not in components_set:
                    components_set.add(comp)
                    components_list.append(comp)
                    
            # Dla context diagramu używamy System, dla container - Container
            if diagram_type == "context":
                if "web" in prompt_lower and ("app" in prompt_lower or "application" in prompt_lower):
                    comp = 'System(webapp, "Web Application", "Web Application")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "mobile" in prompt_lower or "ios" in prompt_lower or "android" in prompt_lower:
                    comp = 'System(mobile, "Mobile App", "Mobile App")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "api" in prompt_lower and "gateway" in prompt_lower:
                    comp = 'System(api, "API Gateway", "API Gateway")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "order" in prompt_lower and "service" in prompt_lower:
                    comp = 'System(orders, "Order Service", "Order Service")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "inventory" in prompt_lower and "service" in prompt_lower:
                    comp = 'System(inventory, "Inventory Service", "Inventory Service")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "database" in prompt_lower or "postgres" in prompt_lower:
                    comp = 'SystemDb(db, "Database", "Database")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
            else:
                # Container diagram
                if "web" in prompt_lower and ("app" in prompt_lower or "application" in prompt_lower):
                    comp = 'Container(webapp, "Web Application", "React", "Web Application")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "mobile" in prompt_lower or "ios" in prompt_lower or "android" in prompt_lower:
                    comp = 'Container(mobile, "Mobile App", "iOS/Android", "Mobile App")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "api" in prompt_lower and "gateway" in prompt_lower:
                    comp = 'Container(api, "API Gateway", "Node.js", "API Gateway")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "order" in prompt_lower and "service" in prompt_lower:
                    comp = 'Container(orders, "Order Service", "Microservice", "Order Service")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "inventory" in prompt_lower and "service" in prompt_lower:
                    comp = 'Container(inventory, "Inventory Service", "Microservice", "Inventory Service")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                        
                if "database" in prompt_lower or "postgres" in prompt_lower:
                    comp = 'ContainerDb(db, "Database", "PostgreSQL", "Database")'
                    if comp not in components_set:
                        components_set.add(comp)
                        components_list.append(comp)
                            
        # Dodaj Customer jeśli nie ma
        customer_comp = 'Person(customer, "Customer", "Users browsing and purchasing")'
        if customer_comp not in components_set:
            components_list.insert(0, customer_comp)
            components_set.add(customer_comp)
                
        # Generuj relacje na podstawie komponentów
        has_customer = any("customer" in c.lower() for c in components_list)
        has_webapp = any("webapp" in c.lower() for c in components_list)
        has_mobile = any("mobile" in c.lower() for c in components_list)
        has_api = any(" api" in c.lower() or "api," in c.lower() for c in components_list)
        has_orders = any("orders" in c.lower() for c in components_list)
        has_inventory = any("inventory" in c.lower() for c in components_list)
        has_db = any("db" in c.lower() for c in components_list)
        has_payment = any("payment" in c.lower() for c in components_list)
        has_shipping = any("shipping" in c.lower() for c in components_list)
        
        if has_customer and has_webapp:
            relationships.append('Rel(customer, webapp, "Browses products, places orders", "HTTPS")')
        if has_customer and has_mobile:
            relationships.append('Rel(customer, mobile, "Browses products, places orders", "HTTPS")')
        if has_webapp and has_api:
            relationships.append('Rel(webapp, api, "Makes API calls", "HTTPS/REST")')
        if has_mobile and has_api:
            relationships.append('Rel(mobile, api, "Makes API calls", "HTTPS/REST")')
        if has_api and has_orders:
            relationships.append('Rel(api, orders, "Routes order requests", "REST/JSON")')
        if has_api and has_inventory:
            relationships.append('Rel(api, inventory, "Routes inventory requests", "REST/JSON")')
        if has_orders and has_db:
            relationships.append('Rel(orders, db, "Reads/writes order data", "SQL/TCP")')
        if has_inventory and has_db:
            relationships.append('Rel(inventory, db, "Reads/writes inventory data", "SQL/TCP")')
        if has_orders and has_payment:
            relationships.append('Rel(orders, payment, "Processes payments", "HTTPS/API")')
        if has_orders and has_shipping:
            relationships.append('Rel(orders, shipping, "Creates shipping labels", "HTTPS/API")')
        if has_orders and has_inventory:
            relationships.append('Rel(orders, inventory, "Checks stock, reserves items", "REST/JSON")')
            
        # Buduj kod PlantUML - użyj odpowiedniego include w zależności od typu
        if diagram_type == "context":
            include_file = "C4_Context.puml"
        elif diagram_type == "container":
            include_file = "C4_Container.puml"
        elif diagram_type == "component":
            include_file = "C4_Component.puml"
        elif diagram_type == "code":
            include_file = "C4_Component.puml"  # Code używa Component
        else:
            include_file = "C4_Context.puml"  # Domyślnie context
            
        code = f"""@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/{include_file}

LAYOUT_WITH_LEGEND()

title E-commerce System

"""
        code += "\n".join(components_list)
        if relationships:
            code += "\n\n"
            code += "\n".join(relationships)
        code += "\n\n@enduml"
        
        return code
        
    def generate_uml_from_prompt(self, prompt: str) -> str:
        """Generuje kod PlantUML UML z promptu"""
        # Prosty parser dla UML class diagram
        code = "@startuml\n"
        # TODO: Rozszerzyć parser
        code += "class User {\n  +id: int\n  +name: string\n}\n"
        code += "@enduml"
        return code
        
    def generate_sequence_from_prompt(self, prompt: str) -> str:
        """Generuje kod PlantUML sequence z promptu"""
        code = "@startuml\n"
        # TODO: Rozszerzyć parser
        code += "Alice -> Bob: Hello\n"
        code += "@enduml"
        return code
        
    def generate_flowchart_from_prompt(self, prompt: str) -> str:
        """Generuje kod Mermaid flowchart z promptu"""
        code = "flowchart TD\n"
        # TODO: Rozszerzyć parser
        code += "    Start --> End\n"
        return code
        
    def process_prompt(self, prompt: str):
        """Przetwórz prompt i wygeneruj diagram"""
        print("Parsowanie promptu...")
        tool_config = self.parse_prompt(prompt)
        
        print(f"Używam narzędzia: {tool_config['tool']}")
        print(f"Parametry:")
        print(f"  - diagram_type: {tool_config['arguments'].get('diagram_type', 'N/A')}")
        print(f"  - output_path: {tool_config['arguments'].get('output_path', 'N/A')}")
        print(f"  - format: {tool_config['arguments'].get('format', 'N/A')}")
        
        success, result = self.call_tool(tool_config['tool'], tool_config['arguments'])
        
        if success:
            print(f"\n✓ Sukces!")
            # Wyświetl tylko pierwsze 200 znaków wyniku
            if len(result) > 200:
                print(result[:200] + "...")
            else:
                print(result)
            
            # Sprawdź czy plik został utworzony
            output_path = tool_config['arguments'].get('output_path', '')
            if output_path:
                file_path = Path(output_path)
                if file_path.exists():
                    size = file_path.stat().st_size
                    print(f"\n✓ Plik utworzony: {output_path} ({size} bytes)")
                else:
                    print(f"\n⚠ Plik nie został utworzony: {output_path}")
        else:
            print(f"\n✗ Błąd: {result}")
            
    def cleanup(self):
        """Zamknij połączenie"""
        if self.process:
            self.process.terminate()
            self.process.wait()


def main():
    parser = argparse.ArgumentParser(description='MCP Client - Generuj diagramy z promptów')
    parser.add_argument('-f', '--file', help='Wczytaj prompt z pliku')
    parser.add_argument('-p', '--prompt', help='Prompt z linii komend')
    parser.add_argument('-i', '--interactive', action='store_true', help='Tryb interaktywny')
    
    args = parser.parse_args()
    
    # Sprawdź czy kontenery działają
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    if "mcp-documentation-server" not in result.stdout:
        print("❌ Kontener mcp-documentation-server nie działa!")
        print("Uruchom: docker compose up -d")
        sys.exit(1)
        
    client = MCPClient()
    
    try:
        client.start_server()
        
        if args.file:
            # Wczytaj z pliku
            with open(args.file, 'r') as f:
                prompt = f.read()
            client.process_prompt(prompt)
        elif args.prompt:
            # Z linii komend
            client.process_prompt(args.prompt)
        elif args.interactive:
            # Tryb interaktywny
            print("Tryb interaktywny - wpisz prompt (Ctrl+D aby zakończyć):")
            prompt = sys.stdin.read()
            client.process_prompt(prompt)
        else:
            # Domyślnie czytaj z stdin
            prompt = sys.stdin.read()
            if prompt.strip():
                client.process_prompt(prompt)
            else:
                parser.print_help()
                
    finally:
        client.cleanup()


if __name__ == "__main__":
    main()

