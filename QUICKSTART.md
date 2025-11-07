# Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Docker Desktop, Colima, or Minikube installed and running
- Microsoft 365 (Outlook) account
- 5 minutes to set up Azure AD app

## Step 1: Azure AD Setup (One-time, ~3 minutes)

1. Go to https://portal.azure.com
2. Navigate to **Azure Active Directory** → **App registrations** → **New registration**
3. Fill in:
   - Name: `Top 5 Things Generator`
   - Supported account types: Single tenant
   - Redirect URI: Leave blank
4. Click **Register** and save the **Client ID** and **Tenant ID**
5. Go to **Certificates & secrets** → **New client secret** → Save the secret value
6. Go to **API permissions** → **Add permission** → **Microsoft Graph** → **Application permissions**:
   - Add: `User.Read.All`, `Calendars.Read`, `Mail.Read`
   - Click **Grant admin consent** (REQUIRED - must have admin rights)

## Step 2: Configure App (~1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure AD details
nano .env  # or use your preferred editor

# Generate a secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
# Copy the output and paste as SECRET_KEY in .env
```

Your `.env` should look like:
```
CLIENT_ID=abc123...
CLIENT_SECRET=xyz789...
TENANT_ID=def456...
USER_EMAIL=your-email@company.com
SECRET_KEY=generated-random-key
```

## Step 3: Run the App (~1 minute)

### Option A: Using the start script (easiest)
```bash
./start.sh
```

### Option B: Using Docker Compose
```bash
docker-compose up --build
```

### Option C: Using Colima
```bash
colima start
docker-compose up --build
```

## Step 4: Use the App

1. Open http://localhost:5000 in your browser
2. Click **Login with Microsoft 365**
3. Authenticate and grant permissions
4. Click **Generate Draft**
5. Wait ~30 seconds for analysis
6. Copy or download your email draft!

## What You'll Get

A formatted email draft like:

```
Subject: Top 5 Things - Apple | Azure | LinkedIn

Industry Business Development / Account Updates

Apple -
  Testing and confirming Kuberay functionality with Run:ai features
  Multi-GPU fractions for Ray distributed workloads
  Technical champion sees value in Run:ai fractions

Azure Partnership -
  Working with team to validate Run:ai on Azure GPU nodes
  Presented to GBB tech team at Azure

LinkedIn -
  Successful EBC with leadership focused on Optimization/Efficiency
  Development team evaluating Run:ai fractions

...
```

## Troubleshooting

**"Redirect URI mismatch"**
→ Make sure Azure AD redirect URI is exactly `http://localhost:5000/callback`

**"Docker not running"**
→ Start Docker Desktop or run `colima start`

**"Port 5000 in use"**
→ Stop other services or change port in docker-compose.yml

**"No data found"**
→ Make sure you have calendar events and sent emails in the past 30 days

## Next Steps

- Customize keywords in `analyzer.py`
- Modify email format in `email_generator.py`
- Adjust analysis period in the web UI (7-90 days)

## Need Help?

See detailed instructions in:
- `SETUP.md` - Complete setup guide
- `README.md` - Full documentation

