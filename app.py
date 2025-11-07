from flask import Flask, render_template, redirect, url_for, session, request, jsonify
import msal
import json
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
    if 'user' not in session:
        return render_template('index.html', logged_in=False)
    return render_template('index.html', logged_in=True, user=session['user'])

@app.route('/login')
def login():
    """Initiate OAuth login flow"""
    auth_url = auth_handler.get_auth_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """OAuth callback handler"""
    # Get authorization code from query params
    auth_code = request.args.get('code')
    
    if not auth_code:
        return "Error: No authorization code received", 400
    
    # Exchange code for token
    result = auth_handler.get_token_from_code(auth_code)
    
    if 'error' in result:
        return f"Error: {result.get('error_description', 'Authentication failed')}", 400
    
    # Store token and user info in session
    session['access_token'] = result['access_token']
    
    # Get user profile
    graph_client = GraphClient(result['access_token'])
    user_profile = graph_client.get_user_profile()
    session['user'] = {
        'name': user_profile.get('displayName', 'User'),
        'email': user_profile.get('mail') or user_profile.get('userPrincipalName', '')
    }
    
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/generate')
def generate_page():
    """Page to generate email draft"""
    if 'access_token' not in session:
        return redirect(url_for('login'))
    
    return render_template('generate.html', user=session.get('user'))

@app.route('/api/generate', methods=['POST'])
def generate_draft():
    """API endpoint to generate email draft"""
    if 'access_token' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Get parameters from request
        data = request.get_json() or {}
        days_back = data.get('days_back', Config.DAYS_TO_ANALYZE)
        
        # Initialize Graph client
        graph_client = GraphClient(session['access_token'])
        
        # Fetch calendar events
        print(f"Fetching calendar events from past {days_back} days...")
        calendar_events = graph_client.get_calendar_events(days_back=days_back)
        print(f"Found {len(calendar_events)} calendar events")
        
        # Fetch sent emails
        print(f"Fetching sent emails from past {days_back} days...")
        sent_emails = graph_client.get_sent_emails(days_back=days_back)
        print(f"Found {len(sent_emails)} sent emails")
        
        # Analyze data
        print("Analyzing data...")
        analyzer = DataAnalyzer()
        analysis_results = analyzer.analyze_data(calendar_events, sent_emails)
        
        # Generate email draft
        print("Generating email draft...")
        generator = EmailDraftGenerator(user_info=session.get('user'))
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
    """API endpoint to check authentication status"""
    return jsonify({
        'authenticated': 'access_token' in session,
        'user': session.get('user')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

