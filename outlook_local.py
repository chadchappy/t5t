import sqlite3
import os
from datetime import datetime, timedelta
from pathlib import Path
import json

class OutlookLocalReader:
    """
    Read email and calendar data directly from Outlook for Mac's local SQLite database.
    No authentication or API keys required!
    """
    
    def __init__(self, profile_name="Main Profile"):
        """
        Initialize the Outlook local database reader
        
        Args:
            profile_name: Name of the Outlook profile (default: "Main Profile")
        """
        self.profile_name = profile_name
        self.db_path = self._find_outlook_database()
        
    def _find_outlook_database(self):
        """Find the Outlook SQLite database on Mac"""
        base_path = Path.home() / "Library" / "Group Containers" / "UBF8T346G9.Office" / "Outlook" / "Outlook 15 Profiles"
        profile_path = base_path / self.profile_name / "Data" / "Outlook.sqlite"
        
        if not profile_path.exists():
            raise FileNotFoundError(
                f"Outlook database not found at: {profile_path}\n"
                f"Make sure Outlook for Mac is installed and you have a profile named '{self.profile_name}'"
            )
        
        return str(profile_path)
    
    def _get_connection(self):
        """Get a read-only connection to the Outlook database"""
        # Open in read-only mode to avoid locking issues
        conn = sqlite3.connect(f'file:{self.db_path}?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_sent_emails(self, days_back=30):
        """
        Get sent emails from the last N days
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of email dictionaries with subject, recipients, date, etc.
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        query = """
        SELECT 
            m.Record_RecordID,
            m.Message_NormalizedSubject as subject,
            m.Message_RecipientList as recipients,
            m.Message_DisplayTo as to_display,
            m.Message_TimeSent as sent_date,
            m.Message_Preview as preview,
            m.PathToDataFile as data_file,
            f.Folder_Name as folder_name
        FROM Mail m
        LEFT JOIN Folders f ON m.Record_FolderID = f.Record_RecordID
        WHERE m.Message_IsOutgoingMessage = 1
          AND m.Message_TimeSent >= ?
          AND m.Message_Sent = 1
        ORDER BY m.Message_TimeSent DESC
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (cutoff_date,))
        
        emails = []
        for row in cursor.fetchall():
            email = {
                'id': row['Record_RecordID'],
                'subject': row['subject'] or '',
                'recipients': row['recipients'] or '',
                'to_display': row['to_display'] or '',
                'sent_date': row['sent_date'],
                'preview': row['preview'] or '',
                'folder': row['folder_name'] or 'Sent Items',
                'data_file': row['data_file']
            }
            
            # Try to get full body if available
            if row['data_file']:
                email['body'] = self._get_email_body(row['data_file'])
            
            emails.append(email)
        
        conn.close()
        return emails
    
    def get_calendar_events(self, days_back=30):
        """
        Get calendar events from the last N days
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of calendar event dictionaries
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        query = """
        SELECT 
            c.Record_RecordID,
            c.Calendar_StartDateUTC as start_date,
            c.Calendar_EndDateUTC as end_date,
            c.Calendar_IsRecurring as is_recurring,
            c.Calendar_AttendeeCount as attendee_count,
            c.PathToDataFile as data_file,
            f.Folder_Name as calendar_name
        FROM CalendarEvents c
        LEFT JOIN Folders f ON c.Record_FolderID = f.Record_RecordID
        WHERE c.Calendar_StartDateUTC >= ?
        ORDER BY c.Calendar_StartDateUTC DESC
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query, (cutoff_date,))
        
        events = []
        for row in cursor.fetchall():
            event = {
                'id': row['Record_RecordID'],
                'start': row['start_date'],
                'end': row['end_date'],
                'is_recurring': bool(row['is_recurring']),
                'attendee_count': row['attendee_count'] or 0,
                'calendar': row['calendar_name'] or 'Calendar',
                'data_file': row['data_file']
            }
            
            # Try to get event details (subject, location, etc.) from data file
            if row['data_file']:
                details = self._get_event_details(row['data_file'])
                event.update(details)
            
            events.append(event)
        
        conn.close()
        return events
    
    def _get_email_body(self, data_file_path):
        """
        Get email body from the data file
        
        Note: Email bodies are stored in separate files in the profile directory.
        This is a simplified version - full implementation would parse the MIME structure.
        """
        try:
            profile_base = Path(self.db_path).parent.parent
            full_path = profile_base / data_file_path
            
            if full_path.exists() and full_path.stat().st_size < 1024 * 1024:  # Max 1MB
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Simple extraction - could be improved
                    return content[:1000]  # First 1000 chars
        except Exception as e:
            pass
        
        return ""
    
    def _get_event_details(self, data_file_path):
        """
        Get calendar event details from the data file
        
        Returns dict with subject, location, body, etc.
        """
        details = {
            'subject': '',
            'location': '',
            'body': '',
            'organizer': '',
            'attendees': []
        }
        
        try:
            profile_base = Path(self.db_path).parent.parent
            full_path = profile_base / data_file_path
            
            if full_path.exists() and full_path.stat().st_size < 512 * 1024:  # Max 512KB
                with open(full_path, 'rb') as f:
                    content = f.read()
                    
                # Try to decode as text
                try:
                    text = content.decode('utf-8', errors='ignore')
                    
                    # Simple parsing - look for common patterns
                    # This is a simplified version - full implementation would parse iCal format
                    for line in text.split('\n'):
                        if line.startswith('SUMMARY:'):
                            details['subject'] = line.replace('SUMMARY:', '').strip()
                        elif line.startswith('LOCATION:'):
                            details['location'] = line.replace('LOCATION:', '').strip()
                        elif line.startswith('DESCRIPTION:'):
                            details['body'] = line.replace('DESCRIPTION:', '').strip()
                        elif line.startswith('ORGANIZER'):
                            details['organizer'] = line.split(':')[-1].strip()
                        elif line.startswith('ATTENDEE'):
                            attendee = line.split(':')[-1].strip()
                            if attendee:
                                details['attendees'].append(attendee)
                except:
                    pass
                    
        except Exception as e:
            pass
        
        return details
    
    def get_user_email(self):
        """Get the user's email address from the account settings"""
        query = """
        SELECT 
            AccountsMail.Account_EmailAddress as email
        FROM AccountsMail
        LIMIT 1
        """
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        
        if row and row['email']:
            return row['email']
        
        return "user@example.com"
    
    def test_connection(self):
        """Test the database connection and return basic stats"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Count sent emails
            cursor.execute("SELECT COUNT(*) as count FROM Mail WHERE Message_IsOutgoingMessage = 1")
            sent_count = cursor.fetchone()['count']
            
            # Count calendar events
            cursor.execute("SELECT COUNT(*) as count FROM CalendarEvents")
            event_count = cursor.fetchone()['count']
            
            # Get user email
            user_email = self.get_user_email()
            
            conn.close()
            
            return {
                'success': True,
                'database_path': self.db_path,
                'user_email': user_email,
                'sent_emails_count': sent_count,
                'calendar_events_count': event_count
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

