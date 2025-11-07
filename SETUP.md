# Setup Guide - Top 5 Things Email Generator

This guide will walk you through setting up the Top 5 Things Email Generator from scratch.

## Step 1: Azure AD App Registration

### Why do we need this?
To access your Outlook calendar and emails securely, we need to register this app with Microsoft Azure AD. This gives the app permission to read (but not modify) your data.

### Registration Steps

1. **Go to Azure Portal**
   - Navigate to https://portal.azure.com
   - Sign in with your NVIDIA Microsoft 365 account

2. **Navigate to App Registrations**
   - Click on "Azure Active Directory" in the left sidebar
   - Click on "App registrations"
   - Click "New registration"

3. **Configure the Application**
   - **Name**: `Top 5 Things Generator` (or any name you prefer)
   - **Supported account types**: Select "Accounts in this organizational directory only (NVIDIA only - Single tenant)"
   - **Redirect URI**: 
     - Platform: Web
     - URI: `http://localhost:5000/callback`
   - Click **Register**

4. **Save Application Details**
   - After registration, you'll see the app overview page
   - **Copy and save** the following (you'll need these later):
     - Application (client) ID
     - Directory (tenant) ID

5. **Create a Client Secret**
   - In the left sidebar, click "Certificates & secrets"
   - Click "New client secret"
   - Description: `Top5Agent Secret`
   - Expires: Choose 24 months (or per your org policy)
   - Click **Add**
   - **IMPORTANT**: Copy the secret **Value** immediately (you won't be able to see it again!)

6. **Configure API Permissions**
   - In the left sidebar, click "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph"
   - Select "Delegated permissions"
   - Search for and add these permissions:
     - ✅ `User.Read` - Read your profile
     - ✅ `Calendars.Read` - Read your calendar
     - ✅ `Mail.Read` - Read your mail
   - Click "Add permissions"
   
7. **Grant Admin Consent** (if applicable)
   - If you have admin rights, click "Grant admin consent for [Your Org]"
   - If not, you may need to request IT admin to grant consent
   - This step may not be required depending on your org's policies

## Step 2: Configure the Application

1. **Copy the environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file**
   ```bash
   nano .env  # or use your preferred editor
   ```

3. **Fill in your Azure AD details**
   ```
   CLIENT_ID=<paste your Application (client) ID>
   CLIENT_SECRET=<paste your client secret value>
   TENANT_ID=<paste your Directory (tenant) ID>
   SECRET_KEY=<generate a random key - see below>
   REDIRECT_URI=http://localhost:5000/callback
   ```

4. **Generate a SECRET_KEY**
   ```bash
   python3 -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copy the output and paste it as your SECRET_KEY in .env

## Step 3: Choose Your Container Platform

### Option A: Docker (Recommended)

1. **Install Docker Desktop** (if not already installed)
   - Download from https://www.docker.com/products/docker-desktop

2. **Build and run**
   ```bash
   docker-compose up --build
   ```

3. **Access the app**
   - Open browser to http://localhost:5000

### Option B: Colima (macOS alternative to Docker Desktop)

1. **Install Colima**
   ```bash
   brew install colima docker docker-compose
   ```

2. **Start Colima**
   ```bash
   colima start
   ```

3. **Build and run**
   ```bash
   docker-compose up --build
   ```

4. **Access the app**
   - Open browser to http://localhost:5000

### Option C: Minikube (Kubernetes)

1. **Install Minikube**
   ```bash
   brew install minikube
   ```

2. **Start Minikube**
   ```bash
   minikube start
   ```

3. **Build in Minikube's Docker**
   ```bash
   eval $(minikube docker-env)
   docker build -t top5agent .
   ```

4. **Create Kubernetes resources**
   ```bash
   # Create deployment
   kubectl create deployment top5agent --image=top5agent:latest --port=5000
   
   # Create ConfigMap for environment variables
   kubectl create configmap top5agent-config \
     --from-literal=CLIENT_ID=$CLIENT_ID \
     --from-literal=TENANT_ID=$TENANT_ID \
     --from-literal=REDIRECT_URI=http://localhost:5000/callback
   
   # Create Secret for sensitive data
   kubectl create secret generic top5agent-secret \
     --from-literal=CLIENT_SECRET=$CLIENT_SECRET \
     --from-literal=SECRET_KEY=$SECRET_KEY
   
   # Expose the service
   kubectl expose deployment top5agent --type=NodePort --port=5000
   
   # Get the URL
   minikube service top5agent --url
   ```

5. **Access the app**
   - Use the URL from the last command

## Step 4: First Run

1. **Open the application**
   - Navigate to http://localhost:5000 in your browser

2. **Login**
   - Click "Login with Microsoft 365"
   - You'll be redirected to Microsoft login
   - Sign in with your NVIDIA account
   - Grant the requested permissions

3. **Generate your first draft**
   - Click "Generate Draft"
   - Wait 30-60 seconds for analysis
   - Review the generated email draft

## Troubleshooting

### "AADSTS50011: The redirect URI specified in the request does not match"
- **Solution**: Make sure the redirect URI in Azure AD exactly matches `http://localhost:5000/callback`

### "AADSTS65001: The user or administrator has not consented"
- **Solution**: Go back to Azure AD > API permissions and grant admin consent

### "Connection refused" or "Cannot connect to Docker daemon"
- **Solution**: Make sure Docker/Colima is running
  ```bash
  # For Docker Desktop: Check if it's running in your menu bar
  # For Colima:
  colima status
  colima start  # if not running
  ```

### "Port 5000 already in use"
- **Solution**: Stop the service using port 5000 or change the port in docker-compose.yml

### No calendar events or emails found
- **Solution**: 
  - Make sure you have events/emails in the past 30 days
  - Check that permissions were granted correctly
  - Try logging out and logging back in

## Security Best Practices

1. **Never commit .env file**
   - It's already in .gitignore
   - Never share your CLIENT_SECRET

2. **Rotate secrets regularly**
   - Update client secret in Azure AD every 6-12 months
   - Generate new SECRET_KEY periodically

3. **Use read-only permissions**
   - The app only requests read permissions
   - Never grant write permissions

4. **Run locally only**
   - This app is designed for local use
   - Don't deploy to public servers

## Next Steps

- Customize the email template in `email_generator.py`
- Add custom keywords in `analyzer.py`
- Adjust analysis period in the web UI

## Getting Help

If you encounter issues:
1. Check the troubleshooting section above
2. Review container logs: `docker-compose logs`
3. Contact your IT department for Azure AD issues

