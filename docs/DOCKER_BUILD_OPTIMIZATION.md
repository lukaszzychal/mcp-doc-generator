# Optymalizacja budowy obrazów Dockera

## Przegląd

Ten dokument opisuje strategię optymalizacji budowy obrazów Dockera w projekcie MCP Documentation Server. Implementacja obejmuje inteligentne wykrywanie zmian, cache'owanie warstw BuildKit oraz automatyczne pomijanie niepotrzebnych buildów.

## Strategia cache'owania

### 1. Cache mounts dla pip i npm

Dockerfile wykorzystuje cache mounts dla pip i npm, co pozwala na:
- **Szybsze rebuildy** - pakiety są cache'owane między buildami
- **Mniejsze obrazy** - cache nie jest częścią warstw obrazu
- **Oszczędność transferu** - tylko nowe pakiety są pobierane

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

RUN --mount=type=cache,target=/root/.npm \
    npm install -g @mermaid-js/mermaid-cli
```

### 2. Wykrywanie zmian w plikach

Skrypt `scripts/docker-build.sh` monitoruje zmiany w:
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`

Hash'y plików są przechowywane w `.docker-cache/file-hashes.txt` i porównywane przy każdym buildzie.

### 3. BuildKit cache

BuildKit automatycznie cache'uje warstwy obrazu:
- **Lokalnie:** Cache w lokalnym systemie plików
- **CI/CD:** Cache jako GitHub Actions artifacts (GHA cache)

## Użycie

### Lokalne budowanie

#### Automatyczne (zalecane)

```bash
# Używa inteligentnego wykrywania zmian
./scripts/docker-build.sh
```

Skrypt automatycznie:
- Sprawdza zmiany w monitorowanych plikach
- Buduje tylko gdy potrzeba
- Pomija build jeśli nic się nie zmieniło

#### Wymuszenie budowy

```bash
# Zawsze buduje, nawet bez zmian
./scripts/docker-build.sh --force
```

#### Standardowe budowanie

```bash
# Tradycyjne podejście (zawsze buduje)
docker compose build
```

### Integracja z install.sh

Skrypt `install.sh` automatycznie używa `docker-build.sh` jeśli jest dostępny:

```bash
./scripts/install.sh
```

## CI/CD (GitHub Actions)

Workflow `.github/workflows/docker-build.yml` automatycznie:
- Wykrywa zmiany w plikach Docker
- Używa GitHub Actions cache dla warstw BuildKit
- Pushuje obrazy do GitHub Container Registry (tylko dla push, nie dla PR)

### Konfiguracja

Workflow jest automatycznie uruchamiany gdy:
- Push do `main` lub `develop` z zmianami w:
  - `Dockerfile`
  - `docker-compose.yml`
  - `requirements.txt`
  - `src/**`
- Pull Request do `main` lub `develop` z podobnymi zmianami
- Ręczne uruchomienie (`workflow_dispatch`)

## Oszczędności zasobów

### Czas budowy

| Scenariusz | Bez optymalizacji | Z optymalizacją | Oszczędność |
|------------|-------------------|-----------------|-------------|
| Zmiana tylko w `src/` | 6-12 min | 5-10s | ~99% |
| Zmiana w `requirements.txt` | 6-12 min | 1-2 min | ~80-85% |
| Zmiana w `Dockerfile` | 6-12 min | 5-10 min | ~10-20% |
| Brak zmian | 6-12 min | 0s | 100% |

### Transfer danych

- **Lokalnie (z cache):** ~10-50MB zamiast ~1-2GB (95% oszczędności)
- **CI/CD (z cache):** ~50-200MB zamiast ~1-2GB (90% oszczędności)

### Rozmiar obrazu

**Standardowy obraz (Dockerfile):**
- Obraz końcowy: ~800MB-1.2GB
- Cache BuildKit: ~500MB-1GB (współdzielony, automatycznie zarządzany)
- Cache mounts: ~200-400MB (współdzielony między buildami)

**Distroless obraz (Dockerfile.distroless):**
- Obraz końcowy: ~500-700MB (**~300-500MB mniej**)
- Cache BuildKit: ~500MB-1GB (współdzielony)
- Cache mounts: ~200-400MB (współdzielony)
- **Oszczędność rozmiaru:** 25-40% mniejszy obraz

## Struktura cache

```
.docker-cache/
├── file-hashes.txt          # Hash'y monitorowanych plików
└── changed-files.txt        # Lista zmienionych plików (tymczasowy)
```

Pliki cache są automatycznie tworzone i zarządzane przez skrypt.

## Troubleshooting

### Problem: Build zawsze się wykonuje mimo braku zmian

**Rozwiązanie:**
1. Sprawdź czy `.docker-cache/file-hashes.txt` istnieje
2. Sprawdź czy obrazy Dockera istnieją: `docker images`
3. Użyj `--force` aby wymusić rebuild i zaktualizować cache

### Problem: Cache nie działa w CI/CD

**Rozwiązanie:**
1. Upewnij się że workflow używa `cache-from: type=gha`
2. Sprawdź czy GitHub Actions ma dostęp do cache (wymaga uprawnień)
3. Pierwszy build zawsze będzie pełny - cache działa od drugiego builda

### Problem: Błędy BuildKit

**Rozwiązanie:**
1. Upewnij się że Docker wspiera BuildKit (Docker 18.09+)
2. Sprawdź zmienne środowiskowe: `DOCKER_BUILDKIT=1`
3. W docker-compose.yml upewnij się że BuildKit jest włączony

### Wyczyszczenie cache

```bash
# Usuń lokalny cache
rm -rf .docker-cache/

# Usuń cache BuildKit
docker builder prune

# Usuń wszystkie nieużywane obrazy
docker image prune -a
```

## Zaawansowane użycie

### Własne pliki do monitorowania

Edytuj `scripts/docker-build.sh` i dodaj pliki do tablicy `MONITORED_FILES`:

```bash
MONITORED_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
    "twoj-plik.txt"  # Dodaj tutaj
)
```

### Cache z Docker Registry

Aby użyć cache z Docker Registry (np. Docker Hub, GHCR):

```bash
# Build z cache z registry
docker buildx build \
  --cache-from type=registry,ref=ghcr.io/user/repo:cache \
  --cache-to type=registry,ref=ghcr.io/user/repo:cache,mode=max \
  -t image:tag .
```

### Multi-stage build z Distroless

Dla jeszcze większych oszczędności można użyć multi-stage build z Distroless. Projekt zawiera gotowy `Dockerfile.distroless`:

**Korzyści Distroless:**
- **Mniejszy obraz:** ~300-500MB mniej niż standardowy
- **Wyższe bezpieczeństwo:** Brak shell, minimalna powierzchnia ataku
- **Non-root user:** Domyślnie działa jako użytkownik `nonroot`
- **Szybsze uruchamianie:** Mniej do załadowania

**Użycie:**

```bash
# Build z Distroless
docker build -f Dockerfile.distroless -t mcp-server:distroless .

# Lub z docker-compose
docker compose -f docker-compose.distroless.yml build
docker compose -f docker-compose.distroless.yml up -d
```

**Uwagi:**
- Distroless nie ma shell, więc debugowanie jest trudniejsze
- Użyj `:debug` wariantu obrazu Distroless jeśli potrzebujesz shell do debugowania
- Wszystkie binarne (pandoc, graphviz, nodejs) i ich zależności są kopiowane z build stage

## Best practices

1. **Zawsze używaj `docker-build.sh`** zamiast bezpośredniego `docker compose build`
2. **Commit'uj `.docker-cache/`** do git (opcjonalnie) dla współdzielonego cache w zespole
3. **Regularnie czyść cache** jeśli zajmuje za dużo miejsca
4. **Monitoruj rozmiar cache** - BuildKit automatycznie zarządza, ale warto sprawdzać
5. **Używaj `--force`** tylko gdy potrzebujesz pełnego rebuilda

## Przyszłe ulepszenia

- [x] Multi-stage build z Distroless dla mniejszych obrazów
- [x] Integracja z Docker Registry dla współdzielonego cache w zespole (GHCR w ci.yml)
- [ ] Automatyczne czyszczenie starego cache
- [ ] Metryki i raportowanie oszczędności czasu/transferu
- [ ] Wsparcie dla innych systemów CI/CD (GitLab CI, Jenkins)
- [ ] Automatyczne testowanie obu wariantów (standardowy i Distroless)

## Referencje

- [Docker BuildKit documentation](https://docs.docker.com/build/buildkit/)
- [Docker cache mounts](https://docs.docker.com/build/cache/backends/)
- [GitHub Actions cache](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Distroless images](https://github.com/GoogleContainerTools/distroless)

