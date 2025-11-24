#!/usr/bin/env python3
"""
Test naprawionych narzędzi: Mermaid i draw.io
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.mermaid import generate_flowchart, generate_sequence, generate_gantt
from tools.drawio import generate_diagram as generate_drawio_diagram


async def test_mermaid_flowchart():
    """Test Mermaid Flowchart"""
    print("\n1️⃣  Testing: Mermaid Flowchart (FIXED)")
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
    result = await generate_flowchart(content, "output/fixed_flowchart.png", "png")
    print(f"   {result}")


async def test_mermaid_sequence():
    """Test Mermaid Sequence"""
    print("\n2️⃣  Testing: Mermaid Sequence (FIXED)")
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
    result = await generate_sequence(content, "output/fixed_sequence.png", "png")
    print(f"   {result}")


async def test_mermaid_gantt():
    """Test Mermaid Gantt"""
    print("\n3️⃣  Testing: Mermaid Gantt (FIXED)")
    content = """
gantt
    title Harmonogram Projektu
    dateFormat YYYY-MM-DD
    
    section Faza 1
    Analiza       :a1, 2025-12-01, 7d
    Projektowanie :a2, after a1, 10d
    
    section Faza 2
    Backend       :b1, after a2, 21d
    Frontend      :b2, after a2, 21d
"""
    result = await generate_gantt(content, "output/fixed_gantt.png", "png")
    print(f"   {result}")


async def test_drawio():
    """Test draw.io (using online API)"""
    print("\n4️⃣  Testing: draw.io Cloud Diagram (FIXED)")
    content = """<mxfile host="app.diagrams.net">
  <diagram name="AWS Architecture" id="1">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <mxCell id="2" value="User" style="shape=actor;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="80" width="60" height="80" as="geometry"/>
        </mxCell>
        <mxCell id="3" value="AWS Cloud" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="200" y="40" width="400" height="200" as="geometry"/>
        </mxCell>
        <mxCell id="4" value="EC2 Instance" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
          <mxGeometry x="240" y="80" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="5" value="RDS Database" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;" vertex="1" parent="1">
          <mxGeometry x="440" y="80" width="120" height="60" as="geometry"/>
        </mxCell>
        <mxCell id="6" value="" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="2" target="4">
          <mxGeometry width="50" height="50" relative="1" as="geometry"/>
        </mxCell>
        <mxCell id="7" value="" style="endArrow=classic;html=1;exitX=1;exitY=0.5;entryX=0;entryY=0.5;" edge="1" parent="1" source="4" target="5">
          <mxGeometry width="50" height="50" relative="1" as="geometry"/>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""
    result = await generate_drawio_diagram(content, "output/fixed_cloud.png", "png")
    print(f"   {result}")


async def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🔧 TEST NAPRAWIONYCH NARZĘDZI (Mermaid + draw.io)")
    print("="*70)
    
    tests = [
        test_mermaid_flowchart,
        test_mermaid_sequence,
        test_mermaid_gantt,
        test_drawio,
    ]
    
    passed = 0
    failed = []
    
    for test in tests:
        try:
            await test()
            if "✓" in str(test):
                passed += 1
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            failed.append((test.__name__, str(e)))
    
    print("\n" + "="*70)
    print("📊 WYNIKI")
    print("="*70)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {len(failed)}/{len(tests)}")
    
    if failed:
        print("\n❌ Failed tests:")
        for name, error in failed:
            print(f"  - {name}: {error}")
    else:
        print("\n🎉 Wszystkie naprawione narzędzia działają!")
    
    print("\n📁 Wygenerowane pliki: output/fixed_*.png")
    print("="*70)


if __name__ == "__main__":
    asyncio.run(main())

