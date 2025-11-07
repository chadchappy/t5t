import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure AD Configuration (App-only authentication)
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')

    # User email address to access (your email)
    USER_EMAIL = os.getenv('USER_EMAIL')

    # Microsoft Graph API Configuration
    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'

    # Application permissions (not delegated) for app-only access
    SCOPE = ['https://graph.microsoft.com/.default']

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Graph API Endpoints
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

    # Analysis Configuration
    DAYS_TO_ANALYZE = 30  # Look back 30 days
    TOP_N_ITEMS = 7  # Generate top 5-7 items

