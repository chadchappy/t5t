# Top 5 Things Email Generator - Project Summary

## Overview

A containerized web application that automatically generates monthly "Top 5 Things" email drafts for NVIDIA employees by analyzing Outlook calendar events and sent emails.

## What It Does

1. **Authenticates** with Microsoft 365 using OAuth2 (read-only)
2. **Fetches** calendar events and sent emails from the past 30 days
3. **Analyzes** data using NLP to identify:
   - Most frequently mentioned customers/partners
   - Common topics and technical keywords
   - Active projects (PoC, PoV, etc.)
4. **Generates** a formatted email draft in NVIDIA's "Top 5 Things" format
5. **Displays** the draft for review, copy, or download

## Key Features

✅ **Secure & Private**
- Read-only access to calendar and email
- OAuth2 authentication via Microsoft
- No permanent data storage
- Runs entirely in local container

✅ **Smart Analysis**
- NLP-powered entity extraction using spaCy
- Frequency-based ranking
- Context extraction for each item
- Customizable keywords and patterns

✅ **Easy to Use**
- Simple web interface
- One-click draft generation
- Copy to clipboard or download
- Customizable analysis period (7-90 days)

✅ **Containerized**
- Works with Docker, Colima, or Minikube
- Isolated environment
- Easy deployment
- No local Python setup required

## Technology Stack

### Backend
- **Python 3.11** - Core language
- **Flask** - Web framework
- **MSAL** - Microsoft Authentication Library
- **Microsoft Graph API** - Calendar and email access
- **spaCy** - Natural Language Processing
- **Pandas/NumPy** - Data analysis

### Frontend
- **HTML/CSS/JavaScript** - Web UI
- **Responsive design** - Works on all devices

### Infrastructure
- **Docker** - Containerization
- **Gunicorn** - Production WSGI server
- **Docker Compose** - Multi-container orchestration

## Project Structure

```
t5tagent/
├── app.py                  # Main Flask application
├── auth.py                 # MSAL OAuth2 authentication
├── config.py               # Configuration settings
├── graph_client.py         # Microsoft Graph API client
├── analyzer.py             # NLP data analysis engine
├── email_generator.py      # Email draft generation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── docker-compose.yml      # Docker Compose config
├── Makefile                # Common commands
├── start.sh                # Quick start script
├── .env.example            # Environment template
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   └── generate.html      # Draft generation page
├── data/                   # Session data (gitignored)
├── README.md               # Full documentation
├── SETUP.md                # Detailed setup guide
├── QUICKSTART.md           # Quick start guide
└── PROJECT_SUMMARY.md      # This file
```

## How to Use

### First Time Setup

1. **Register Azure AD App** (one-time, ~3 minutes)
   - See SETUP.md for detailed instructions
   - Get Client ID, Tenant ID, and Client Secret

2. **Configure Environment** (~1 minute)
   ```bash
   make setup
   # Edit .env with your Azure AD credentials
   ```

3. **Start the App** (~1 minute)
   ```bash
   make start
   # or: ./start.sh
   # or: docker-compose up
   ```

### Regular Use

1. Open http://localhost:5000
2. Login with Microsoft 365
3. Click "Generate Draft"
4. Wait ~30 seconds
5. Copy or download the draft
6. Customize and send!

## Common Commands

```bash
make help       # Show all available commands
make setup      # Initial setup
make start      # Start the application
make stop       # Stop the application
make logs       # View logs
make clean      # Clean up containers
make test       # Test connectivity
```

Or use the start script:
```bash
./start.sh              # Start normally
./start.sh --rebuild    # Rebuild and start
```

## Security & Privacy

### What the App CAN Do
✅ Read your calendar events
✅ Read your sent emails
✅ Analyze data locally
✅ Generate email drafts

### What the App CANNOT Do
❌ Send emails
❌ Create/modify calendar events
❌ Access other people's data
❌ Store data permanently
❌ Share data externally

### Permissions Required
- `User.Read` - Read your profile
- `Calendars.Read` - Read calendar (read-only)
- `Mail.Read` - Read mail (read-only)

## Customization

### Change Analysis Period
- In UI: Adjust "Days to analyze" (7-90 days)
- In code: Edit `DAYS_TO_ANALYZE` in `config.py`

### Modify Email Format
Edit `email_generator.py`:
- Subject line format
- Body structure
- Number of items

### Add Custom Keywords
Edit `analyzer.py`:
```python
self.tech_keywords = {
    'your', 'custom', 'keywords'
}
```

### Change Port
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 8080 to your preferred port
```

## Output Format

The generated email follows this format:

```
Subject: Top 5 Things - [Top 3 Customers/Projects]

Industry Business Development / Account Updates

[Customer/Project Name] -
  [Context from meetings and emails]
  [Key activities and discussions]
  [Status and next steps]

[Next Customer/Project] -
  ...

---
Generated from X calendar events and Y sent emails
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Redirect URI mismatch | Ensure Azure AD URI is exactly `http://localhost:5000/callback` |
| Docker not running | Start Docker Desktop or `colima start` |
| Port 5000 in use | Change port in docker-compose.yml |
| No data found | Check you have events/emails in past 30 days |
| Authentication failed | Verify .env credentials match Azure AD |

## Performance

- **Startup time**: ~10 seconds
- **Analysis time**: 30-60 seconds (depends on data volume)
- **Memory usage**: ~500MB
- **Disk space**: ~1GB (container + dependencies)

## Limitations

- Analyzes up to 999 calendar events and 999 emails (Graph API limits)
- NLP accuracy depends on data quality
- Requires manual review and customization of draft
- English language only (spaCy model)

## Future Enhancements

Potential improvements:
- [ ] Support for multiple languages
- [ ] Integration with other email providers (Gmail, etc.)
- [ ] Machine learning for better topic extraction
- [ ] Historical tracking of generated drafts
- [ ] Email template customization UI
- [ ] Scheduled automatic generation
- [ ] Export to multiple formats (PDF, Word, etc.)

## Support

For issues or questions:
1. Check SETUP.md and README.md
2. Review troubleshooting section
3. Check container logs: `make logs`
4. Contact your IT department for Azure AD issues

## License

Internal tool for NVIDIA employees. Not for public distribution.

## Credits

Built with:
- Flask - https://flask.palletsprojects.com/
- MSAL - https://github.com/AzureAD/microsoft-authentication-library-for-python
- spaCy - https://spacy.io/
- Microsoft Graph API - https://developer.microsoft.com/graph

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-07  
**Author**: Built for NVIDIA employees

