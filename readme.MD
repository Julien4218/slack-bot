# Slack Bot

## Installation

1. **Clone the repository:**

2. **Install dependencies:**
    ```bash
     pip install -r requirements.txt 
    ```

## Configuration

### Slack App

1. Create a Slack App
- Go to https://api.slack.com/apps “Create New App”
- Enable Slash Commands, Bot Token Scopes, and Event Subscriptions

2. Define the Slash Command
- Command: /slack close-old-channels
- Request URL: your server endpoint (e.g., https://yourdomain.com/slack/close-old)
- Method: POST
- Slack will send a payload like:
```json
{
  "user_id": "U123456",
  "channel_id": "C123456",
  "command": "/slack close-old-channels",
  "text": ""
}
```

3. Bot Token Scopes
Add these scopes:
- channels:read
- channels:history
- chat:write
- users:read
- commands

### Env file
1. **Create a `.env` file:**
To obtain your Slack bot token and signing secret:
- Go to [Slack API: Your Apps](https://api.slack.com/apps) and click **Create New App**.
- Choose **From scratch** and provide an app name and workspace.
- Navigate to **OAuth & Permissions** and add the required scopes for your bot.
- Click **Install App to Workspace** and authorize.
- Copy the **Bot User OAuth Token** and paste it into your `.env` file as `SLACK_BOT_TOKEN`.
- Go to **Basic Information** and copy the **Signing Secret**. Paste it into your `.env` file as `SLACK_SIGNING_SECRET`.
```
SLACK_BOT_TOKEN=your-slack-bot-token
SLACK_SIGNING_SECRET=your-signing-secret
```

2. **(Optional) Add New Relic monitoring:**
To enable New Relic monitoring, add the following to your `.env` file:
```
NEW_RELIC_LICENSE_KEY=your-new-relic-license-key
NEW_RELIC_APP_NAME=your-app-name
```

## Running Locally

```bash
npm start
```
or
```bash
yarn start
```

The bot will start and connect to Slack. Check your terminal for logs and status.

## Usage

### Close Old Channels

To close old channels using the bot, type the following command in any Slack channel where the bot is present:

```
/slack close-old-channels
```

The bot will process the request and archive channels that meet the criteria for being considered "old." Check the channel or your direct messages for a summary of the action taken.

### Dry Run Mode

To preview which channels would be closed without making changes, use the dry run option:

```
/slack close-old-channels --dry-run
```

The bot will list channels that match the criteria but will not archive them.
