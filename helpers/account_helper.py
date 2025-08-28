import json
import time
from enum import Enum

import allure
from requests import JSONDecodeError

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from retrying import retry

class TokenType(str, Enum):
    ACTIVATE = "activate"
    RESET_PASSWORD = "reset_password"


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            token = function(*args, **kwargs)
            count += 1
            print(f"Попытка получения токена номер {count}!")
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    @allure.step("Регистрация нового пользователя")
    def register_new_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

        start_time = time.time()
        token = self.get_token_by_login(login=login, token_type=TokenType.ACTIVATE)
        end_time = time.time()
        assert end_time - start_time < 3, "Время ожидания активации превышено"
        assert token is not None, f"Токен для пользователя {login}, не был получен"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    @allure.step("Аутентификация нового пользователя")
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response = False,
            validate_headers = False
    ):
        login_credentials = LoginCredentials(login=login, password=password, rememberMe=remember_me)
        response = self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials, validate_response=validate_response
            )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], f"Токен для пользователя {login} не был получен"
        return response


    def change_email(
            self,
            login: str,
            password: str,
            new_email: str
            ):
        change_email = ChangeEmail(login=login, password=password, email=new_email)
        self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        token = self.get_token_by_login(login=login, token_type=TokenType.ACTIVATE)
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def change_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
            ):
        reset_password = ResetPassword(login=login, email=email)
        response = self.user_login(login=login, password=old_password)
        self.dm_account_api.account_api.post_v1_account_password(
            reset_password=reset_password,
            headers={
                "x-dm-auth-token": response.headers["x-dm-auth-token"]
            }
        )
        token = self.get_token_by_login(login=login, token_type=TokenType.RESET_PASSWORD)

        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=old_password,
            newPassword=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        return response


    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_token_by_login(
            self,
            login: str,
            token_type: TokenType = TokenType.ACTIVATE, ) -> str | None:
        token = None
        if token_type == TokenType.ACTIVATE:
            link_type = "ConfirmationLinkUrl"
        elif token_type == TokenType.RESET_PASSWORD:
            link_type = "ConfirmationLinkUri"

        emails = self.mailhog.mailhog_api.get_api_v2_messages(limit=10).json()["items"]
        for email in emails:
            try:
                user_data = json.loads(email["Content"]["Body"])
            except (JSONDecodeError, KeyError):
                continue
            if user_data.get("Login") == login and user_data.get(link_type):
                token_link_url = user_data[link_type]
                token = token_link_url.split("/")[-1]
                return token
        return token


    def auth_client(self, login: str, password: str):
        response = self.user_login(login=login, password=password)
        token = {"x-dm-auth-token": response.headers["x-dm-auth-token"]}
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def user_logout(self, token: str | None):
        headers ={}
        if token:
            headers = {"x-dm-auth-token": token}
        response = self.dm_account_api.login_api.delete_v1_account_login(headers=headers)
        assert response.status_code == 204, "Сессия пользователя не завершена!"
        return response

    def user_logout_all(self, token: str | None):
        headers = {}
        if token:
            headers = {"x-dm-auth-token": token}
        response = self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)
        assert response.status_code == 204, "Сессии пользователя не завершены!"
        return response