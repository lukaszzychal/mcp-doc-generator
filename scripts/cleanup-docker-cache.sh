#!/bin/bash
# Script to clean up old Docker cache locally
# Usage: ./scripts/cleanup-docker-cache.sh [--dry-run] [--aggressive]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

DRY_RUN=false
AGGRESSIVE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --aggressive)
      AGGRESSIVE=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --dry-run      Show what would be deleted without actually deleting"
      echo "  --aggressive   More aggressive cleanup (removes all unused resources)"
      echo "  --help, -h     Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

echo "================================================"
echo "  Docker Cache Cleanup"
echo "================================================"
echo ""

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY RUN MODE - Nothing will be deleted"
    echo ""
fi

# Check Docker
if ! command -v docker >/dev/null 2>&1; then
    print_error "Docker not found. Please install Docker first."
    exit 1
fi

# Get disk usage before cleanup
print_info "Checking current disk usage..."
BEFORE_SIZE=$(docker system df --format "{{.Size}}" | head -n1)
print_info "Current Docker disk usage: $BEFORE_SIZE"
echo ""

# Cleanup local .docker-cache directory
if [ -d ".docker-cache" ]; then
    print_info "Cleaning local .docker-cache directory..."
    if [ "$DRY_RUN" = true ]; then
        print_info "Would remove: .docker-cache/"
    else
        rm -rf .docker-cache/
        print_success "Removed .docker-cache/"
    fi
    echo ""
fi

# Cleanup BuildKit cache
print_info "Cleaning BuildKit cache..."
if [ "$DRY_RUN" = true ]; then
    print_info "Would run: docker builder prune -f"
else
    docker builder prune -f
    print_success "BuildKit cache cleaned"
fi
echo ""

# Cleanup unused images
print_info "Cleaning unused Docker images..."
if [ "$DRY_RUN" = true ]; then
    print_info "Would run: docker image prune -a -f"
else
    docker image prune -a -f
    print_success "Unused images cleaned"
fi
echo ""

# Cleanup stopped containers
print_info "Cleaning stopped containers..."
if [ "$DRY_RUN" = true ]; then
    print_info "Would run: docker container prune -f"
else
    docker container prune -f
    print_success "Stopped containers cleaned"
fi
echo ""

# Cleanup unused volumes
print_info "Cleaning unused volumes..."
if [ "$DRY_RUN" = true ]; then
    print_info "Would run: docker volume prune -f"
else
    docker volume prune -f
    print_success "Unused volumes cleaned"
fi
echo ""

# Aggressive cleanup
if [ "$AGGRESSIVE" = true ]; then
    print_warning "Running aggressive cleanup..."
    
    if [ "$DRY_RUN" = true ]; then
        print_info "Would run: docker system prune -a --volumes -f"
    else
        read -p "This will remove ALL unused Docker resources. Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker system prune -a --volumes -f
            print_success "Aggressive cleanup completed"
        else
            print_info "Aggressive cleanup cancelled"
        fi
    fi
    echo ""
fi

# Get disk usage after cleanup
if [ "$DRY_RUN" = false ]; then
    print_info "Checking disk usage after cleanup..."
    AFTER_SIZE=$(docker system df --format "{{.Size}}" | head -n1)
    print_info "Docker disk usage after cleanup: $AFTER_SIZE"
    echo ""
    
    print_success "Cleanup completed!"
else
    print_info "Dry run completed. Use without --dry-run to actually clean."
fi

echo ""
echo "================================================"

