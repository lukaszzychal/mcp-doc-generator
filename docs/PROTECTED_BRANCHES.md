# 🔒 Chronione Branche

## ⚠️ Ważne: Te branche są chronione!

Branche `docs-commercial` i `full-version` zostały usunięte z GitHub i są dostępne **tylko lokalnie**.

## 📌 Backup

Backup został utworzony jako tagi Git:

- **docs-commercial**: `backup/docs-commercial-20251126-014944`
- **full-version**: `backup/full-version-20251126-014944`

Tagi backup są dostępne na GitHub.

## 🔄 Przywracanie branchy (jeśli przypadkiem usuniesz lokalnie)

```bash
# Przywróć docs-commercial
git fetch origin
git checkout -b docs-commercial backup/docs-commercial-20251126-014944

# Przywróć full-version
git checkout -b full-version backup/full-version-20251126-014944
```

## 🛡️ Zabezpieczenia

- ✅ Branche są oznaczone w konfiguracji Git jako chronione
- ✅ Backup tagi są na GitHub
- ✅ Dokumentacja w `.git/protected-branches.txt`

## 📝 Status

- ❌ **GitHub**: Usunięte (niewidoczne dla innych użytkowników)
- ✅ **Lokalnie**: Dostępne i chronione
- ✅ **Backup**: Dostępny na GitHub jako tagi

---

**Data utworzenia backupu:** 2025-11-26 01:49:44

