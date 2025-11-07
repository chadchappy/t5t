import subprocess
import json
from datetime import datetime, timedelta
import re

class OutlookAppleScriptReader:
    """
    Read email and calendar data from Outlook for Mac using AppleScript.
    No authentication required - works with local Outlook app.
    """
    
    def __init__(self):
        """Initialize the AppleScript reader"""
        self.outlook_running = self._check_outlook_running()
    
    def _check_outlook_running(self):
        """Check if Microsoft Outlook is running"""
        script = '''
        tell application "System Events"
            return (name of processes) contains "Microsoft Outlook"
        end tell
        '''
        try:
            result = self._run_applescript(script)
            return result.strip().lower() == 'true'
        except:
            return False
    
    def _run_applescript(self, script):
        """Execute an AppleScript and return the result"""
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode != 0:
                raise Exception(f"AppleScript error: {result.stderr}")
            return result.stdout
        except subprocess.TimeoutExpired:
            raise Exception("AppleScript execution timed out")
        except Exception as e:
            raise Exception(f"Failed to run AppleScript: {str(e)}")
    
    def is_available(self):
        """Check if Outlook is available via AppleScript"""
        return self.outlook_running
    
    def get_sent_emails(self, days_back=30):
        """
        Get sent emails from the last N days using AppleScript
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of email dictionaries
        """
        if not self.outlook_running:
            raise Exception("Microsoft Outlook is not running. Please open Outlook and try again.")
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        cutoff_str = cutoff_date.strftime("%m/%d/%Y")
        
        # AppleScript to get sent emails
        script = f'''
        set cutoffDate to date "{cutoff_str}"
        set emailList to {{}}
        
        tell application "Microsoft Outlook"
            try
                set sentFolder to sent items folder of default account
                set sentMessages to messages of sentFolder whose time sent > cutoffDate
                
                repeat with msg in sentMessages
                    try
                        set msgSubject to subject of msg
                        set msgSentDate to time sent of msg as string
                        set msgRecipients to ""
                        set msgPreview to content of msg
                        
                        -- Get recipients
                        try
                            set toRecips to to recipients of msg
                            repeat with recip in toRecips
                                try
                                    set recipEmail to email address of address of recip
                                    set recipName to name of recip
                                    if msgRecipients is "" then
                                        set msgRecipients to recipName & " <" & recipEmail & ">"
                                    else
                                        set msgRecipients to msgRecipients & "; " & recipName & " <" & recipEmail & ">"
                                    end if
                                end try
                            end repeat
                        end try
                        
                        -- Truncate preview to first 500 chars
                        if length of msgPreview > 500 then
                            set msgPreview to text 1 thru 500 of msgPreview
                        end if
                        
                        -- Build JSON-like string (we'll parse it in Python)
                        set emailData to "EMAILSTART|||" & msgSubject & "|||" & msgSentDate & "|||" & msgRecipients & "|||" & msgPreview & "|||EMAILEND"
                        set end of emailList to emailData
                    end try
                end repeat
                
                return emailList as string
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
        
        try:
            result = self._run_applescript(script)
            return self._parse_email_results(result)
        except Exception as e:
            raise Exception(f"Failed to get sent emails: {str(e)}")
    
    def get_calendar_events(self, days_back=30):
        """
        Get calendar events from the last N days using AppleScript
        
        Args:
            days_back: Number of days to look back (default: 30)
            
        Returns:
            List of calendar event dictionaries
        """
        if not self.outlook_running:
            raise Exception("Microsoft Outlook is not running. Please open Outlook and try again.")
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        cutoff_str = cutoff_date.strftime("%m/%d/%Y")
        
        # AppleScript to get calendar events
        script = f'''
        set cutoffDate to date "{cutoff_str}"
        set eventList to {{}}
        
        tell application "Microsoft Outlook"
            try
                set defaultCal to default calendar
                set calEvents to calendar events of defaultCal whose start time > cutoffDate
                
                repeat with evt in calEvents
                    try
                        set evtSubject to subject of evt
                        set evtStart to start time of evt as string
                        set evtEnd to end time of evt as string
                        set evtLocation to location of evt
                        set evtAttendees to ""
                        set evtOrganizer to ""
                        
                        -- Get organizer
                        try
                            set evtOrganizer to email address of address of organizer of evt
                        end try
                        
                        -- Get attendees
                        try
                            set attendeeList to attendees of evt
                            repeat with attendee in attendeeList
                                try
                                    set attendeeEmail to email address of address of attendee
                                    set attendeeName to name of attendee
                                    if evtAttendees is "" then
                                        set evtAttendees to attendeeName & " <" & attendeeEmail & ">"
                                    else
                                        set evtAttendees to evtAttendees & "; " & attendeeName & " <" & attendeeEmail & ">"
                                    end if
                                end try
                            end repeat
                        end try
                        
                        -- Build event data string
                        set eventData to "EVENTSTART|||" & evtSubject & "|||" & evtStart & "|||" & evtEnd & "|||" & evtLocation & "|||" & evtOrganizer & "|||" & evtAttendees & "|||EVENTEND"
                        set end of eventList to eventData
                    end try
                end repeat
                
                return eventList as string
            on error errMsg
                return "ERROR: " & errMsg
            end try
        end tell
        '''
        
        try:
            result = self._run_applescript(script)
            return self._parse_event_results(result)
        except Exception as e:
            raise Exception(f"Failed to get calendar events: {str(e)}")
    
    def get_user_email(self):
        """Get the user's email address from Outlook"""
        if not self.outlook_running:
            return None
        
        script = '''
        tell application "Microsoft Outlook"
            try
                set defaultAcct to default account
                set userEmail to email address of defaultAcct
                return userEmail
            on error
                return ""
            end try
        end tell
        '''
        
        try:
            result = self._run_applescript(script)
            email = result.strip()
            return email if email else None
        except:
            return None
    
    def _parse_email_results(self, result):
        """Parse the AppleScript email results into a list of dictionaries"""
        emails = []
        
        if result.startswith("ERROR:"):
            raise Exception(result)
        
        # Split by EMAILSTART and EMAILEND markers
        email_blocks = result.split("EMAILSTART|||")[1:]  # Skip first empty element
        
        for block in email_blocks:
            if "|||EMAILEND" not in block:
                continue
            
            # Remove the EMAILEND marker
            block = block.split("|||EMAILEND")[0]
            
            # Split by delimiter
            parts = block.split("|||")
            
            if len(parts) >= 4:
                email = {
                    'subject': parts[0].strip(),
                    'sent_date': parts[1].strip(),
                    'recipients': parts[2].strip(),
                    'preview': parts[3].strip() if len(parts) > 3 else '',
                    'body': parts[3].strip() if len(parts) > 3 else ''
                }
                emails.append(email)
        
        return emails
    
    def _parse_event_results(self, result):
        """Parse the AppleScript event results into a list of dictionaries"""
        events = []
        
        if result.startswith("ERROR:"):
            raise Exception(result)
        
        # Split by EVENTSTART and EVENTEND markers
        event_blocks = result.split("EVENTSTART|||")[1:]  # Skip first empty element
        
        for block in event_blocks:
            if "|||EVENTEND" not in block:
                continue
            
            # Remove the EVENTEND marker
            block = block.split("|||EVENTEND")[0]
            
            # Split by delimiter
            parts = block.split("|||")
            
            if len(parts) >= 7:
                event = {
                    'subject': parts[0].strip(),
                    'start': parts[1].strip(),
                    'end': parts[2].strip(),
                    'location': parts[3].strip(),
                    'organizer': parts[4].strip(),
                    'attendees': parts[5].strip(),
                    'attendee_list': [a.strip() for a in parts[5].split(';') if a.strip()]
                }
                events.append(event)
        
        return events
    
    def test_connection(self):
        """Test the AppleScript connection and return basic info"""
        try:
            if not self.outlook_running:
                return {
                    'success': False,
                    'error': 'Microsoft Outlook is not running',
                    'suggestion': 'Please open Microsoft Outlook and try again'
                }
            
            user_email = self.get_user_email()
            
            # Try to get a count of sent emails
            script = '''
tell application "Microsoft Outlook"
    try
        set sentFolder to sent items folder of default account
        set msgCount to count of messages of sentFolder
        return msgCount
    on error
        return 0
    end try
end tell
'''

            sent_count = int(self._run_applescript(script).strip())

            # Try to get a count of calendar events
            script = '''
tell application "Microsoft Outlook"
    try
        set defaultCal to default calendar
        set evtCount to count of calendar events of defaultCal
        return evtCount
    on error
        return 0
    end try
end tell
'''

            event_count = int(self._run_applescript(script).strip())
            
            return {
                'success': True,
                'method': 'AppleScript',
                'user_email': user_email,
                'sent_emails_count': sent_count,
                'calendar_events_count': event_count,
                'outlook_running': True
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

