# bedrock-line
Amazon Bedrock Agent API Deployment Guide 📝
This guide will walk you through the process of deploying a Bedrock API and integrating it with a LINE messaging channel.

###  ✅ Prerequisites

  AWS account with Bedrock access
  - LINE Developer account
  - Git
  - AWS SAM CLI

## Register your LINE Developer Account

  - Create your LINE developer account at this link:
    https://developers.line.biz/console/
  - Create a provider that your messaging channel will be inside.
  - Create a 'Messaging API' channel:
        Click on "Create a new channel"
        Select "Messaging API" as the channel type

       <img width="824" alt="Screenshot 2567-07-24 at 11 25 27" src="https://github.com/user-attachments/assets/5cd0daf6-7af8-4051-867a-f8654935aaf7">

  - Key in the basic information for your Messaging API:
    1. Region
    2. Channel name
    3. Channel description
    4. Category
    5. Subcategory
    6. Email address
       
  - Agree to the terms of service and click "Create"
  
  Now you're all set with your LINE developer account!


## 💻 Deployment Steps

### 1. Clone the Git repository 📁:
  on your local computer or AWS Cloud9 environment
```
git clone <repository-url>
```
### 2. Create a 'config.json' file inside the 'line' folder with the following structure:

```
{
    "<your-line-user-id>":{
        "LINE_TOKEN": "<your-line-channel-access-token>",
        "type": "bedrock-agent",
        "agentId": "<your-bedrock-agent-id>",
        "agentAliasId": "<your-bedrock-agent-alias-id>"
    }
}
```
  🚛 Navigate to Line Developer Console, 
  - Go to General Settings tab to get your LINE User ID
    
    <img width="549" alt="Screenshot 2567-07-24 at 12 13 18" src="https://github.com/user-attachments/assets/84131eae-26fa-4a76-a35f-7e5d0455e53b">

  - GO to Meesaging API tab, issue your channel access token (long-lived)
    
    <img width="367" alt="Screenshot 2567-07-24 at 12 09 25" src="https://github.com/user-attachments/assets/6dcbb05d-5a44-4352-92c3-4ddbc5053810">

    
  🚚 Navigate to Amazon Bedrock in AWS Management Console,
  - Find 'ID' in Agent Overview to get your agent id
    
    ![image](https://github.com/user-attachments/assets/461bf41a-66ef-4f97-9a5f-948cf3d41f91)

  - Find 'Alias ID' in Alias to get your agent alias id
    
    ![image](https://github.com/user-attachments/assets/709eaf48-5aa9-4e65-bc02-f96794c8ceb6)

  
### 4. Check your Bedrock Agent Region 🗺️.
  - Open the app.py file in the 'line_reply' folder
  - Ensure region_name in the ''get_bedrock_agent_response' function matches the region where your Bedrock agent resides.
  - If region does not match, change the region_name to the correct region.
    
![image](https://github.com/user-attachments/assets/ab393799-90aa-4a22-a7bc-787ab23a3565)


### 5. Build and deploy the application using SAM🐹:
```
sam build
sam deploy
```
### 6. After deployment, note the output URL. This will be your webhook URL🔗
  The URL will be in the 'Value' field from 'HelloWorldApi' key

  ![image](https://github.com/user-attachments/assets/a646f759-eb70-409b-a7ae-57244d9b7306)


### 7. In the LINE Developers Console 📝:

  Go to the Messaging API tab
  - Edit the Webhook settings
    
    ![image](https://github.com/user-attachments/assets/1bc1ab5f-7b34-4c82-8a6e-0d4cd8519386)

  - Paste the URL from step 6 as your webhook URL
    
    ![image](https://github.com/user-attachments/assets/09d760db-bf4f-4ea1-89e3-c0f7856ccae4)

  - Click "Verify" to ensure the connection is working
  - Turn on the "Use webhook" option
    
    ![image](https://github.com/user-attachments/assets/2c6c3f26-8a87-41ef-b4dd-d63290c04d4c)




### ✅ Your Bedrock API should now be successfully deployed and integrated with your LINE messaging channel.

### 📌 Troubleshooting
  If you encounter any issues during deployment or integration, please check the following:
  
  - Ensure all IDs in the config.json file are correct
  - Verify that the region in app.py matches your Bedrock agent's region
  - Check AWS CloudWatch logs for any error messages
