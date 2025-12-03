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

**Important:** If you already have a Railway project and service, connect GitHub repo to the existing service instead of creating a new one:

1. Go to [railway.app](https://railway.app)
2. Open your existing project (e.g., `mcp-doc-generator`)
3. Click on your service (e.g., `mcp-doc-generator`)
4. Go to "Settings" tab
5. Scroll to "GitHub" section
6. Click "Connect GitHub Repo"
7. Select your repository
8. Choose the branch (usually `main`)
9. Railway will automatically detect `railway.toml` and start deployment

**⚠️ Warning:** If you create a new project from GitHub UI, Railway may create a new service with a random name (e.g., `humble-abundance`). Always connect GitHub repo to your existing service to avoid duplicate services.

**For New Projects:**
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

### Automatic Deployment via GitHub Repo (Recommended)

Once you connect your GitHub repository to Railway, every push to the connected branch will automatically trigger a deployment.

#### How It Works

1. **Connect GitHub Repo** (one-time setup):
   - Go to your service in Railway dashboard
   - Settings → GitHub → Connect GitHub Repo
   - Select repository and branch (usually `main`)

2. **Automatic Deployments**:
   - Every `git push` to the connected branch triggers a new deployment
   - Railway automatically:
     - Detects changes
     - Builds Docker image using `Dockerfile`
     - Deploys using configuration from `railway.toml`
     - Starts the server with `python src/server.py`

3. **Deploy on Push**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin main
   # Railway automatically deploys! 🚀
   ```

#### Benefits of GitHub Integration

- ✅ **Automatic deployments** - No manual `railway up` needed
- ✅ **Deploy on every push** - Always up-to-date
- ✅ **Build logs in Railway** - Track deployment progress
- ✅ **Rollback support** - Easy to revert to previous versions
- ✅ **Branch deployments** - Can deploy different branches to different environments

#### Configure Branch Deployments

You can configure which branches trigger deployments:

1. Go to service Settings → GitHub
2. Configure branch settings:
   - **Production branch**: Usually `main` or `master`
   - **Auto-deploy**: Enable/disable automatic deployments
   - **Pull Request Deploys**: Deploy PRs to preview environments (optional)

### Manual Deployment (CLI)

If you prefer manual control or want to deploy without pushing to GitHub:

```bash
# Deploy current directory
railway up

# Deploy specific service
railway up --service mcp-doc-generator
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

### Multiple Services Created

**Problem:** Railway created multiple services (e.g., `humble-abundance` instead of `mcp-doc-generator`)

**Solutions:**
- Connect GitHub repo to existing service, don't create new project
- Go to your service → Settings → GitHub → Connect GitHub Repo
- Delete unwanted services from project settings
- Use `railway link-service <service-name>` to link to correct service

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

## Integration with Cursor AI

> **⚠️ Important:** Railway-deployed MCP servers are **not directly compatible** with Cursor AI integration. MCP servers use stdio (stdin/stdout) protocol, which requires a local process that Cursor can spawn. Railway deployments run in the cloud and don't expose stdio interfaces.

### Why Railway + Cursor is Challenging

- MCP servers communicate via stdio (stdin/stdout)
- Cursor needs to spawn server as local child process
- Railway-deployed processes don't expose stdio to external clients

### Workaround: Use Railway CLI with Cursor

You can use Railway CLI to run the server locally while using Railway's environment and configuration:

#### Step 1: Install and Configure Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link
```

#### Step 2: Configure Cursor

Add this configuration to Cursor MCP settings:

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "railway",
      "args": [
        "run",
        "python",
        "src/server.py"
      ],
      "env": {
        "RAILWAY_ENVIRONMENT": "production"
      }
    }
  }
}
```

**How it works:**
- `railway run` executes commands in Railway's environment
- Uses Railway's environment variables and configuration
- Runs locally but with Railway context
- Maintains stdio communication for Cursor

#### Step 3: Restart Cursor

After adding the configuration, restart Cursor to apply changes.

### Recommended Approach

**For Cursor integration:** Use local deployment (npx or Docker) - it's simpler and faster:

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.7"
      ]
    }
  }
}
```

**For Railway deployment:** Use for cloud hosting, API access, scheduled tasks, or team sharing.

See [CURSOR_NPX_SETUP.md](CURSOR_NPX_SETUP.md) for complete Cursor configuration guide.

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Reference](https://docs.railway.app/develop/cli)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [CURSOR_NPX_SETUP.md](CURSOR_NPX_SETUP.md) - Cursor AI integration guide

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

**Ważne:** Jeśli masz już projekt i serwis Railway, połącz repozytorium GitHub z istniejącym serwisem zamiast tworzyć nowy:

1. Przejdź do [railway.app](https://railway.app)
2. Otwórz swój istniejący projekt (np. `mcp-doc-generator`)
3. Kliknij na swój serwis (np. `mcp-doc-generator`)
4. Przejdź do zakładki "Settings"
5. Przewiń do sekcji "GitHub"
6. Kliknij "Connect GitHub Repo"
7. Wybierz swoje repozytorium
8. Wybierz branch (zwykle `main`)
9. Railway automatycznie wykryje `railway.toml` i rozpocznie wdrożenie

**⚠️ Ostrzeżenie:** Jeśli utworzysz nowy projekt z UI GitHub, Railway może utworzyć nowy serwis z losową nazwą (np. `humble-abundance`). Zawsze łącz repozytorium GitHub z istniejącym serwisem, aby uniknąć duplikatów serwisów.

**Dla Nowych Projektów:**
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

### Automatyczne Wdrożenie przez GitHub Repo (Zalecane)

Po połączeniu repozytorium GitHub z Railway, każdy push do połączonego brancha automatycznie uruchomi wdrożenie.

#### Jak To Działa

1. **Połącz GitHub Repo** (jednorazowa konfiguracja):
   - Przejdź do swojego serwisu w dashboard Railway
   - Settings → GitHub → Connect GitHub Repo
   - Wybierz repozytorium i branch (zwykle `main`)

2. **Automatyczne Wdrożenia**:
   - Każdy `git push` do połączonego brancha uruchamia nowe wdrożenie
   - Railway automatycznie:
     - Wykrywa zmiany
     - Buduje obraz Docker używając `Dockerfile`
     - Wdraża używając konfiguracji z `railway.toml`
     - Uruchamia serwer z `python src/server.py`

3. **Wdróż przez Push**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin main
   # Railway automatycznie wdraża! 🚀
   ```

#### Korzyści Integracji GitHub

- ✅ **Automatyczne wdrożenia** - Nie trzeba ręcznie używać `railway up`
- ✅ **Wdrożenie przy każdym pushu** - Zawsze aktualne
- ✅ **Logi buildów w Railway** - Śledź postęp wdrożenia
- ✅ **Wsparcie rollback** - Łatwe cofanie do poprzednich wersji
- ✅ **Wdrożenia branchy** - Możesz wdrażać różne branche do różnych środowisk

#### Konfiguracja Wdrożeń Branchy

Możesz skonfigurować, które branche uruchamiają wdrożenia:

1. Przejdź do Settings serwisu → GitHub
2. Skonfiguruj ustawienia branchy:
   - **Production branch**: Zwykle `main` lub `master`
   - **Auto-deploy**: Włącz/wyłącz automatyczne wdrożenia
   - **Pull Request Deploys**: Wdrażaj PR do środowisk preview (opcjonalne)

### Ręczne Wdrożenie (CLI)

Jeśli wolisz ręczną kontrolę lub chcesz wdrożyć bez pushowania do GitHub:

```bash
# Wdróż bieżący katalog
railway up

# Wdróż konkretny serwis
railway up --service mcp-doc-generator
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

### Utworzono Wiele Serwisów

**Problem:** Railway utworzył wiele serwisów (np. `humble-abundance` zamiast `mcp-doc-generator`)

**Rozwiązania:**
- Połącz repozytorium GitHub z istniejącym serwisem, nie twórz nowego projektu
- Przejdź do swojego serwisu → Settings → GitHub → Connect GitHub Repo
- Usuń niepotrzebne serwisy z ustawień projektu
- Użyj `railway link-service <service-name>` aby połączyć się z właściwym serwisem

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

## Integracja z Cursor AI

> **⚠️ Ważne:** Serwery MCP wdrożone na Railway **nie są bezpośrednio kompatybilne** z integracją Cursor AI. Serwery MCP używają protokołu stdio (stdin/stdout), co wymaga lokalnego procesu, który Cursor może uruchomić. Wdrożenia Railway działają w chmurze i nie udostępniają interfejsów stdio.

### Dlaczego Railway + Cursor Jest Wyzwaniem

- Serwery MCP komunikują się przez stdio (stdin/stdout)
- Cursor musi uruchomić serwer jako lokalny proces potomny
- Procesy wdrożone na Railway nie udostępniają stdio zewnętrznym klientom

### Obejście: Użyj Railway CLI z Cursor

Możesz użyć Railway CLI do uruchomienia serwera lokalnie, używając środowiska i konfiguracji Railway:

#### Krok 1: Zainstaluj i Skonfiguruj Railway CLI

```bash
# Zainstaluj Railway CLI
npm install -g @railway/cli

# Zaloguj się
railway login

# Połącz z projektem
railway link
```

#### Krok 2: Skonfiguruj Cursor

Dodaj tę konfigurację do ustawień MCP w Cursor:

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "railway",
      "args": [
        "run",
        "python",
        "src/server.py"
      ],
      "env": {
        "RAILWAY_ENVIRONMENT": "production"
      }
    }
  }
}
```

**Jak to działa:**
- `railway run` wykonuje komendy w środowisku Railway
- Używa zmiennych środowiskowych i konfiguracji Railway
- Działa lokalnie, ale z kontekstem Railway
- Utrzymuje komunikację stdio dla Cursor

#### Krok 3: Zrestartuj Cursor

Po dodaniu konfiguracji, zrestartuj Cursor aby zastosować zmiany.

### Zalecane Podejście

**Dla integracji Cursor:** Użyj lokalnego wdrożenia (npx lub Docker) - jest prostsze i szybsze:

```json
{
  "mcpServers": {
    "mcp-doc-generator": {
      "command": "npx",
      "args": [
        "github:lukaszzychal/mcp-doc-generator#v0.1.7"
      ]
    }
  }
}
```

**Dla wdrożenia Railway:** Użyj dla hostingu w chmurze, dostępu API, zaplanowanych zadań lub udostępniania zespołowi.

Zobacz [CURSOR_NPX_SETUP.md](CURSOR_NPX_SETUP.md) dla kompletnego przewodnika konfiguracji Cursor.

## Dodatkowe Zasoby

- [Dokumentacja Railway](https://docs.railway.app)
- [Referencja Railway CLI](https://docs.railway.app/develop/cli)
- [Najlepsze Praktyki Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [CURSOR_NPX_SETUP.md](CURSOR_NPX_SETUP.md) - Przewodnik integracji Cursor AI

---

**Ostatnia aktualizacja:** 2025-01-24

