#!/bin/bash
# Base system setup for Ubuntu

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../utils/common.sh"

main() {
    log_info "Starting base system setup"

    # Update system
    log_info "Updating package lists"
    sudo apt-get update

    log_info "Upgrading system packages"
    sudo apt-get upgrade -y

    # Install essential packages
    log_info "Installing essential packages"
    sudo apt-get install -y \
        curl \
        wget \
        git \
        vim \
        htop \
        tree \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release \
        build-essential

    # Configure SSH (if custom port specified)
    if [[ "${SSH_PORT:-22}" != "22" ]]; then
        log_info "Configuring SSH port ${SSH_PORT}"
        configure_ssh_port "${SSH_PORT}"
    fi

    # Configure user
    configure_user

    log_success "Base system setup completed"
}

configure_ssh_port() {
    local port=$1

    log_info "Setting SSH port to ${port}"
    sudo sed -i "s/#Port 22/Port ${port}/" /etc/ssh/sshd_config
    sudo systemctl restart ssh

    # Configure UFW if installed
    if command -v ufw >/dev/null; then
        sudo ufw allow "${port}/tcp"
    fi
}

configure_user() {
    local user="${DEPLOY_USER:-ubuntu}"

    log_info "Configuring user ${user}"

    # Add user to docker group (if docker is installed)
    if getent group docker >/dev/null; then
        sudo usermod -aG docker "${user}"
    fi

    # Set up user directories
    sudo -u "${user}" mkdir -p "/home/${user}"/{bin,scripts,workspace}
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
