# Różnica między C4 Context a Container Diagram

## C4 Context Diagram - CO POWINIEN ZAWIERAĆ:

```
Person (Customer)
    ↓
System (E-commerce Platform) ← JEDEN BLOK, nie rozłożony!
    ↓
System_Ext (Payment Gateway)
System_Ext (Shipping Service)
```

**Elementy:**
- ✅ Person: Customer
- ✅ System: E-commerce Platform (JEDEN blok, cały system)
- ✅ System_Ext: Payment Gateway, Shipping Service
- ❌ NIE MA: Web Application, Mobile App, API Gateway, Order Service, Inventory Service, Database

## C4 Container Diagram - CO POWINIEN ZAWIERAĆ:

```
Person (Customer)
    ↓
Container (Web Application)
Container (Mobile App)
    ↓
Container (API Gateway)
    ↓
Container (Order Service) → Container (Database)
Container (Inventory Service) → Container (Database)
    ↓
System_Ext (Payment Gateway)
System_Ext (Shipping Service)
```

**Elementy:**
- ✅ Person: Customer
- ✅ Container: Web Application, Mobile App, API Gateway, Order Service, Inventory Service, Database
- ✅ System_Ext: Payment Gateway, Shipping Service

## Kluczowa różnica:

**Context Diagram:**
- System pokazany jako **JEDEN blok** "E-commerce Platform"
- Nie pokazuje wewnętrznej struktury
- Pokazuje tylko: kto używa systemu (Person) i z jakimi systemami zewnętrznymi współpracuje

**Container Diagram:**
- System **rozłożony na kontenery** (Web App, Mobile App, API Gateway, Services, Database)
- Pokazuje wewnętrzną architekturę
- Pokazuje, jak kontenery komunikują się ze sobą

## Przykład poprawnego Context diagramu:

```plantuml
Person(customer, "Customer", "Users browsing and purchasing")
System(ecommerce, "E-commerce Platform", "Online shopping platform")
System_Ext(payment, "Payment Gateway", "External payment system")
System_Ext(shipping, "Shipping Service", "External shipping provider")

Rel(customer, ecommerce, "Browses products, places orders", "HTTPS")
Rel(ecommerce, payment, "Processes payments", "HTTPS/REST API")
Rel(ecommerce, shipping, "Creates shipping labels", "HTTPS/REST API")
```

## Przykład poprawnego Container diagramu:

```plantuml
Person(customer, "Customer", "Users browsing and purchasing")
Container(webapp, "Web Application", "React", "Web Application")
Container(mobile, "Mobile App", "iOS/Android", "Mobile App")
Container(api, "API Gateway", "Node.js", "API Gateway")
Container(orders, "Order Service", "Python", "Order Service")
Container(inventory, "Inventory Service", "Python", "Inventory Service")
ContainerDb(db, "Database", "PostgreSQL", "Database")
System_Ext(payment, "Payment Gateway", "External payment system")
System_Ext(shipping, "Shipping Service", "External shipping provider")

Rel(customer, webapp, "Browses products, places orders", "HTTPS")
Rel(customer, mobile, "Browses products, places orders", "HTTPS")
Rel(webapp, api, "Makes API calls", "HTTPS/REST")
Rel(mobile, api, "Makes API calls", "HTTPS/REST")
Rel(api, orders, "Routes order requests", "REST/JSON")
Rel(api, inventory, "Routes inventory requests", "REST/JSON")
Rel(orders, db, "Reads/writes order data", "SQL/TCP")
Rel(inventory, db, "Reads/writes inventory data", "SQL/TCP")
Rel(orders, payment, "Processes payments", "HTTPS/API")
Rel(orders, shipping, "Creates shipping labels", "HTTPS/API")
```

