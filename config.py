import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure AD Configuration (Device Code Flow - Public Client)
    # Using Microsoft's public multi-tenant client ID for device code flow
    # This works without any Azure AD setup required!
    CLIENT_ID = os.getenv('CLIENT_ID', '04b07795-8ddb-461a-bbee-02f9e1bf7b46')  # Microsoft Azure CLI public client

    # Microsoft Graph API Configuration
    AUTHORITY = 'https://login.microsoftonline.com/common'  # Multi-tenant

    # Delegated permissions (user context) - no admin consent required
    SCOPE = [
        'User.Read',
        'Calendars.Read',
        'Mail.Read'
    ]

    # Token cache location
    TOKEN_CACHE_FILE = os.getenv('TOKEN_CACHE_FILE', './data/token_cache.json')

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Graph API Endpoints
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

    # Analysis Configuration
    DAYS_TO_ANALYZE = 30  # Look back 30 days
    TOP_N_ITEMS = 7  # Generate top 5-7 items

