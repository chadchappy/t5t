# Setup Guide - Top 5 Things Email Generator

This guide will walk you through setting up the Top 5 Things Email Generator.

## Prerequisites

- **Docker** (or Colima/Minikube) installed and running
- **Microsoft 365 account** (work/school account)
- **That's it!** No Azure AD setup required

## Quick Setup (2 minutes)

### Step 1: Install Docker

If you don't have Docker installed:

**macOS:**
```bash
# Option 1: Docker Desktop
# Download from https://www.docker.com/products/docker-desktop

# Option 2: Colima (lightweight alternative)
brew install colima docker
colima start
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

**Windows:**
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
```

### Step 2: Run the Container

```bash
# Pull and run the container
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Step 3: Authenticate

The container will display:

```
To sign in, use a web browser to open the page:
    https://microsoft.com/devicelogin

And enter the code: ABC-DEF-123
```

1. Open `https://microsoft.com/devicelogin` in your browser
2. Enter the code shown (e.g., `ABC-DEF-123`)
3. Sign in with your Microsoft 365 account
4. Click **Accept** to grant read-only permissions

### Step 4: Get Your Draft

The container will:
- Fetch your calendar events (past 30 days)
- Fetch your sent emails (past 30 days)
- Analyze the data
- Generate and display your email draft
- Save it to `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

**Done!** Your draft is ready to use.

## Advanced Setup

### Customizing Analysis Period

```bash
# Analyze the past 60 days instead of 30
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Building from Source

If you want to modify the code:

1. **Clone the repository**
   ```bash
   git clone https://github.com/chadchappy/t5t.git
   cd t5t
   ```

2. **Edit the code**
   - `email_generator.py` - Modify email format
   - `analyzer.py` - Adjust NLP analysis
   - `config.py` - Change default settings

3. **Build and run**
   ```bash
   docker build -t t5t:custom .
   docker run -it -v $(pwd)/output:/app/output t5t:custom
   ```

### Running Locally (Without Docker)

If you prefer to run without Docker:

1. **Clone the repository**
   ```bash
   git clone https://github.com/chadchappy/t5t.git
   cd t5t
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Run the CLI script**
   ```bash
   python generate_draft.py
   ```

## Troubleshooting

### "Failed to acquire token"
- **Solution**: Make sure you:
  1. Visited `https://microsoft.com/devicelogin` (not a different URL)
  2. Entered the code exactly as shown
  3. Signed in with your Microsoft 365 work account
  4. Clicked "Accept" to grant permissions

### "Docker not running"
- **Solution**:
  ```bash
  # For Docker Desktop: Check if it's running in your menu bar
  # For Colima:
  colima status
  colima start  # if not running
  ```

### "No calendar events found" or "No sent emails found"
- **Solution**:
  - Make sure you have events/emails in the past 30 days
  - Verify you granted permissions when authenticating
  - Try increasing the analysis period:
    ```bash
    docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
    ```

### "Permission denied" on output folder
- **Solution**:
  ```bash
  mkdir -p output
  chmod 755 output
  ```

### Token expired
- **Solution**: Just run the container again and re-authenticate. Tokens typically last 60-90 days.

## Security Best Practices

1. **Run in trusted environment**
   - Only run the container on your own machine
   - Don't share your token cache file

2. **Review permissions**
   - The app only requests read-only access
   - You can review permissions before accepting

3. **Keep container updated**
   - Pull the latest image regularly:
     ```bash
     docker pull ghcr.io/chadchappy/t5t:latest
     ```

4. **Monitor access**
   - Check Microsoft 365 audit logs periodically
   - Review your account's app permissions at https://account.microsoft.com/privacy/app-permissions

5. **Revoke access when done**
   - If you stop using the app, revoke its permissions
   - Delete the token cache: `rm -rf ./data/token_cache.json`

## Next Steps

- Customize the email template in `email_generator.py`
- Add custom keywords in `analyzer.py`
- Adjust analysis period with `DAYS_BACK` environment variable

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review the documentation:
   - `README.md` - Full documentation
   - `QUICKSTART.md` - Quick start guide
   - `AUTHENTICATION.md` - Authentication details
3. Open an issue: https://github.com/chadchappy/t5t/issues

