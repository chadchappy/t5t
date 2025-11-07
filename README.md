# Top 5 Things Email Generator

[![Build and Push Docker Image](https://github.com/chadchappy/t5t/actions/workflows/docker-build.yml/badge.svg)](https://github.com/chadchappy/t5t/actions/workflows/docker-build.yml)
[![Test Application](https://github.com/chadchappy/t5t/actions/workflows/test.yml/badge.svg)](https://github.com/chadchappy/t5t/actions/workflows/test.yml)

An automated tool that analyzes your Microsoft 365 calendar and sent emails to generate a monthly "Top 5 Things" update email draft for NVIDIA employees.

**🐳 Pre-built Docker images available at:** `ghcr.io/chadchappy/t5t:latest`

## Features

- 🔐 **Automated API Access** - App-only authentication with Microsoft 365 (no interactive login required)
- 📅 **Calendar Analysis** - Identifies frequent meetings and topics
- 📧 **Email Analysis** - Analyzes sent emails for customer and project mentions
- 🤖 **AI-Powered Extraction** - Uses NLP to identify customers, projects, and topics
- 📝 **Formatted Draft Generation** - Creates email drafts in the specified NVIDIA format
- 🐳 **Containerized** - Runs locally in Docker/Colima/Minikube
- 🔒 **Privacy-First** - No data stored permanently, read-only API access

## Prerequisites

- Docker, Colima, or Minikube installed
- Microsoft 365 account (Outlook)
- Azure AD App Registration (see setup below)

## Quick Start

### Option A: Using Pre-built Docker Image (Fastest)

```bash
# 1. Pull the latest image
docker pull ghcr.io/chadchappy/t5t:latest

# 2. Create .env file with your Azure AD credentials
cp .env.example .env
# Edit .env with your values

# 3. Run the container
docker run -p 5000:5000 --env-file .env ghcr.io/chadchappy/t5t:latest

# 4. Open http://localhost:5000
```

### Option B: Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/chadchappy/t5t.git
cd t5t

# 2. Configure environment
cp .env.example .env
# Edit .env with your Azure AD credentials

# 3. Pull and start
docker-compose pull
docker-compose up

# 4. Open http://localhost:5000
```

### Option C: Build from Source

Follow the detailed setup instructions below.

## Detailed Setup

### 1. Azure AD App Registration

Before running the app, you need to register it in Azure AD for app-only authentication:

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Configure the app:
   - **Name**: Top 5 Things Generator
   - **Supported account types**: Accounts in this organizational directory only (Single tenant)
   - **Redirect URI**: Leave blank (not needed for app-only auth)
4. Click **Register**
5. Note down the **Application (client) ID** and **Directory (tenant) ID**
6. Go to **Certificates & secrets** > **New client secret**
   - Description: Top5Agent Secret
   - Expires: 24 months (or as per your org policy)
   - Click **Add** and copy the secret **Value** (you won't see it again!)
7. Go to **API permissions** > **Add a permission** > **Microsoft Graph** > **Application permissions**
   - **IMPORTANT:** Select "Application permissions" (NOT Delegated permissions)
   - Add these permissions:
     - `User.Read.All`
     - `Calendars.Read`
     - `Mail.Read`
   - Click **Add permissions**
   - Click **Grant admin consent** (REQUIRED - must have admin rights or request IT admin)

### 2. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your Azure AD details:
   ```bash
   CLIENT_ID=your-application-client-id
   CLIENT_SECRET=your-client-secret-value
   TENANT_ID=your-directory-tenant-id
   USER_EMAIL=your-email@company.com
   SECRET_KEY=generate-a-random-secret-key
   ```

3. Generate a secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

### 3. Run with Docker

```bash
# Build the container
docker build -t top5agent .

# Run the container
docker run -p 5000:5000 --env-file .env top5agent
```

Or use Docker Compose:

```bash
docker-compose up --build
```

### 4. Run with Colima

```bash
# Start Colima (if not already running)
colima start

# Build and run with Docker Compose
docker-compose up --build
```

### 5. Run with Minikube

```bash
# Start Minikube
minikube start

# Build the image in Minikube's Docker daemon
eval $(minikube docker-env)
docker build -t top5agent .

# Create a deployment
kubectl create deployment top5agent --image=top5agent:latest --port=5000

# Expose the service
kubectl expose deployment top5agent --type=NodePort --port=5000

# Get the URL
minikube service top5agent --url
```

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Click **Login with Microsoft 365**
3. Authenticate with your Microsoft account
4. Grant the requested permissions (read-only)
5. Click **Generate Email Draft**
6. Wait 30-60 seconds while the app analyzes your data
7. Review the generated draft
8. Copy to clipboard or download as text
9. Paste into your email client and customize as needed

## How It Works

1. **Authentication**: Uses OAuth2 to securely access your Microsoft 365 account with read-only permissions
2. **Data Collection**: Fetches calendar events and sent emails from the past 30 days via Microsoft Graph API
3. **Analysis**: Uses spaCy NLP to extract:
   - Organization names (customers/partners)
   - People mentioned
   - Technical topics and keywords
   - Project patterns (PoC, PoV, etc.)
4. **Ranking**: Ranks entities by frequency and relevance
5. **Draft Generation**: Creates a formatted email draft following the NVIDIA template

## Security & Privacy

- ✅ **Read-only access** - Cannot send emails or modify calendar
- ✅ **No permanent storage** - Data is processed in memory only
- ✅ **Local processing** - Runs entirely in your local container
- ✅ **Session-based** - Tokens stored only in session, cleared on logout
- ✅ **No external APIs** - All processing happens locally

## Customization

### Adjust Analysis Period

Change the number of days to analyze (default: 30):
- In the web UI: Use the "Days to analyze" input field
- In code: Edit `DAYS_TO_ANALYZE` in `config.py`

### Modify Email Format

Edit `email_generator.py` to customize:
- Subject line format
- Body structure
- Number of items (default: 5-7)

### Add Custom Keywords

Edit `analyzer.py` to add domain-specific keywords:
```python
self.tech_keywords = {
    'your', 'custom', 'keywords', 'here'
}
```

## Troubleshooting

### "Authentication failed"
- Verify your Azure AD app credentials in `.env`
- Ensure redirect URI matches exactly: `http://localhost:5000/callback`
- Check that API permissions are granted

### "No data found"
- Ensure you have calendar events and sent emails in the past 30 days
- Check that you granted the required permissions
- Try increasing the analysis period

### Container won't start
- Verify Docker/Colima/Minikube is running
- Check that port 5000 is not already in use
- Review container logs: `docker logs <container-id>`

## Docker Images

### Available Images

Pre-built Docker images are automatically built and published to GitHub Container Registry:

- **Latest stable:** `ghcr.io/chadchappy/t5t:latest`
- **Main branch:** `ghcr.io/chadchappy/t5t:main`
- **Specific commit:** `ghcr.io/chadchappy/t5t:sha-<commit>`

### Pulling Images

```bash
# Pull latest
docker pull ghcr.io/chadchappy/t5t:latest

# Pull specific version
docker pull ghcr.io/chadchappy/t5t:v1.0.0
```

### Automated Builds

Docker images are automatically built and pushed to GHCR when:
- Code is pushed to main/master branch
- Dockerfile or Python files are modified
- Manually triggered via GitHub Actions

See [DEPLOYMENT.md](DEPLOYMENT.md) for more deployment options.

## Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the app
python app.py
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

GitHub Actions will automatically:
- Run tests on your PR
- Build Docker image (but not push)
- Report status

### Project Structure

```
.
├── app.py                 # Main Flask application
├── auth.py               # MSAL authentication handler
├── config.py             # Configuration settings
├── graph_client.py       # Microsoft Graph API client
├── analyzer.py           # Data analysis and NLP
├── email_generator.py    # Email draft generation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── generate.html
├── Dockerfile            # Container definition
├── docker-compose.yml    # Docker Compose configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## License

This is an internal tool for NVIDIA employees. Not for public distribution.

## Support

For issues or questions, contact your IT department or the tool maintainer.

