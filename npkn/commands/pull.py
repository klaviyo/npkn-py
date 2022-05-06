import os
import shutil
from npkn.utils import config, logger, log_error_and_exit, run_with_loading_message
import npkn.commands.helpers as helpers


def pull_and_init_local_function(function, workspace):
    function_data = helpers.fetch_function_data(function['uid'])
    helpers.make_local_function_folder(function_data["runtime"], function['name'], workspace['uid'], os.getcwd(),
                                       uid=function_data['uid'],
                                       code=function_data['codeStrTest'],
                                       modules=function_data.get('pythonRequirements') if function_data[
                                                                                              'runtime'] == 'python3.8' else
                                       function_data['nodeModules'],
                                       env=function_data['env'].get('values'))


def list_files(startpath):
    """
    Adapted from https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('  {}{}/'.format(indent, os.path.basename(root)))
        for f in files:
            print('  ├── {}'.format(f))

    print("\n")


def pull(name, force):
    dest = os.path.join(os.getcwd(), name)

    if os.path.exists(dest):
        if force:
            logger.debug(f"Overwriting {dest}...")
        else:
            log_error_and_exit(f"Directory {dest} already exists. Use --force to overwrite.")

        shutil.rmtree(dest)

    parts = name.split(":")

    if len(parts) == 2:
        workspace_name, function_name = parts
    else:
        function_name = parts[0]
        workspace_name = None

    try:
        # get user account
        workspaces = helpers.get_user_workspaces()
        workspace = None
        # find workspace-function pair
        for _workspace in workspaces:
            if workspace_name is None:
                if _workspace['uid'] == config["account_id"]:
                    workspace = _workspace
                    break
            else:
                if _workspace['name'] == workspace_name:
                    workspace = _workspace
                    break

        if workspace is None:
            log_error_and_exit("Unable to retrieve workspace")

        function = None

        for uid, object in workspace['objects'].items():
            if object['type'] == 'folder':
                for _uid, _object in object['objects'].items():
                    if _object['name'] == function_name:
                        function = _object
                        break
            elif object['name'] == function_name:
                function = object
                break

        if function is None:
            log_error_and_exit(f"Unable to find function named {function_name}")

        logger.debug(function)

        run_with_loading_message(pull_and_init_local_function, f"Pulling function '{name}'", args=[function, workspace])
        list_files(os.path.join(os.getcwd(), name))
    except BaseException as e:
        print(e)
        shutil.rmtree(dest)
        log_error_and_exit(e)
