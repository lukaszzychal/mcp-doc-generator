# 🌿 Branch Structure / Struktura Branchy

## 📋 Overview / Przegląd

Ten projekt ma 3 główne branche z różnymi celami:

---

## 🌿 Branch: `main` (Wersja Podstawowa / Basic Version)

**Status:** ✅ Production Ready  
**Dla kogo:** Użytkownicy którzy chcą podstawowej funkcjonalności za darmo

### 🎯 Co zawiera:

**Expert Mode ONLY:**
- ✅ 11 MCP tools
- ✅ PlantUML (C4, UML, Sequence diagrams)
- ✅ Mermaid (Flowcharts, Sequence, Gantt)
- ✅ Graphviz (Dependency graphs)
- ✅ draw.io (Cloud diagrams)
- ✅ Export to PDF/DOCX (Pandoc)
- ✅ Polish language support
- ✅ Docker Compose setup
- ✅ Auto installer

### 💰 Cost:
- **$0** - Completely FREE!

### 📚 Use Case:
- Developers who know PlantUML/Mermaid syntax
- Teams that want full control over diagrams
- Projects with zero budget for AI tools
- Offline usage required

### 🚀 Quick Start:
```bash
git checkout main
./install.sh
docker compose up -d
```

---

## 🌿 Branch: `full-version` (Pełna Wersja / Complete Version)

**Status:** ✅ Production Ready  
**Dla kogo:** Użytkownicy którzy chcą maksymalną produktywność

### 🎯 Co zawiera:

**All 3 Modes:**
1. **Expert Mode** (11 tools) - Pełna kontrola
2. **Template Mode** (+3 tools) - 10 gotowych szablonów
3. **Smart Mode** (+2 tools) - AI-powered generation

**Total:** 16 MCP tools

### 💰 Cost:
- **Expert Mode:** $0
- **Template Mode:** $0 (FREE!)
- **Smart Mode:** ~$0.01-0.02 per diagram (opcjonalnie)

### 🎨 Features:
- ✅ Wszystko z `main` branch
- ✅ 10 pre-built templates (e-commerce, microservices, API gateway, etc.)
- ✅ AI-powered diagram generation (OpenAI integration)
- ✅ Natural language input
- ✅ 10x faster with templates (30 seconds vs 5 minutes)
- ✅ Auto template suggestions (save money!)

### 📚 Use Case:
- Teams that want productivity boost
- Non-technical users (Template/Smart Mode)
- Quick prototyping (Smart Mode)
- Standardized documentation (Template Mode)
- Budget available for AI ($1-2/month)

### 🚀 Quick Start:
```bash
git checkout full-version
./install.sh
docker compose up -d

# Optional: Set OpenAI API key for Smart Mode
export OPENAI_API_KEY='sk-...'
```

### 📖 Documentation:
- `TEMPLATE_MODE_IMPLEMENTED.md` - Template Mode guide
- `SMART_MODE_IMPLEMENTED.md` - Smart Mode guide
- `HYBRID_MODES_COMPLETE.md` - Complete overview
- `examples/template_mode_examples.md` - Examples

---

## 🌿 Branch: `docs-commercial` (Dokumentacja Biznesowa)

**Status:** 📚 Documentation Only  
**Dla kogo:** Twórcy projektu, marketing, komercjalizacja

### 🎯 Co zawiera:

**Dokumenty strategiczne:**
- `STRATEGIA_KOMERCJALIZACJI.md` - Strategia komercjalizacji
- `MARKETING_MONETIZATION_GUIDE.md` - Marketing & monetyzacja
- `ROADMAP.md` - Roadmap rozwoju projektu
- `articles/` - Artykuły do publikacji (Dev.to, Medium, etc.)

### 💡 Use Case:
- Planning project monetization
- Marketing materials
- Blog articles
- Business strategy
- Future roadmap

**Note:** Ten branch NIE zawiera kodu, tylko dokumentację biznesową.

---

## 🆚 Porównanie Branchy

| Feature | `main` | `full-version` | `docs-commercial` |
|---------|--------|----------------|-------------------|
| **Expert Mode** | ✅ (11 tools) | ✅ (11 tools) | ❌ No code |
| **Template Mode** | ❌ | ✅ (3 tools, 10 templates) | ❌ |
| **Smart Mode** | ❌ | ✅ (2 tools, OpenAI) | ❌ |
| **Total Tools** | 11 | 16 | N/A |
| **Cost** | $0 | $0-2/month | N/A |
| **Ease of Use** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | N/A |
| **Speed** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | N/A |
| **Learning Curve** | High | Low | N/A |
| **Best For** | Experts | Everyone | Business docs |

---

## 🔄 Jak Przełączać się Między Branchami

### Użyj wersji podstawowej (FREE):
```bash
git checkout main
git pull origin main
docker compose down
docker compose up -d
```

### Użyj pełnej wersji (Expert + Template + Smart):
```bash
git checkout full-version
git pull origin full-version
docker compose down
docker compose up -d
```

### Zobacz dokumenty biznesowe:
```bash
git checkout docs-commercial
# Nie uruchamiaj Docker - to tylko dokumenty!
```

---

## 🔒 Branch Protection

**Protected branches:**
- ✅ `main` - requires pull request reviews
- ✅ `full-version` - requires pull request reviews
- ✅ `docs-commercial` - requires pull request reviews

**Rules:**
- ❌ No direct pushes to protected branches
- ❌ No force push
- ❌ No deletion
- ✅ Require pull request with approvals
- ✅ Require status checks to pass

---

## 💡 Rekomendacje

### Dla użytkowników:
1. **Start with `main`** - see if basic version is enough (FREE!)
2. **Try `full-version`** - if you want productivity boost
3. **Choose based on needs:**
   - FREE + full control → `main`
   - FREE + easy + fast → `full-version` (use Template Mode)
   - AI magic + budget → `full-version` (use Smart Mode)

### Dla developerów:
1. **Fork from `full-version`** - najpełniejsza wersja
2. **Pull request to appropriate branch**
3. **Don't touch `docs-commercial`** unless you're updating business docs

---

## 📊 Statistics

| Metric | `main` | `full-version` |
|--------|--------|----------------|
| **Lines of Code** | ~2,500 | ~5,800 |
| **Files** | ~25 | ~45 |
| **MCP Tools** | 11 | 16 |
| **Templates** | 0 | 10 |
| **Documentation** | Basic | Comprehensive |

---

## ❓ FAQ

### Q: Który branch powinienem użyć?
**A:** 
- Jeśli jesteś ekspertem i chcesz za darmo → `main`
- Jeśli chcesz produktywności i łatwości → `full-version`

### Q: Czy mogę przejść z main na full-version później?
**A:** TAK! Po prostu:
```bash
git checkout full-version
docker compose down && docker compose up -d
```

### Q: Czy Smart Mode jest wymagany w full-version?
**A:** NIE! Smart Mode jest opcjonalny. Możesz używać tylko Expert + Template Mode (100% FREE).

### Q: Co jeśli nie mam budżetu na Smart Mode?
**A:** Użyj Template Mode - jest za darmo i 10x szybszy niż Expert Mode!

### Q: Czy main będzie aktualizowany?
**A:** TAK! Bugfixy i nowe features w Expert Mode będą dodawane do obu branchy.

---

## 🚀 Next Steps

1. **Choose your branch:** `main` or `full-version`
2. **Read the docs:** README.md in chosen branch
3. **Follow Quick Start**
4. **Start generating diagrams!**

---

**Ostatnia aktualizacja:** 24 Listopada 2025  
**Status:** ✅ All branches production ready

