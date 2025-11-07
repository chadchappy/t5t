# Authentication Guide - App-Only Access

This application uses **app-only authentication** (also called "client credentials flow") to access your Microsoft 365 calendar and email data. This means the app can run automatically without requiring you to log in interactively each time.

## What is App-Only Authentication?

App-only authentication allows an application to access Microsoft Graph API using its own identity rather than on behalf of a user. This is ideal for:

- ✅ Automated/scheduled tasks
- ✅ Background services
- ✅ Server-to-server communication
- ✅ No interactive login required

## How It Works

1. **Azure AD App Registration**: You register the application in Azure AD with application permissions
2. **Admin Consent**: An admin grants the app permission to access specific resources
3. **Client Credentials**: The app uses its Client ID and Client Secret to authenticate
4. **Access Token**: Microsoft issues an access token that allows the app to access the specified user's data
5. **API Calls**: The app uses the token to read calendar and email data

## Security Considerations

### ✅ Advantages

- **No password storage**: Your personal password is never stored or used
- **Scoped permissions**: The app only has read access to calendar and email
- **Auditable**: All API access is logged in Microsoft 365 audit logs
- **Revocable**: Admin can revoke access at any time from Azure AD
- **Local execution**: All processing happens in your local container

### ⚠️ Important Notes

- **Admin consent required**: Application permissions require admin approval
- **Protect your secrets**: Keep CLIENT_SECRET secure and never commit to git
- **Read-only access**: The app cannot send emails or create calendar events
- **Single user**: The app accesses only the mailbox specified in USER_EMAIL

## Required Permissions

The app requires these **Application permissions** (not Delegated):

| Permission | Purpose | Scope |
|------------|---------|-------|
| `User.Read.All` | Read user profile information | Read-only |
| `Calendars.Read` | Access calendar events | Read-only |
| `Mail.Read` | Access sent emails | Read-only |

## Setup Steps

### 1. Register App in Azure AD

```bash
1. Go to https://portal.azure.com
2. Navigate to Azure Active Directory → App registrations → New registration
3. Fill in:
   - Name: Top 5 Things Generator
   - Supported account types: Single tenant
   - Redirect URI: Leave blank
4. Click Register
```

### 2. Create Client Secret

```bash
1. Go to Certificates & secrets
2. Click New client secret
3. Description: T5T Secret
4. Expires: 24 months (or per your org policy)
5. Click Add
6. COPY THE SECRET VALUE IMMEDIATELY (you won't see it again!)
```

### 3. Configure Application Permissions

```bash
1. Go to API permissions
2. Click Add a permission
3. Select Microsoft Graph
4. Select Application permissions (NOT Delegated)
5. Search and add:
   - User.Read.All
   - Calendars.Read
   - Mail.Read
6. Click Add permissions
```

### 4. Grant Admin Consent (REQUIRED)

```bash
1. Click "Grant admin consent for [Your Organization]"
2. Confirm the consent
3. Verify all permissions show green checkmarks
```

**Note**: If you don't have admin rights, you must request your IT administrator to grant consent.

### 5. Configure Environment Variables

Create a `.env` file with:

```bash
CLIENT_ID=<your-application-client-id>
CLIENT_SECRET=<your-client-secret-value>
TENANT_ID=<your-directory-tenant-id>
USER_EMAIL=<your-email@company.com>
SECRET_KEY=<generate-random-key>
```

## Troubleshooting

### Error: "Insufficient privileges to complete the operation"

**Cause**: Admin consent not granted or application permissions not configured correctly.

**Solution**:
1. Verify you selected "Application permissions" (not Delegated)
2. Ensure admin consent was granted (green checkmarks in Azure AD)
3. Wait 5-10 minutes for permissions to propagate

### Error: "Failed to acquire token"

**Cause**: Invalid CLIENT_ID, CLIENT_SECRET, or TENANT_ID.

**Solution**:
1. Verify all values in `.env` are correct
2. Ensure CLIENT_SECRET hasn't expired
3. Check for extra spaces or quotes in `.env` file

### Error: "User not found"

**Cause**: USER_EMAIL doesn't exist in your tenant or is incorrectly formatted.

**Solution**:
1. Verify USER_EMAIL matches your Microsoft 365 email exactly
2. Ensure the user exists in your Azure AD tenant
3. Try using the UserPrincipalName format (e.g., user@company.onmicrosoft.com)

### Error: "Access denied"

**Cause**: The app doesn't have permission to access the specified mailbox.

**Solution**:
1. Verify admin consent was granted
2. Check that all three permissions are present and consented
3. Ensure you're accessing your own mailbox (not another user's)

## Comparison: App-Only vs Delegated Permissions

| Feature | App-Only (This App) | Delegated |
|---------|---------------------|-----------|
| Interactive login | ❌ Not required | ✅ Required |
| Admin consent | ✅ Required | ⚠️ Sometimes |
| Runs unattended | ✅ Yes | ❌ No |
| Access scope | Specific user via config | Current logged-in user |
| Token lifetime | ~60 minutes | Varies |
| Best for | Automation, scheduled tasks | Interactive apps |

## Security Best Practices

1. **Protect CLIENT_SECRET**
   - Never commit to version control
   - Use `.env` file (already in `.gitignore`)
   - Rotate secrets periodically

2. **Limit Permissions**
   - Only grant necessary permissions
   - Use read-only permissions when possible
   - Review permissions regularly

3. **Monitor Access**
   - Check Microsoft 365 audit logs
   - Review Azure AD sign-in logs
   - Monitor for unusual activity

4. **Secure Environment**
   - Run in trusted container environment
   - Keep Docker images updated
   - Use secrets management for production

## Additional Resources

- [Microsoft Graph App-Only Access](https://learn.microsoft.com/en-us/graph/auth-v2-service)
- [Application Permissions Reference](https://learn.microsoft.com/en-us/graph/permissions-reference)
- [Azure AD App Registration](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Client Credentials Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow)

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Azure AD audit logs for permission errors
3. Verify all setup steps were completed
4. Check application logs: `docker-compose logs -f`

