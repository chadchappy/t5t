# Quick Start Guide

Get up and running in 2 minutes!

## Prerequisites

- Docker Desktop, Colima, or Minikube installed and running
- Microsoft 365 (Outlook) account
- **That's it!** No Azure AD setup required

## Step 1: Run the Container

```bash
# Pull and run the container
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

**Using Colima?**
```bash
colima start
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

## Step 2: Authenticate

The container will display something like:

```
To sign in, use a web browser to open the page:
    https://microsoft.com/devicelogin

And enter the code: ABC-DEF-123
```

1. Open `https://microsoft.com/devicelogin` in your browser
2. Enter the code shown (e.g., `ABC-DEF-123`)
3. Sign in with your Microsoft 365 account
4. Click **Accept** to grant read-only permissions

## Step 3: Wait for Analysis

The container will:
1. ✓ Fetch your calendar events (past 30 days)
2. ✓ Fetch your sent emails (past 30 days)
3. ✓ Analyze the data using NLP
4. ✓ Generate your email draft
5. ✓ Display and save the draft

This takes about 30-60 seconds.

## Step 4: Get Your Draft

The draft will be:
- **Displayed in the terminal** - Copy directly from there
- **Saved to a file** - Check `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

## What You'll Get

A formatted email draft with a **fixed subject line**:

```
Subject: Top 5 Things - Run:ai | NALA | SA

Run:ai -
Working with Databricks team on GPU fractions integration
Technical discussions with LinkedIn on multi-GPU workloads
Presented to Azure GBB tech team

NALA -
Ongoing PoV with customer for optimization features
Weekly sync meetings with technical champions

SA -
Solution architecture reviews for enterprise deployments
Best practices documentation updates

...
```

## Customization

### Analyze More Days

```bash
# Analyze the past 60 days instead of 30
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Modify the Code

```bash
# Clone and customize
git clone https://github.com/chadchappy/t5t.git
cd t5t

# Edit files:
# - email_generator.py (change subject/body format)
# - analyzer.py (adjust NLP analysis)
# - config.py (change defaults)

# Build and run
docker build -t t5t:custom .
docker run -it -v $(pwd)/output:/app/output t5t:custom
```

## Troubleshooting

**"Failed to acquire token"**
→ Make sure you entered the code correctly at https://microsoft.com/devicelogin

**"Docker not running"**
→ Start Docker Desktop or run `colima start`

**"No calendar events found" or "No sent emails found"**
→ Make sure you have data in the past 30 days, or increase `DAYS_BACK`:
```bash
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

**"Permission denied" on output folder**
→ Make sure the output directory is writable:
```bash
mkdir -p output
chmod 755 output
```

## Advanced Usage

### Run Without Docker

```bash
git clone https://github.com/chadchappy/t5t.git
cd t5t
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python generate_draft.py
```

### Use AppleScript (Mac Only)

If you have Outlook for Mac running, the app will automatically try to read from it locally first (no authentication needed), then fall back to Microsoft Graph API if needed.

## Need Help?

See detailed documentation:
- `README.md` - Full documentation
- `README_CLI.md` - CLI usage examples
- Open an issue: https://github.com/chadchappy/t5t/issues

