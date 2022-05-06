
import npkn.commands.helpers as helpers
from npkn.utils import run_with_loading_message
from npkn.api import client, APIException


def do_deploy(uid):
    res, err = client.post("deploy", uid=uid)

    if err:
        raise APIException(err)

    return res


def deploy(name):
    function_dir, data = helpers.find_local_function(name)
    uid = data['uid']
    run_with_loading_message(do_deploy, "Deploying", args=[uid])








