import msal
import os
import json
from config import Config

class MSALAuth:
    """Handles Microsoft Authentication Library (MSAL) operations using device code flow"""

    def __init__(self):
        self.client_id = Config.CLIENT_ID
        self.authority = Config.AUTHORITY
        self.scope = Config.SCOPE
        self.cache_file = Config.TOKEN_CACHE_FILE

    def get_access_token(self):
        """
        Get access token using device code flow with token caching
        This allows authentication without Azure AD admin access
        """
        # Load token cache
        cache = self._load_cache()
        app = self._build_msal_app(cache=cache)

        # Try to get token from cache first
        accounts = app.get_accounts()
        if accounts:
            print("Found cached account, attempting silent token acquisition...")
            result = app.acquire_token_silent(scopes=self.scope, account=accounts[0])
            if result and 'access_token' in result:
                print("✓ Token acquired from cache")
                return result['access_token']

        # If no cached token, use device code flow
        print("\n" + "="*60)
        print("AUTHENTICATION REQUIRED")
        print("="*60)

        flow = app.initiate_device_flow(scopes=self.scope)

        if 'user_code' not in flow:
            raise Exception(f"Failed to create device flow: {flow.get('error_description', 'Unknown error')}")

        print(flow['message'])
        print("\n" + "="*60)
        print("Waiting for you to complete authentication in your browser...")
        print("="*60 + "\n")

        # Wait for user to authenticate
        result = app.acquire_token_by_device_flow(flow)

        if 'access_token' in result:
            # Save the cache
            self._save_cache(cache)
            print("✓ Authentication successful! Token cached for future use.\n")
            return result['access_token']
        else:
            error = result.get('error_description', result.get('error', 'Unknown error'))
            raise Exception(f"Failed to acquire token: {error}")

    def clear_cache(self):
        """Clear the token cache (force re-authentication)"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
            print(f"✓ Token cache cleared: {self.cache_file}")

    def _build_msal_app(self, cache=None):
        """Build MSAL public client application for device code flow"""
        return msal.PublicClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            token_cache=cache
        )

    def _load_cache(self):
        """Load token cache from file"""
        cache = msal.SerializableTokenCache()
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache.deserialize(f.read())
        return cache

    def _save_cache(self, cache):
        """Save token cache to file"""
        if cache.has_state_changed:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            with open(self.cache_file, 'w') as f:
                f.write(cache.serialize())

