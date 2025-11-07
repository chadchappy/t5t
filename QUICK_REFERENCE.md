# Quick Reference - Once You Have the Client ID

## What You Need from IT
- **Application (client) ID** (looks like: `12345678-1234-1234-1234-123456789abc`)

## Setup (One-Time)

### Option 1: Create .env File (Recommended)
```bash
cd /Users/chadc/Documents/augment-projects/t5tagent
echo "CLIENT_ID=your-client-id-from-IT" > .env
```

### Option 2: Pass as Environment Variable
No setup needed - just use the command in "Run" section below.

## Run

### Option 1: With .env File
```bash
cd /Users/chadc/Documents/augment-projects/t5tagent
docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
```

### Option 2: With Environment Variable
```bash
cd /Users/chadc/Documents/augment-projects/t5tagent
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

### Option 3: Build and Run Locally
```bash
cd /Users/chadc/Documents/augment-projects/t5tagent
echo "CLIENT_ID=your-client-id-from-IT" > .env
docker build -t t5t:local .
docker run -it -v $(pwd)/output:/app/output t5t:local
```

## Authentication Flow

1. Container displays a code (e.g., `ABC-DEF-123`)
2. Open browser → `https://microsoft.com/devicelogin`
3. Enter the code
4. Sign in with your `@nvidia.com` account
5. Click "Accept" to approve permissions
6. Wait for draft generation
7. Draft saved to `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`

## Customization

### Analyze More Days
```bash
docker run -it \
  -e CLIENT_ID=your-client-id-from-IT \
  -e DAYS_BACK=60 \
  -v $(pwd)/output:/app/output \
  ghcr.io/chadchappy/t5t:latest
```

### Use Latest Code from GitHub
```bash
cd /Users/chadc/Documents/augment-projects/t5tagent
git pull origin main
docker build -t t5t:local .
docker run -it -v $(pwd)/output:/app/output t5t:local
```

## Troubleshooting

### Still Getting AADSTS65002 Error?
- Make sure you created the `.env` file OR passed `-e CLIENT_ID=...`
- Verify the Client ID is correct (no extra spaces)
- If using local build, rebuild after creating `.env`: `docker build -t t5t:local .`

### No Calendar/Email Data Found?
- Increase analysis period: `-e DAYS_BACK=60`
- Check that you have calendar events and sent emails in that period

### Token Expired?
- Just run the container again and re-authenticate
- Tokens typically last 60-90 days

## Files

- **Draft output:** `./output/top5_draft_YYYY-MM-DD_HHMMSS.txt`
- **Token cache:** `./data/token_cache.json` (auto-created)
- **Configuration:** `.env` (you create this)

## Support

- Full documentation: [README.md](README.md)
- NVIDIA-specific guide: [NVIDIA_SETUP.md](NVIDIA_SETUP.md)
- Quick start: [QUICKSTART.md](QUICKSTART.md)
- Authentication details: [AUTHENTICATION.md](AUTHENTICATION.md)

