from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):


    def post_v1_account(self, registration: Registration):
        """
        Register new user
        :return:
        """
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def put_v1_account_token(self, token, validate_response=True, **kwargs):
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

    def put_v1_account_email(self, change_email: ChangeEmail, validate_response=True):
        """
        Change registered user email
        :return:
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        response = self.put(
            path=f'/v1/account/email',
            headers=headers,
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def get_v1_account(self,validate_response=True,**kwargs):
        """
        Get current user
        :return:
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    def post_v1_account_password(self, reset_password: ResetPassword, validate_response=True, **kwargs):
        """
        Reset registered user password
        :return:
        """
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            if response.status_code == 201:
                return UserEnvelope(**response.json())
        return response


    def put_v1_account_password(self,change_password: ChangePassword, validate_response=True):
        """
        Change registered user password
        :return:
        """
        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response