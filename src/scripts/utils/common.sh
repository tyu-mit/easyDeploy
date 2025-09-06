#!/bin/bash
# Common utilities for easyDeploy scripts

set -euo pipefail

# Color codes for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" >&2
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" >&2
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if running as root
is_root() {
    [[ $EUID -eq 0 ]]
}

# Check if running on Ubuntu
is_ubuntu() {
    [[ -f /etc/os-release ]] && grep -q "ID=ubuntu" /etc/os-release
}

# Get Ubuntu version
get_ubuntu_version() {
    if is_ubuntu; then
        grep VERSION_ID /etc/os-release | cut -d'"' -f2
    else
        echo "unknown"
    fi
}

# Check if GPU is available
has_gpu() {
    command_exists nvidia-smi && nvidia-smi >/dev/null 2>&1
}

# Wait for package lock to be released
wait_for_apt_lock() {
    local timeout=300
    local elapsed=0

    while fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
        if [[ $elapsed -ge $timeout ]]; then
            log_error "Timeout waiting for apt lock to be released"
            return 1
        fi

        log_info "Waiting for apt lock to be released..."
        sleep 5
        elapsed=$((elapsed + 5))
    done
}

# Execute command with retry
retry() {
    local max_attempts=$1
    shift
    local attempt=1

    while [[ $attempt -le $max_attempts ]]; do
        if "$@"; then
            return 0
        fi

        log_warning "Attempt $attempt failed. Retrying in 5 seconds..."
        sleep 5
        attempt=$((attempt + 1))
    done

    log_error "All $max_attempts attempts failed"
    return 1
}

# Check required environment variables
check_env_vars() {
    local missing_vars=()

    for var in "$@"; do
        if [[ -z "${!var:-}" ]]; then
            missing_vars+=("$var")
        fi
    done

    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        log_error "Missing required environment variables: ${missing_vars[*]}"
        return 1
    fi
}

# Create directory with proper permissions
create_dir() {
    local dir=$1
    local owner=${2:-$(whoami)}
    local group=${3:-$(id -gn)}
    local mode=${4:-755}

    if [[ ! -d "$dir" ]]; then
        log_info "Creating directory: $dir"
        sudo mkdir -p "$dir"
        sudo chown "$owner:$group" "$dir"
        sudo chmod "$mode" "$dir"
    fi
}
