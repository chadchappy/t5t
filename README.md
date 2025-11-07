# Top 5 Things Email Generator

[![Build and Push Docker Image](https://github.com/chadchappy/t5t/actions/workflows/docker-build.yml/badge.svg)](https://github.com/chadchappy/t5t/actions/workflows/docker-build.yml)
[![Test Application](https://github.com/chadchappy/t5t/actions/workflows/test.yml/badge.svg)](https://github.com/chadchappy/t5t/actions/workflows/test.yml)

A simple CLI tool that analyzes your Microsoft 365 calendar and sent emails to generate a monthly "Top 5 Things" update email draft.

**🐳 Pre-built Docker images available at:** `ghcr.io/chadchappy/t5t:latest`

## Features

- 🔐 **Simple Authentication** - One-time device code flow
- 📅 **Calendar Analysis** - Identifies frequent meetings and topics
- 📧 **Email Analysis** - Analyzes sent emails for customer and project mentions
- 🤖 **AI-Powered Extraction** - Uses NLP to identify customers, projects, and topics
- 📝 **Formatted Draft Generation** - Creates email drafts in the specified format
- 🐳 **Containerized** - Runs in Docker with one simple command
- 🔒 **Privacy-First** - Read-only access, no data stored, local processing only

## Prerequisites

- Docker (or Colima/Minikube)
- Microsoft 365 account (Outlook)
- **For NVIDIA users:** Azure AD app registration required (see [NVIDIA Setup Guide](NVIDIA_SETUP.md))
- **For other users:** No Azure AD setup required

## Quick Start

> **⚠️ NVIDIA Users:** If you're using NVIDIA's Azure AD, you need to request an app registration from IT first. See the [NVIDIA Setup Guide](NVIDIA_SETUP.md) for detailed instructions.

### Using Pre-built Docker Image (Recommended)

```bash
# Pull and run the container
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest

# For NVIDIA users with custom Client ID:
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

**What happens:**
1. Container starts and displays a device code (e.g., `ABC-DEF-123`)
2. You visit `https://microsoft.com/devicelogin` in your browser
3. Enter the code and sign in with your Microsoft 365 account
4. Approve read-only access (Calendars.Read, Mail.Read, User.Read)
5. Container fetches your data, analyzes it, and generates the draft
6. Draft is displayed in terminal and saved to `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

**Example output:**
```
======================================================================
  TOP 5 THINGS EMAIL DRAFT GENERATOR
  Read-only access to your Microsoft 365 email and calendar
======================================================================

📊 Analysis period: Last 30 days
🔐 Authentication: Microsoft 365 (one-time device code flow)
📖 Access: Read-only (no emails sent, no calendar changes)

──────────────────────────────────────────────────────────────────────
  STEP 1: AUTHENTICATION
──────────────────────────────────────────────────────────────────────

To sign in, use a web browser to open the page:
    https://microsoft.com/devicelogin

And enter the code: ABC-DEF-123

Waiting for you to complete authentication...
✓ Authentication successful!

[... analysis steps ...]

──────────────────────────────────────────────────────────────────────
  YOUR EMAIL DRAFT
──────────────────────────────────────────────────────────────────────

Subject: Top 5 Things - Run:ai | NALA | SA

======================================================================

Run:ai -
Working with Databricks team on GPU fractions integration
Technical discussions with LinkedIn on multi-GPU workloads

NALA -
Ongoing PoV with customer for optimization features
Weekly sync meetings with technical champions

SA -
Solution architecture reviews for enterprise deployments

======================================================================

✓ Draft saved to: ./output/top5_draft_2025-11-07_143022.txt

🎉 Done! Your Top 5 Things email draft is ready.
```

### Customizing Analysis Period

```bash
# Analyze the past 60 days instead of 30
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Using with Colima

```bash
# Start Colima (if not already running)
colima start

# Run the container
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Using with Minikube

```bash
# Start Minikube
minikube start

# Pull and run
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

## How It Works

1. **Authentication**: Uses Microsoft's device code flow for secure, one-time authentication
   - No Azure AD app registration required
   - Uses Microsoft's public client ID
   - Read-only delegated permissions
2. **Data Collection**: Fetches calendar events and sent emails from the past 30 days via Microsoft Graph API
3. **Analysis**: Uses spaCy NLP to extract:
   - Organization names (customers/partners)
   - People mentioned
   - Technical topics and keywords
   - Project patterns (PoC, PoV, etc.)
4. **Ranking**: Ranks entities by frequency and relevance
5. **Draft Generation**: Creates a formatted email draft with fixed subject line:
   - **Subject:** `Top 5 Things - Run:ai | NALA | SA`
   - **Body:** Organized by customer/project with bullet points

## Security & Privacy

- ✅ **Read-only access** - Cannot send emails or modify calendar entries
- ✅ **No permanent storage** - Data is processed in memory only
- ✅ **Local processing** - Runs entirely in your local container
- ✅ **One-time authentication** - No persistent tokens stored
- ✅ **No external APIs** - All processing happens locally
- ✅ **No Azure AD setup** - Uses Microsoft's public client ID

## Configuration

### Environment Variables

You can customize the behavior with environment variables:

```bash
# Analyze the past 60 days instead of 30
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest

# Custom token cache location
docker run -it -e TOKEN_CACHE_FILE=/app/data/my_cache.json -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

Available options:
- `DAYS_BACK` - Number of days to analyze (default: 30)
- `TOKEN_CACHE_FILE` - Where to cache the auth token (default: ./data/token_cache.json)

### Customizing the Code

If you want to modify the email format or analysis logic:

1. Clone the repository:
   ```bash
   git clone https://github.com/chadchappy/t5t.git
   cd t5t
   ```

2. Edit the files:
   - `email_generator.py` - Modify email subject/body format
   - `analyzer.py` - Adjust NLP analysis and keyword extraction
   - `config.py` - Change default settings

3. Build and run locally:
   ```bash
   docker build -t t5t:custom .
   docker run -it -v $(pwd)/output:/app/output t5t:custom
   ```

## Troubleshooting

### "Failed to acquire token"

Make sure you:
1. Visited the correct URL (https://microsoft.com/devicelogin)
2. Entered the code exactly as shown
3. Signed in with your Microsoft 365 account
4. Approved the permissions when prompted

### "No calendar events found" or "No sent emails found"

- Check that you have calendar events/emails in the specified time period
- Make sure you're using the correct Microsoft 365 account
- Try increasing `DAYS_BACK` to analyze a longer period:
  ```bash
  docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
  ```

### Container won't start

- Verify Docker/Colima/Minikube is running: `docker ps`
- Check container logs: `docker logs <container-id>`
- Make sure you're using the `-it` flag for interactive mode

## Docker Images

### Available Images

Pre-built Docker images are automatically built and published to GitHub Container Registry:

- **Latest stable:** `ghcr.io/chadchappy/t5t:latest`
- **Specific commit:** `ghcr.io/chadchappy/t5t:<commit-sha>`

### Pulling Images

```bash
# Pull latest
docker pull ghcr.io/chadchappy/t5t:latest

# Run directly
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Automated Builds

Docker images are automatically built and pushed to GHCR when:
- Code is pushed to main branch
- Dockerfile or Python files are modified
- Manually triggered via GitHub Actions

## Development

### Local Development (without Docker)

```bash
# Clone the repository
git clone https://github.com/chadchappy/t5t.git
cd t5t

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the CLI script
python generate_draft.py
```

### Building from Source

```bash
# Clone the repository
git clone https://github.com/chadchappy/t5t.git
cd t5t

# Build the Docker image
docker build -t t5t:local .

# Run your local build
docker run -it -v $(pwd)/output:/app/output t5t:local
```

### Project Structure

```
.
├── generate_draft.py      # Main CLI script
├── auth.py                # MSAL authentication (device code flow)
├── config.py              # Configuration settings
├── graph_client.py        # Microsoft Graph API client
├── analyzer.py            # Data analysis and NLP
├── email_generator.py     # Email draft generation
├── outlook_applescript.py # AppleScript support for local Outlook
├── outlook_data_source.py # Unified data source with fallback
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Advanced Usage

### AppleScript Support (Mac Only)

If you have Outlook for Mac running locally, the app can optionally read from it directly using AppleScript (no authentication needed). This is implemented as a fallback option in `outlook_data_source.py`.

To use AppleScript mode:
1. Make sure Microsoft Outlook for Mac is running
2. The app will automatically try AppleScript first, then fall back to Graph API if needed

### Running the Web UI (Legacy)

The repository still contains the old Flask web UI in `app.py`. To run it:

```bash
# Install additional dependencies
pip install flask gunicorn

# Run the Flask app
python app.py

# Or with Docker
docker run -p 5000:5000 ghcr.io/chadchappy/t5t:latest python app.py
```

**Note:** The web UI is deprecated and may be removed in future versions. Use the CLI script instead.

## License

This is an internal tool. Not for public distribution.

## Support

For issues or questions:
- Open an issue on GitHub: https://github.com/chadchappy/t5t/issues
- Contact the maintainer

