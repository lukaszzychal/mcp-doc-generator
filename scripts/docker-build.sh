#!/bin/bash
# Intelligent Docker build script with change detection
# Only rebuilds when Dockerfile, docker-compose.yml, or requirements.txt change

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CACHE_DIR=".docker-cache"
HASH_FILE="${CACHE_DIR}/file-hashes.txt"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Files to monitor for changes
MONITORED_FILES=(
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
)

# Function to print colored messages
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

# Function to calculate file hash
calculate_hash() {
    local file="$1"
    if [ -f "$file" ]; then
        if command -v sha256sum >/dev/null 2>&1; then
            sha256sum "$file" | cut -d' ' -f1
        elif command -v shasum >/dev/null 2>&1; then
            shasum -a 256 "$file" | cut -d' ' -f1
        else
            # Fallback to md5 if sha256 not available
            md5sum "$file" 2>/dev/null | cut -d' ' -f1 || echo "unknown"
        fi
    else
        echo "missing"
    fi
}

# Function to get stored hash for a file
get_stored_hash() {
    local file="$1"
    if [ -f "$HASH_FILE" ]; then
        grep "^${file}:" "$HASH_FILE" | cut -d':' -f2 | tr -d ' '
    else
        echo ""
    fi
}

# Function to save hash for a file
save_hash() {
    local file="$1"
    local hash="$2"
    local temp_file=$(mktemp)
    
    if [ -f "$HASH_FILE" ]; then
        # Remove old entry if exists
        grep -v "^${file}:" "$HASH_FILE" > "$temp_file" || true
        mv "$temp_file" "$HASH_FILE"
    else
        touch "$HASH_FILE"
    fi
    
    # Add new entry
    echo "${file}:${hash}" >> "$HASH_FILE"
}

# Function to check if build is needed
check_build_needed() {
    local needs_build=false
    local changed_files=()
    
    # Create cache directory if it doesn't exist
    mkdir -p "$CACHE_DIR"
    
    print_info "Checking for changes in monitored files..."
    
    for file in "${MONITORED_FILES[@]}"; do
        local file_path="${PROJECT_ROOT}/${file}"
        local current_hash=$(calculate_hash "$file_path")
        local stored_hash=$(get_stored_hash "$file")
        
        if [ "$current_hash" != "$stored_hash" ]; then
            if [ -z "$stored_hash" ]; then
                print_info "  ${file}: new file (hash: ${current_hash:0:8}...)"
            else
                print_warning "  ${file}: changed (${stored_hash:0:8}... → ${current_hash:0:8}...)"
            fi
            needs_build=true
            changed_files+=("$file")
            save_hash "$file" "$current_hash"
        else
            print_success "  ${file}: unchanged"
        fi
    done
    
    # Check if Docker image exists
    local image_name="mcp-server"
    if ! docker images --format "{{.Repository}}" | grep -q "^${image_name}$" && \
       ! docker images --format "{{.Repository}}:{{.Tag}}" | grep -q "^${image_name}:"; then
        print_info "Docker image '${image_name}' not found"
        needs_build=true
        changed_files+=("image-missing")
    fi
    
    if [ "$needs_build" = true ]; then
        echo "true"
        echo "${changed_files[@]}" > "${CACHE_DIR}/changed-files.txt"
    else
        echo "false"
    fi
}

# Function to build Docker images
build_images() {
    local changed_files_content=""
    if [ -f "${CACHE_DIR}/changed-files.txt" ]; then
        changed_files_content=$(cat "${CACHE_DIR}/changed-files.txt")
    fi
    
    print_info "Building Docker images..."
    print_info "Changed files: ${changed_files_content:-all}"
    
    # Determine compose command
    local compose_cmd="docker compose"
    if ! docker compose version >/dev/null 2>&1; then
        compose_cmd="docker-compose"
    fi
    
    # Enable BuildKit for better caching
    export DOCKER_BUILDKIT=1
    export COMPOSE_DOCKER_CLI_BUILD=1
    
    # Build with BuildKit cache
    cd "$PROJECT_ROOT"
    if $compose_cmd build --progress=plain; then
        print_success "Docker images built successfully"
        return 0
    else
        print_error "Docker build failed"
        return 1
    fi
}

# Main function
main() {
    local force_build=false
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force|-f)
                force_build=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --force, -f    Force rebuild even if no changes detected"
                echo "  --help, -h     Show this help message"
                echo ""
                echo "This script intelligently builds Docker images only when:"
                echo "  - Dockerfile, docker-compose.yml, or requirements.txt change"
                echo "  - Docker image doesn't exist"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    cd "$PROJECT_ROOT"
    
    if [ "$force_build" = true ]; then
        print_info "Force build requested - rebuilding all images"
        build_images
    else
        local build_needed=$(check_build_needed)
        
        if [ "$build_needed" = "true" ]; then
            build_images
        else
            print_success "No changes detected - skipping build"
            print_info "Use --force to rebuild anyway"
            exit 0
        fi
    fi
}

# Run main function
main "$@"

