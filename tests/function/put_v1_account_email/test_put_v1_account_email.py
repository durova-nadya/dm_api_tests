from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

def test_post_v1_account_login():
    #  Регистрация пользователя

    host = 'http://5.63.153.31:5051'
    account_api = AccountApi(host=host)
    login_api = LoginApi(host=host)
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'Putin'
    email = f'{login}@mail.ru'
    password = '1234567'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"
    # pprint.pprint(response.json())

    # # Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # # Изменить email

    json_data = {
        'login': login,
        'password': password,
        'email': f'{login}_new@mail.ru',
    }

    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Email не был изменён"

    # #Войти после смены email

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь смог авторизоваться после смены емайла"

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()

    print(response.status_code)
    assert response.status_code == 200, "Письма не были получены"


    #Получить новый токен после смены емайл

    token = get_rename_token_by_email(login, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"


def get_activation_token_by_login(
        login,
        response
        ):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token

def get_rename_token_by_email(
        login,
        response
        ):
    token = None
    for item in response.json()['items']:
        to_mailbox = item['To'][0]['Mailbox']
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login and to_mailbox == login + '_new':
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token

"""
- Регистрируемся

     - Получаем активационный токен

     - Активируем

     - Заходим

     - Меняем емейл

     - Пытаемся войти, получаем 403

     - На почте находим токен по новому емейлу для подтверждения смены емейла

     - .Активируем этот токен

     -  Логинимся
"""