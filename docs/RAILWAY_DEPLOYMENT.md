# Railway Deployment Guide / Przewodnik Wdrożenia na Railway

**Language / Język:** [English](#english) | [Polski](#polski)

---

<a name="english"></a>
# English

## Overview

This guide explains how to deploy the MCP Documentation Server to Railway platform.

> **⚠️ Important Note:** MCP servers communicate via stdio (stdin/stdout) protocol, not HTTP. Railway can run stdio-based services, but they won't have HTTP healthchecks. MCP servers are typically used locally where clients spawn them as child processes. Railway deployment is useful for specific use cases where you need the server running in the cloud.

## Prerequisites

- Railway account ([railway.app](https://railway.app))
- GitHub repository with your code
- Railway CLI (optional, but recommended)

## Step 1: Install Railway CLI

### Option A: Using npm (Recommended)

```bash
npm install -g @railway/cli
```

### Option B: Using Homebrew (macOS)

```bash
brew install railway
```

### Option C: Using Scoop (Windows)

```scoop
scoop bucket add railway https://github.com/railwayapp/homebrew-tap
scoop install railway
```

### Option D: Direct Download

Download from [Railway CLI Releases](https://github.com/railwayapp/cli/releases)

## Step 2: Login to Railway

```bash
railway login
```

This will open your browser to authenticate with Railway.

## Step 3: Create a New Project

### Option A: Using Railway Dashboard

1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will automatically detect `railway.toml` and start deployment

### Option B: Using Railway CLI

```bash
# Initialize Railway in your project directory
railway init

# Link to existing project or create new one
railway link
```

## Step 4: Configure Environment Variables (Optional)

If your server needs environment variables, set them in Railway:

### Using Railway Dashboard

1. Go to your project in Railway dashboard
2. Select your service
3. Go to "Variables" tab
4. Add variables as needed

### Using Railway CLI

```bash
railway variables set PLANTUML_SERVER=http://localhost:8080
railway variables set PYTHONPATH=/app
railway variables set PYTHONUNBUFFERED=1
```

## Step 5: Deploy

### Automatic Deployment (GitHub Integration)

1. Push your code to GitHub:
   ```bash
   git add .
   git commit -m "feat(deploy): configure Railway deployment"
   git push origin main
   ```

2. Railway will automatically:
   - Detect changes
   - Build Docker image using `Dockerfile`
   - Deploy using configuration from `railway.toml`
   - Start the server with `python src/server.py`

### Manual Deployment (CLI)

```bash
# Deploy current directory
railway up
```

## Step 6: Monitor Deployment

### View Logs

```bash
railway logs
```

### View Logs in Dashboard

1. Go to Railway dashboard
2. Select your project
3. Click on your service
4. View "Deployments" tab for build logs
5. View "Logs" tab for runtime logs

## Configuration File: `railway.toml`

Your `railway.toml` file configures how Railway builds and runs your app:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "python src/server.py"
# Note: healthcheckPath removed - MCP server uses stdio protocol, not HTTP
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Key Points:

- **`builder = "DOCKERFILE"`**: Railway uses your Dockerfile to build the image
- **`dockerfilePath = "Dockerfile"`**: Location of Dockerfile
- **`startCommand`**: Command to start the server (must match Dockerfile CMD)
- **No `healthcheckPath`**: Stdio servers don't have HTTP endpoints
- **`restartPolicyType`**: Restart behavior on failure

## Troubleshooting

### Build Fails

**Problem:** Docker build fails

**Solutions:**
- Check Dockerfile syntax
- Verify all dependencies in `requirements.txt`
- Check Railway build logs for specific errors
- Ensure Dockerfile is in project root

### Server Doesn't Start

**Problem:** Service shows as "crashed" or doesn't start

**Solutions:**
- Check logs: `railway logs`
- Verify `startCommand` matches Dockerfile CMD
- Ensure Python path is correct (`PYTHONPATH=/app`)
- Check that all required files are copied in Dockerfile

### Process Restarts Frequently

**Problem:** Service keeps restarting

**Solutions:**
- Check application logs for errors
- Verify all dependencies are installed
- Ensure output directory permissions: `RUN mkdir -p /app/output`
- Check if server is waiting for external services (e.g., PlantUML server)

### Stdio Communication Issues

**Problem:** MCP client can't communicate with Railway-deployed server

**Solutions:**
- Remember: MCP servers are typically used locally
- Railway deployment is for specific use cases
- Clients connecting to Railway need special configuration
- Consider using local deployment for standard MCP usage

## Understanding Stdio vs HTTP

### Stdio Protocol (MCP)

- Communication via stdin/stdout
- No HTTP endpoints
- No healthcheck endpoints
- Process-based monitoring
- Typical for local development

### HTTP Protocol (Web Apps)

- Communication via HTTP requests
- Healthcheck endpoints available
- URL-based access
- Typical for web services

**Our MCP server uses stdio**, so:
- ✅ Railway can run it (process-based)
- ❌ No HTTP healthchecks
- ❌ No direct HTTP access
- ✅ Process monitoring works

## Railway CLI Commands Reference

```bash
# Login
railway login

# Initialize project
railway init

# Link to project
railway link

# Deploy
railway up

# View logs
railway logs

# Set variables
railway variables set KEY=value

# List variables
railway variables

# Open dashboard
railway open

# Check status
railway status
```

## Next Steps

1. **Monitor your deployment** - Check logs regularly
2. **Set up custom domain** (optional) - Railway provides free subdomain
3. **Configure auto-deploy** - Already enabled with GitHub integration
4. **Set up alerts** - Configure notifications in Railway dashboard

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

<a name="polski"></a>
# Polski

## Przegląd

Ten przewodnik wyjaśnia, jak wdrożyć serwer MCP Documentation Server na platformę Railway.

> **⚠️ Ważna Uwaga:** Serwery MCP komunikują się przez protokół stdio (stdin/stdout), nie przez HTTP. Railway może uruchamiać serwisy oparte na stdio, ale nie będą miały HTTP healthchecków. Serwery MCP są zazwyczaj używane lokalnie, gdzie klienci uruchamiają je jako procesy potomne. Wdrożenie na Railway jest przydatne w specyficznych przypadkach, gdy potrzebujesz serwera działającego w chmurze.

## Wymagania Wstępne

- Konto Railway ([railway.app](https://railway.app))
- Repozytorium GitHub z kodem
- Railway CLI (opcjonalne, ale zalecane)

## Krok 1: Instalacja Railway CLI

### Opcja A: Używając npm (Zalecane)

```bash
npm install -g @railway/cli
```

### Opcja B: Używając Homebrew (macOS)

```bash
brew install railway
```

### Opcja C: Używając Scoop (Windows)

```scoop
scoop bucket add railway https://github.com/railwayapp/homebrew-tap
scoop install railway
```

### Opcja D: Bezpośrednie Pobranie

Pobierz z [Railway CLI Releases](https://github.com/railwayapp/cli/releases)

## Krok 2: Logowanie do Railway

```bash
railway login
```

To otworzy przeglądarkę do uwierzytelnienia z Railway.

## Krok 3: Utworzenie Nowego Projektu

### Opcja A: Używając Dashboard Railway

1. Przejdź do [railway.app](https://railway.app)
2. Kliknij "New Project"
3. Wybierz "Deploy from GitHub repo"
4. Wybierz swoje repozytorium
5. Railway automatycznie wykryje `railway.toml` i rozpocznie wdrożenie

### Opcja B: Używając Railway CLI

```bash
# Inicjalizacja Railway w katalogu projektu
railway init

# Połączenie z istniejącym projektem lub utworzenie nowego
railway link
```

## Krok 4: Konfiguracja Zmiennych Środowiskowych (Opcjonalne)

Jeśli serwer potrzebuje zmiennych środowiskowych, ustaw je w Railway:

### Używając Dashboard Railway

1. Przejdź do swojego projektu w dashboard Railway
2. Wybierz swój serwis
3. Przejdź do zakładki "Variables"
4. Dodaj zmienne według potrzeb

### Używając Railway CLI

```bash
railway variables set PLANTUML_SERVER=http://localhost:8080
railway variables set PYTHONPATH=/app
railway variables set PYTHONUNBUFFERED=1
```

## Krok 5: Wdrożenie

### Automatyczne Wdrożenie (Integracja GitHub)

1. Wypchnij kod do GitHub:
   ```bash
   git add .
   git commit -m "feat(deploy): configure Railway deployment"
   git push origin main
   ```

2. Railway automatycznie:
   - Wykryje zmiany
   - Zbuduje obraz Docker używając `Dockerfile`
   - Wdroży używając konfiguracji z `railway.toml`
   - Uruchomi serwer z `python src/server.py`

### Ręczne Wdrożenie (CLI)

```bash
# Wdróż bieżący katalog
railway up
```

## Krok 6: Monitorowanie Wdrożenia

### Przeglądanie Logów

```bash
railway logs
```

### Przeglądanie Logów w Dashboard

1. Przejdź do dashboard Railway
2. Wybierz swój projekt
3. Kliknij na swój serwis
4. Zobacz zakładkę "Deployments" dla logów budowania
5. Zobacz zakładkę "Logs" dla logów runtime

## Plik Konfiguracyjny: `railway.toml`

Plik `railway.toml` konfiguruje, jak Railway buduje i uruchamia aplikację:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "python src/server.py"
# Uwaga: healthcheckPath usunięty - serwer MCP używa protokołu stdio, nie HTTP
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Kluczowe Punkty:

- **`builder = "DOCKERFILE"`**: Railway używa Dockerfile do budowania obrazu
- **`dockerfilePath = "Dockerfile"`**: Lokalizacja Dockerfile
- **`startCommand`**: Komenda uruchomienia serwera (musi pasować do CMD w Dockerfile)
- **Brak `healthcheckPath`**: Serwery stdio nie mają endpointów HTTP
- **`restartPolicyType`**: Zachowanie restartu przy awarii

## Rozwiązywanie Problemów

### Błąd Budowania

**Problem:** Budowanie Docker nie powiodło się

**Rozwiązania:**
- Sprawdź składnię Dockerfile
- Zweryfikuj wszystkie zależności w `requirements.txt`
- Sprawdź logi budowania Railway dla konkretnych błędów
- Upewnij się, że Dockerfile jest w głównym katalogu projektu

### Serwer Nie Uruchamia Się

**Problem:** Serwis pokazuje się jako "crashed" lub nie uruchamia się

**Rozwiązania:**
- Sprawdź logi: `railway logs`
- Zweryfikuj, że `startCommand` pasuje do CMD w Dockerfile
- Upewnij się, że ścieżka Pythona jest poprawna (`PYTHONPATH=/app`)
- Sprawdź, czy wszystkie wymagane pliki są skopiowane w Dockerfile

### Proces Często Się Restartuje

**Problem:** Serwis ciągle się restartuje

**Rozwiązania:**
- Sprawdź logi aplikacji pod kątem błędów
- Zweryfikuj, czy wszystkie zależności są zainstalowane
- Upewnij się o uprawnieniach katalogu wyjściowego: `RUN mkdir -p /app/output`
- Sprawdź, czy serwer czeka na zewnętrzne serwisy (np. serwer PlantUML)

### Problemy z Komunikacją Stdio

**Problem:** Klient MCP nie może komunikować się z serwerem wdrożonym na Railway

**Rozwiązania:**
- Pamiętaj: serwery MCP są zazwyczaj używane lokalnie
- Wdrożenie na Railway jest dla specyficznych przypadków użycia
- Klienci łączący się z Railway potrzebują specjalnej konfiguracji
- Rozważ użycie lokalnego wdrożenia dla standardowego użycia MCP

## Zrozumienie Stdio vs HTTP

### Protokół Stdio (MCP)

- Komunikacja przez stdin/stdout
- Brak endpointów HTTP
- Brak endpointów healthcheck
- Monitorowanie oparte na procesach
- Typowe dla lokalnego rozwoju

### Protokół HTTP (Aplikacje Web)

- Komunikacja przez żądania HTTP
- Dostępne endpointy healthcheck
- Dostęp oparty na URL
- Typowe dla serwisów web

**Nasz serwer MCP używa stdio**, więc:
- ✅ Railway może go uruchomić (oparte na procesach)
- ❌ Brak HTTP healthchecków
- ❌ Brak bezpośredniego dostępu HTTP
- ✅ Monitorowanie procesów działa

## Referencja Komend Railway CLI

```bash
# Logowanie
railway login

# Inicjalizacja projektu
railway init

# Połączenie z projektem
railway link

# Wdrożenie
railway up

# Przeglądanie logów
railway logs

# Ustawianie zmiennych
railway variables set KEY=value

# Lista zmiennych
railway variables

# Otwarcie dashboard
railway open

# Sprawdzenie statusu
railway status
```

## Następne Kroki

1. **Monitoruj wdrożenie** - Sprawdzaj logi regularnie
2. **Skonfiguruj domenę niestandardową** (opcjonalne) - Railway zapewnia darmową subdomenę
3. **Skonfiguruj auto-wdrożenie** - Już włączone z integracją GitHub
4. **Skonfiguruj alerty** - Skonfiguruj powiadomienia w dashboard Railway

## Dodatkowe Zasoby

- [Dokumentacja Railway](https://docs.railway.app)
- [Referencja Railway CLI](https://docs.railway.app/develop/cli)
- [Najlepsze Praktyki Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

**Ostatnia aktualizacja:** 2025-01-24

