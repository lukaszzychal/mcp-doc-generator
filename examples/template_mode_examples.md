# 📐 Template Mode - Examples

**Template Mode** makes diagram generation **10x easier** by providing pre-built templates.  
Instead of writing full PlantUML/Mermaid code, you just fill in the blanks!

---

## 🎯 Why Use Template Mode?

### Before (Expert Mode):
```python
# You need to write ALL this code:
generate_c4_diagram(
    diagram_type="context",
    content="""
    @startuml
    !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml
    
    title C4 Context: My E-commerce System
    
    Person(customer, "Customer", "End user")
    System(shop, "E-commerce System", "Main shopping platform")
    System_Ext(payment, "Payment Gateway", "Stripe payment processing")
    System_Ext(email, "Email Service", "SendGrid")
    
    Rel(customer, shop, "Browses products, places orders")
    Rel(shop, payment, "Processes payments", "HTTPS/REST")
    Rel(shop, email, "Sends confirmations", "SMTP")
    
    SHOW_LEGEND()
    @enduml
    """,
    output_path="output/c4.png"
)
```

### After (Template Mode):
```python
# Just fill in the variables!
generate_from_template(
    template_name="c4_ecommerce_basic",
    variables={
        "system_name": "My E-commerce System",
        "customer_label": "Customer",
        "system_description": "Main shopping platform",
        "payment_provider": "Stripe",
        "email_provider": "SendGrid",
        "delivery_provider": "DHL"
    },
    output_path="output/c4.png"
)
```

**Result:** 90% less code, 10x faster! ⚡

---

## 📋 Step 1: List Available Templates

```python
# Get all available templates
list_templates()
```

**Output:**
```
📋 Available Diagram Templates:

🏗️  C4 Architecture:
   - c4_ecommerce_basic
   - c4_microservices_basic
   - c4_api_gateway
   - c4_event_driven

📐 UML Diagrams:
   - uml_class_basic
   - uml_domain_model

📊 Mermaid Diagrams:
   - mermaid_flowchart_approval
   - mermaid_sequence_auth
   - mermaid_gantt_project

🔗 Graphviz Graphs:
   - graphviz_services_deps

ℹ️  Use get_template_info('template_name') to see required variables.
```

---

## 📖 Step 2: Get Template Info

```python
# See what variables a template needs
get_template_info("c4_ecommerce_basic")
```

**Output:**
```
📋 Template: c4_ecommerce_basic
   Type: C4
   Variables (9):
     - system_name
     - customer_label
     - system_description
     - payment_provider
     - email_provider
     - delivery_provider
     - ...

   Usage:
   generate_from_template(
       template_name="c4_ecommerce_basic",
       variables={
           "system_name": "...",
           "customer_label": "...",
           "system_description": "...",
           # ... 6 more variables
       },
       output_path="output/diagram.png"
   )
```

---

## 🚀 Step 3: Generate from Template

### Example 1: E-commerce C4 Diagram

```python
generate_from_template(
    template_name="c4_ecommerce_basic",
    variables={
        "system_name": "ShopNow E-commerce",
        "customer_label": "Online Shopper",
        "system_description": "Modern e-commerce platform",
        "payment_provider": "Stripe Payment Gateway",
        "email_provider": "SendGrid Email Service",
        "delivery_provider": "DHL Delivery Network"
    },
    output_path="output/ecommerce-c4.png",
    format="png"
)
```

**Result:** Beautiful C4 Context diagram in seconds! ✅

---

### Example 2: Microservices Architecture

```python
generate_from_template(
    template_name="c4_microservices_basic",
    variables={
        "system_name": "Order Management Platform",
        "user_label": "System Administrator",
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
    output_path="output/microservices-c4.png"
)
```

---

### Example 3: API Gateway Pattern

```python
generate_from_template(
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
    output_path="output/api-gateway-c4.svg",
    format="svg"
)
```

---

### Example 4: Authentication Flow (Mermaid Sequence)

```python
generate_from_template(
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
    output_path="output/auth-flow.png"
)
```

---

### Example 5: Approval Workflow (Flowchart)

```python
generate_from_template(
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
    output_path="output/approval-flow.png"
)
```

---

### Example 6: Project Timeline (Gantt)

```python
generate_from_template(
    template_name="mermaid_gantt_project",
    variables={
        "project_name": "Website Redesign Project",
        "date_format": "YYYY-MM-DD",
        "section1_name": "Planning",
        "task1_1_name": "Requirements gathering",
        "task1_1_status": "done",
        "task1_1_id": "t1",
        "task1_1_start": "2025-01-01",
        "task1_1_duration": "7d",
        "task1_2_name": "Design mockups",
        "task1_2_status": "done",
        "task1_2_id": "t2",
        "task1_2_start": "2025-01-08",
        "task1_2_duration": "10d",
        "task1_3_name": "Stakeholder approval",
        "task1_3_status": "active",
        "task1_3_id": "t3",
        "task1_3_start": "2025-01-18",
        "task1_3_duration": "3d",
        "section2_name": "Development",
        "task2_1_name": "Frontend development",
        "task2_1_status": "",
        "task2_1_id": "t4",
        "task2_1_start": "after t3",
        "task2_1_duration": "14d",
        "task2_2_name": "Backend API",
        "task2_2_status": "",
        "task2_2_id": "t5",
        "task2_2_start": "after t3",
        "task2_2_duration": "10d",
        "section3_name": "Deployment",
        "task3_1_name": "Testing",
        "task3_1_status": "",
        "task3_1_id": "t6",
        "task3_1_start": "after t4",
        "task3_1_duration": "5d",
        "task3_2_name": "Production deploy",
        "task3_2_status": "",
        "task3_2_id": "t7",
        "task3_2_start": "after t6",
        "task3_2_duration": "1d"
    },
    output_path="output/project-timeline.png"
)
```

---

### Example 7: Service Dependencies (Graphviz)

```python
generate_from_template(
    template_name="graphviz_services_deps",
    variables={
        "graph_name": "ServiceDependencies",
        "graph_title": "Microservices Dependency Graph",
        "rankdir": "LR",
        "node_shape": "ellipse",
        "service1_id": "api_gateway",
        "service1_label": "API Gateway",
        "service1_color": "lightblue",
        "service2_id": "auth_service",
        "service2_label": "Auth Service",
        "service2_color": "lightgreen",
        "service3_id": "user_service",
        "service3_label": "User Service",
        "service3_color": "lightgreen",
        "service4_id": "product_service",
        "service4_label": "Product Service",
        "service4_color": "lightgreen",
        "service5_id": "order_service",
        "service5_label": "Order Service",
        "service5_color": "lightgreen",
        "external1_id": "payment_api",
        "external1_label": "Payment API (Stripe)",
        "external2_id": "email_api",
        "external2_label": "Email API (SendGrid)",
        "external_color": "lightyellow",
        "dep1_label": "authenticate",
        "dep2_label": "route",
        "dep3_label": "get user",
        "dep4_label": "get products",
        "dep5_label": "create order",
        "dep6_label": "process payment",
        "dep7_label": "send email"
    },
    output_path="output/service-deps.svg",
    format="svg"
)
```

---

## 🎨 UML Domain Model Example

```python
generate_from_template(
    template_name="uml_domain_model",
    variables={
        "domain_name": "E-commerce Order Domain",
        "value_object1_name": "OrderId",
        "value_object1_type": "UUID",
        "value_object2_name": "Money",
        "value_object2_type": "Decimal",
        "aggregate_root": "Order",
        "id_type": "OrderId",
        "field1": "totalAmount",
        "field1_type": "Money",
        "field2": "status",
        "field2_type": "OrderStatus",
        "method1": "addItem(item: OrderItem)",
        "method2": "calculateTotal(): Money",
        "entity1_name": "OrderItem",
        "entity1_field1": "quantity",
        "entity1_field1_type": "int",
        "entity1_method1": "calculateSubtotal(): Money",
        "domain_service": "OrderPricingService",
        "service_method1": "calculateDiscount(order: Order): Money",
        "service_method2": "applyPromoCode(order: Order, code: string): void",
        "repository_interface": "OrderRepository"
    },
    output_path="output/domain-model.png"
)
```

---

## 💡 Tips & Best Practices

### 1. Start Simple
```python
# First, see what's available
list_templates()

# Then check what variables you need
get_template_info("c4_ecommerce_basic")

# Finally, generate!
generate_from_template(...)
```

### 2. Use Default Values for Optional Variables
```python
# If a variable is optional, you can skip it or use defaults
variables = {
    "system_name": "My System",
    "payment_provider": "Stripe",  # Required
    # Optional variables will use template defaults
}
```

### 3. Combine with Expert Mode
```python
# Use templates for standard parts
generate_from_template("c4_microservices_basic", {...})

# Use expert mode for custom details
generate_c4_diagram("component", custom_code, ...)
```

### 4. Export to Different Formats
```python
# PNG for presentations
generate_from_template(..., format="png")

# SVG for web/scalability
generate_from_template(..., format="svg")

# PDF for documentation
generate_from_template(..., format="pdf")
```

---

## 🆚 Template Mode vs Expert Mode

| Feature | Expert Mode | Template Mode |
|---------|-------------|---------------|
| **Ease of Use** | ⭐⭐⭐ Requires knowledge | ⭐⭐⭐⭐⭐ Just fill variables |
| **Speed** | ⭐⭐⭐ 5-10 minutes | ⭐⭐⭐⭐⭐ 30 seconds |
| **Flexibility** | ⭐⭐⭐⭐⭐ Full control | ⭐⭐⭐ Limited to template |
| **Code Amount** | 50-100 lines | 10-20 variables |
| **Learning Curve** | High | Low |
| **Best For** | Custom diagrams | Common patterns |

---

## 📚 Next Steps

1. **Explore all templates:** `list_templates()`
2. **Try a simple one:** Start with `c4_ecommerce_basic`
3. **Check variables:** `get_template_info("template_name")`
4. **Generate your first diagram:** `generate_from_template(...)`
5. **Customize:** Modify variables to match your system

---

## 🎯 When to Use Which Mode?

### Use **Expert Mode** when:
- ✅ You need custom, unique diagrams
- ✅ Template doesn't match your needs
- ✅ You know PlantUML/Mermaid well
- ✅ Maximum control required

### Use **Template Mode** when:
- ✅ Building common architectures (e-commerce, microservices, API gateway)
- ✅ Need quick prototypes
- ✅ Don't know PlantUML/Mermaid syntax
- ✅ Standardizing team documentation
- ✅ Want to save time! ⚡

---

**Happy templating!** 🎉

