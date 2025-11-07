import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Azure AD Configuration
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/callback')
    
    # Microsoft Graph API Configuration
    AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
    SCOPE = [
        'User.Read',
        'Calendars.Read',
        'Mail.Read'
    ]
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Graph API Endpoints
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
    
    # Analysis Configuration
    DAYS_TO_ANALYZE = 30  # Look back 30 days
    TOP_N_ITEMS = 7  # Generate top 5-7 items

