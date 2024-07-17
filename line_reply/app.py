import json

import requests

import boto3


def get_bedrock_kb_response(event):
    line_event = event["events"][0]
    message = line_event["message"]["text"]
    bot_config = event["bot_config"]
    knowledgeBaseId = bot_config["knowledgeBaseId"]
    bedrock = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    res = bedrock.retrieve_and_generate(
        input={"text": message},
        retrieveAndGenerateConfiguration={
            "knowledgeBaseConfiguration": {
                "modelArn": "anthropic.claude-3-sonnet-20240229-v1:0",
                "knowledgeBaseId": knowledgeBaseId,
            },
            "type": "KNOWLEDGE_BASE",
        },
    )

    message_body = []
    message_body.append({"type": "text", "text": res["output"]["text"]})

    for citation in res["citations"]:
        message_body.append(
            {
                "type": "text",
                "text": citation["generatedResponsePart"]["textResponsePart"]["text"],
            }
        )
        for reference in citation["retrievedReferences"]:
            message_body.append({"type": "text", "text": reference["content"]["text"]})

    return message_body


def get_apigateway_response(event):
    line_event = event["events"][0]
    message = line_event["message"]["text"]
    bot_config = event["bot_config"]
    base_url = bot_config["base_url"]
    api_key = bot_config["api_key"]
    message = line_event["message"]["text"]

    headers = {"Content-Type": "application/json", "x-api-key": api_key}

    body = {
        "message": {
            "content": [{"contentType": "text", "body": message}],
            "model": "claude-v3-sonnet",
        },
        "continueGenerate": False,
    }

    r = requests.post(f"{base_url}/conversation", headers=headers, json=body)
    print(json.dumps(r.json()))

    conversation_id = r.json()["conversationId"]
    message_id = r.json()["messageId"]

    while True:
        r = requests.get(
            f"{base_url}/conversation/{conversation_id}/{message_id}", headers=headers
        )
        if r.status_code == 200:
            break
    print(json.dumps(r.json()))

    response = r.json()["message"]

    message_body = []
    message_body.append({"type": "text", "text": response["content"][0]["body"]})

    if "usedChunks" in response.keys():
        usedChunks = response["usedChunks"]

        if usedChunks is None:
            usedChunks = []

        for chunk in usedChunks:
            message_body.append(
                {"type": "text", "text": f"```^{chunk['rank']}\n{chunk['content']}```"}
            )

    # print(message)
    # return r.json()["message"]["content"][0]["body"]
    return message_body


def send_message(event, message_body):
    line_event = event["events"][0]
    line_token = event["bot_config"]["LINE_TOKEN"]
    # reply_token = line_event["replyToken"]

    print(json.dumps(message_body))

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(line_token),
    }

    user_id = line_event["source"]["userId"]
    body = {
        "to": user_id,
        "messages": [message_body],
    }
    # url = "https://api.line.me/v2/bot/message/reply"
    url = "https://api.line.me/v2/bot/message/push"

    response = requests.post(url, headers=headers, json=body)

    print(json.dumps(response.json()))


def lambda_handler(event, context):

    print(json.dumps(event))
    line_event = event["events"][0]
    message = line_event["message"]["text"]
    bot_config = event["bot_config"]

    type = bot_config["type"]

    generate_responsefn = {
        "apigateway": get_apigateway_response,
        "bedrock-kb": get_bedrock_kb_response,
    }

    fn = generate_responsefn[type]

    message_body = fn(event)

    for m in message_body:
        send_message(event, m)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
