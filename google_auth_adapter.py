from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from iauth_client import IAuthClient

class GoogleAuthAdapter(IAuthClient):
    def __init__(self, gauth: GoogleAuth):
        self._gauth = gauth

    def authenticate(self):
        # Load client secrets
        self._gauth.LoadClientConfigFile("client_secrets.json")
        # Try to load saved client credentials
        self._gauth.LoadCredentialsFile("credentials.json")
        if self._gauth.credentials is None or self._gauth.access_token_expired:
            # Authenticate if they're not there or expired
            self._gauth.LocalWebserverAuth()
        # Save the current credentials to a file
        self._gauth.SaveCredentialsFile("credentials.json")

def get_authenticated_drive() -> GoogleDrive:
    gauth = GoogleAuth()
    auth_adapter = GoogleAuthAdapter(gauth)
    # AuthProvider is now in a separate module, so we need to import it here
    from auth_provider import AuthProvider
    auth_provider = AuthProvider(auth_adapter)
    auth_provider.authenticate()
    return GoogleDrive(gauth)
