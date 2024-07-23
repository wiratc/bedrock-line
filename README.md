# bedrock-line
Bedrock API Deployment Guide
This guide will walk you through the process of deploying a Bedrock API and integrating it with a LINE messaging channel.

##Prerequisites

AWS account with Bedrock access
- LINE Developer account
- Git
- AWS SAM CLI

##Deployment Steps

### 1. Clone the Git repository:
```
git clone <repository-url>
```

### 2. Create a config.json file inside the line folder with the following structure:
```
{
  "line_user_id": "<your-line-user-id>",
  "agent_id": "<your-bedrock-agent-id>",
  "agent_alias_id": "<your-bedrock-agent-alias-id>"
}
```

### 3. Open the app.py file in the line_reply folder and ensure that the region name in the get_bedrock_agent_response function matches the region where your Bedrock agent resides.

### 4. In the LINE Developers Console:
- Create a new Messaging API channel
- Go to the Basic Settings tab and copy your LINE User ID


### 5. In the AWS Console:
- Navigate to the Bedrock service
- Copy your Agent ID and Agent Alias ID


### 6. Update the config.json file with the values obtained in steps 4 and 5.
### 7. Build and deploy the application using SAM:
```
sam build
sam deploy
```
### 8. After deployment, note the output URL. This will be your webhook URL.
### 9. In the LINE Developers Console:

Go to the Messaging API tab
- Edit the Webhook settings
- Paste the URL from step 8 as your webhook URL
- Click "Verify" to ensure the connection is working
- Turn on the "Use webhook" option



Your Bedrock API should now be successfully deployed and integrated with your LINE messaging channel.

#Troubleshooting
If you encounter any issues during deployment or integration, please check the following:

- Ensure all IDs in the config.json file are correct
- Verify that the region in app.py matches your Bedrock agent's region
- Check AWS CloudWatch logs for any error messages
