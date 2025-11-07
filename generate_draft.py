#!/usr/bin/env python3
"""
Top 5 Things Email Draft Generator - CLI Version

One-time authentication, read email and calendar, generate draft, and exit.
No persistent tokens, no web server - just a simple CLI tool.
"""

import sys
import os
from datetime import datetime
from pathlib import Path
from auth import MSALAuth
from graph_client import GraphClient
from analyzer import DataAnalyzer
from email_generator import EmailDraftGenerator
from config import Config

def print_banner():
    """Print application banner"""
    print("\n" + "=" * 70)
    print("  TOP 5 THINGS EMAIL DRAFT GENERATOR")
    print("  Read-only access to your Microsoft 365 email and calendar")
    print("=" * 70 + "\n")

def print_section(title):
    """Print a section header"""
    print(f"\n{'─' * 70}")
    print(f"  {title}")
    print(f"{'─' * 70}\n")

def save_draft_to_file(draft, output_dir="./output"):
    """Save the draft to a text file"""
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filename = f"top5_draft_{timestamp}.txt"
    filepath = Path(output_dir) / filename
    
    # Format the draft
    content = f"Subject: {draft['subject']}\n\n"
    content += "=" * 70 + "\n\n"
    content += draft['body']
    content += "\n\n" + "=" * 70 + "\n"
    content += f"Generated: {draft['metadata']['generated_at']}\n"
    content += f"Calendar events analyzed: {draft['metadata']['calendar_events_analyzed']}\n"
    content += f"Emails analyzed: {draft['metadata']['emails_analyzed']}\n"
    content += f"Top items identified: {draft['metadata']['items_count']}\n"
    
    # Save to file
    with open(filepath, 'w') as f:
        f.write(content)
    
    return str(filepath)

def main():
    """Main function"""
    try:
        print_banner()
        
        # Get parameters
        days_back = int(os.getenv('DAYS_BACK', Config.DAYS_TO_ANALYZE))
        
        print(f"📊 Analysis period: Last {days_back} days")
        print(f"🔐 Authentication: Microsoft 365 (one-time device code flow)")
        print(f"📖 Access: Read-only (no emails sent, no calendar changes)\n")
        
        # Step 1: Authentication
        print_section("STEP 1: AUTHENTICATION")
        print("Authenticating with Microsoft 365...")
        print("This requires one-time approval in your browser.\n")
        
        auth_handler = MSALAuth()
        access_token = auth_handler.get_access_token()
        
        # Step 2: Get user profile
        print_section("STEP 2: FETCHING USER PROFILE")
        graph_client = GraphClient(access_token)
        user_profile = graph_client.get_user_profile()
        
        user_email = user_profile.get('mail') or user_profile.get('userPrincipalName', 'Unknown')
        user_name = user_profile.get('displayName', 'User')
        
        print(f"✓ Authenticated as: {user_name} ({user_email})\n")
        
        # Step 3: Fetch calendar events
        print_section("STEP 3: FETCHING CALENDAR EVENTS")
        print(f"📅 Retrieving calendar events from the past {days_back} days...")
        calendar_events = graph_client.get_calendar_events(days_back=days_back)
        print(f"✓ Found {len(calendar_events)} calendar events\n")
        
        # Step 4: Fetch sent emails
        print_section("STEP 4: FETCHING SENT EMAILS")
        print(f"📧 Retrieving sent emails from the past {days_back} days...")
        sent_emails = graph_client.get_sent_emails(days_back=days_back)
        print(f"✓ Found {len(sent_emails)} sent emails\n")
        
        # Step 5: Analyze data
        print_section("STEP 5: ANALYZING DATA")
        print("🔍 Analyzing calendar and email data...")
        print("   - Identifying frequently discussed customers")
        print("   - Identifying key projects and topics")
        print("   - Ranking by frequency and relevance...\n")
        
        analyzer = DataAnalyzer()
        analysis_results = analyzer.analyze_data(calendar_events, sent_emails)
        
        top_items_count = len(analysis_results.get('top_items', []))
        print(f"✓ Identified {top_items_count} top items\n")
        
        # Step 6: Generate email draft
        print_section("STEP 6: GENERATING EMAIL DRAFT")
        print("✍️  Generating email draft in specified format...\n")
        
        user_info = {
            'email': user_email,
            'name': user_name
        }
        generator = EmailDraftGenerator(user_info=user_info)
        draft = generator.generate_draft(analysis_results)
        
        print("✓ Email draft generated successfully!\n")
        
        # Step 7: Display and save draft
        print_section("YOUR EMAIL DRAFT")
        print(f"\nSubject: {draft['subject']}\n")
        print("=" * 70 + "\n")
        print(draft['body'])
        print("\n" + "=" * 70 + "\n")
        
        # Save to file
        output_file = save_draft_to_file(draft)
        print(f"✓ Draft saved to: {output_file}\n")
        
        # Summary
        print_section("SUMMARY")
        print(f"✓ User: {user_name} ({user_email})")
        print(f"✓ Calendar events analyzed: {len(calendar_events)}")
        print(f"✓ Sent emails analyzed: {len(sent_emails)}")
        print(f"✓ Top items identified: {top_items_count}")
        print(f"✓ Draft saved to: {output_file}")
        print("\n" + "=" * 70 + "\n")
        
        print("🎉 Done! Your Top 5 Things email draft is ready.\n")
        print("📝 Copy the content above or use the saved file to create your email.\n")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.\n")
        return 1
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}\n")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())

