# 🧠 Smart Analysis & AI-Assisted Generation - Future Enhancement

**Status:** 💭 PLANOWANE  
**Priorytet:** 🟡 MEDIUM  
**Effort:** 3-5 dni  
**Data:** 23 Listopada 2025

---

## 🎯 Problem

Obecnie:
- **Claude (LLM)** analizuje prompt użytkownika
- **Claude (LLM)** generuje kod PlantUML/Mermaid
- **MCP Server** tylko renderuje gotowy kod → obraz

**Brak:** MCP Server nie ma własnej inteligencji do analizy promptów.

---

## 💡 Rozwiązanie: Hybrid Approach

### Koncepcja

Dodać **DWA TRYBY** dla każdego narzędzia:

```
┌─────────────────────────────────────────────────────────────┐
│                    HYBRID APPROACH                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MODE 1: EXPERT                  MODE 2: SMART             │
│  ┌─────────────────────┐        ┌─────────────────────┐   │
│  │ User → Gotowy kod   │        │ User → Prompt       │   │
│  │ Claude → Kod        │        │ MCP → Analiza       │   │
│  │ MCP → Render        │        │ MCP → Kod           │   │
│  │                     │        │ MCP → Render        │   │
│  │ MAKSYMALNA KONTROLA │        │ SZYBKIE I ŁATWE     │   │
│  └─────────────────────┘        └─────────────────────┘   │
│                                                             │
│  Użytkownik wybiera który tryb chce użyć!                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Szczegółowe Porównanie Podejść

### Obecne (Status Quo)
```
USER: "Wygeneruj C4 dla e-commerce..."
  ↓
CLAUDE: Analizuje → Generuje kod PlantUML
  ↓
MCP: generate_c4_diagram(content="@startuml Person(user)...")
  ↓
PlantUML Server → PNG
```

**Zalety:**
- ✅ Działa natychmiast
- ✅ Claude jest bardzo dobry w generowaniu kodu
- ✅ Elastyczne - Claude dostosowuje się do każdego promptu

**Wady:**
- ❌ Zależy od Claude (nie działa z innymi LLM)
- ❌ Brak kontroli - nie wiemy jak Claude interpretuje
- ❌ Nie można używać standalone (poza Claude)

---

### Poziom 1: Rule-Based (Reguły + Szablony)

```python
# MCP Server z prostymi regułami
def analyze_prompt(prompt: str) -> dict:
    # Wykryj wzorce regex
    if "e-commerce" in prompt.lower():
        return {"template": "ecommerce"}
    if "microservices" in prompt.lower():
        return {"template": "microservices"}
    
    # Wyciągnij elementy
    elements = re.findall(r"z (\w+)", prompt)
    return {"elements": elements}
```

**Zalety:**
- ✅ Szybkie (milisekundy)
- ✅ Deterministyczne (zawsze ten sam wynik)
- ✅ Działa offline
- ✅ Zero kosztów

**Wady:**
- ❌ Bardzo ograniczone (tylko proste wzorce)
- ❌ Trudne w rozbudowie (każdy przypadek = nowa reguła)
- ❌ Nie radzi sobie ze złożonymi promptami
- ❌ Brak elastyczności

**Use Case:** Proste, powtarzalne scenariusze z predefined templates.

---

### Poziom 2: NLP-Based (Lokalny model AI)

```python
from transformers import pipeline

# Używa BERT, spaCy lub podobnych
nlp_ner = pipeline("ner", model="bert-base-polish")
nlp_classify = pipeline("text-classification")

def analyze_prompt(prompt: str) -> dict:
    # Named Entity Recognition
    entities = nlp_ner(prompt)
    # {"user", "e-commerce system", "payment gateway"}
    
    # Classification
    diagram_type = nlp_classify(prompt)
    # "c4_context"
    
    return build_structure(entities, diagram_type)
```

**Zalety:**
- ✅ Niezależne od zewnętrznych API
- ✅ Precyzyjne dla trenowanych scenariuszy
- ✅ Działa offline
- ✅ Darmowe (po instalacji modelu)

**Wady:**
- ❌ Wymaga pobierania/trenowania modeli (GB)
- ❌ Złożone w implementacji
- ❌ Wolniejsze niż reguły (sekundy)
- ❌ Ograniczone do języka polskiego (trzeba trenować)

**Use Case:** Produkcja z dużą ilością użytkowników, gdy koszt API jest problemem.

---

### Poziom 3: OpenAI API (Zewnętrzny LLM)

```python
import openai

async def analyze_prompt(prompt: str) -> dict:
    response = await openai.ChatCompletion.acreate(
        model="gpt-4",
        messages=[{
            "role": "system",
            "content": "Przeanalizuj prompt i zwróć strukturę diagramu C4 w JSON"
        }, {
            "role": "user",
            "content": prompt
        }]
    )
    return json.loads(response.content)
```

**Zalety:**
- ✅ Najlepsza jakość analizy
- ✅ Uniwersalne (rozumie wszystko)
- ✅ Łatwe w implementacji (kilka linii)
- ✅ Działa z dowolnym językiem

**Wady:**
- 💰 Koszt API ($0.01-0.03 per request)
- ⚠️ Wymaga internetu
- ⚠️ Wolniejsze (1-3 sekundy)
- ⚠️ Zależność od OpenAI

**Use Case:** Prototyping, B2B z budżetem, premium features.

---

## 🎯 HYBRID APPROACH - Szczegółowe Wyjaśnienie

### Idea

**Zamiast wybierać JEDEN z powyższych, oferujemy WSZYSTKIE!**

```
User może wybrać:
┌────────────────────────────────────────────────────────────┐
│ 1. EXPERT MODE (obecny)                                    │
│    generate_c4_diagram(content="@startuml...")             │
│    → Pełna kontrola, user pisze kod                        │
│                                                            │
│ 2. TEMPLATE MODE (Poziom 1)                               │
│    generate_c4_diagram_from_template(                      │
│        template="ecommerce",                               │
│        customize={"add_payment": true}                     │
│    )                                                       │
│    → Szybkie, z gotowych szablonów                         │
│                                                            │
│ 3. SMART MODE (Poziom 3 - OpenAI)                         │
│    generate_c4_diagram_smart(                              │
│        prompt="system e-commerce z użytkownikiem..."       │
│    )                                                       │
│    → AI analizuje i generuje automatycznie                 │
└────────────────────────────────────────────────────────────┘
```

### Dlaczego Hybrid?

| Scenario | Best Mode | Reason |
|----------|-----------|--------|
| **Zaawansowany użytkownik, potrzebuje precyzji** | EXPERT | Pełna kontrola nad kodem |
| **Powtarzalny diagram (np. daily reports)** | TEMPLATE | Szybkie, bez kosztów API |
| **Pierwszy raz, chce coś szybko** | SMART | AI pomaga, nie trzeba znać składni |
| **Offline, brak internetu** | EXPERT lub TEMPLATE | Bez zależności zewnętrznych |
| **Prototyping, eksperymentowanie** | SMART | Najszybsze iteracje |

---

## 📈 Przykład w Praktyce

### Scenariusz: Dokumentacja Microservices

**User:** "Chcę diagram zależności między moimi 5 microservices"

#### Tryb 1: EXPERT
```
User → pisze DOT code ręcznie
digraph {
  "API Gateway" -> "Auth Service"
  "API Gateway" -> "Order Service"
  ...
}
```
**Czas:** 5-10 minut  
**Kontrola:** 100%  
**Koszt:** $0

#### Tryb 2: TEMPLATE
```
generate_dependency_graph_from_template(
  template="microservices_5",
  services=["API Gateway", "Auth", "Order", "Payment", "Notification"]
)
```
**Czas:** 30 sekund  
**Kontrola:** 60%  
**Koszt:** $0

#### Tryb 3: SMART
```
generate_dependency_graph_smart(
  prompt="""
  5 microservices:
  - API Gateway (główny entry point)
  - Auth Service (autoryzacja)
  - Order Service (zamówienia, zależy od Auth i Payment)
  - Payment Service (płatności external)
  - Notification Service (emaile, SMS)
  """
)
```
**Czas:** 10 sekund  
**Kontrola:** 80%  
**Koszt:** $0.02

---

## 🚀 Plan Implementacji

### Faza A: Template Mode (1-2 dni)

```python
# src/tools/templates.py

TEMPLATES = {
    "ecommerce_c4": """
        Person(user, "Użytkownik")
        System(shop, "{{system_name}}")
        System_Ext(payment, "{{payment_provider}}")
        Rel(user, shop, "Przegląda produkty, składa zamówienia")
        Rel(shop, payment, "Przetwarza płatności", "HTTPS")
    """,
    "microservices_basic": """...""",
}

async def generate_from_template(
    tool_name: str,
    template_id: str,
    variables: dict,
    output_path: str
) -> str:
    template = TEMPLATES.get(f"{tool_name}_{template_id}")
    code = template.format(**variables)
    return await render(code, output_path)
```

**Nowe narzędzia MCP:**
- `generate_c4_diagram_from_template`
- `generate_flowchart_from_template`
- `generate_dependency_graph_from_template`

---

### Faza B: Smart Mode (1 dzień)

```python
# src/tools/smart_analyzer.py

import openai

async def generate_smart(
    tool_name: str,
    prompt: str,
    output_path: str,
    model: str = "gpt-4o-mini"  # Cheaper option
) -> str:
    # Analiza przez OpenAI
    analysis = await openai_analyze(tool_name, prompt, model)
    
    # Generowanie kodu
    code = generate_code_from_analysis(tool_name, analysis)
    
    # Rendering
    return await render(code, output_path)
```

**Nowe narzędzia MCP:**
- `generate_c4_diagram_smart`
- `generate_flowchart_smart`
- `generate_uml_diagram_smart`
- (wszystkie narzędzia mają wersję _smart)

**Konfiguracja:**
```bash
# .env
OPENAI_API_KEY=sk-...
SMART_MODE_MODEL=gpt-4o-mini  # lub gpt-4
SMART_MODE_ENABLED=true
```

---

### Faza C: UI/UX Improvements (1 dzień)

**Auto-detection:** MCP może automatycznie wybierać tryb

```python
async def generate_c4_diagram_auto(
    content_or_prompt: str,
    output_path: str
) -> str:
    """
    Automatycznie wykrywa czy to kod czy prompt.
    """
    if content_or_prompt.startswith("@startuml"):
        # To jest kod → EXPERT mode
        return await generate_c4_diagram(content_or_prompt, ...)
    
    elif content_or_prompt in TEMPLATES:
        # To jest ID template → TEMPLATE mode
        return await generate_from_template(...)
    
    else:
        # To jest naturalny prompt → SMART mode
        return await generate_smart(content_or_prompt, ...)
```

---

## 💰 Cost Analysis

### Dla 1000 diagramów/miesiąc

| Mode | Cost per diagram | Total Monthly |
|------|------------------|---------------|
| EXPERT | $0 | **$0** |
| TEMPLATE | $0 | **$0** |
| SMART (GPT-4o-mini) | $0.005 | **$5** |
| SMART (GPT-4) | $0.02 | **$20** |

**Hybrid:** Użytkownicy wybierają, średni koszt: **$2-8/miesiąc**

---

## ✅ Zalety Hybrid Approach

1. ✅ **Elastyczność** - każdy user wybiera co mu pasuje
2. ✅ **Zero lock-in** - nie jesteś zależny od jednej metody
3. ✅ **Optymalizacja kosztów** - używasz API tylko gdy potrzeba
4. ✅ **Stopniowa adopcja** - możesz zacząć od EXPERT, przejść na SMART
5. ✅ **Backward compatibility** - stare narzędzia działają bez zmian

---

## 🎯 Rekomendacja

**START:** Implement Faza A (Templates) + Faza B (Smart)

**Dlaczego:**
- Templates są darmowe i szybkie (1-2 dni work)
- Smart mode daje największą wartość (1 dzień work)
- Razem: **2-3 dni**, huge impact

**SKIP:** Poziom 2 (NLP-Based) - za dużo pracy, małe benefits

---

## 📝 TODO Items

- [ ] Zaimplementować system templates (TEMPLATES dict)
- [ ] Dodać `_from_template` variants dla każdego narzędzia
- [ ] Zintegrować OpenAI API dla smart mode
- [ ] Dodać `_smart` variants dla każdego narzędzia
- [ ] Stworzyć bibliotekę prompt templates dla OpenAI
- [ ] Dodać auto-detection mode
- [ ] Testy dla każdego trybu
- [ ] Dokumentacja użycia + przykłady
- [ ] Update README z opisem trybów

---

## 🔗 Related Documents

- `ROADMAP.md` - Plan rozszerzeń (Faza 4-6)
- `PROJECT_SUMMARY.md` - Obecny status
- `examples/example_usage.md` - Przykłady użycia

---

**Next Steps:** Zdecyduj czy chcesz to zaimplementować teraz czy później.

**Estimated Effort:** 2-3 dni (Template + Smart modes)  
**Impact:** 🔥🔥🔥 Very High - znacznie upraszcza użytkowanie!

