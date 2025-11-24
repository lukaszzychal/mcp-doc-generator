# Przykłady Użycia MCP Documentation Server

## Przykład 1: Generowanie C4 Context Diagram

**Prompt do Claude:**

```
Wygeneruj C4 Context Diagram dla systemu e-commerce z następującymi elementami:
- Użytkownik (Klient sklepu)
- System E-Commerce (główny system)
- Payment Gateway (system płatności zewnętrzny)
- Email Service (wysyłka emaili)

Zapisz jako output/c4-context.png
```

**Wygenerowany kod PlantUML:**

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title System E-Commerce - Context Diagram

Person(customer, "Klient", "Użytkownik sklepu internetowego")
System(ecommerce, "System E-Commerce", "Platforma sprzedażowa online")
System_Ext(payment, "Payment Gateway", "Zewnętrzny system płatności")
System_Ext(email, "Email Service", "Serwis wysyłki emaili")

Rel(customer, ecommerce, "Przegląda produkty, składa zamówienia")
Rel(ecommerce, payment, "Przetwarza płatności", "HTTPS")
Rel(ecommerce, email, "Wysyła powiadomienia", "SMTP")

@enduml
```

## Przykład 2: Diagram Sekwencji - Proces Zamówienia

**Prompt:**

```
Stwórz diagram sekwencji dla procesu składania zamówienia w systemie e-commerce:
1. Użytkownik dodaje produkt do koszyka
2. Użytkownik przechodzi do płatności
3. System weryfikuje dostępność
4. System wysyła żądanie płatności do Payment Gateway
5. Payment Gateway potwierdza płatność
6. System tworzy zamówienie
7. System wysyła email potwierdzający

Zapisz jako output/order-sequence.png
```

## Przykład 3: ADR - Wybór Bazy Danych

**Prompt:**

```
Utwórz ADR dokumentujący wybór PostgreSQL jako głównej bazy danych dla systemu e-commerce.

Użyj szablonu ADR z następującymi danymi:
- Numer: 001
- Tytuł: Wybór PostgreSQL jako głównej bazy danych
- Status: Accepted
- Autor: Jan Kowalski
- Kontekst: Potrzebujemy relacyjnej bazy danych z ACID
- Decyzja: PostgreSQL ze względu na dojrzałość, wydajność i wsparcie JSON
- Pozytywne: ACID, JSON support, performance, open source
- Negatywne: Wymaga więcej zasobów niż MySQL
- Alternatywy: MySQL, MongoDB, CockroachDB

Zapisz jako output/adr-001-postgresql.md
```

## Przykład 4: Microservices Overview

**Prompt:**

```
Wygeneruj kompletny przegląd architektury microservices dla systemu e-commerce zawierający:

Serwisy:
1. API Gateway (Node.js, port 3000)
2. Auth Service (Node.js, port 3001)
3. Product Service (Python, port 8001)
4. Order Service (Python, port 8002)
5. Payment Service (Java, port 8003)

Dodaj:
- Diagram C4 Container
- Graf zależności między serwisami
- Dokumentację każdego serwisu
- Wyeksportuj wszystko do PDF

Zapisz jako output/microservices-architecture.pdf
```

## Przykład 5: API Documentation

**Prompt:**

```
Utwórz dokumentację API dla endpointu tworzenia zamówienia:

POST /api/orders
- Wymaga autoryzacji Bearer token
- Request body: { "items": [...], "shipping_address": {...}, "payment_method": "..." }
- Response: { "order_id": "...", "status": "...", "total": ... }

Dodaj diagram sekwencji pokazujący flow tego endpointu.

Użyj szablonu API Spec i wyeksportuj do PDF.
```

## Przykład 6: Gantt Chart - Timeline Projektu

**Prompt:**

```
Utwórz wykres Gantta dla projektu e-commerce:

Fazy:
- Analiza wymagań: 2 tygodnie (od 1 grudnia)
- Design UI/UX: 2 tygodnie
- Development Backend: 4 tygodnie
- Development Frontend: 4 tygodnie (rozpoczyna się po 2 tygodniach backend)
- Testing: 2 tygodnie
- Deployment: 1 tydzień

Zapisz jako output/project-timeline.png
```

## Przykład 7: Infrastructure Diagram

**Prompt:**

```
Stwórz diagram infrastruktury AWS dla systemu e-commerce:

- VPC z 2 availability zones
- Application Load Balancer
- ECS Cluster z microservices
- RDS PostgreSQL (Multi-AZ)
- ElastiCache Redis
- S3 dla plików statycznych
- CloudFront jako CDN

Zapisz jako output/aws-infrastructure.png
```

## Przykład 8: Kompletna Dokumentacja w Jednym Commandi

**Prompt:**

```
Przygotuj kompletną dokumentację architektury systemu e-commerce:

1. C4 Context Diagram (użytkownik, systemy zewnętrzne)
2. C4 Container Diagram (microservices, bazy danych)
3. Diagram sekwencji dla procesu zamówienia
4. Graf zależności między microservices
5. ADR dla kluczowych decyzji technologicznych
6. API Spec dla głównych endpointów
7. Microservices Overview

Wygeneruj wszystkie diagramy i połącz je w jeden PDF z tytułem "Dokumentacja Architektury E-Commerce" i spisem treści.
```

## Przykład 9: UML Class Diagram

**Prompt:**

```
Wygeneruj diagram klas UML dla domenowego modelu zamówień:

Klasy:
- Order (id, status, total, created_at)
- OrderItem (id, product_id, quantity, price)
- Product (id, name, price, stock)
- Customer (id, name, email)
- Address (id, street, city, postal_code)

Relacje:
- Order ma wiele OrderItems (1:n)
- Order ma jednego Customera (n:1)
- Order ma Address (1:1)
- OrderItem odnosi się do Product (n:1)

Zapisz jako output/order-domain-model.png
```

## Przykład 10: Deployment Diagram

**Prompt:**

```
Stwórz diagram wdrożenia (deployment diagram UML) pokazujący:

- Load Balancer (nginx)
- 3x Application Servers (Docker containers)
- PostgreSQL Database (primary + read replica)
- Redis Cache
- RabbitMQ Message Broker

Z zaznaczeniem protokołów komunikacji (HTTP, TCP, AMQP).

Zapisz jako output/deployment-diagram.png
```

## Tips & Tricks

### Najlepsze praktyki:

1. **Zawsze podawaj pełną ścieżkę output**: `output/my-diagram.png`
2. **Używaj polskich opisów** - wszystkie narzędzia wspierają UTF-8
3. **Łącz diagramy z tekstem** - generuj Markdown + diagramy, potem eksportuj do PDF
4. **Używaj szablonów** - szablony ADR, API Spec są gotowe do użycia
5. **Testuj lokalnie** - najpierw PNG, potem PDF dla dokumentów finalnych

### Skróty:

```
"Wygeneruj C4" = C4 Context Diagram
"Utwórz flowchart" = Mermaid Flowchart
"ADR dla..." = ADR z template
"API docs" = API Specification
"Do PDF" = Export to PDF z TOC
```

### Workflow produkcyjny:

```
1. Wygeneruj diagramy (PNG/SVG)
2. Utwórz dokumenty Markdown z embedded images
3. Połącz wszystko w jeden Markdown
4. Wyeksportuj do PDF z tytułem i spisem treści
```

