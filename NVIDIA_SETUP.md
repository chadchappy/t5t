# Setup Guide for NVIDIA Users

This guide is specifically for NVIDIA employees who need to set up the Top 5 Things Email Generator with NVIDIA's Azure AD.

## Why You Need This

NVIDIA's Azure AD requires pre-authorization for third-party applications. The default public client ID won't work, so you need to request IT to create a custom Azure AD app registration.

## Step 1: Request Azure AD App Registration from IT

Send this email to your IT support team:

---

**Subject:** Azure AD App Registration Request - Top 5 Things Email Generator

**Body:**

Hi IT Team,

I need an Azure AD app registration created for a personal productivity tool that generates email drafts by analyzing my Outlook calendar and sent emails.

**App Details:**
- **Name:** Top 5 Things Generator (or similar)
- **Supported account types:** Single tenant (NVIDIA only)
- **Redirect URI:** Not needed (uses device code flow)
- **Authentication:** Public client (device code flow)

**Required API Permissions (Microsoft Graph - Delegated):**
- `User.Read` - Read user profile
- `Calendars.Read` - Read user's calendar  
- `Mail.Read` - Read user's mail

**Important Notes:**
- These are **delegated permissions** (not application permissions) - the app accesses data on behalf of the signed-in user only
- **No admin consent required** for delegated permissions
- **Read-only access** - cannot send emails or modify calendar
- The app runs locally in a Docker container on my machine
- Uses device code flow authentication (no client secret needed)

**What I need from you:**
- The **Application (client) ID** after registration

**Optional (if you want to review the code):**
- GitHub repository: https://github.com/chadchappy/t5t

Please let me know if you need any additional information.

Thanks!

---

## Step 2: Configure the Application

Once IT provides the **Client ID**, follow these steps:

### Option A: Using Environment Variable (Recommended for Docker)

1. **Create a `.env` file** in the project directory:
   ```bash
   cd /path/to/t5tagent
   cp .env.example .env
   ```

2. **Edit the `.env` file**:
   ```bash
   nano .env
   ```

3. **Add your Client ID**:
   ```bash
   CLIENT_ID=your-client-id-from-IT
   ```

4. **Save and exit** (Ctrl+X, then Y, then Enter)

### Option B: Using Docker Environment Variable (No .env file needed)

You can pass the Client ID directly when running the container:

```bash
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

## Step 3: Run the Application

### Using Pre-built Docker Image (Easiest)

```bash
# Pull the latest image
docker pull ghcr.io/chadchappy/t5t:latest

# Run with your Client ID
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

### Building Locally

```bash
# Clone the repository
git clone https://github.com/chadchappy/t5t.git
cd t5t

# Create .env file with your Client ID
echo "CLIENT_ID=your-client-id-from-IT" > .env

# Build the Docker image
docker build -t t5t:local .

# Run the container
docker run -it -v $(pwd)/output:/app/output t5t:local
```

## Step 4: Authenticate

When you run the container, you'll see:

```
============================================================
AUTHENTICATION REQUIRED
============================================================
To sign in, use a web browser to open the page 
https://microsoft.com/devicelogin and enter the code ABC-123-XYZ

============================================================
Waiting for you to complete authentication in your browser...
============================================================
```

1. **Open your browser** and go to `https://microsoft.com/devicelogin`
2. **Enter the code** shown in the terminal
3. **Sign in** with your NVIDIA Microsoft 365 account
4. **Click "Accept"** to grant permissions

The app will then:
- Fetch your calendar events (past 30 days)
- Fetch your sent emails (past 30 days)
- Analyze the data
- Generate your email draft
- Save it to `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

## Troubleshooting

### Error: "AADSTS65002: Consent between first party application..."

This means you're still using the default public client ID. Make sure you:
1. Got the Client ID from IT
2. Set it in your `.env` file or passed it via `-e CLIENT_ID=...`
3. Rebuilt the Docker image if using local build

### Error: "AADSTS50020: User account from identity provider does not exist"

You're trying to sign in with a personal Microsoft account instead of your NVIDIA work account. Use your `@nvidia.com` email address.

### Error: "No calendar events found" or "No sent emails found"

This is normal if you don't have data in the past 30 days. You can increase the analysis period:

```bash
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -e DAYS_BACK=60 \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

### Token Expired

Tokens typically last 60-90 days. When expired, just run the container again and re-authenticate.

## Security Notes

- **Read-only access**: The app cannot send emails or modify your calendar
- **Local execution**: All processing happens in your local Docker container
- **Token caching**: Authentication tokens are cached in `./data/token_cache.json` to avoid re-authentication on every run
- **Delegated permissions**: The app accesses data on your behalf, not as a service account

## Support

If you encounter issues:
1. Check this troubleshooting guide
2. Review the main documentation: `README.md`, `QUICKSTART.md`, `AUTHENTICATION.md`
3. Open an issue: https://github.com/chadchappy/t5t/issues

## What IT Needs to Know

If IT has questions about the app registration:

**Q: Why delegated permissions instead of application permissions?**
A: Delegated permissions access data on behalf of the signed-in user only. Application permissions would require admin consent and access all users' data, which is unnecessary and a security risk.

**Q: Why no redirect URI?**
A: The app uses device code flow, which doesn't require a redirect URI. The user authenticates in their own browser, not in the app.

**Q: Is this secure?**
A: Yes. The app:
- Uses Microsoft's official authentication libraries (MSAL)
- Requests only read-only permissions
- Runs locally in a Docker container
- Doesn't store passwords or credentials
- Uses standard OAuth2 device code flow

**Q: Can we review the code?**
A: Absolutely! The code is open source: https://github.com/chadchappy/t5t

