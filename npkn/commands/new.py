from uuid import uuid4
import shutil

from npkn.api import client, config, APIException
from .helpers import make_local_function_folder, add_function_uid_to_metadata
from npkn.utils import log_error_and_exit, logger, run_with_loading_message


def do_new_api_call(runtime, workspace_id, name, folder_path):
    try:
        data, err = client.post("new", runtime=runtime, workspaceId=workspace_id, name=name)
    except BaseException as e:
        shutil.rmtree(folder_path)
        raise APIException(e)

    return data


def new(name, runtime, workspace):

    if workspace is None:
        workspace_id = config['account_id']
    else:
        workspace_id = workspace

    if not name:
        name = str('%032x' % uuid4().int)[:6]

    try:
        folder_path = make_local_function_folder(runtime, name, workspace_id)
    except BaseException as e:
        log_error_and_exit(e)

    data = run_with_loading_message(do_new_api_call, f"Creating new function '{name}'", args=[runtime, workspace_id, name, folder_path])

    # add function uid to metadata.yaml
    logger.debug("Adding UID to metadata file")
    add_function_uid_to_metadata(folder_path, data['napkin']['uid'])
    logger.info(f"Successfully created new {runtime} function {name} 🚀")
