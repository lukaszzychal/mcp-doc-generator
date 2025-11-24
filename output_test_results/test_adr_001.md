# ADR-001: Wybór PostgreSQL jako głównej bazy danych

**Data:** 2025-11-24  
**Status:** Zaakceptowane  
**Autor:** Łukasz Żychal

## Kontekst

System e-commerce wymaga niezawodnej bazy danych do przechowywania danych o produktach, zamówieniach i użytkownikach.

## Decyzja

Wybraliśmy PostgreSQL jako główną bazę danych relacyjnych dla systemu.

## Konsekwencje

### Pozytywne

- Wsparcie ACID
- Zaawansowane typy danych (JSON, Array)
- Silna społeczność
- Dobra dokumentacja
- Bezpłatna licencja open-source

### Negatywne

- Wymaga więcej zasobów niż MySQL
- Bardziej złożona konfiguracja replikacji

## Alternatywy

- MySQL: prostszy, ale mniej funkcjonalny
- MongoDB: NoSQL, ale system wymaga transakcji ACID

## Odnośniki

{{references}}

---

## Metadata

- **ADR Number:** 001
- **Data utworzenia:** 2025-11-24
- **Ostatnia aktualizacja:** {{last_updated}}
- **Status:** Zaakceptowane
  - Draft (Projekt)
  - Proposed (Zaproponowana)
  - Accepted (Zaakceptowana)
  - Deprecated (Przestarzała)
  - Superseded (Zastąpiona)

