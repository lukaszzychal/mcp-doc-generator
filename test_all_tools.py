#!/usr/bin/env python3
"""
Test wszystkich 11 narzędzi MCP
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.plantuml import generate_c4_diagram, generate_uml_diagram, generate_sequence_diagram
from tools.mermaid import generate_flowchart, generate_sequence, generate_gantt
from tools.graphviz import generate_graph
from tools.drawio import generate_diagram as generate_drawio_diagram
from tools.export import export_to_pdf, export_to_docx, create_from_template


async def test_1_c4_context():
    """Test 1: C4 Context Diagram"""
    print("\n1️⃣  Testing: generate_c4_diagram (Context)")
    content = """
Person(user, "Klient", "Użytkownik systemu e-commerce")
System(shop, "System E-Commerce", "Platforma sprzedażowa")
System_Ext(payment, "Payment Gateway", "Bramka płatności")
System_Ext(email, "Email Service", "Wysyłka powiadomień")

Rel(user, shop, "Przegląda produkty, składa zamówienia", "HTTPS")
Rel(shop, payment, "Przetwarza płatności", "API")
Rel(shop, email, "Wysyła potwierdzenia", "SMTP")
"""
    result = await generate_c4_diagram("context", content, "output/test_c4_context.png", "png")
    print(f"   ✅ {result}")


async def test_2_c4_container():
    """Test 2: C4 Container Diagram"""
    print("\n2️⃣  Testing: generate_c4_diagram (Container)")
    content = """
Person(user, "User")
Container(web, "Web App", "React", "SPA")
Container(api, "API", "Python/FastAPI", "REST API")
ContainerDb(db, "Database", "PostgreSQL", "Stores data")

Rel(user, web, "Uses", "HTTPS")
Rel(web, api, "API calls", "JSON/HTTPS")
Rel(api, db, "Reads/Writes", "SQL")
"""
    result = await generate_c4_diagram("container", content, "output/test_c4_container.png", "png")
    print(f"   ✅ {result}")


async def test_3_uml_class():
    """Test 3: UML Class Diagram"""
    print("\n3️⃣  Testing: generate_uml_diagram (Class)")
    content = """
class User {
  +id: int
  +name: string
  +email: string
  +login()
  +logout()
}

class Order {
  +id: int
  +date: datetime
  +total: decimal
  +process()
}

class Product {
  +id: int
  +name: string
  +price: decimal
}

User "1" --> "*" Order : places
Order "*" --> "*" Product : contains
"""
    result = await generate_uml_diagram("class", content, "output/test_uml_class.png", "png")
    print(f"   ✅ {result}")


async def test_4_sequence():
    """Test 4: Sequence Diagram (PlantUML)"""
    print("\n4️⃣  Testing: generate_sequence_diagram")
    content = """
actor User
participant "Web App" as Web
participant "API Gateway" as API
database "Database" as DB

User -> Web: Login request
Web -> API: POST /auth/login
API -> DB: Verify credentials
DB --> API: User data
API --> Web: JWT Token
Web --> User: Login success
"""
    result = await generate_sequence_diagram(content, "output/test_sequence.png", "png")
    print(f"   ✅ {result}")


async def test_5_flowchart():
    """Test 5: Mermaid Flowchart"""
    print("\n5️⃣  Testing: generate_flowchart")
    content = """
flowchart TD
    Start([Start]) --> Input[Wprowadź dane]
    Input --> Validate{Walidacja}
    Validate -->|Poprawne| Process[Przetwórz dane]
    Validate -->|Błędne| Error[Wyświetl błąd]
    Error --> Input
    Process --> Save[Zapisz do bazy]
    Save --> Success([Koniec])
"""
    result = await generate_flowchart(content, "output/test_flowchart.png", "png")
    print(f"   ✅ {result}")


async def test_6_mermaid_sequence():
    """Test 6: Mermaid Sequence Diagram"""
    print("\n6️⃣  Testing: generate_sequence (Mermaid)")
    content = """
sequenceDiagram
    participant U as User
    participant W as Web
    participant A as API
    participant D as Database
    
    U->>W: Open page
    W->>A: GET /data
    A->>D: SELECT * FROM users
    D-->>A: Result set
    A-->>W: JSON response
    W-->>U: Display data
"""
    result = await generate_sequence(content, "output/test_mermaid_seq.png", "png")
    print(f"   ✅ {result}")


async def test_7_gantt():
    """Test 7: Gantt Chart"""
    print("\n7️⃣  Testing: generate_gantt")
    content = """
gantt
    title Harmonogram Projektu E-Commerce
    dateFormat YYYY-MM-DD
    
    section Faza 1: Planowanie
    Analiza wymagań       :a1, 2025-12-01, 7d
    Projektowanie         :a2, after a1, 10d
    
    section Faza 2: Rozwój
    Backend API          :b1, after a2, 21d
    Frontend React       :b2, after a2, 21d
    Integracja           :b3, after b1, 7d
    
    section Faza 3: Testowanie
    Testy jednostkowe    :c1, after b2, 5d
    Testy integracyjne   :c2, after b3, 7d
    Testy akceptacyjne   :c3, after c2, 5d
"""
    result = await generate_gantt(content, "output/test_gantt.png", "png")
    print(f"   ✅ {result}")


async def test_8_dependency_graph():
    """Test 8: Dependency Graph"""
    print("\n8️⃣  Testing: generate_dependency_graph")
    content = """
digraph Dependencies {
    rankdir=LR;
    node [shape=box, style=rounded];
    
    "API Gateway" -> "Auth Service";
    "API Gateway" -> "Order Service";
    "API Gateway" -> "Product Service";
    
    "Order Service" -> "Payment Service";
    "Order Service" -> "Inventory Service";
    "Order Service" -> "Notification Service";
    
    "Payment Service" -> "External Payment API";
    "Notification Service" -> "Email Service";
    "Notification Service" -> "SMS Service";
    
    "Product Service" -> "Database";
    "Order Service" -> "Database";
    "Auth Service" -> "Database";
}
"""
    result = await generate_graph(content, "output/test_dependencies.png", "png", "dot")
    print(f"   ✅ {result}")


async def test_9_cloud_diagram():
    """Test 9: Cloud Architecture Diagram"""
    print("\n9️⃣  Testing: generate_cloud_diagram")
    # Minimal draw.io XML
    content = """<mxfile>
  <diagram name="AWS Architecture">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="User" style="shape=actor;html=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="80" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="AWS Cloud" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="200" y="40" width="200" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="" style="endArrow=classic;html=1;" edge="1" parent="1" source="2" target="3">
          <mxGeometry width="50" height="50" relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    result = await generate_drawio_diagram(content, "output/test_cloud.png", "png")
    print(f"   ✅ {result}")


async def test_10_export_pdf():
    """Test 10: Export to PDF"""
    print("\n🔟 Testing: export_to_pdf")
    markdown = """# Dokumentacja Techniczna

## 1. Przegląd Systemu

System e-commerce składa się z następujących komponentów:

- **Frontend**: React SPA
- **Backend**: Python/FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis

## 2. Architektura

System wykorzystuje architekturę mikroserwisów z następującymi serwisami:

1. Auth Service
2. Order Service
3. Product Service
4. Payment Service

## 3. API Endpoints

### Authentication
- `POST /auth/login` - Logowanie użytkownika
- `POST /auth/register` - Rejestracja
- `POST /auth/refresh` - Odświeżenie tokena

### Orders
- `GET /orders` - Lista zamówień
- `POST /orders` - Nowe zamówienie
- `GET /orders/{id}` - Szczegóły zamówienia

## 4. Bezpieczeństwo

- JWT tokens
- HTTPS
- Rate limiting
- Input validation
"""
    result = await export_to_pdf(
        markdown,
        "output/test_documentation.pdf",
        title="Dokumentacja E-Commerce",
        author="Łukasz Żychal",
        include_toc=True
    )
    print(f"   ✅ {result}")


async def test_11_export_docx():
    """Test 11: Export to DOCX"""
    print("\n1️⃣1️⃣  Testing: export_to_docx")
    markdown = """# Specyfikacja API

## Wprowadzenie

Niniejszy dokument opisuje API systemu e-commerce.

## Endpointy

### POST /auth/login

**Opis**: Logowanie użytkownika

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

**Response**:
```json
{
  "token": "jwt.token.here",
  "user": {
    "id": 123,
    "email": "user@example.com"
  }
}
```

### GET /products

**Opis**: Lista produktów

**Query Parameters**:
- `page`: Numer strony (default: 1)
- `limit`: Liczba rekordów (default: 20)

**Response**:
```json
{
  "data": [...],
  "total": 150,
  "page": 1
}
```
"""
    result = await export_to_docx(
        markdown,
        "output/test_api_spec.docx",
        title="Specyfikacja API",
        author="Łukasz Żychal"
    )
    print(f"   ✅ {result}")


async def test_12_template_adr():
    """Test 12: Document from Template (ADR)"""
    print("\n1️⃣2️⃣  Testing: create_from_template (ADR)")
    variables = {
        "number": "001",
        "title": "Wybór PostgreSQL jako głównej bazy danych",
        "date": "2025-11-24",
        "status": "Zaakceptowane",
        "author": "Łukasz Żychal",
        "context": "System e-commerce wymaga niezawodnej bazy danych do przechowywania danych o produktach, zamówieniach i użytkownikach.",
        "decision": "Wybraliśmy PostgreSQL jako główną bazę danych relacyjnych dla systemu.",
        "positive_consequences": "- Wsparcie ACID\n- Zaawansowane typy danych (JSON, Array)\n- Silna społeczność\n- Dobra dokumentacja\n- Bezpłatna licencja open-source",
        "negative_consequences": "- Wymaga więcej zasobów niż MySQL\n- Bardziej złożona konfiguracja replikacji",
        "alternatives": "- MySQL: prostszy, ale mniej funkcjonalny\n- MongoDB: NoSQL, ale system wymaga transakcji ACID"
    }
    result = await create_from_template("adr", variables, "output/test_adr_001.md")
    print(f"   ✅ {result}")


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 TEST WSZYSTKICH 11 NARZĘDZI MCP")
    print("="*70)
    
    tests = [
        test_1_c4_context,
        test_2_c4_container,
        test_3_uml_class,
        test_4_sequence,
        test_5_flowchart,
        test_6_mermaid_sequence,
        test_7_gantt,
        test_8_dependency_graph,
        test_9_cloud_diagram,
        test_10_export_pdf,
        test_11_export_docx,
        test_12_template_adr,
    ]
    
    failed = []
    for test in tests:
        try:
            await test()
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
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

