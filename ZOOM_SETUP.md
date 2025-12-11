# Zoom Integration Setup Guide

This guide will help you set up Zoom video conferencing integration with MectoFitness CRM.

## Prerequisites

- A Zoom account (Pro, Business, or Enterprise plan recommended for API access)
- Access to the Zoom App Marketplace
- Admin access to your MectoFitness CRM instance

## Step 1: Create a Zoom Server-to-Server OAuth App

1. Go to the [Zoom App Marketplace](https://marketplace.zoom.us/)
2. Click "Develop" in the top menu, then select "Build App"
3. Choose "Server-to-Server OAuth" as the app type
4. Fill in the app information:
   - **App Name**: MectoFitness CRM
   - **Description**: Video conferencing integration for MectoFitness CRM
   - **Developer Contact**: Your email address

## Step 2: Configure App Credentials

1. After creating the app, you'll see your **Account ID**, **Client ID**, and **Client Secret**
2. Copy these credentials - you'll need them for the next step
3. In the "Scopes" section, add the following permissions:
   - `meeting:write:admin` - Create and manage meetings
   - `meeting:read:admin` - Read meeting information
   - `recording:read:admin` - Access meeting recordings (optional)
   - `user:read:admin` - Read user information

## Step 3: Configure Environment Variables

Add the following variables to your `.env` file:

```bash
# Zoom Integration
ZOOM_CLIENT_ID=your-zoom-client-id-here
ZOOM_CLIENT_SECRET=your-zoom-client-secret-here
ZOOM_ACCOUNT_ID=your-zoom-account-id-here
```

Replace the placeholder values with your actual credentials from Step 2.

## Step 4: Activate the App

1. In the Zoom App Marketplace, go to your app's settings
2. Click "Activate" to enable the app
3. Confirm that you want to activate it for your account

## Step 5: Connect in MectoFitness CRM

1. Log in to your MectoFitness CRM account
2. Navigate to **Settings** → **Integrations**
3. Find "Zoom" in the list of available integrations
4. Click "Connect"
5. Verify that the connection status shows as "Connected"

## Using Zoom Integration

### Create a Zoom Meeting for a Session

1. Go to **Sessions** in the navigation menu
2. Select or create a training session
3. Click "Add Video Conference"
4. Select "Zoom" as the platform
5. The system will automatically create a Zoom meeting with:
   - Meeting topic based on client name
   - Scheduled time matching your session
   - Appropriate security settings (waiting room, password)

### Share Meeting Details with Clients

After creating a Zoom meeting:
- The meeting URL and password are automatically saved to the session
- Share these details with your client via email or the messaging system
- Clients can join directly from the meeting URL

### Features

- **Auto-Recording**: Meetings are automatically recorded to the cloud
- **Waiting Room**: Enabled by default for security
- **Video Settings**: Both host and participant video enabled
- **Audio**: Both computer and phone audio supported

## Webhooks (Optional)

To receive real-time updates about meeting events:

1. In your Zoom app settings, go to "Event Subscriptions"
2. Add the following endpoint URL:
   ```
   https://your-domain.com/api/v1/zoom/webhook
   ```
3. Subscribe to the following events:
   - `meeting.started`
   - `meeting.ended`
   - `recording.completed`

## Troubleshooting

### Connection Failed
- Verify your credentials are correct in the `.env` file
- Ensure the Zoom app is activated in the marketplace
- Check that all required scopes are added to your app

### Meetings Not Creating
- Verify your Zoom account has meeting creation privileges
- Check the server logs for detailed error messages
- Ensure the session has a valid scheduled time

### Recordings Not Available
- Verify the `recording:read:admin` scope is enabled
- Recordings may take a few minutes to process after the meeting ends
- Check Zoom's cloud storage limits for your account

## Best Practices

1. **Test First**: Create a test session and meeting before going live with clients
2. **Communicate Clearly**: Always send meeting details well in advance
3. **Check Settings**: Review Zoom settings before important sessions
4. **Monitor Usage**: Keep track of your Zoom account's usage limits
5. **Update Regularly**: Keep your integration credentials secure and rotate them periodically

## Security Considerations

- Never commit your Zoom credentials to version control
- Use environment variables for all sensitive information
- Enable waiting rooms for all client sessions
- Consider using meeting passwords for additional security
- Regularly review access logs in the Zoom dashboard

## Support

For issues specific to Zoom's API, consult:
- [Zoom API Documentation](https://marketplace.zoom.us/docs/api-reference)
- [Zoom Developer Forum](https://devforum.zoom.us/)

For MectoFitness CRM support:
- Open an issue in the GitHub repository
- Contact support@mectofitness.com
