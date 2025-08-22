from iauth_client import IAuthClient

class AuthProvider:
    def __init__(self, auth_client: IAuthClient):
        self.auth_client = auth_client

    def authenticate(self):
        self.auth_client.authenticate()