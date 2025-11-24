# 📐 Diagram Templates Library

Pre-built, customizable diagram templates for common architecture patterns.

## 🎯 Template Mode vs Expert Mode

### Expert Mode (Current)
```python
# You write the full PlantUML/Mermaid code
generate_c4_diagram(
    diagram_type="context",
    content="""
    Person(user, "User")
    System(shop, "E-commerce")
    ...full code...
    """,
    output_path="output/c4.png"
)
```

### Template Mode (NEW)
```python
# You just fill in the blanks
generate_from_template(
    template_name="ecommerce_basic",
    variables={
        "system_name": "My Shop",
        "payment_provider": "Stripe"
    },
    output_path="output/c4.png"
)
```

---

## 📁 Available Templates

### C4 Architecture Templates
- `ecommerce_basic.puml` - Basic e-commerce with payment gateway
- `microservices_basic.puml` - Microservices architecture
- `api_gateway.puml` - API Gateway pattern
- `event_driven.puml` - Event-driven architecture

### UML Templates
- `class_diagram_basic.puml` - Basic class relationships
- `domain_model.puml` - DDD domain model

### Mermaid Templates
- `flowchart_approval.mmd` - Approval workflow
- `sequence_auth.mmd` - Authentication flow
- `gantt_project.mmd` - Project timeline

### Graphviz Templates
- `dependency_graph_services.dot` - Microservices dependencies
- `dependency_graph_modules.dot` - Module dependencies

---

## 🔧 Template Variables

Each template supports variables in format: `{{variable_name}}`

Example:
```
Person(user, "{{user_label}}")
System(main, "{{system_name}}")
System_Ext(ext, "{{external_system}}")
```

### Common Variables:
- `{{system_name}}` - Main system name
- `{{user_label}}` - User/actor name
- `{{external_system}}` - External service name
- `{{description}}` - Description text
- `{{version}}` - Version number

---

## 📖 Usage Examples

See `examples/template_usage.md` for detailed examples.

