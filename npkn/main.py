import click
import os
import requests

runtimes = ['python3.8', 'node14x']
name_argument = click.argument("name")
workspace_option = click.option("-w", "--workspace", default="default", help="Workspace the function belongs to (default workspace used if not provided")


def load_config():
    account_id = os.getenv('NAPKIN_ACCOUNT_ID')
    secret_key = os.getenv('NAPKIN_SECRET_KEY')
    default_runtime = os.getenv("NPKN_DEFAULT_RUNTIME")

    if default_runtime is None:
        print("No default runtime set")
    elif default_runtime.lower() not in runtimes:
        print(f"Invalid default runtime value set: {default_runtime}. Must be one of: {runtimes}")
        default_runtime = None

    if account_id is None or secret_key is None:
        print("Credentials not set")

    return {
        'account_id': account_id,
        'secret_key': secret_key,
        'default_runtime': default_runtime
    }


config = load_config()


class APIClient:
    Protocol = "https"
    Subdomain = "api"
    ApiVersion = "v1"

    BaseUrl = f"{Protocol}://npkn.net/api/{ApiVersion}"

    def _api_call(self, method: str, **kwargs):
        methods = {
            'POST': requests.post,
            'GET': requests.get,
            'DELETE': requests.delete
        }

        res = methods[method](self.BaseUrl, **{
            'headers': {
                'napkin-user-uid': self._user_uid,
                'napkin-api-key': self._api_key
            },
            **kwargs,
        })

        return res
    pass


client = APIClient()


@click.group()
def cli():
    pass


@cli.command(help="Create a new Napkin function")
@click.option("-r", "--runtime", type=click.Choice(runtimes, case_sensitive=False), default=config['default_runtime'])
@click.option("-n", "--name", help="Function name (optional)")
def new(runtime, name):
    click.echo('Create new function')
    # needs to make directory, init files, send create request


@cli.command(help="Run an existing napkin function")
@name_argument
@workspace_option
def run(name, workspace):
    click.echo('Run function')
    # needs to checkpoint + run


@cli.command(help="Deploy pending changes for a given function")
@name_argument
@workspace_option
def deploy(name, workspace):
    click.echo("Deploy")
