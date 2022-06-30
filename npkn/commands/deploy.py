
import npkn.commands.helpers as helpers
from npkn.utils import run_with_loading_message, logger
from npkn.api import client, APIException
from colorama import Fore


def do_deploy(uid):
    res, err = client.post("deploy", uid=uid)

    if err:
        raise APIException(err)

    return res


def deploy(name):
    function_dir, data = helpers.find_local_function(name)
    uid = data['uid']
    deploy_details = run_with_loading_message(do_deploy, "Deploying", args=[uid])

    endpoint_url = deploy_details['endpoint_url']
    print("Changes are now live at: " + Fore.RED + endpoint_url)
