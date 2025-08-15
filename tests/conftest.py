import datetime
import random
import string
from collections import namedtuple

import pytest
import structlog

from helpers.account_helper import AccountHelper
from restclient.configation import Configuration as DmApiConfiguration
from restclient.configation import Configuration as MailhogConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, ensure_ascii=True, sort_keys=True)
    ]
)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope="session")
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(login="AlisaLuu", password="777777777")
    return account_helper

@pytest.fixture
def prepare_user():
    # now = datetime.datetime.now()
    # data = now.strftime("%d_%m_%Y_%H_%M_%S")
    # login = f'joy_{data}'
    characters = string.ascii_letters + string.digits  # Все английские буквы (в верхнем и нижнем регистре) и цифры
    random_part = ''.join(random.choice(characters) for _ in range(7))  # Генерируем случайную строку
    login = "joy_" + random_part
    password = 'abcd12345'
    email = f'{login}@mail.ru'
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
