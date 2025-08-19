from dm_api_account.models.registration import Registration
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):


    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        Register new user
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def put_v1_account_token(
            self,
            token,
            validate_response=True,
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
        if validate_response:
            return UserEnvelope(**response.json())
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
        # UserEnvelope(**response.json())
        return response

    def post_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        Reset registered user password
        :param json_data:
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response


    def put_v1_account_password(
            self,
            json_data
    ):
        """
        Change registered user password
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=json_data
        )
        return response

