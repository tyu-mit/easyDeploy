# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**easyDeploy** is an automation deployment toolkit designed to simplify the setup of cloud services and software environments for robotics AI development. The project provides scripts and utilities to quickly deploy and configure the complex software stacks commonly needed in robotics research and development.

Inspired by [IsaacAutomator](https://github.com/isaac-sim/IsaacAutomator), but focused on simpler, faster deployment using bash scripts instead of Ansible for better performance and reduced complexity.

### Project Purpose
- Automate deployment of robotics AI development environments
- Simplify cloud service provisioning and configuration
- Provide reusable deployment scripts for common robotics software stacks
- Streamline the setup process for robotics research and development workflows
- Fast, lightweight alternative to Ansible-based deployment solutions

## Project Structure

**Current State:**
- `.gitignore` - Comprehensive Python gitignore with robotics-specific additions
- `LICENSE` - MIT License (Copyright 2025 tyu-mit)
- `CLAUDE.md` - Project guidance and architecture documentation

**Planned Architecture:**
```
easyDeploy/
├── src/
│   ├── python/              # Core Python orchestration layer
│   │   ├── cli/            # Command-line interface
│   │   ├── cloud/          # Cloud provider management (GCP, Azure)
│   │   ├── config/         # Configuration management
│   │   ├── deploy/         # Deployment orchestration
│   │   └── utils/          # Common utilities
│   └── scripts/            # Bash configuration scripts
│       ├── system/         # Base system configuration
│       ├── gpu/            # GPU drivers and CUDA setup
│       ├── ros/            # ROS/ROS2 environment setup
│       └── isaac/          # Isaac Sim configuration
├── templates/              # Configuration file templates
├── state/                  # Deployment state management
├── deploy-gcp*             # GCP deployment entry point
├── deploy-azure*           # Azure deployment entry point (future)
└── requirements.txt        # Python dependencies
```

## Development Environment

Python-based robotics deployment project with support for:
- **Package Management**: Poetry/pip for dependency management
- **Cloud SDKs**: Google Cloud SDK, Azure SDK for Python
- **Testing**: pytest for comprehensive testing
- **CLI Framework**: Click for command-line interface
- **Configuration**: YAML/JSON for deployment configurations
- **Logging**: Structured logging for deployment tracking

## Deployment Targets

easyDeploy is designed to support two primary deployment scenarios:

### 1. Cloud Services (Single-User VMs)
- **Target Platforms**: Google Cloud Platform (GCP) primary, Azure secondary
- **Target Environment**: Cloud-based virtual machines for individual developers
- **Default User**: `ubuntu` (standard cloud VM username)
- **Use Cases**: Personal development, research, prototyping
- **Configuration**: Single-user setup with full system access

### 2. On-Premises Workstations (Multi-User)
- **Target Environment**: Company-owned physical or virtual machines
- **Authentication**: Azure AD integration for user management
- **User Management**: Automatic user directory creation on first login
- **Configuration**: Multi-user environment with shared resources

### Hardware Configurations

#### GPU-Enabled Systems
- **Primary Use Cases**:
  - Isaac Sim development and simulation
  - AI/ML model training and inference
  - Computer vision processing
- **Software Stack**: CUDA, cuDNN, ML frameworks, Isaac Sim

#### CPU-Only Systems
- **Primary Use Cases**:
  - Robot hardware control development
  - Non-ML robotics software development
  - System integration and testing
- **Software Stack**: ROS/ROS2, control libraries, communication protocols

## Typical Software Environments

When developing easyDeploy, consider these common robotics AI environments:
- ROS/ROS2 development environments
- Computer vision libraries (OpenCV, PIL, etc.)
- Machine learning frameworks (PyTorch, TensorFlow, JAX)
- Simulation environments (Gazebo, Isaac Sim, etc.)
- Hardware interface libraries (camera drivers, sensor interfaces)
- Development tools (IDEs, debugging tools, visualization)

## Technical Architecture

**Python-Driven Design:**
- Python serves as the primary orchestration layer for all user interactions and backend execution
- Bash scripts are used for specific system configuration tasks, called from Python
- Cloud operations use Python SDKs (Google Cloud SDK, Azure SDK) rather than CLI tools when possible

**Simplified Three-Layer Architecture:**
1. **Python Interface Layer** - User interaction, parameter validation, workflow orchestration
2. **Cloud Management Layer** - GCP/Azure resource provisioning using Python SDKs
3. **Configuration Layer** - Bash scripts for system setup, software installation, environment configuration

## Development Guidelines

- **Python-first approach**: Use Python for orchestration, user interaction, and cloud resource management
- **Strategic bash usage**: Use bash scripts only for system-level configuration tasks
- **Cloud SDK integration**: Prefer Python cloud SDKs over CLI tools for better error handling and integration
- Focus on idempotent deployment scripts that can be run multiple times safely
- Start with GCP support, design for Azure extensibility
- Provide clear configuration options and environment variable support
- Include comprehensive logging and error handling for deployment processes
- Design scripts to handle both single-user (cloud VM) and multi-user (on-premises) environments
- Consider GPU vs CPU-only deployment requirements in script design

## Philosophy

> Think carefully and implement the most concise solution that changes as little code as possible.

### Error Handling

- **Fail fast** for critical configuration (missing text model)
- **Log and continue** for optional features (extraction model)
- **Graceful degradation** when external services unavailable
- **User-friendly messages** through resilience layer

### Testing

- Always use the test-runner agent to execute tests.
- Do not use mock services for anything ever.
- Do not move on to the next test until the current test is complete.
- If the test fails, consider checking if the test is structured correctly before deciding we need to refactor the codebase.
- Tests to be verbose so we can use them for debugging.

## USE SUB-AGENTS FOR CONTEXT OPTIMIZATION

### 1. Always use the file-analyzer sub-agent when asked to read files.
The file-analyzer agent is an expert in extracting and summarizing critical information from files, particularly log files and verbose outputs. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 2. Always use the code-analyzer sub-agent when asked to search code, analyze code, research bugs, or trace logic flow.

The code-analyzer agent is an expert in code analysis, logic tracing, and vulnerability detection. It provides concise, actionable summaries that preserve essential information while dramatically reducing context usage.

### 3. Always use the test-runner sub-agent to run tests and analyze the test results.

Using the test-runner agent ensures:

- Full test output is captured for debugging
- Main conversation stays clean and focused
- Context usage is optimized
- All issues are properly surfaced
- No approval dialogs interrupt the workflow

## ABSOLUTE RULES

- NO PARTIAL IMPLEMENTATION
- NO SIMPLIFICATION : no "//This is simplified stuff for now, complete implementation would blablabla"
- NO CODE DUPLICATION : check existing codebase to reuse functions and constants Read files before writing new functions. Use common sense function name to find them easily.
- NO DEAD CODE : either use or delete from codebase completely
- IMPLEMENT TEST FOR EVERY FUNCTIONS
- NO CHEATER TESTS : test must be accurate, reflect real usage and be designed to reveal flaws. No useless tests! Design tests to be verbose so we can use them for debuging.
- NO INCONSISTENT NAMING - read existing codebase naming patterns.
- NO OVER-ENGINEERING - Don't add unnecessary abstractions, factory patterns, or middleware when simple functions would work. Don't think "enterprise" when you need "working"
- NO MIXED CONCERNS - Don't put validation logic inside API handlers, database queries inside UI components, etc. instead of proper separation
- NO RESOURCE LEAKS - Don't forget to close database connections, clear timeouts, remove event listeners, or clean up file handles

## Important Instruction Reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
