import os
from npkn.api import client, APIException
from npkn.utils import log_error_and_exit, load_yaml, write_yaml
from npkn import constants
from colorama import Back


def find_local_function(name) -> tuple:
    _dir = os.getcwd()
    data = {}

    if name is None:
        # look for meta.yaml in _dir and try to read name from there
        function_dir = _dir
        config_file_path = os.path.join(_dir, constants.CONFIG_FILE_NAME)
        if not os.path.exists(config_file_path):
            log_error_and_exit(
                f"Either function name must be supplied or current directory must contain a valid {constants.CONFIG_FILE_NAME}."
            )
        else:
            data = load_yaml(config_file_path)

            if 'uid' not in data:
                log_error_and_exit(f"{constants.CONFIG_FILE_NAME} must contain a valid 'uid'.")

            uid = data['uid']
    else:
        function_dir = os.path.join(_dir, name)
        config_file_path = os.path.join(function_dir, constants.CONFIG_FILE_NAME)
        try:
            data = load_yaml(config_file_path)
        except BaseException as e:
            log_error_and_exit(f"Encountered the following error while attempting to read {config_file_path}: {e}")

    print(f"Function: {data['name']} | Workspace: default")

    return function_dir, data


def make_local_function_folder(runtime: str, name: str, workspace: str, directory=None, code=None, uid=None,
                               modules=None, env=None) -> str:
    """
    In current working dir, create a new folder with the function name.
    Inside the folder create the following files:
        - function.[js|py]
        - meta.yaml


    Initialize the function.[js|py] with hello world
    Initialize the meta.yaml with function metadata

    Raises BaseException
    Returns abs path to folder that was created
    """

    if directory is None:
        directory = os.getcwd()

    working_dir = directory

    folder_path = os.path.join(working_dir, name)

    if os.path.exists(folder_path):
        msg = f"A folder named '{name}'" + \
              " already exists in the current directory " \
              + Back.BLACK + "(Napkin function names are CASE-INSENSITIVE)" \
              + Back.RESET + ".\n\nPlease choose a different name."
        log_error_and_exit(msg)

    os.mkdir(folder_path)

    if runtime == "nodejs14.x":
        if code is None:
            code = constants.DEFAULT_JS_CODE
        file_ext = "js"
    elif runtime == "python3.8":
        if code is None:
            code = constants.DEFAULT_PY_CODE
        file_ext = "py"
    else:
        raise ValueError(f"Unknown runtime: {runtime}")

    code_path = os.path.join(folder_path, f"function.{file_ext}")
    meta_path = os.path.join(folder_path, constants.CONFIG_FILE_NAME)

    with open(code_path, 'w') as f:
        f.write(code)

    metadata = {
        'runtime': runtime,
        'name': name,
        'workspace': workspace,
        'uid': uid
    }

    if modules is not None and len(modules) > 0:
        module_list = {m['name']: m['version'] for m in modules if not m['transitive']}
        metadata['modules'] = module_list

    if env is not None and len(env) > 0:
        metadata['env'] = env

    write_yaml(meta_path, metadata)

    return folder_path


def add_function_uid_to_metadata(folder_path, uid):
    meta_path = os.path.join(folder_path, constants.CONFIG_FILE_NAME)
    data = load_yaml(meta_path)

    data['uid'] = uid

    write_yaml(meta_path, data)


def get_user_workspaces():
    account, err = client.get("account")

    if err:
        log_error_and_exit(err)

    return account['workspaces']


def fetch_function_data(uid):
    function_data, err = client.get("function", uid=uid)

    if err:
        raise APIException(err)

    return function_data['function']
