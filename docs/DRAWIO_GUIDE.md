# 📐 Jak Używać Plików draw.io

## ✅ Wygenerowany Plik

**Lokalizacja:** `output/full_aws_architecture.drawio`  
**Rozmiar:** 5.6 KB (96 linii)  
**Typ:** XML - natywny format draw.io

---

## 🎨 Co Zawiera Diagram AWS Architecture:

### Komponenty:
1. **Użytkownik** (Actor)
2. **AWS Cloud** (Container)
3. **CloudFront CDN** (Content Delivery)
4. **Application Load Balancer** (ALB)
5. **EC2 Instances** x2 (API Servers)
6. **RDS PostgreSQL** (Database)
7. **S3 Bucket** (Static Assets)
8. **ElastiCache Redis** (Cache)

### Połączenia:
- User → CloudFront (HTTPS)
- CloudFront → ALB
- ALB → EC2 Instances (Load balanced)
- EC2 → RDS (SQL queries)
- EC2 → ElastiCache (Caching)
- ALB → S3 (Static files)

---

## 📖 Jak Otworzyć i Wyeksportować:

### Metoda 1: draw.io Online (Najszybsza) ✅

1. Otwórz: https://app.diagrams.net/
2. Kliknij: **File → Open from... → Device**
3. Wybierz: `full_aws_architecture.drawio`
4. Edytuj diagram (opcjonalnie)
5. Eksportuj:
   - **File → Export as → PNG** (dla prezentacji)
   - **File → Export as → SVG** (dla dokumentacji)
   - **File → Export as → PDF** (dla druku)

### Metoda 2: draw.io Desktop ✅

1. Pobierz: https://github.com/jgraph/drawio-desktop/releases
2. Zainstaluj aplikację desktop
3. Otwórz plik `.drawio`
4. Eksportuj do PNG/SVG/PDF

### Metoda 3: draw.io CLI (Zaawansowana) 🔧

```bash
# Zainstaluj draw.io desktop z CLI
brew install --cask drawio  # macOS
# lub pobierz z GitHub releases

# Eksportuj z linii komend
drawio -x -f png -o output/architecture.png output/full_aws_architecture.drawio
drawio -x -f svg -o output/architecture.svg output/full_aws_architecture.drawio
drawio -x -f pdf -o output/architecture.pdf output/full_aws_architecture.drawio
```

### Metoda 4: VS Code Extension 🆕

1. Zainstaluj extension: **Draw.io Integration**
2. Otwórz plik `.drawio` bezpośrednio w VS Code
3. Edytuj i eksportuj

---

## 🔄 Jak Używać w MCP Server:

### Generowanie Diagramu:

```python
from tools.drawio import generate_diagram

# Przygotuj XML
content = """<mxfile host="app.diagrams.net">
  <diagram name="My Diagram">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        
        <!-- Twoje komponenty -->
        <mxCell id="server" value="API Server" 
                style="rounded=0;whiteSpace=wrap;html=1;" 
                vertex="1" parent="1">
          <mxGeometry x="100" y="100" width="120" height="60"/>
        </mxCell>
        
        <mxCell id="db" value="Database" 
                style="shape=cylinder3;whiteSpace=wrap;html=1;" 
                vertex="1" parent="1">
          <mxGeometry x="300" y="100" width="100" height="80"/>
        </mxCell>
        
        <!-- Połączenia -->
        <mxCell id="arrow" style="endArrow=classic;html=1;" 
                edge="1" parent="1" source="server" target="db">
          <mxGeometry width="50" height="50" relative="1"/>
        </mxCell>
        
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

# Wygeneruj plik
result = await generate_diagram(
    content=content,
    output_path="output/my_diagram.drawio",
    format="png"
)
```

---

## 🎨 Dostępne Style i Kształty:

### Podstawowe Kształty:
- `shape=actor` - Actor (użytkownik)
- `shape=cylinder3` - Cylinder (baza danych)
- `shape=ellipse` - Elipsa
- `rounded=1` - Zaokrąglony prostokąt
- `rounded=0` - Ostrokątny prostokąt

### Kolory AWS:
- **CloudFront/CDN**: `fillColor=#d5e8d4;strokeColor=#82b366`
- **Compute (EC2)**: `fillColor=#ffe6cc;strokeColor=#d79b00`
- **Database (RDS)**: `fillColor=#f8cecc;strokeColor=#b85450`
- **Storage (S3)**: `fillColor=#dae8fc;strokeColor=#6c8ebf`
- **Network (ALB)**: `fillColor=#e1d5e7;strokeColor=#9673a6`
- **Container**: `fillColor=#fff2cc;strokeColor=#d6b656`

### Strzałki:
```xml
<mxCell id="arrow1" value="HTTPS" 
        style="endArrow=classic;html=1;" 
        edge="1" parent="1" 
        source="source_id" 
        target="target_id">
  <mxGeometry width="50" height="50" relative="1"/>
</mxCell>
```

---

## 💡 Przykłady Użycia:

### 1. Cloud Architecture (AWS/Azure/GCP)
```
User → CloudFront → ALB → EC2 → RDS
                         ↓
                        S3
```

### 2. Microservices Architecture
```
API Gateway → [Service 1, Service 2, Service 3] → Database
                                    ↓
                                 Message Queue
```

### 3. Network Diagram
```
Internet → Firewall → Load Balancer → Web Servers → App Servers → DB
```

---

## 🚀 Integracja z AI (Przyszłość)

W przyszłości możemy dodać:

1. **AI-Generated Diagrams**: Opisz słownie → AI generuje draw.io XML
2. **Smart Layout**: Automatyczne rozmieszczenie komponentów
3. **Template Library**: Gotowe szablony dla różnych architektur
4. **Export Pipeline**: Automatyczny export do wszystkich formatów

---

## 📚 Przydatne Linki:

- **draw.io Online**: https://app.diagrams.net/
- **draw.io Desktop**: https://github.com/jgraph/drawio-desktop
- **draw.io Dokumentacja**: https://www.diagrams.net/doc/
- **draw.io XML Format**: https://jgraph.github.io/mxgraph/docs/js-api/files/model/mxGraphModel-js.html
- **AWS Architecture Icons**: https://aws.amazon.com/architecture/icons/

---

## ✅ Podsumowanie:

| Metoda | Szybkość | Trudność | Edycja | Eksport |
|--------|----------|----------|---------|---------|
| draw.io Online | ⚡ Instant | ⭐ Łatwa | ✅ Tak | PNG/SVG/PDF |
| draw.io Desktop | 🚀 Szybka | ⭐⭐ Średnia | ✅ Tak | Wszystkie |
| draw.io CLI | 🔧 Zaawansowana | ⭐⭐⭐ Trudna | ❌ Nie | Batch export |
| VS Code Extension | 💻 Wygodna | ⭐⭐ Średnia | ✅ Tak | Wbudowane |

**Rekomendacja:** Użyj **draw.io Online** dla szybkiego podglądu i exportu.

---

**Status:** ✅ Gotowe do użycia!  
**Plik:** `output/full_aws_architecture.drawio` (5.6 KB)

