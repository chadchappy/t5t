from flask import Flask, render_template, request, jsonify
from outlook_data_source import OutlookDataSource
from analyzer import DataAnalyzer
from email_generator import EmailDraftGenerator
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize unified data source (AppleScript + Graph API fallback)
data_source = OutlookDataSource()

@app.route('/')
def index():
    """Home page"""
    # Get user info from data source
    try:
        user_profile = data_source.get_user_profile()
        user_info = {
            'email': user_profile.get('email', 'Unknown'),
            'name': user_profile.get('displayName', 'User'),
            'method': user_profile.get('method', 'Unknown')
        }
    except:
        user_info = {
            'email': 'Unknown',
            'name': 'User',
            'method': 'Not connected'
        }
    return render_template('index.html', user=user_info)

@app.route('/generate')
def generate_page():
    """Page to generate email draft"""
    # Get user info from data source
    try:
        user_profile = data_source.get_user_profile()
        user_info = {
            'email': user_profile.get('email', 'Unknown'),
            'name': user_profile.get('displayName', 'User'),
            'method': user_profile.get('method', 'Unknown')
        }
    except:
        user_info = {
            'email': 'Unknown',
            'name': 'User',
            'method': 'Not connected'
        }
    return render_template('generate.html', user=user_info)

@app.route('/api/generate', methods=['POST'])
def generate_draft():
    """API endpoint to generate email draft"""
    try:
        # Get parameters from request
        data = request.get_json() or {}
        days_back = data.get('days_back', Config.DAYS_TO_ANALYZE)

        print(f"\n{'='*60}")
        print(f"GENERATING TOP 5 THINGS EMAIL DRAFT")
        print(f"{'='*60}\n")

        # Fetch calendar events (tries AppleScript first, falls back to Graph API)
        print(f"📅 Fetching calendar events from past {days_back} days...")
        calendar_events = data_source.get_calendar_events(days_back=days_back)

        # Fetch sent emails (tries AppleScript first, falls back to Graph API)
        print(f"📧 Fetching sent emails from past {days_back} days...")
        sent_emails = data_source.get_sent_emails(days_back=days_back)

        # Analyze data
        print("🔍 Analyzing data...")
        analyzer = DataAnalyzer()
        analysis_results = analyzer.analyze_data(calendar_events, sent_emails)
        print(f"✓ Identified {len(analysis_results.get('top_items', []))} top items\n")

        # Generate email draft
        print("✍️  Generating email draft...")
        user_profile = data_source.get_user_profile()
        user_info = {
            'email': user_profile.get('email', 'Unknown'),
            'name': user_profile.get('displayName', 'User')
        }
        generator = EmailDraftGenerator(user_info=user_info)
        draft = generator.generate_draft(analysis_results)
        print("✓ Email draft generated successfully!\n")

        print(f"{'='*60}")
        print(f"SUMMARY")
        print(f"{'='*60}")
        print(f"Data source: {data_source.get_active_method()}")
        print(f"Calendar events analyzed: {len(calendar_events)}")
        print(f"Sent emails analyzed: {len(sent_emails)}")
        print(f"Top items identified: {len(analysis_results.get('top_items', []))}")
        print(f"{'='*60}\n")

        return jsonify({
            'success': True,
            'draft': draft,
            'analysis': {
                'calendar_events': len(calendar_events),
                'sent_emails': len(sent_emails),
                'top_items_count': len(analysis_results.get('top_items', [])),
                'data_source': data_source.get_active_method()
            }
        })

    except Exception as e:
        print(f"\n❌ Error generating draft: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """API endpoint to check connection status"""
    connection_status = data_source.test_connection()
    return jsonify({
        'configured': True,
        'connection_status': connection_status,
        'recommended_method': connection_status.get('recommended_method')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

