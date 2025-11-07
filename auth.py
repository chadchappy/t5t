import msal
from config import Config

class MSALAuth:
    """Handles Microsoft Authentication Library (MSAL) operations for app-only access"""

    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.authority = Config.AUTHORITY
        self.scope = Config.SCOPE
        self.user_email = Config.USER_EMAIL

    def get_access_token(self):
        """
        Get access token using client credentials flow (app-only authentication)
        This allows automated access without user interaction
        """
        app = self._build_msal_app()
        result = app.acquire_token_for_client(scopes=self.scope)

        if 'access_token' in result:
            return result['access_token']
        else:
            error = result.get('error_description', result.get('error', 'Unknown error'))
            raise Exception(f"Failed to acquire token: {error}")

    def _build_msal_app(self):
        """Build MSAL confidential client application for app-only access"""
        return msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority
        )

