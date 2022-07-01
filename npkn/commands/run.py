import os
from npkn import constants
from npkn.utils import (
    log_error_and_exit,
    load_yaml,
    run_with_loading_message
)

import npkn.commands.helpers as helpers

from npkn.api import client, APIException


def modules_need_sync(local_modules, remote_modules) -> bool:
    if not remote_modules and not local_modules:
        return False

    if not remote_modules and local_modules or (remote_modules and not local_modules):
        return True

    if len(local_modules) != len(remote_modules):
        return True

    # currently, modules list has 2 possible representations depending on runtime (python vs js)
    # python    : List[dict]
    # js        : dict
    if isinstance(remote_modules, list):
        rm_dict = {x['distribution']: x['version'] for x in remote_modules}
    else:
        rm_dict = remote_modules

    for k, v in local_modules.items():
        if v != rm_dict.get(k):
            if rm_dict.get(k) is not None and v == "*":
                pass
            else:
                return True

    return False


def sync_modules(function_uid, modules):
    res, err = client.post("sync/modules", function_uid=function_uid, modules=modules)

    if err:
        raise APIException(err)


def sync_env_vars(function_uid, env_vars):
    res, err = client.post("sync/env", function_uid=function_uid, env=env_vars)

    if err:
        raise APIException(err)


def sync_code(function_uid, code_str):
    res, err = client.post("sync/code", function_uid=function_uid, code_str=code_str)

    if err:
        raise APIException(err)

    if not res.get('success'):
        raise APIException(res.get('error'))


def env_vars_need_sync(local_env, remote_env) -> bool:
    return local_env != remote_env.get('values')


def code_needs_sync(local_code, remote_code) -> bool:
    return local_code != remote_code


def load_function_code(func_path):
    with open(func_path) as f:
        return f.read()


def default_js_function() -> str:
    # use CommonJS until we have a way to transpile ES modules
    return constants.DEFAULT_JS_CODE_COMPILED


def default_py_function() -> str:
    return constants.DEFAULT_PY_CODE


def run(name):
    """
    - syncing modules...
    - syncing environment...
    - Synced ✔
    - Running...
    """
    function_dir, data = helpers.find_local_function(name)
    uid = data['uid']

    remote_function_data = helpers.fetch_function_data(uid)
    function_path = f"{function_dir}/function.{'py' if data['runtime'] == 'python3.8' else 'js'}"
    code = load_function_code(function_path)

    local_modules = data.get('modules', {})
    local_env = data.get('env', {})

    modules_key = "pythonRequirements" if remote_function_data['runtime'] == 'python3.8' else "nodeModules"

    if modules_need_sync(local_modules, remote_function_data[modules_key]):
        run_with_loading_message(sync_modules, "Syncing modules", args=[uid, local_modules])

    if env_vars_need_sync(local_env, remote_function_data['env']):
        run_with_loading_message(sync_env_vars, "Syncing environment", args=[uid, local_env])

    if code_needs_sync(code, remote_function_data['codeStrTest']):
        run_with_loading_message(sync_code, "Syncing code", args=[uid, code])

    data, err = client.post("run", uid=uid, workspace_uid=data['workspace'])

    if err:
        log_error_and_exit(err)

    print(data)
