#!/bin/bash
# NVIDIA GPU driver and CUDA setup

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../utils/common.sh"

# Default versions
readonly CUDA_VERSION="${CUDA_VERSION:-12.0}"
readonly NVIDIA_DOCKER_VERSION="${NVIDIA_DOCKER_VERSION:-2.13.0-1}"

main() {
    log_info "Starting NVIDIA GPU setup"

    if ! has_gpu; then
        log_warning "No NVIDIA GPU detected. Skipping GPU setup."
        return 0
    fi

    # Install NVIDIA drivers
    install_nvidia_drivers

    # Install CUDA
    install_cuda

    # Install NVIDIA Docker
    install_nvidia_docker

    # Verify installation
    verify_installation

    log_success "NVIDIA GPU setup completed"
}

install_nvidia_drivers() {
    log_info "Installing NVIDIA drivers"

    # Add NVIDIA repository
    wget -qO - "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d .)/x86_64/3bf863cc.pub" | sudo apt-key add -
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu$(lsb_release -rs | tr -d .)/x86_64 /" | sudo tee /etc/apt/sources.list.d/cuda.list

    sudo apt-get update

    # Install recommended driver
    sudo apt-get install -y nvidia-driver-535

    log_info "NVIDIA drivers installed. Reboot may be required."
}

install_cuda() {
    log_info "Installing CUDA ${CUDA_VERSION}"

    local cuda_version_nodot
    cuda_version_nodot=$(echo "${CUDA_VERSION}" | tr -d '.')

    # Install CUDA toolkit
    sudo apt-get install -y "cuda-toolkit-${cuda_version_nodot}"

    # Add CUDA to PATH
    {
        echo "# CUDA paths"
        echo "export PATH=/usr/local/cuda-${CUDA_VERSION}/bin:\$PATH"
        echo "export LD_LIBRARY_PATH=/usr/local/cuda-${CUDA_VERSION}/lib64:\$LD_LIBRARY_PATH"
    } | sudo tee /etc/environment.d/cuda.conf

    # Source the environment
    export PATH="/usr/local/cuda-${CUDA_VERSION}/bin:$PATH"
    export LD_LIBRARY_PATH="/usr/local/cuda-${CUDA_VERSION}/lib64:$LD_LIBRARY_PATH"
}

install_nvidia_docker() {
    log_info "Installing NVIDIA Docker"

    # Add NVIDIA Docker repository
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
    curl -s -L "https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list" | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    sudo apt-get update
    sudo apt-get install -y "nvidia-docker2=${NVIDIA_DOCKER_VERSION}"

    # Restart Docker daemon
    sudo systemctl restart docker
}

verify_installation() {
    log_info "Verifying NVIDIA installation"

    # Check driver
    if nvidia-smi >/dev/null 2>&1; then
        log_success "NVIDIA driver verification passed"
        nvidia-smi
    else
        log_error "NVIDIA driver verification failed"
        return 1
    fi

    # Check CUDA
    if nvcc --version >/dev/null 2>&1; then
        log_success "CUDA verification passed"
        nvcc --version
    else
        log_warning "CUDA verification failed (may require reboot)"
    fi

    # Check NVIDIA Docker
    if command_exists docker && docker run --rm --gpus all nvidia/cuda:${CUDA_VERSION}-base-ubuntu20.04 nvidia-smi >/dev/null 2>&1; then
        log_success "NVIDIA Docker verification passed"
    else
        log_warning "NVIDIA Docker verification failed (may require reboot)"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
