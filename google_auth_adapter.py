from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from iauth_client import IAuthClient

class GoogleAuthAdapter(IAuthClient):
    def __init__(self, gauth: GoogleAuth):
        self._gauth = gauth

    def authenticate(self):
        self._gauth.settings['access_type'] = 'offline' # Request a refresh token
        self._gauth.settings['api_version'] = 'v3' # Set API version to v3
        # Try to load saved client credentials
        self._gauth.LoadCredentialsFile("credentials.json")
        if self._gauth.credentials is None:
            # Authenticate if they're not there
            self._gauth.LocalWebserverAuth()
        elif self._gauth.access_token_expired:
            # Refresh them if expired
            self._gauth.Refresh()
        else:
            # Initialize the saved creds
            self._gauth.Authorize()
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
