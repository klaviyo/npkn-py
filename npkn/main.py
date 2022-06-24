import click
import sys
from npkn.constants import RUNTIMES
from npkn.utils import config
from npkn import commands
from . import __version__ as current_version, __file__ as module_location


@click.group()
def cli():
    pass


@cli.command(help="""
Pull function(s) from napkin.io to your local machine. 
By default this will copy all of your workspaces and functions.
""")
@click.argument("name")
@click.option("--force", is_flag=True)
def pull(**kwargs):
    commands.pull(kwargs['name'], kwargs['force'])


@cli.command(help="""
See available commands and current npkn version
""")
def help():
    with click.Context(cli) as ctx:
        click.echo(cli.get_help(ctx))

    print("\nEnvironment Variables\n---------------------")
    print("- NPKN_ACCOUNT_ID")
    print("- NPKN_SECRET_KEY")
    print("- NPKN_LOG_LEVEL")

    print(f"\nnpkn v{current_version} {module_location}")


@cli.command(help="Run an existing napkin function")
@click.option("-n", "--name", default=None)
def run(name=None):
    commands.run(name)


@cli.command(help="Create a new Napkin function")
@click.argument('name', required=False)
@click.option("-r", "--runtime", type=click.Choice(RUNTIMES, case_sensitive=False), default=config['default_runtime'])
@click.option("-w", "--workspace", default=None,
              help="[EXPERIMENTAL] Workspace the function belongs to (default workspace used if not provided")
def new(name=None, runtime=None, workspace=None):
    commands.new(name, runtime, workspace)


@cli.command(help="Deploy pending changes for a given function")
@click.option('-n', '--name', default=None)
def deploy(name=None):
    commands.deploy(name)


if __name__ == "__main__":
    cli()
