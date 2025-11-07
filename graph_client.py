import requests
from datetime import datetime, timedelta
from config import Config

class GraphClient:
    """Client for interacting with Microsoft Graph API"""
    
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        self.base_url = Config.GRAPH_API_ENDPOINT
    
    def get_user_profile(self):
        """Get the current user's profile"""
        url = f'{self.base_url}/me'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_calendar_events(self, days_back=30):
        """
        Fetch calendar events from the past N days
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of calendar events
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)
        end_date = datetime.utcnow()
        
        # Format dates for Graph API
        start_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_str = end_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        url = f'{self.base_url}/me/calendarview'
        params = {
            'startDateTime': start_str,
            'endDateTime': end_str,
            '$top': 999,  # Get up to 999 events
            '$select': 'subject,start,end,attendees,organizer,body'
        }
        
        events = []
        while url:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            events.extend(data.get('value', []))
            
            # Handle pagination
            url = data.get('@odata.nextLink')
            params = None  # nextLink includes all params
        
        return events
    
    def get_sent_emails(self, days_back=30):
        """
        Fetch sent emails from the past N days
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of sent email messages
        """
        start_date = datetime.utcnow() - timedelta(days=days_back)
        start_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        url = f'{self.base_url}/me/mailFolders/SentItems/messages'
        params = {
            '$filter': f'sentDateTime ge {start_str}',
            '$top': 999,
            '$select': 'subject,sentDateTime,toRecipients,ccRecipients,body,bodyPreview'
        }
        
        emails = []
        while url:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            emails.extend(data.get('value', []))
            
            # Handle pagination
            url = data.get('@odata.nextLink')
            params = None  # nextLink includes all params
        
        return emails

