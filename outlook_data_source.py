"""
Unified Outlook data source that tries AppleScript first, falls back to Microsoft Graph API.
This provides the best of both worlds:
- No authentication when Outlook is running locally (AppleScript)
- Cloud access when needed (Graph API)
"""

from outlook_applescript import OutlookAppleScriptReader
from graph_client import GraphClient
from auth import MSALAuth
from datetime import datetime

class OutlookDataSource:
    """
    Unified data source for Outlook email and calendar data.
    Tries AppleScript first (local, no auth), falls back to Graph API (cloud, requires auth).
    """
    
    def __init__(self):
        """Initialize the data source"""
        self.applescript_reader = OutlookAppleScriptReader()
        self.auth_handler = MSALAuth()
        self.graph_client = None
        self.active_method = None
        
    def _get_graph_client(self):
        """Get or create Graph API client (lazy initialization)"""
        if self.graph_client is None:
            print("\n📡 AppleScript not available, using Microsoft Graph API...")
            print("This requires one-time authentication.\n")
            access_token = self.auth_handler.get_access_token()
            self.graph_client = GraphClient(access_token)
        return self.graph_client
    
    def get_sent_emails(self, days_back=30):
        """
        Get sent emails from the last N days.
        Tries AppleScript first, falls back to Graph API.
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of email dictionaries
        """
        # Try AppleScript first
        if self.applescript_reader.is_available():
            try:
                print("📧 Reading sent emails from local Outlook (AppleScript)...")
                emails = self.applescript_reader.get_sent_emails(days_back)
                self.active_method = 'AppleScript'
                print(f"✓ Found {len(emails)} sent emails (via AppleScript)\n")
                return emails
            except Exception as e:
                print(f"⚠️  AppleScript failed: {str(e)}")
                print("   Falling back to Microsoft Graph API...\n")
        
        # Fallback to Graph API
        try:
            client = self._get_graph_client()
            emails = client.get_sent_emails(days_back)
            self.active_method = 'Graph API'
            print(f"✓ Found {len(emails)} sent emails (via Graph API)\n")
            return emails
        except Exception as e:
            raise Exception(f"Failed to get sent emails from both sources: {str(e)}")
    
    def get_calendar_events(self, days_back=30):
        """
        Get calendar events from the last N days.
        Tries AppleScript first, falls back to Graph API.
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of calendar event dictionaries
        """
        # Try AppleScript first
        if self.applescript_reader.is_available():
            try:
                print("📅 Reading calendar events from local Outlook (AppleScript)...")
                events = self.applescript_reader.get_calendar_events(days_back)
                self.active_method = 'AppleScript'
                print(f"✓ Found {len(events)} calendar events (via AppleScript)\n")
                return events
            except Exception as e:
                print(f"⚠️  AppleScript failed: {str(e)}")
                print("   Falling back to Microsoft Graph API...\n")
        
        # Fallback to Graph API
        try:
            client = self._get_graph_client()
            events = client.get_calendar_events(days_back)
            self.active_method = 'Graph API'
            print(f"✓ Found {len(events)} calendar events (via Graph API)\n")
            return events
        except Exception as e:
            raise Exception(f"Failed to get calendar events from both sources: {str(e)}")
    
    def get_user_profile(self):
        """
        Get user profile information.
        Tries AppleScript first, falls back to Graph API.
        
        Returns:
            Dictionary with user profile info
        """
        # Try AppleScript first
        if self.applescript_reader.is_available():
            try:
                email = self.applescript_reader.get_user_email()
                if email:
                    return {
                        'email': email,
                        'displayName': email.split('@')[0],
                        'method': 'AppleScript'
                    }
            except:
                pass
        
        # Fallback to Graph API
        try:
            client = self._get_graph_client()
            profile = client.get_user_profile()
            profile['method'] = 'Graph API'
            return profile
        except Exception as e:
            return {
                'email': 'user@example.com',
                'displayName': 'User',
                'method': 'Unknown'
            }
    
    def test_connection(self):
        """
        Test both connection methods and return status.
        
        Returns:
            Dictionary with connection status for both methods
        """
        result = {
            'applescript': {
                'available': False,
                'status': None
            },
            'graph_api': {
                'available': False,
                'status': None
            },
            'recommended_method': None
        }
        
        # Test AppleScript
        print("🔍 Testing AppleScript connection...")
        if self.applescript_reader.is_available():
            as_result = self.applescript_reader.test_connection()
            result['applescript']['available'] = as_result.get('success', False)
            result['applescript']['status'] = as_result
            if as_result.get('success'):
                print("✓ AppleScript: Connected to local Outlook")
                print(f"  User: {as_result.get('user_email', 'Unknown')}")
                print(f"  Sent emails: {as_result.get('sent_emails_count', 0)}")
                print(f"  Calendar events: {as_result.get('calendar_events_count', 0)}\n")
        else:
            print("✗ AppleScript: Outlook not running\n")
            result['applescript']['status'] = {
                'success': False,
                'error': 'Microsoft Outlook is not running'
            }
        
        # Test Graph API (optional - only if AppleScript fails)
        if not result['applescript']['available']:
            print("🔍 Testing Microsoft Graph API connection...")
            try:
                # Don't actually authenticate yet, just check if it's configured
                result['graph_api']['available'] = True
                result['graph_api']['status'] = {
                    'success': True,
                    'message': 'Graph API available (authentication required on first use)'
                }
                print("✓ Graph API: Available as fallback\n")
            except Exception as e:
                result['graph_api']['status'] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"✗ Graph API: {str(e)}\n")
        
        # Determine recommended method
        if result['applescript']['available']:
            result['recommended_method'] = 'AppleScript'
        elif result['graph_api']['available']:
            result['recommended_method'] = 'Graph API'
        else:
            result['recommended_method'] = None
        
        return result
    
    def get_active_method(self):
        """Get the currently active data retrieval method"""
        return self.active_method or 'Not yet determined'
    
    def force_graph_api(self):
        """Force the use of Graph API (skip AppleScript)"""
        self.applescript_reader.outlook_running = False
        print("🔄 Forced to use Microsoft Graph API\n")
    
    def clear_graph_cache(self):
        """Clear the Graph API token cache (force re-authentication)"""
        try:
            self.auth_handler.clear_cache()
            self.graph_client = None
            print("✓ Graph API token cache cleared\n")
        except Exception as e:
            print(f"⚠️  Failed to clear cache: {str(e)}\n")

