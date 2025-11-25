#!/usr/bin/env python3
"""
Generuje przykładowe pliki dla wszystkich narzędzi MCP.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_client import MCPClient
import time

def generate_all_examples():
    """Generuje przykłady dla wszystkich narzędzi"""
    client = MCPClient()
    
    try:
        client.start_server()
        print("Generowanie przykładów dla wszystkich narzędzi MCP...\n")
        
        # Używamy output/ bo jest zmountowany w Docker
        examples_dir = "../output"
        os.makedirs(examples_dir, exist_ok=True)
        
        # 1. C4 Context Diagram - Professional E-commerce System
        print("1. C4 Context Diagram (Professional E-commerce)...")
        prompt = """Generate a C4 context diagram for an e-commerce system with the following components:

External Systems:
- Users (customers browsing and purchasing)
- Payment Gateway (Stripe/PayPal)
- Shipping Service (FedEx/UPS)

System Boundary - E-commerce Platform:
- Web Application (React frontend)
- Mobile App (iOS/Android)
- API Gateway (Node.js)
- Order Service
- Inventory Service
- Database (PostgreSQL)

Show relationships between all components with descriptions and protocols (HTTPS, REST API).

Save as: output/example_c4_context.png"""
        client.process_prompt(prompt)
        time.sleep(2)
        
        # 2. C4 Container Diagram - Detailed Microservices
        print("\n2. C4 Container Diagram (Microservices Architecture)...")
        prompt = """Generate a C4 container diagram for e-commerce platform showing:

Containers:
- Web Application (React, serves static content)
- Mobile App (iOS/Android native apps)
- API Gateway (Node.js, handles routing and authentication)
- Order Service (Python, processes orders)
- Inventory Service (Python, manages stock)
- Payment Service (Java, handles payments)
- Notification Service (Node.js, sends emails/SMS)
- Database (PostgreSQL, primary data store)
- Cache (Redis, session and cache storage)

Show all relationships with protocols and data flows.

Save as: output/example_c4_container.png"""
        client.process_prompt(prompt)
        time.sleep(2)
        
        # 3. UML Class Diagram - E-commerce Domain Model
        print("\n3. UML Class Diagram (E-commerce Domain Model)...")
        prompt = """Generate a UML class diagram for an e-commerce domain model with the following classes:

1. User
   - id: UUID
   - email: String
   - password: String
   - firstName: String
   - lastName: String
   - createdAt: DateTime
   + register()
   + login()
   + updateProfile()

2. Product
   - id: UUID
   - name: String
   - description: String
   - price: Decimal
   - stock: Integer
   - category: Category
   + updatePrice()
   + checkAvailability()

3. Order
   - id: UUID
   - userId: UUID
   - orderDate: DateTime
   - status: OrderStatus
   - totalAmount: Decimal
   - items: List<OrderItem>
   + calculateTotal()
   + updateStatus()
   + cancel()

4. OrderItem
   - id: UUID
   - orderId: UUID
   - productId: UUID
   - quantity: Integer
   - price: Decimal
   + getSubtotal()

5. Payment
   - id: UUID
   - orderId: UUID
   - amount: Decimal
   - method: PaymentMethod
   - status: PaymentStatus
   - processedAt: DateTime
   + process()
   + refund()

Relationships:
- User has many Orders (1:*)
- Order has many OrderItems (1:*)
- OrderItem references Product (*:1)
- Order has one Payment (1:1)

Save as: output/example_uml_class.png"""
        client.process_prompt(prompt)
        time.sleep(2)
        
        # 4. Sequence Diagram - OAuth 2.0 Authentication Flow
        print("\n4. Sequence Diagram (OAuth 2.0 Authentication)...")
        prompt = """Generate a sequence diagram showing user authentication flow with OAuth 2.0:

Participants:
- User (Browser)
- Frontend (React App)
- API Gateway
- Auth Service
- Database
- OAuth Provider (Google)

Flow:
1. User clicks "Login with Google" button
2. Frontend redirects to OAuth Provider
3. User enters credentials on OAuth Provider
4. OAuth Provider validates and returns authorization code
5. Frontend sends code to API Gateway
6. API Gateway forwards to Auth Service
7. Auth Service exchanges code for access token with OAuth Provider
8. Auth Service creates/updates user in Database
9. Auth Service generates JWT token
10. JWT returned to Frontend via API Gateway
11. Frontend stores JWT and redirects to dashboard
12. User is logged in

Include error handling for failed authentication.

Save as: output/example_sequence.png"""
        client.process_prompt(prompt)
        time.sleep(2)
        
        # 5. Flowchart - Order Processing Workflow
        print("\n5. Flowchart (Order Processing Workflow)...")
        prompt = """Generate a flowchart for e-commerce order processing workflow:

Start: New Order Received
↓
Check Product Availability
  → If OUT OF STOCK: Send "Out of Stock" notification → End
  → If IN STOCK: Continue
↓
Validate Payment Information
  → If INVALID: Request Payment Update → Loop back
  → If VALID: Continue
↓
Process Payment
  → If FAILED: Send Payment Failed notification → End
  → If SUCCESS: Continue
↓
Reserve Inventory
↓
Create Shipping Label
↓
Notify Warehouse
↓
Update Order Status to "Processing"
↓
Send Confirmation Email to Customer
↓
Wait for Shipping
  → If SHIPPED: Update to "Shipped" → Track Package
  → If DELAYED: Send Delay notification
↓
Wait for Delivery
  → If DELIVERED: Update to "Delivered" → Request Review
  → If FAILED DELIVERY: Contact Customer → Reschedule
↓
End: Order Complete

Save as: output/example_flowchart.png"""
        client.process_prompt(prompt)
        time.sleep(2)
        
        # 6. Mermaid Sequence
        print("\n6. Mermaid Sequence Diagram...")
        prompt = """Generate Mermaid sequence diagram:
User requests data from API, API queries database, database returns data, API responds to user.

Save as: output/example_mermaid_sequence.png"""
        client.process_prompt(prompt)
        time.sleep(1)
        
        # 7. Gantt Chart - Q1 2025 Roadmap
        print("\n7. Gantt Chart (Q1 2025 Product Roadmap)...")
        gantt_content = """gantt
    title MCP Documentation Server Launch - Q1 2025
    dateFormat YYYY-MM-DD
    section Planning & Design
    Requirements gathering :a1, 2025-01-01, 5d
    Architecture design :a2, after a1, 5d
    UI/UX mockups :a3, after a2, 5d
    section Development Sprint 1
    Core MCP server :b1, 2025-01-16, 8d
    PlantUML integration :b2, after b1, 4d
    Mermaid integration :b3, after b2, 3d
    section Development Sprint 2
    Graphviz integration :c1, 2025-02-01, 5d
    draw.io integration :c2, after c1, 4d
    PDF/DOCX export :c3, after c2, 5d
    section Testing & QA
    Unit tests :d1, 2025-02-15, 5d
    Integration tests :d2, after d1, 5d
    Performance testing :d3, after d2, 3d
    Bug fixes :d4, after d3, 5d
    section Documentation
    User guides :e1, 2025-03-01, 5d
    API documentation :e2, after e1, 3d
    Video tutorials :e3, after e2, 2d
    section Launch
    Beta release :f1, 2025-03-11, 5d
    User feedback :f2, after f1, 4d
    Production launch :f3, 2025-03-21, 10d"""
        success, result = client.call_tool("generate_gantt", {
            "content": gantt_content,
            "output_path": "output/example_gantt.png",
            "format": "png"
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        time.sleep(2)
        
        # 8. Dependency Graph - Microservices Architecture
        print("\n8. Dependency Graph (Microservices)...")
        graph_content = """digraph G {
    rankdir=LR;
    node [shape=box, style=rounded];
    
    api_gateway [label="API Gateway", color=blue, style=filled, fillcolor=lightblue];
    user_service [label="User Service", color=blue, style=filled, fillcolor=lightblue];
    product_service [label="Product Service", color=blue, style=filled, fillcolor=lightblue];
    order_service [label="Order Service", color=blue, style=filled, fillcolor=lightblue];
    payment_service [label="Payment Service", color=blue, style=filled, fillcolor=lightblue];
    notification_service [label="Notification Service", color=green, style=filled, fillcolor=lightgreen];
    inventory_service [label="Inventory Service", color=blue, style=filled, fillcolor=lightblue];
    shipping_service [label="Shipping Service", color=green, style=filled, fillcolor=lightgreen];
    
    api_gateway -> user_service [label="orchestration"];
    api_gateway -> product_service [label="orchestration"];
    api_gateway -> order_service [label="orchestration"];
    api_gateway -> payment_service [label="orchestration"];
    
    order_service -> product_service [label="get product info"];
    order_service -> inventory_service [label="check stock"];
    order_service -> payment_service [label="process payment"];
    order_service -> notification_service [label="send confirmations"];
    order_service -> shipping_service [label="create shipment"];
    
    payment_service -> notification_service [label="payment updates"];
    shipping_service -> notification_service [label="shipping updates"];
    inventory_service -> product_service [label="product data"];
}"""
        success, result = client.call_tool("generate_dependency_graph", {
            "content": graph_content,
            "output_path": "output/example_dependency_graph.png",
            "format": "png",
            "layout": "dot"
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        time.sleep(2)
        
        # 9. Cloud Diagram (minimal)
        print("\n9. Cloud Diagram...")
        prompt = """Generate cloud architecture diagram with:
- AWS EC2 instance
- RDS database
- S3 storage

Save as: output/example_cloud.png"""
        client.process_prompt(prompt)
        time.sleep(1)
        
        # 10. Export to PDF - With Embedded Diagram
        print("\n10. Export to PDF (with embedded C4 diagram)...")
        # Pandoc runs in Docker container, so use /app/output/ path
        # Images must be accessible from the container's perspective
        c4_diagram_path = "/app/output/example_c4_context.png"
        
        markdown = f"""# E-Commerce System Architecture Documentation

## Overview

This document describes the architecture of our e-commerce platform, including system boundaries, external integrations, and internal components.

## System Context

The following diagram shows the high-level context of our e-commerce system:

![C4 Context Diagram]({c4_diagram_path})

*Figure 1: C4 Context Diagram showing external systems and main e-commerce platform*

### External Systems

- **Users**: Customers browsing and purchasing products
- **Payment Gateway**: External payment processing (Stripe/PayPal)
- **Shipping Service**: External delivery service (FedEx/UPS)

### System Boundary

The E-Commerce Platform includes:
- Web Application (React frontend)
- Mobile App (iOS/Android)
- API Gateway (Node.js)
- Order Service
- Inventory Service
- Database (PostgreSQL)

## Architecture Decisions

### Technology Stack

- **Frontend**: React.js for web, React Native for mobile
- **Backend**: Node.js with Express for API Gateway
- **Services**: Python for business logic services
- **Database**: PostgreSQL for primary data store
- **Cache**: Redis for session management

### Communication Protocols

- HTTPS for external communication
- REST API for service-to-service communication
- WebSocket for real-time updates

## Next Steps

1. Implement microservices architecture
2. Add monitoring and logging
3. Set up CI/CD pipeline
4. Deploy to production"""
        success, result = client.call_tool("export_to_pdf", {
            "markdown_content": markdown,
            "output_path": "output/example_export.pdf",
            "title": "E-Commerce System Architecture",
            "author": "MCP Documentation Server",
            "include_toc": True
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        time.sleep(2)
        
        # 11. Export to DOCX - With Embedded Diagram
        print("\n11. Export to DOCX (with embedded diagram)...")
        # Use same markdown with embedded diagram
        success, result = client.call_tool("export_to_docx", {
            "markdown_content": markdown,
            "output_path": "output/example_export.docx",
            "title": "E-Commerce System Architecture",
            "author": "MCP Documentation Server"
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        time.sleep(2)
        
        # 11b. Create Markdown document with embedded diagram
        print("\n11b. Markdown Document (with embedded diagram)...")
        markdown_doc = f"""# E-Commerce System Architecture Documentation

## Overview

This document describes the architecture of our e-commerce platform.

## System Context

![C4 Context Diagram](example_c4_context.png)

*Figure 1: C4 Context Diagram*

## Architecture Details

### External Systems

- **Users**: Customers browsing and purchasing products
- **Payment Gateway**: External payment processing (Stripe/PayPal)
- **Shipping Service**: External delivery service (FedEx/UPS)

### System Components

- Web Application (React frontend)
- Mobile App (iOS/Android)
- API Gateway (Node.js)
- Order Service
- Inventory Service
- Database (PostgreSQL)

## Technology Stack

- **Frontend**: React.js, React Native
- **Backend**: Node.js, Python
- **Database**: PostgreSQL
- **Cache**: Redis
"""
        # Write markdown file
        markdown_path = "../output/example_with_diagram.md"
        os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_doc)
        print(f"  ✓ Markdown document created: {markdown_path}")
        time.sleep(1)
        
        # 12. ADR Template - REST to GraphQL Migration
        print("\n12. ADR Template (REST to GraphQL Migration)...")
        success, result = client.call_tool("create_document_from_template", {
            "template_type": "adr",
            "variables": {
                "title": "ADR-001: Migration from REST to GraphQL",
                "author": "Architecture Team",
                "date": "2025-01-15",
                "status": "Accepted",
                "context": "Current REST API has over-fetching and under-fetching issues. Multiple endpoints make mobile app slow (too many requests). Frontend teams want more flexibility in data queries. Need better real-time capabilities.",
                "decision": "Migrate to GraphQL API while maintaining REST for backwards compatibility during transition period.",
                "consequences": "Positive: Single endpoint for all queries, clients can request exactly what they need, better developer experience, built-in introspection and documentation, real-time subscriptions support. Negative: Learning curve for team, need to implement caching strategy, query complexity management required, additional tooling needed."
            },
            "output_path": "output/example_adr.md"
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        time.sleep(2)
        
        # 13. API Spec Template
        print("\n13. API Spec Template...")
        success, result = client.call_tool("create_document_from_template", {
            "template_type": "api_spec",
            "variables": {
                "title": "Example API",
                "version": "1.0.0",
                "base_url": "https://api.example.com"
            },
            "output_path": "output/example_api_spec.md"
        })
        print(f"  {'✓' if success else '✗'}: {result[:80]}")
        
        print("\n" + "="*60)
        print("Generowanie przykładów zakończone!")
        print("="*60)
        
        # Skopiuj pliki z output/ do examples/generated/
        import pathlib
        import shutil
        output_dir = pathlib.Path("../output").absolute()
        examples_gen_dir = pathlib.Path("../examples/generated").absolute()
        examples_gen_dir.mkdir(parents=True, exist_ok=True)
        
        copied = 0
        if output_dir.exists():
            for f in output_dir.iterdir():
                if f.is_file() and f.name.startswith("example_"):
                    dst = examples_gen_dir / f.name
                    shutil.copy2(f, dst)
                    copied += 1
                    print(f"  ✓ Skopiowano: {f.name}")
        
        print(f"\nPliki zapisane w: {examples_gen_dir}/")
        print(f"Skopiowano {copied} plików z output/ do examples/generated/")
        print("\nWygenerowane pliki:")
        if os.path.exists(examples_gen_dir):
            for f in sorted(os.listdir(examples_gen_dir)):
                if os.path.isfile(os.path.join(examples_gen_dir, f)):
                    size = os.path.getsize(os.path.join(examples_gen_dir, f))
                    print(f"  - {f} ({size:,} bytes)")
        
    finally:
        client.cleanup()

if __name__ == "__main__":
    generate_all_examples()

