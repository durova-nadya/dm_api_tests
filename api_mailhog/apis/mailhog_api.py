import requests


class MailhogApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def get_api_v2_messages(
            self,
            limit=50
    ):
        """
        Get Users emails
        :return:
        """
        params = {
            'limit': limit,
        }

        response = requests.get(
            url='http://5.63.153.31:5025/api/v2/messages',
            params=params,
            verify=False
        )
        return response
