from flask import Flask, render_template, request, jsonify
from auth import MSALAuth
from graph_client import GraphClient
from analyzer import DataAnalyzer
from email_generator import EmailDraftGenerator
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize auth handler
auth_handler = MSALAuth()

@app.route('/')
def index():
    """Home page"""
    user_info = {
        'email': Config.USER_EMAIL,
        'name': Config.USER_EMAIL.split('@')[0] if Config.USER_EMAIL else 'User'
    }
    return render_template('index.html', user=user_info)

@app.route('/generate')
def generate_page():
    """Page to generate email draft"""
    user_info = {
        'email': Config.USER_EMAIL,
        'name': Config.USER_EMAIL.split('@')[0] if Config.USER_EMAIL else 'User'
    }
    return render_template('generate.html', user=user_info)

@app.route('/api/generate', methods=['POST'])
def generate_draft():
    """API endpoint to generate email draft"""
    try:
        # Get parameters from request
        data = request.get_json() or {}
        days_back = data.get('days_back', Config.DAYS_TO_ANALYZE)

        # Get access token using app-only authentication
        print("Acquiring access token...")
        access_token = auth_handler.get_access_token()

        # Initialize Graph client
        graph_client = GraphClient(access_token, Config.USER_EMAIL)

        # Fetch calendar events
        print(f"Fetching calendar events from past {days_back} days for {Config.USER_EMAIL}...")
        calendar_events = graph_client.get_calendar_events(days_back=days_back)
        print(f"Found {len(calendar_events)} calendar events")

        # Fetch sent emails
        print(f"Fetching sent emails from past {days_back} days for {Config.USER_EMAIL}...")
        sent_emails = graph_client.get_sent_emails(days_back=days_back)
        print(f"Found {len(sent_emails)} sent emails")

        # Analyze data
        print("Analyzing data...")
        analyzer = DataAnalyzer()
        analysis_results = analyzer.analyze_data(calendar_events, sent_emails)

        # Generate email draft
        print("Generating email draft...")
        user_info = {
            'email': Config.USER_EMAIL,
            'name': Config.USER_EMAIL.split('@')[0] if Config.USER_EMAIL else 'User'
        }
        generator = EmailDraftGenerator(user_info=user_info)
        draft = generator.generate_draft(analysis_results)

        return jsonify({
            'success': True,
            'draft': draft,
            'analysis': {
                'calendar_events': len(calendar_events),
                'sent_emails': len(sent_emails),
                'top_items_count': len(analysis_results.get('top_items', []))
            }
        })

    except Exception as e:
        print(f"Error generating draft: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """API endpoint to check configuration status"""
    return jsonify({
        'configured': bool(Config.CLIENT_ID and Config.CLIENT_SECRET and Config.USER_EMAIL),
        'user_email': Config.USER_EMAIL
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

