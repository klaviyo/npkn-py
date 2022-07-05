import os
import logging
import yaml
from typing import Union
from npkn.constants import RUNTIMES
from colorama import Fore, deinit
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv("NPKN_LOG_LEVEL", "WARN"))


def log_error_and_exit(err: Union[BaseException, str]) -> None:
    print(Fore.RED + str(err) + Fore.RESET)
    deinit()
    sys.exit(1)


def load_config():
    account_id = os.getenv('NPKN_ACCOUNT_ID')
    secret_key = os.getenv('NPKN_SECRET_KEY')
    default_runtime = os.getenv("NPKN_DEFAULT_RUNTIME")
    api_host = os.getenv("NPKN_API_HOST", "https://api.napkin.io")

    if default_runtime is None:
        logger.debug("No default runtime set")
    elif default_runtime.lower() not in RUNTIMES:
        logger.error(f"Invalid default runtime value set: {default_runtime}. Must be one of: {RUNTIMES}")
        default_runtime = None

    if account_id is None or secret_key is None:
        logger.info("Credentials not set")

    return {
        'account_id': account_id,
        'secret_key': secret_key,
        'default_runtime': default_runtime,
        'api_host': api_host
    }


def run_with_loading_message(fn, message, args=None, kwargs=None):
    _args = args if args is not None else []
    _kwargs = kwargs if kwargs is not None else {}
    print(f"{message} ⌛", end="\r")
    result = fn(*_args, **_kwargs)
    print(f"{message} ✅")

    return result


def load_yaml(file_path):
    if not os.path.exists(file_path):
        raise ValueError(f"No such file: {file_path}")
    with open(file_path) as f:
        return yaml.safe_load(f)


def write_yaml(file_path, data):
    with open(file_path, 'w') as f:
        f.write(yaml.dump(data))


config = load_config()
