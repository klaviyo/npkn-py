import requests
import os
from urllib.parse import urljoin
import traceback
from npkn.utils import logger, config


class APIException(Exception):
    pass


class APIClient:
    Protocol = "https"
    ApiVersion = "1"
    BaseUrl = f"{config['api_host']}/api/{ApiVersion}/"

    def __init__(self, user_uid, api_key):
        self._user_uid = user_uid
        self._api_key = api_key
        self.debug = False

    def _api_call(self, method: str, endpoint: str, **kwargs):
        methods = {
            'POST': requests.post,
            'GET': requests.get,
            'DELETE': requests.delete
        }
        url = urljoin(self.BaseUrl, endpoint)
        res = methods[method](url, **{
            'headers': {
                'napkin-user-uid': self._user_uid,
                'napkin-api-key': self._api_key
            },
            **kwargs,
        })

        return res

    def get(self, endpoint, **kwargs) -> tuple:
        """
        Return tuple of (response_data, error)
        """
        return self._handle_api_call("GET", endpoint, params=kwargs)

    def _handle_api_call(self, method, endpoint, params=None, **kwargs) -> tuple:
        try:
            res = self._api_call(method, endpoint, params=params, json=kwargs)

            if not res.ok:
                try:
                    logger.debug("Error response:")
                    logger.debug(res.json())
                    return None, res.json()
                except BaseException:
                    return None, res.content

            data = res.json()
        except BaseException as e:
            logger.debug(traceback.format_exc())
            return None, e

        logger.debug("Success response:")
        logger.debug(data)
        return data, None

    def post(self, endpoint, **kwargs) -> tuple:
        """
        Return tuple of (response_data, error)
        """
        return self._handle_api_call("POST", endpoint, **kwargs)


client = APIClient(config['account_id'], config['secret_key'])