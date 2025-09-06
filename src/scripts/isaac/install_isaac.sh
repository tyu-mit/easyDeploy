#!/bin/bash
# Isaac Sim installation script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../utils/common.sh"

# Default versions and settings
readonly ISAAC_VERSION="${ISAAC_VERSION:-2023.1.1}"
readonly NGC_API_KEY="${NGC_API_KEY:-}"
readonly INSTALL_ISAAC_LAB="${INSTALL_ISAAC_LAB:-true}"

main() {
    log_info "Starting Isaac Sim installation"

    # Check prerequisites
    check_prerequisites

    # Install Docker if not present
    install_docker

    # Setup NGC authentication
    setup_ngc_auth

    # Pull Isaac Sim container
    pull_isaac_container

    # Install Isaac Lab if requested
    if [[ "$INSTALL_ISAAC_LAB" == "true" ]]; then
        install_isaac_lab
    fi

    # Create desktop shortcuts
    create_desktop_shortcuts

    log_success "Isaac Sim installation completed"
}

check_prerequisites() {
    log_info "Checking prerequisites"

    if [[ -z "$NGC_API_KEY" ]]; then
        log_error "NGC_API_KEY environment variable is required"
        log_info "Please obtain an API key from https://ngc.nvidia.com/setup/api-key"
        return 1
    fi

    if ! has_gpu; then
        log_warning "No GPU detected. Isaac Sim may not work properly without GPU acceleration."
    fi
}

install_docker() {
    if command_exists docker; then
        log_info "Docker already installed"
        return 0
    fi

    log_info "Installing Docker"

    # Add Docker GPG key
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Add Docker repository
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Add user to docker group
    local user="${DEPLOY_USER:-ubuntu}"
    sudo usermod -aG docker "$user"

    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
}

setup_ngc_auth() {
    log_info "Setting up NGC authentication"

    local user="${DEPLOY_USER:-ubuntu}"

    # Login to NGC registry
    sudo -u "$user" docker login nvcr.io -u "\$oauthtoken" -p "$NGC_API_KEY"
}

pull_isaac_container() {
    log_info "Pulling Isaac Sim container (version ${ISAAC_VERSION})"

    local user="${DEPLOY_USER:-ubuntu}"
    local container_name="nvcr.io/nvidia/isaac-sim:${ISAAC_VERSION}"

    sudo -u "$user" docker pull "$container_name"

    # Tag as latest for convenience
    sudo -u "$user" docker tag "$container_name" "isaac-sim:latest"
}

install_isaac_lab() {
    log_info "Installing Isaac Lab"

    local user="${DEPLOY_USER:-ubuntu}"
    local isaac_lab_dir="/home/${user}/IsaacLab"

    # Clone Isaac Lab repository
    if [[ ! -d "$isaac_lab_dir" ]]; then
        sudo -u "$user" git clone https://github.com/isaac-sim/IsaacLab.git "$isaac_lab_dir"
    fi

    # Make install script executable
    chmod +x "${isaac_lab_dir}/isaaclab.sh"

    log_info "Isaac Lab cloned to ${isaac_lab_dir}"
    log_info "Run './isaaclab.sh --help' for usage instructions"
}

create_desktop_shortcuts() {
    log_info "Creating desktop shortcuts"

    local user="${DEPLOY_USER:-ubuntu}"
    local desktop_dir="/home/${user}/Desktop"
    local applications_dir="/home/${user}/.local/share/applications"

    create_dir "$desktop_dir" "$user" "$(id -gn $user)"
    create_dir "$applications_dir" "$user" "$(id -gn $user)"

    # Isaac Sim desktop shortcut
    cat > "${desktop_dir}/isaac-sim.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Isaac Sim
Comment=NVIDIA Isaac Sim
Exec=docker run --rm -it --gpus all -e DISPLAY=\$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix isaac-sim:latest
Icon=applications-science
Terminal=true
Categories=Development;Science;
EOF

    chmod +x "${desktop_dir}/isaac-sim.desktop"
    chown "${user}:$(id -gn $user)" "${desktop_dir}/isaac-sim.desktop"

    # Copy to applications directory
    cp "${desktop_dir}/isaac-sim.desktop" "$applications_dir/"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
