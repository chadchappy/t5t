# Top 5 Things Email Draft Generator - CLI Version

Generate your monthly "Top 5 Things" email draft by analyzing your Microsoft 365 calendar and sent emails.

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Run the container (one-time authentication required)
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest

# Follow the prompts:
# 1. Visit https://microsoft.com/devicelogin
# 2. Enter the code shown
# 3. Sign in with your Microsoft 365 account
# 4. Approve read-only access
# 5. Wait for the draft to be generated
```

Your draft will be:
- Displayed in the terminal
- Saved to `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

### Using Python Locally

```bash
# Clone the repository
git clone https://github.com/chadchappy/t5t.git
cd t5t

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the script
python generate_draft.py
```

## 📧 What It Does

1. **Authenticates** with Microsoft 365 (one-time device code flow)
2. **Reads** your calendar events from the past 30 days
3. **Reads** your sent emails from the past 30 days
4. **Analyzes** the data to identify:
   - Most frequently discussed customers
   - Key projects and topics
   - PoC/PoV activities
5. **Generates** an email draft in this format:

```
Subject: Top 5 Things - Run:ai | NALA | SA

Run:ai -
[Your activities and updates related to Run:ai]

NALA -
[Your activities and updates related to NALA]

SA -
[Your activities and updates related to SA]

[Additional items...]
```

6. **Saves** the draft to a file for you to review and send

## 🔒 Security & Privacy

- ✅ **Read-only access** - Cannot send emails or create calendar entries
- ✅ **One-time authentication** - No persistent tokens stored
- ✅ **Local processing** - All analysis happens in the container
- ✅ **No data sent externally** - Your data stays with you
- ✅ **Open source** - Review the code yourself

## ⚙️ Configuration

### Environment Variables

You can customize the behavior with environment variables:

```bash
# Analyze the past 60 days instead of 30
docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

Available options:
- `DAYS_BACK` - Number of days to analyze (default: 30)
- `TOKEN_CACHE_FILE` - Where to cache the auth token (default: ./data/token_cache.json)

## 📝 Example Output

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

Authenticating with Microsoft 365...
This requires one-time approval in your browser.

To sign in, use a web browser to open the page:
    https://microsoft.com/devicelogin

And enter the code: ABC-DEF-123

Waiting for you to complete authentication in your browser...
✓ Authentication successful! Token cached for future use.

──────────────────────────────────────────────────────────────────────
  STEP 2: FETCHING USER PROFILE
──────────────────────────────────────────────────────────────────────

✓ Authenticated as: Chad Chapman (chad.chapman@nvidia.com)

──────────────────────────────────────────────────────────────────────
  STEP 3: FETCHING CALENDAR EVENTS
──────────────────────────────────────────────────────────────────────

📅 Retrieving calendar events from the past 30 days...
✓ Found 89 calendar events

──────────────────────────────────────────────────────────────────────
  STEP 4: FETCHING SENT EMAILS
──────────────────────────────────────────────────────────────────────

📧 Retrieving sent emails from the past 30 days...
✓ Found 247 sent emails

──────────────────────────────────────────────────────────────────────
  STEP 5: ANALYZING DATA
──────────────────────────────────────────────────────────────────────

🔍 Analyzing calendar and email data...
   - Identifying frequently discussed customers
   - Identifying key projects and topics
   - Ranking by frequency and relevance...

✓ Identified 7 top items

──────────────────────────────────────────────────────────────────────
  STEP 6: GENERATING EMAIL DRAFT
──────────────────────────────────────────────────────────────────────

✍️  Generating email draft in specified format...

✓ Email draft generated successfully!

──────────────────────────────────────────────────────────────────────
  YOUR EMAIL DRAFT
──────────────────────────────────────────────────────────────────────

Subject: Top 5 Things - Run:ai | NALA | SA

======================================================================

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

======================================================================

✓ Draft saved to: ./output/top5_draft_2025-11-07_143022.txt

──────────────────────────────────────────────────────────────────────
  SUMMARY
──────────────────────────────────────────────────────────────────────

✓ User: Chad Chapman (chad.chapman@nvidia.com)
✓ Calendar events analyzed: 89
✓ Sent emails analyzed: 247
✓ Top items identified: 7
✓ Draft saved to: ./output/top5_draft_2025-11-07_143022.txt

======================================================================

🎉 Done! Your Top 5 Things email draft is ready.

📝 Copy the content above or use the saved file to create your email.
```

## 🛠️ Troubleshooting

### "Failed to acquire token"

Make sure you:
1. Visited the correct URL (https://microsoft.com/devicelogin)
2. Entered the code exactly as shown
3. Signed in with your Microsoft 365 account
4. Approved the permissions

### "No calendar events found"

- Check that you have calendar events in the specified time period
- Make sure you're using the correct Microsoft 365 account
- Try increasing `DAYS_BACK` to analyze a longer period

### "No sent emails found"

- Check that you have sent emails in the specified time period
- Make sure you're using the correct Microsoft 365 account
- Try increasing `DAYS_BACK` to analyze a longer period

## 📦 Building the Docker Image

```bash
# Build locally
docker build -t t5t:latest .

# Run locally built image
docker run -it -v $(pwd)/output:/app/output t5t:latest
```

## 🤝 Contributing

This is a personal tool, but feel free to fork and customize for your needs!

## 📄 License

MIT License - See LICENSE file for details

