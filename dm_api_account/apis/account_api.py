from restclient.client import RestClient


class AccountApi(RestClient):


    def post_v1_account(
            self,
            json_data
    ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token,
            **kwargs
    ):
        """
        Activate registered user
        :param token:
        :return:
        """

        response = self.put(
            path=f'/v1/account/{token}'
        )
        return response

    def put_v1_account_email(
            self,
            json_data
    ):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        response = self.put(
            path=f'/v1/account/email',
            headers=headers,
            json=json_data
        )
        return response


    def get_v1_account(
            self,
            **kwargs
    ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response