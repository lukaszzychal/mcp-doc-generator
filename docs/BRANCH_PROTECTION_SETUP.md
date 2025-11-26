# 🔒 Branch Protection Setup

## ✅ Co Zostało Zrobione

### 3 Branche Utworzone:

1. **`main`** - Wersja podstawowa (Expert Mode, 11 tools)
2. **`full-version`** - Pełna wersja (16 tools: Expert + Template + Smart)
3. **`docs-commercial`** - Dokumenty biznesowe (tylko docs, bez kodu)

---

## 🔒 Branch Protection - Instrukcje Manualne

**⚠️ UWAGA:** Branch protection rules muszą być ustawione przez właściciela repo na GitHub.

### Krok po kroku:

1. **Przejdź do GitHub:**
   ```
   https://github.com/lukaszzychal/mcp-doc-generator/settings/branches
   ```

2. **Dodaj rule dla `main`:**
   - Click "Add rule"
   - Branch name pattern: `main`
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass
   - ✅ Do not allow bypassing the above settings
   - ✅ Restrict who can push to matching branches
   - ✅ Do not allow deletions
   - ✅ Do not allow force pushes
   - Click "Create"

3. **Dodaj rule dla `full-version`:**
   - Click "Add rule"
   - Branch name pattern: `full-version`
   - (Same settings as main)
   - Click "Create"

4. **Dodaj rule dla `docs-commercial`:**
   - Click "Add rule"
   - Branch name pattern: `docs-commercial`
   - (Same settings as main)
   - Click "Create"

---

## 🔒 Alternatywa: GitHub CLI

Jeśli masz `gh` CLI zainstalowane:

```bash
# Protect main branch
gh api repos/lukaszzychal/mcp-doc-generator/branches/main/protection \
  -X PUT \
  -F required_status_checks='{"strict":true,"contexts":[]}' \
  -F enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}' \
  -F restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false

# Protect full-version branch
gh api repos/lukaszzychal/mcp-doc-generator/branches/full-version/protection \
  -X PUT \
  -F required_status_checks='{"strict":true,"contexts":[]}' \
  -F enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}' \
  -F restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false

# Protect docs-commercial branch  
gh api repos/lukaszzychal/mcp-doc-generator/branches/docs-commercial/protection \
  -X PUT \
  -F required_status_checks='{"strict":true,"contexts":[]}' \
  -F enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}' \
  -F restrictions=null \
  -F allow_force_pushes=false \
  -F allow_deletions=false
```

---

## 📋 Protection Rules Summary

| Rule | main | full-version | docs-commercial |
|------|------|--------------|-----------------|
| **Require PR** | ✅ | ✅ | ✅ |
| **Require reviews** | ✅ (1) | ✅ (1) | ✅ (1) |
| **Require status checks** | ✅ | ✅ | ✅ |
| **Block force push** | ✅ | ✅ | ✅ |
| **Block deletion** | ✅ | ✅ | ✅ |
| **Enforce for admins** | ✅ | ✅ | ✅ |

---

## 🔄 Workflow After Protection

### Making Changes:

1. **Create feature branch:**
   ```bash
   git checkout main  # or full-version
   git pull
   git checkout -b feature/my-feature
   ```

2. **Make changes and commit:**
   ```bash
   # Edit files
   git add .
   git commit -m "feat: Add new feature"
   git push origin feature/my-feature
   ```

3. **Create Pull Request:**
   - Go to GitHub
   - Click "Compare & pull request"
   - Select base branch (main or full-version)
   - Add description
   - Request review
   - Wait for approval
   - Merge

### Emergency Hotfix:

If you MUST push directly (not recommended):
1. Temporarily disable branch protection
2. Push fix
3. Re-enable protection immediately

**Better:** Create hotfix branch and fast-track PR review.

---

## ✅ Verification

Po ustawieniu protection, sprawdź:

```bash
# Try to push to protected branch (should fail)
git checkout main
echo "test" >> test.txt
git add test.txt
git commit -m "test"
git push origin main
# Expected: Error - protected branch

# Clean up
git reset --hard HEAD~1
```

---

## 📊 Benefits of Branch Protection

| Benefit | Description |
|---------|-------------|
| **Quality** | Every change reviewed before merge |
| **Safety** | No accidental force push/delete |
| **History** | Clean, reviewable commit history |
| **Collaboration** | Team can review and approve |
| **Documentation** | PRs document why changes made |

---

## 🚨 Common Issues

### Issue 1: Can't push even though I'm owner
**Solution:** Branch protection applies to everyone, including owners. Create PR.

### Issue 2: Status checks required but none defined
**Solution:** In branch protection settings, uncheck "Require status checks" or add CI/CD.

### Issue 3: Need to force push for rebase
**Solution:** Don't force push to protected branches. Rebase on feature branch, then merge.

---

## 📝 Notes

- Protection rules stored on GitHub server
- Not in git repository
- Must be set by repo owner/admin
- Can be changed anytime (but shouldn't be!)

---

**Date:** 24 Listopada 2025 (zaktualizowano: 2025-11-26)  
**Status:** ✅ **AKTYWNE** - Branch protection włączone dla `main`  
**Priority:** ✅ COMPLETED

## ✅ Aktualny Status (2025-11-26)

Branch protection zostało **pomyślnie włączone i zweryfikowane** dla gałęzi `main`:

- ✅ **Require pull request reviews** - Wymagana 1 recenzja przed merge (ZWERYFIKOWANE)
- ✅ **Enforce for admins** - Dotyczy również właściciela repo (ZWERYFIKOWANE)
- ✅ **Block force pushes** - Zabronione force push (ZWERYFIKOWANE)
- ✅ **Block deletions** - Zabronione usuwanie brancha (ZWERYFIKOWANE)
- ✅ **Dismiss stale reviews** - Automatyczne odrzucanie przestarzałych recenzji (ZWERYFIKOWANE)

**Ważne:** Teraz nawet Ty (właściciel) musisz tworzyć Pull Requesty do `main`!

**Weryfikacja:** Status został zweryfikowany przez GitHub API - wszystkie zabezpieczenia są aktywne.

