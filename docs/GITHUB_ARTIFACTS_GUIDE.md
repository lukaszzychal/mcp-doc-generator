# 📦 Gdzie znaleźć artefakty i obrazy Docker w GitHubie

Ten przewodnik wyjaśnia, gdzie można znaleźć zbudowane obrazy Docker i inne artefakty w GitHubie.

## 🐳 GitHub Container Registry (GHCR) - Obrazy Docker

Workflow `docker-build.yml` automatycznie buduje i publikuje obrazy Docker do **GitHub Container Registry**.

### Lokalizacja obrazów w GitHubie

#### Metoda 1: Przez stronę repozytorium (najłatwiejsza)

1. Przejdź do swojego repozytorium:
   ```
   https://github.com/[twoja-nazwa-uzytkownika]/MCPServer
   ```
   Przykład: `https://github.com/lukaszzychal/MCPServer`

2. W prawym górnym rogu strony repozytorium znajdziesz ikonę **"Packages"** (lub "Package" jeśli jest tylko jeden)
   - Kliknij na nią, aby zobaczyć wszystkie pakiety powiązane z repozytorium

3. Zobaczysz obraz: **`mcp-server`**
   - Kliknij na niego, aby zobaczyć szczegóły, wersje i tagi

#### Metoda 2: Przez bezpośredni link

Bezpośredni link do pakietu:
```
https://github.com/users/[twoja-nazwa-uzytkownika]/packages/container/mcp-server
```

#### Metoda 3: Przez profil użytkownika

1. Przejdź do swojego profilu GitHub
2. Kliknij na zakładkę **"Packages"**
3. Znajdź pakiet `mcp-server`

### Co zobaczysz w pakiecie

- **Wszystkie wersje obrazów** - zbudowane obrazy z różnymi tagami
- **Szczegóły obrazu** - rozmiar, architektury (amd64, arm64), data publikacji
- **Tagi** - np. `main`, `v0.1.2`, hash commita
- **Pull command** - komendę do pobrania obrazu:
  ```bash
  docker pull ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server:main
  ```

### Tagi obrazów

Zgodnie z konfiguracją workflow, obrazy są tagowane następująco:

- `main` - dla brancha main
- `v0.1.2` - dla tagów semver (jeśli istnieją)
- `v0.1` - dla major.minor
- `abc1234` - hash commita (krótki format)

## 🔄 GitHub Actions - Workflow Runs

### Lokalizacja uruchomień workflow

1. W repozytorium kliknij na zakładkę **"Actions"** (u góry strony)
2. Zobaczysz listę wszystkich uruchomień workflow
3. Kliknij na konkretne uruchomienie, aby zobaczyć:
   - **Logi** każdego kroku workflow
   - **Czas wykonania**
   - **Status** (sukces/błąd)
   - **Artifacts** (jeśli workflow je tworzy)

### Logi z budowania obrazu

W zakładce Actions możesz zobaczyć:
- Czy build się udał
- Jak długo trwało budowanie
- Pełne logi z Docker BuildKit
- Informacje o cache'u
- Digest zbudowanego obrazu (w kroku "Image digest")

## 📥 Jak pobrać obraz z GitHub Container Registry

### 1. Uwierzytelnienie

Najpierw musisz się zalogować do GitHub Container Registry:

```bash
# Login do GHCR
echo $GITHUB_TOKEN | docker login ghcr.io -u [twoja-nazwa-uzytkownika] --password-stdin
```

Lub jeśli masz Personal Access Token:
```bash
docker login ghcr.io -u [twoja-nazwa-uzytkownika] -p [twoj-token]
```

### 2. Pobranie obrazu

```bash
# Pobierz najnowszą wersję z brancha main
docker pull ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server:main

# Lub konkretną wersję
docker pull ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server:v0.1.2
```

### 3. Użycie obrazu

```bash
# Uruchom kontener
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/output:/app/output \
  ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server:main
```

## 🔍 Weryfikacja obrazów

### Sprawdzenie, które obrazy są dostępne

1. Przejdź do pakietu w GHCR
2. W sekcji "Versions" zobaczysz wszystkie opublikowane obrazy
3. Każdy obraz pokazuje:
   - Tag
   - Architektury (linux/amd64, linux/arm64)
   - Rozmiar
   - Datę publikacji

### Sprawdzenie przez Docker

```bash
# Lista wszystkich obrazów w repozytorium
docker images | grep ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server

# Szczegóły obrazu
docker inspect ghcr.io/[twoja-nazwa-uzytkownika]/mcp-server:main
```

## 🔐 Uprawnienia do pakietu

### Publiczne repozytorium

- Obrazy są **publiczne** jeśli repozytorium jest publiczne
- Możesz zmienić to w ustawieniach pakietu

### Prywatne repozytorium

- Obrazy są **prywatne** domyślnie
- Musisz nadać uprawnienia użytkownikom/organizacjom, które mają mieć dostęp

### Zmiana widoczności pakietu

1. Przejdź do pakietu w GHCR
2. Kliknij **"Package settings"**
3. Przewiń do sekcji **"Danger Zone"**
4. Wybierz **"Change visibility"**

## 📊 Monitoring i statystyki

W pakiecie możesz zobaczyć:
- Liczbę pobrań obrazu
- Historię publikacji
- Używane tagi

## 🆘 Rozwiązywanie problemów

### Obraz nie jest widoczny

1. Sprawdź, czy workflow się wykonało (zakładka Actions)
2. Sprawdź, czy build zakończył się sukcesem
3. Sprawdź, czy obraz został wypchnięty (nie jest to PR)

### Nie mogę pobrać obrazu

1. Sprawdź, czy jesteś zalogowany: `docker login ghcr.io`
2. Sprawdź uprawnienia do pakietu
3. Sprawdź, czy nazwa obrazu jest poprawna

### Nie widzę pakietu w repozytorium

1. Pakiet może być widoczny tylko dla właściciela
2. Sprawdź bezpośredni link do pakietu
3. Sprawdź ustawienia prywatności pakietu

## 🔗 Przydatne linki

- [GitHub Container Registry Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Action Documentation](https://github.com/docker/build-push-action)
- [Working with Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)

---

**Uwaga:** Nazwa pakietu w GHCR to: `ghcr.io/[username]/mcp-server` zgodnie z konfiguracją w `.github/workflows/docker-build.yml` (linia 51).

