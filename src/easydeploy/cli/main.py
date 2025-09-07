"""Main CLI entry point for easyDeploy."""

import click
from rich.console import Console

from easydeploy.cli.gcp import gcp

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="easydeploy")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.pass_context
def main(ctx, verbose):
    """easyDeploy - Automation deployment toolkit for robotics AI development."""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")


@main.command()
@click.option(
    "--platform",
    type=click.Choice(["gcp", "azure"]),
    default="gcp",
    help="Cloud platform to deploy to",
)
@click.option("--instance-type", help="Instance type for the VM")
@click.option("--gpu", is_flag=True, help="Enable GPU support")
@click.argument("deployment_name")
@click.pass_context
def deploy(ctx, platform, instance_type, gpu, deployment_name):
    """Deploy a new robotics development environment."""
    verbose = ctx.obj.get("verbose", False)

    console.print(f"[bold green]Deploying {deployment_name}[/bold green]")
    console.print(f"Platform: {platform}")
    console.print(f"GPU enabled: {gpu}")

    if verbose:
        console.print(f"Instance type: {instance_type}")

    # TODO: Implement deployment logic
    console.print("[yellow]Deployment functionality not yet implemented[/yellow]")


@main.command()
@click.argument("deployment_name")
def destroy(deployment_name):
    """Destroy a deployment."""
    console.print(f"[bold red]Destroying {deployment_name}[/bold red]")
    # TODO: Implement destroy logic
    console.print("[yellow]Destroy functionality not yet implemented[/yellow]")


@main.command()
def list():
    """List all deployments."""
    console.print("[bold blue]Active deployments:[/bold blue]")
    # TODO: Implement list logic
    console.print("[yellow]List functionality not yet implemented[/yellow]")


# Register GCP subcommand group
main.add_command(gcp)


if __name__ == "__main__":
    main()
