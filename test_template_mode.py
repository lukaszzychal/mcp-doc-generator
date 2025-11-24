#!/usr/bin/env python3
"""
Test Template Mode - Pre-built diagram templates
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.templates import (
    list_available_templates,
    get_template_variables,
    get_template_info,
    generate_from_template
)


async def test_list_templates():
    """Test listing available templates"""
    print("\n" + "="*70)
    print("📋 TEST 1: List Available Templates")
    print("="*70)
    
    templates = list_available_templates()
    
    print(f"\n✅ Found {sum(len(v) for v in templates.values())} templates:")
    
    if templates["c4"]:
        print(f"\n🏗️  C4 Architecture ({len(templates['c4'])}):")
        for tmpl in templates["c4"]:
            print(f"   - {tmpl}")
    
    if templates["uml"]:
        print(f"\n📐 UML Diagrams ({len(templates['uml'])}):")
        for tmpl in templates["uml"]:
            print(f"   - {tmpl}")
    
    if templates["mermaid"]:
        print(f"\n📊 Mermaid Diagrams ({len(templates['mermaid'])}):")
        for tmpl in templates["mermaid"]:
            print(f"   - {tmpl}")
    
    if templates["graphviz"]:
        print(f"\n🔗 Graphviz Graphs ({len(templates['graphviz'])}):")
        for tmpl in templates["graphviz"]:
            print(f"   - {tmpl}")


async def test_get_template_variables():
    """Test extracting variables from template"""
    print("\n" + "="*70)
    print("📋 TEST 2: Get Template Variables")
    print("="*70)
    
    template_name = "c4_ecommerce_basic"
    variables = get_template_variables(template_name)
    
    print(f"\n✅ Template '{template_name}' has {len(variables)} variables:")
    for var in variables:
        print(f"   - {var}")


async def test_get_template_info():
    """Test getting template info"""
    print("\n" + "="*70)
    print("📋 TEST 3: Get Template Info")
    print("="*70)
    
    result = await get_template_info("c4_microservices_basic")
    print(f"\n{result}")


async def test_generate_ecommerce():
    """Test generating e-commerce C4 diagram from template"""
    print("\n" + "="*70)
    print("🏗️  TEST 4: Generate E-commerce C4 Diagram")
    print("="*70)
    
    result = await generate_from_template(
        template_name="c4_ecommerce_basic",
        variables={
            "system_name": "ShopNow E-commerce",
            "customer_label": "Online Shopper",
            "system_description": "Modern e-commerce platform",
            "payment_provider": "Stripe Payment Gateway",
            "email_provider": "SendGrid Email Service",
            "delivery_provider": "DHL Delivery Network"
        },
        output_path="output/template_ecommerce.png",
        format="png"
    )
    
    print(f"\n{result}")


async def test_generate_microservices():
    """Test generating microservices architecture"""
    print("\n" + "="*70)
    print("🏗️  TEST 5: Generate Microservices C4 Diagram")
    print("="*70)
    
    result = await generate_from_template(
        template_name="c4_microservices_basic",
        variables={
            "system_name": "Order Management Platform",
            "user_label": "System Admin",
            "user_description": "Manages orders and users",
            "gateway_tech": "Kong API Gateway",
            "auth_service_name": "Auth Service",
            "auth_tech": "Node.js + JWT",
            "user_service_name": "User Service",
            "user_tech": "Python FastAPI",
            "product_service_name": "Product Catalog",
            "product_tech": "Java Spring Boot",
            "order_service_name": "Order Service",
            "order_tech": "Go",
            "user_db_name": "Users DB",
            "product_db_name": "Products DB",
            "order_db_name": "Orders DB",
            "db_tech": "PostgreSQL",
            "queue_name": "Event Bus",
            "queue_tech": "RabbitMQ"
        },
        output_path="output/template_microservices.png"
    )
    
    print(f"\n{result}")


async def test_generate_api_gateway():
    """Test generating API Gateway pattern"""
    print("\n" + "="*70)
    print("🏗️  TEST 6: Generate API Gateway C4 Diagram")
    print("="*70)
    
    result = await generate_from_template(
        template_name="c4_api_gateway",
        variables={
            "system_name": "API Platform",
            "client_label": "API Client",
            "gateway_tech": "Kong Gateway",
            "service1_name": "User Service",
            "service1_tech": "Node.js",
            "service1_description": "User management",
            "service1_route": "users",
            "service2_name": "Product Service",
            "service2_tech": "Python",
            "service2_description": "Product catalog",
            "service2_route": "products",
            "service3_name": "Order Service",
            "service3_tech": "Go",
            "service3_description": "Order processing",
            "service3_route": "orders",
            "cache_tech": "Redis",
            "auth_provider": "Auth0",
            "monitoring_provider": "Datadog"
        },
        output_path="output/template_api_gateway.png"
    )
    
    print(f"\n{result}")


async def test_generate_flowchart():
    """Test generating approval flowchart"""
    print("\n" + "="*70)
    print("📊 TEST 7: Generate Approval Flowchart")
    print("="*70)
    
    result = await generate_from_template(
        template_name="mermaid_flowchart_approval",
        variables={
            "process_name": "Document Approval Process",
            "step1_label": "Submit Document",
            "check1_label": "Valid format?",
            "check1_yes": "Yes",
            "check1_no": "No",
            "review_label": "Manager Review",
            "review_approve": "Approve",
            "review_reject": "Reject",
            "review_revise": "Request Revision",
            "approve_label": "Document Approved",
            "reject_label": "Document Rejected",
            "notify_label": "Notify Submitter"
        },
        output_path="output/template_approval_flow.png"
    )
    
    print(f"\n{result}")


async def test_generate_auth_sequence():
    """Test generating authentication sequence diagram"""
    print("\n" + "="*70)
    print("📊 TEST 8: Generate Auth Sequence Diagram")
    print("="*70)
    
    result = await generate_from_template(
        template_name="mermaid_sequence_auth",
        variables={
            "user_label": "User",
            "frontend_label": "Web App",
            "gateway_label": "API Gateway",
            "auth_service_label": "Auth Service",
            "db_label": "User Database",
            "action1_label": "Enter credentials",
            "action2_label": "POST /login",
            "action3_label": "Validate credentials",
            "action4_label": "Query user",
            "response1_label": "User found",
            "condition1_label": "Valid",
            "condition2_label": "Invalid",
            "success_response": "200 OK + Token",
            "success_token": "JWT Token",
            "success_message": "Login successful",
            "error_response": "401 Unauthorized",
            "error_status": "Error 401",
            "error_message": "Invalid credentials",
            "note_text": "JWT token expires after 1 hour"
        },
        output_path="output/template_auth_sequence.png"
    )
    
    print(f"\n{result}")


async def main():
    """Run all template tests"""
    print("\n" + "="*70)
    print("🧪 TEST TEMPLATE MODE")
    print("="*70)
    
    tests = [
        test_list_templates,
        test_get_template_variables,
        test_get_template_info,
        test_generate_ecommerce,
        test_generate_microservices,
        test_generate_api_gateway,
        test_generate_flowchart,
        test_generate_auth_sequence,
    ]
    
    failed = []
    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"\n❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed.append((test.__name__, str(e)))
    
    print("\n" + "="*70)
    print("📊 PODSUMOWANIE")
    print("="*70)
    print(f"✅ Passed: {len(tests) - len(failed)}/{len(tests)}")
    print(f"❌ Failed: {len(failed)}/{len(tests)}")
    
    if failed:
        print("\n❌ Failed tests:")
        for name, error in failed:
            print(f"  - {name}: {error}")
    else:
        print("\n🎉 Wszystkie testy przeszły pomyślnie!")
    
    print("\n📁 Wygenerowane pliki znajdują się w katalogu: output/")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())

