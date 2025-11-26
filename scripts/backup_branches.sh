#!/bin/bash
# Backup ważnych branchy przed usunięciem z GitHub
# Użycie: ./scripts/backup_branches.sh

set -e

REPO_DIR="/Users/lukaszzychal/PhpstormProjects/MCPServer"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

cd "$REPO_DIR"

echo "🔄 Tworzenie backupu branchy..."
echo ""

# Sprawdź czy branche istnieją lokalnie
if ! git show-ref --verify --quiet refs/heads/docs-commercial; then
    echo "⚠️  Branch docs-commercial nie istnieje lokalnie!"
    exit 1
fi

if ! git show-ref --verify --quiet refs/heads/full-version; then
    echo "⚠️  Branch full-version nie istnieje lokalnie!"
    exit 1
fi

# Utwórz tagi backup
echo "📌 Tworzenie tagów backup..."
git tag backup/docs-commercial-${TIMESTAMP} docs-commercial
git tag backup/full-version-${TIMESTAMP} full-version

echo "✅ Tagi backup utworzone:"
echo "   - backup/docs-commercial-${TIMESTAMP}"
echo "   - backup/full-version-${TIMESTAMP}"
echo ""

# Push tagi na GitHub (opcjonalnie, dla dodatkowego bezpieczeństwa)
read -p "Czy chcesz wypushować tagi backup na GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Wypychanie tagów na GitHub..."
    git push origin backup/docs-commercial-${TIMESTAMP}
    git push origin backup/full-version-${TIMESTAMP}
    echo "✅ Tagi backup wypushowane na GitHub"
else
    echo "⏭️  Pominięto push tagów (zostaną tylko lokalnie)"
fi

echo ""
echo "✅ Backup zakończony pomyślnie!"
echo ""
echo "📝 Aby przywrócić branche w przyszłości:"
echo "   git checkout -b docs-commercial backup/docs-commercial-${TIMESTAMP}"
echo "   git checkout -b full-version backup/full-version-${TIMESTAMP}"

