import msal
from config import Config

class MSALAuth:
    """Handles Microsoft Authentication Library (MSAL) operations"""
    
    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.authority = Config.AUTHORITY
        self.scope = Config.SCOPE
        self.redirect_uri = Config.REDIRECT_URI
        
    def get_auth_url(self):
        """Generate the authorization URL for user login"""
        app = self._build_msal_app()
        auth_url = app.get_authorization_request_url(
            scopes=self.scope,
            redirect_uri=self.redirect_uri
        )
        return auth_url
    
    def get_token_from_code(self, auth_code):
        """Exchange authorization code for access token"""
        app = self._build_msal_app()
        result = app.acquire_token_by_authorization_code(
            code=auth_code,
            scopes=self.scope,
            redirect_uri=self.redirect_uri
        )
        return result
    
    def get_token_from_cache(self, cache):
        """Get token from cache if available"""
        app = self._build_msal_app(cache=cache)
        accounts = app.get_accounts()
        if accounts:
            result = app.acquire_token_silent(
                scopes=self.scope,
                account=accounts[0]
            )
            return result
        return None
    
    def _build_msal_app(self, cache=None):
        """Build MSAL confidential client application"""
        return msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=self.authority,
            token_cache=cache
        )

