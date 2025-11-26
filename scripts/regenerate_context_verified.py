#!/usr/bin/env python3
"""
Regeneruje C4 Context Diagram z pełnym kodem PlantUML i weryfikacją.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_client import MCPClient
import time

def regenerate_context_verified():
    """Regeneruje C4 Context Diagram z pełnym kodem PlantUML"""
    client = MCPClient()
    
    try:
        client.start_server()
        print("Regenerowanie C4 Context Diagram z pełnym kodem PlantUML...\n")
        
        # PEŁNY kod PlantUML dla Context diagramu - TYLKO System(), NIE Container()
        plantuml_content = """title E-commerce System - Context Diagram

Person(customer, "Customer", "Users browsing and purchasing")

System(ecommerce, "E-commerce Platform", "Online shopping platform with product catalog, shopping cart, and order processing")

System_Ext(payment, "Payment Gateway", "External payment system (Stripe/PayPal)")
System_Ext(shipping, "Shipping Service", "External shipping provider (FedEx/UPS)")

Rel(customer, ecommerce, "Browses products, places orders", "HTTPS")
Rel(ecommerce, payment, "Processes payments", "HTTPS/REST API")
Rel(ecommerce, shipping, "Creates shipping labels", "HTTPS/REST API")"""
        
        print("Kod PlantUML do wygenerowania:")
        print("=" * 60)
        print(plantuml_content)
        print("=" * 60)
        print("\nWeryfikacja: Kod zawiera TYLKO System(), NIE Container()")
        print("Oczekiwany wynik: Jeden blok 'E-commerce Platform' + Customer + zewnętrzne systemy\n")
        
        # Wywołaj narzędzie bezpośrednio
        result = client.call_tool("generate_c4_diagram", {
            "diagram_type": "context",
            "content": plantuml_content,
            "output_path": "examples/generated/example_c4_context.png",
            "format": "png"
        })
        
        if result:
            success, message = result
            if success:
                print(f"✓ {message}")
                print("\n✓ Diagram wygenerowany. Sprawdź plik: examples/generated/example_c4_context.png")
                print("  Powinien zawierać TYLKO:")
                print("  - Customer (Person)")
                print("  - E-commerce Platform (System - JEDEN blok)")
                print("  - Payment Gateway (System_Ext)")
                print("  - Shipping Service (System_Ext)")
                print("\n  NIE powinien zawierać:")
                print("  - Web Application")
                print("  - Mobile App")
                print("  - API Gateway")
                print("  - Order Service")
                print("  - Inventory Service")
                print("  - Database")
            else:
                print(f"✗ Błąd: {message}")
                return False
        else:
            print("✗ Błąd: Brak odpowiedzi z serwera")
            return False
        
        time.sleep(1)
        return True
        
    except Exception as e:
        print(f"Błąd: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    regenerate_context_verified()

