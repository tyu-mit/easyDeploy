#!/bin/bash
# ROS2 installation script

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/../utils/common.sh"

# Default ROS2 distribution
readonly ROS_DISTRO="${ROS_DISTRO:-humble}"

main() {
    log_info "Installing ROS2 ${ROS_DISTRO}"

    # Verify Ubuntu version compatibility
    check_ubuntu_compatibility

    # Add ROS2 repository
    add_ros2_repository

    # Install ROS2
    install_ros2_packages

    # Setup environment
    setup_ros2_environment

    # Install additional tools
    install_ros2_tools

    log_success "ROS2 ${ROS_DISTRO} installation completed"
}

check_ubuntu_compatibility() {
    local ubuntu_version
    ubuntu_version=$(get_ubuntu_version)

    case "${ROS_DISTRO}" in
        "humble")
            if [[ "$ubuntu_version" != "22.04" ]]; then
                log_warning "ROS2 Humble is officially supported on Ubuntu 22.04, but found ${ubuntu_version}"
            fi
            ;;
        "iron")
            if [[ "$ubuntu_version" != "22.04" ]]; then
                log_warning "ROS2 Iron is officially supported on Ubuntu 22.04, but found ${ubuntu_version}"
            fi
            ;;
        *)
            log_warning "Unknown ROS2 distribution: ${ROS_DISTRO}"
            ;;
    esac
}

add_ros2_repository() {
    log_info "Adding ROS2 repository"

    # Add ROS2 GPG key
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

    # Add repository to sources list
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

    # Update package list
    sudo apt-get update
}

install_ros2_packages() {
    log_info "Installing ROS2 packages"

    # Install ROS2 desktop full
    sudo apt-get install -y "ros-${ROS_DISTRO}-desktop"

    # Install development tools
    sudo apt-get install -y \
        "ros-${ROS_DISTRO}-ros-base" \
        "ros-dev-tools" \
        python3-colcon-common-extensions \
        python3-rosdep \
        python3-vcstool

    # Initialize rosdep
    if [[ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]]; then
        sudo rosdep init
    fi

    rosdep update
}

setup_ros2_environment() {
    log_info "Setting up ROS2 environment"

    local user="${DEPLOY_USER:-ubuntu}"
    local bashrc="/home/${user}/.bashrc"

    # Add ROS2 setup to bashrc
    if ! grep -q "source /opt/ros/${ROS_DISTRO}/setup.bash" "$bashrc"; then
        {
            echo ""
            echo "# ROS2 ${ROS_DISTRO} setup"
            echo "source /opt/ros/${ROS_DISTRO}/setup.bash"
            echo "export ROS_DOMAIN_ID=42"
            echo "export RMW_IMPLEMENTATION=rmw_fastrtps_cpp"
        } >> "$bashrc"
    fi

    # Create workspace directory
    create_dir "/home/${user}/ros2_ws/src" "$user" "$(id -gn $user)"
}

install_ros2_tools() {
    log_info "Installing additional ROS2 tools"

    # Install common ROS2 packages
    sudo apt-get install -y \
        "ros-${ROS_DISTRO}-rmw-fastrtps-cpp" \
        "ros-${ROS_DISTRO}-rviz2" \
        "ros-${ROS_DISTRO}-rqt" \
        "ros-${ROS_DISTRO}-robot-state-publisher" \
        "ros-${ROS_DISTRO}-joint-state-publisher" \
        "ros-${ROS_DISTRO}-xacro"

    # Install Gazebo (if not CPU-only mode)
    if [[ "${CPU_ONLY:-false}" != "true" ]]; then
        sudo apt-get install -y \
            "ros-${ROS_DISTRO}-gazebo-ros-pkgs" \
            "ros-${ROS_DISTRO}-gazebo-ros2-control"
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
