import requests


class LoginApi:

    def __init__(
            self,
            host,
            headers=None
    ):
        self.host = host
        self.headers = headers

    def post_v1_account_login(
            self,
            json_data
            ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = requests.post(
            url='http://5.63.153.31:5051/v1/account/login',
            json=json_data
        )
        return response
