# 📝 Example Prompts for Claude Desktop

Skopiuj i wklej te prompty bezpośrednio do Claude Desktop po restarcie aplikacji.

---

## 🔧 Test 1: C4 Context Diagram (E-commerce)

**Copy this prompt:**

```
Generate a C4 context diagram for an e-commerce system with the following components:

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

Show relationships between all components with descriptions.

Save the diagram as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/c4-ecommerce-context.png
```

**Expected output:** `c4-ecommerce-context.png`

---

## 📄 Test 2: ADR Document (REST → GraphQL)

**Copy this prompt:**

```
Create an Architecture Decision Record (ADR) document for switching from REST to GraphQL API.

Include the following sections:

**Title:** ADR-001: Migration from REST to GraphQL

**Context:**
- Current REST API has over-fetching and under-fetching issues
- Multiple endpoints make mobile app slow (too many requests)
- Frontend teams want more flexibility in data queries
- Need better real-time capabilities

**Decision:**
Migrate to GraphQL API while maintaining REST for backwards compatibility during transition period.

**Consequences:**

Positive:
- Single endpoint for all queries
- Clients can request exactly what they need
- Better developer experience
- Built-in introspection and documentation
- Real-time subscriptions support

Negative:
- Learning curve for team
- Need to implement caching strategy
- Query complexity management required
- Additional tooling needed

**Alternatives Considered:**
1. Keep REST and optimize endpoints
2. Use gRPC for internal services
3. Implement OData

**Implementation Plan:**
- Phase 1 (Q1 2025): Setup GraphQL server alongside REST
- Phase 2 (Q2 2025): Migrate 50% of endpoints
- Phase 3 (Q3 2025): Complete migration
- Phase 4 (Q4 2025): Deprecate REST API

Save the document in Polish with proper formatting to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/adr-001-rest-to-graphql.md
```

**Expected output:** `adr-001-rest-to-graphql.md`

---

## 📊 Test 3: Gantt Chart (Q1 2025 Roadmap)

**Copy this prompt:**

```
Generate a Gantt chart for our Q1 2025 product roadmap with the following timeline:

Project: MCP Documentation Server Launch

Tasks:
1. Planning & Design (Jan 1 - Jan 15, 2025)
   - Requirements gathering
   - Architecture design
   - UI/UX mockups

2. Development Sprint 1 (Jan 16 - Jan 31, 2025)
   - Core MCP server implementation
   - PlantUML integration
   - Mermaid integration

3. Development Sprint 2 (Feb 1 - Feb 14, 2025)
   - Graphviz integration
   - draw.io integration
   - PDF/DOCX export

4. Testing & QA (Feb 15 - Feb 28, 2025)
   - Unit tests
   - Integration tests
   - Performance testing
   - Bug fixes

5. Documentation (Mar 1 - Mar 10, 2025)
   - User guides
   - API documentation
   - Video tutorials

6. Beta Launch (Mar 11 - Mar 20, 2025)
   - Limited release
   - User feedback collection
   - Bug fixes

7. Production Launch (Mar 21 - Mar 31, 2025)
   - Public release
   - Marketing campaign
   - Community engagement

Save the Gantt chart as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/roadmap-q1-2025.png
```

**Expected output:** `roadmap-q1-2025.png`

---

## 🏗️ Test 4: UML Class Diagram (E-commerce Domain Model)

**Copy this prompt:**

```
Generate a UML class diagram for an e-commerce domain model with the following classes:

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

Save the diagram as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/uml-ecommerce-domain.png
```

**Expected output:** `uml-ecommerce-domain.png`

---

## 🔄 Test 5: Sequence Diagram (User Authentication Flow)

**Copy this prompt:**

```
Generate a sequence diagram showing user authentication flow with OAuth 2.0:

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

Save the diagram as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/sequence-oauth-auth.png
```

**Expected output:** `sequence-oauth-auth.png`

---

## 🌐 Test 6: Flowchart (Order Processing)

**Copy this prompt:**

```
Generate a flowchart for e-commerce order processing workflow:

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

Save the flowchart as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/flowchart-order-processing.png
```

**Expected output:** `flowchart-order-processing.png`

---

## 📦 Test 7: Dependency Graph (Microservices)

**Copy this prompt:**

```
Generate a dependency graph showing relationships between microservices:

Services:
1. api-gateway (entry point)
2. user-service
3. product-service
4. order-service
5. payment-service
6. notification-service
7. inventory-service
8. shipping-service

Dependencies:
- api-gateway → all services (orchestration)
- order-service → product-service (get product info)
- order-service → inventory-service (check stock)
- order-service → payment-service (process payment)
- order-service → notification-service (send confirmations)
- order-service → shipping-service (create shipment)
- payment-service → notification-service (payment updates)
- shipping-service → notification-service (shipping updates)
- inventory-service → product-service (product data)

Use different colors for:
- External APIs (red)
- Core services (blue)
- Support services (green)

Save as PNG to:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/dependency-graph-microservices.png
```

**Expected output:** `dependency-graph-microservices.png`

---

## 📋 Test 8: Export to PDF

**Copy this prompt:**

```
Take the ADR document we created earlier (adr-001-rest-to-graphql.md) 
and export it to PDF with:
- Professional formatting
- Table of contents
- Polish language support
- Page numbers
- Company header: "MCP Documentation Server"
- Author: "Łukasz Żychal"

Save as:
/Users/lukaszzychal/PhpstormProjects/MCPServer/test-server/adr-001-rest-to-graphql.pdf
```

**Expected output:** `adr-001-rest-to-graphql.pdf`

---

## ✅ Verification Checklist

Po uruchomieniu wszystkich testów, sprawdź:

```bash
cd /Users/lukaszzychal/PhpstormProjects/MCPServer/test-server
ls -lh

# Powinieneś zobaczyć:
# ✓ c4-ecommerce-context.png
# ✓ adr-001-rest-to-graphql.md
# ✓ adr-001-rest-to-graphql.pdf
# ✓ roadmap-q1-2025.png
# ✓ uml-ecommerce-domain.png
# ✓ sequence-oauth-auth.png
# ✓ flowchart-order-processing.png
# ✓ dependency-graph-microservices.png
```

---

## 🚨 Ważne Uwagi

### 1. **Ścieżki**
- Używaj **pełnych ścieżek** dla pewności
- Claude może sugerować skróconą ścieżkę - popraw ją

### 2. **Restart Claude**
- Po zmianie config, **ZAWSZE restartuj** Claude Desktop (⌘+Q)

### 3. **Docker Running**
- Upewnij się że Docker działa:
  ```bash
  docker compose ps
  ```

### 4. **Pierwsze Użycie**
- Claude może potrzebować kilku sekund na pierwszy request
- Następne będą szybsze (cache)

---

## 🎯 Success Criteria

Test zakończony sukcesem jeśli:

1. ✅ Wszystkie 8 plików zostały utworzone
2. ✅ Obrazy (PNG) są czytelne i poprawne
3. ✅ Dokumenty (MD/PDF) mają polskie znaki
4. ✅ Claude nie zgłasza błędów połączenia
5. ✅ Generowanie trwa < 30 sekund na diagram

---

**Pro Tip:** Możesz poprosić Claude o modyfikacje:
```
"Make the C4 diagram bigger and add more details"
"Translate the ADR to English"
"Add more tasks to the Gantt chart"
```

---

**Last Updated:** 25 Listopada 2025  
**Tested:** ✅ All prompts verified  
**Status:** 🚀 Ready to use

