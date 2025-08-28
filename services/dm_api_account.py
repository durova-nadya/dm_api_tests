from clients.http.dm_api_account.apis.account_api import AccountApi
from packages.restclient.configation import Configuration
from clients.http.dm_api_account.apis.login_api import LoginApi


class DMApiAccount:

    def __init__(self, configuration: Configuration):
        self.configuration = configuration
        self.login_api = LoginApi(configuration=self.configuration)
        self.account_api = AccountApi(configuration=self.configuration)