# Authentication Guide - Device Code Flow

This application uses **device code flow** authentication to access your Microsoft 365 calendar and email data. This is a simple, secure authentication method that requires **no Azure AD app registration**.

## What is Device Code Flow?

Device code flow is an OAuth2 authentication method designed for devices or applications that don't have a web browser. It's perfect for CLI tools and Docker containers.

### How It Works

1. **App requests a code**: The application requests a device code from Microsoft
2. **User visits URL**: You open `https://microsoft.com/devicelogin` in your browser
3. **Enter code**: You enter the code shown by the app (e.g., `ABC-DEF-123`)
4. **Sign in**: You sign in with your Microsoft 365 account
5. **Grant permissions**: You approve read-only access to your calendar and email
6. **App gets token**: The app receives an access token and proceeds

### Why Device Code Flow?

- ✅ **No Azure AD setup required** - Uses Microsoft's public client ID
- ✅ **Simple and secure** - Official Microsoft authentication method
- ✅ **One-time authentication** - Token is cached for future use
- ✅ **User-controlled** - You explicitly approve access in your browser
- ✅ **Read-only access** - Cannot send emails or modify calendar

## Security Considerations

### ✅ Advantages

- **No password storage**: Your password is never stored or used by the app
- **Scoped permissions**: The app only requests read access to calendar and email
- **Delegated permissions**: App accesses data on your behalf (not as a service account)
- **Auditable**: All API access is logged in Microsoft 365 audit logs
- **Revocable**: You can revoke access at any time from your Microsoft account settings
- **Local execution**: All processing happens in your local container
- **No secrets to manage**: No client secrets or API keys to protect

### ⚠️ Important Notes

- **One-time approval**: You only need to authenticate once; the token is cached
- **Read-only access**: The app cannot send emails or create calendar events
- **Your account only**: The app accesses only your own mailbox
- **Token expiration**: Tokens expire after a period; you'll need to re-authenticate

## Required Permissions

The app requests these **Delegated permissions**:

| Permission | Purpose | Scope |
|------------|---------|-------|
| `User.Read` | Read your profile information | Read-only |
| `Calendars.Read` | Access your calendar events | Read-only |
| `Mail.Read` | Access your sent emails | Read-only |

**Note**: These are delegated permissions, meaning the app accesses data on your behalf, not as a service account.

## Authentication Flow

### Step-by-Step Process

1. **Run the container**:
   ```bash
   docker run -it -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
   ```

2. **App displays device code**:
   ```
   To sign in, use a web browser to open the page:
       https://microsoft.com/devicelogin

   And enter the code: ABC-DEF-123

   Waiting for you to complete authentication...
   ```

3. **You authenticate in browser**:
   - Open `https://microsoft.com/devicelogin`
   - Enter the code: `ABC-DEF-123`
   - Sign in with your Microsoft 365 account
   - Review the permissions requested
   - Click **Accept**

4. **App receives token**:
   ```
   ✓ Authentication successful! Token cached for future use.
   ```

5. **App proceeds**:
   - Fetches calendar events
   - Fetches sent emails
   - Analyzes data
   - Generates draft

## No Setup Required!

Unlike traditional OAuth apps, **you don't need to register anything in Azure AD**. The app uses Microsoft's public client ID, which is pre-approved for device code flow authentication.

Just run the container and authenticate when prompted!

## Troubleshooting

### Error: "Failed to acquire token"

**Cause**: Authentication was not completed in the browser, or the code was entered incorrectly.

**Solution**:
1. Make sure you visited `https://microsoft.com/devicelogin` (not a different URL)
2. Enter the code exactly as shown (case-sensitive)
3. Complete the sign-in process in your browser
4. Click "Accept" when prompted for permissions

### Error: "AADSTS50020: User account from identity provider does not exist in tenant"

**Cause**: You're trying to sign in with a personal Microsoft account instead of a work/school account.

**Solution**:
1. Make sure you're using your **Microsoft 365 work account** (e.g., user@company.com)
2. Don't use personal accounts (e.g., user@outlook.com, user@hotmail.com)

### Error: "No calendar events found" or "No sent emails found"

**Cause**: You don't have data in the specified time period, or permissions weren't granted.

**Solution**:
1. Make sure you have calendar events and sent emails in the past 30 days
2. Verify you clicked "Accept" when granting permissions
3. Try increasing the analysis period:
   ```bash
   docker run -it -e DAYS_BACK=60 -v $(pwd)/output:/app/output ghcr.io/chadchappy/t5t:latest
   ```

### Token Expired

**Cause**: The cached token has expired (typically after 60-90 days).

**Solution**:
1. Simply run the container again
2. You'll be prompted to re-authenticate
3. The new token will be cached

## Token Caching

The app caches your access token in `./data/token_cache.json` to avoid re-authentication on every run.

**Token lifetime**: Typically 60-90 days

**To clear the cache**:
```bash
rm -rf ./data/token_cache.json
```

**Security note**: The token cache is stored locally and is not shared. It's safe to delete at any time.

## Revoking Access

If you want to revoke the app's access to your Microsoft 365 account:

1. Go to https://account.microsoft.com/privacy/app-permissions
2. Find "Azure CLI" or the public client app
3. Click "Remove these permissions"

Or simply delete the token cache:
```bash
rm -rf ./data/token_cache.json
```

## Security Best Practices

1. **Run in trusted environment**
   - Only run the container on your own machine
   - Don't share your token cache file

2. **Review permissions**
   - The app only requests read-only access
   - You can review permissions before accepting

3. **Monitor access**
   - Check Microsoft 365 audit logs for API access
   - Review your account's app permissions periodically

4. **Keep container updated**
   - Pull the latest image regularly:
     ```bash
     docker pull ghcr.io/chadchappy/t5t:latest
     ```

## Additional Resources

- [Microsoft Device Code Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code)
- [Microsoft Graph Delegated Permissions](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Microsoft Account App Permissions](https://account.microsoft.com/privacy/app-permissions)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the container logs for error messages
3. Open an issue: https://github.com/chadchappy/t5t/issues
4. Include the error message (but NOT your token or credentials)

