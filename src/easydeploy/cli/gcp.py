"""GCP-specific CLI commands for easyDeploy."""

import sys

import click
from rich.console import Console

from easydeploy.cloud.gcp.auth import (
    authenticate,
    get_current_project,
    is_authenticated,
    list_projects,
    load_credentials,
    set_project,
)
from easydeploy.utils.logging import setup_logging

console = Console()


@click.group()
def gcp():
    """GCP authentication and deployment commands."""
    pass


@gcp.command()
def login():
    """Authenticate with Google Cloud Platform."""
    console.print("🔐 Starting GCP authentication...")

    if is_authenticated():
        console.print("✅ Already authenticated with GCP")

        # Show current user info
        creds = load_credentials()
        if creds and creds.get("project"):
            console.print(f"📋 Current project: {creds['project']}")

        if not click.confirm("Do you want to re-authenticate?"):
            return

    # Perform authentication
    if authenticate():
        console.print("🎉 GCP authentication successful!")

        # Show authenticated user info
        creds = load_credentials()
        if creds and creds.get("project"):
            console.print(f"📋 Project: {creds['project']}")
    else:
        console.print("❌ Authentication failed")
        console.print("💡 Please try again or check your internet connection")
        sys.exit(1)


@gcp.command()
def logout():
    """Remove GCP authentication."""
    if not is_authenticated():
        console.print("ℹ️  Not currently authenticated with GCP")
        return

    console.print("🔓 Logging out from GCP...")

    # For gcloud-based auth, we revoke the user credentials
    import subprocess

    try:
        subprocess.run(
            ["gcloud", "auth", "revoke", "--all"],
            capture_output=True,
            text=True,
            check=True,
        )
        console.print("✅ Successfully logged out from GCP")
    except (subprocess.CalledProcessError, FileNotFoundError):
        console.print("⚠️  Could not revoke credentials automatically")
        console.print("💡 You may need to run: gcloud auth revoke --all")


@gcp.command()
def status():
    """Show GCP authentication status."""
    console.print("🔍 Checking GCP authentication status...")

    if is_authenticated():
        console.print("✅ Authenticated with GCP")

        # Show current project
        current_project = get_current_project()
        if current_project:
            console.print(f"📋 Current project: {current_project}")
        else:
            console.print("⚠️  No project selected")
            console.print("💡 Run: easydeploy gcp select-project")

        console.print("🔑 Application Default Credentials are active")
    else:
        console.print("❌ Not authenticated with GCP")
        console.print("💡 Run: easydeploy gcp login")


@gcp.command("select-project")
def select_project():
    """Select a GCP project to use."""
    if not is_authenticated():
        console.print("❌ Not authenticated with GCP")
        console.print("💡 Please run: easydeploy gcp login")
        sys.exit(1)

    console.print("🔍 Loading available projects...")
    projects = list_projects()

    if not projects:
        console.print("❌ No projects found or unable to list projects")
        console.print("💡 Make sure you have access to at least one GCP project")
        sys.exit(1)

    console.print("📋 Available projects:")
    for i, project in enumerate(projects, 1):
        console.print(f"  {i}. {project['project_id']} ({project['name']})")

    # Get user selection
    while True:
        try:
            choice = click.prompt("Select a project (number)", type=int)
            if 1 <= choice <= len(projects):
                selected_project = projects[choice - 1]
                if set_project(selected_project["project_id"]):
                    console.print(f"✅ Project set to: {selected_project['project_id']}")
                    break
                else:
                    console.print("❌ Failed to set project. Please try again.")
            else:
                console.print(f"Please enter a number between 1 and {len(projects)}")
        except (click.Abort, KeyboardInterrupt):
            console.print("\n❌ Project selection cancelled")
            sys.exit(1)


@gcp.command("list-projects")
def list_projects_cmd():
    """List available GCP projects."""
    if not is_authenticated():
        console.print("❌ Not authenticated with GCP")
        console.print("💡 Please run: easydeploy gcp login")
        sys.exit(1)

    console.print("🔍 Loading projects...")
    projects = list_projects()

    if not projects:
        console.print("❌ No projects found")
        return

    current_project = get_current_project()
    console.print("📋 Available projects:")

    for project in projects:
        marker = "→" if project["project_id"] == current_project else " "
        console.print(f"  {marker} {project['project_id']} ({project['name']})")

    if current_project:
        console.print(f"\n✅ Current project: {current_project}")
    else:
        console.print("\n💡 No project selected. Use: easydeploy gcp select-project")


def require_gcp_auth(func):
    """Decorator to ensure GCP authentication before running commands."""

    def wrapper(*args, **kwargs):
        if not is_authenticated():
            console.print("❌ Not authenticated with GCP")
            console.print("💡 Please run: easydeploy gcp login")
            sys.exit(1)
        return func(*args, **kwargs)

    return wrapper


def main():
    """Entry point for GCP deployments."""
    # Setup logging
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    setup_logging(verbose)

    # Import here to avoid circular import
    from easydeploy.cli.main import main as main_cli

    # If it's a deploy command, add GCP platform by default
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        if "--platform" not in sys.argv:
            # Insert platform option after 'deploy' command
            sys.argv.insert(2, "--platform")
            sys.argv.insert(3, "gcp")

    # Run main CLI
    main_cli()


if __name__ == "__main__":
    # Check if we're running gcp-specific commands
    if len(sys.argv) > 1 and sys.argv[1] in ["login", "logout", "status"]:
        gcp()
    else:
        main()
