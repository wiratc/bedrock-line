import json

import requests


def get_bot_response(event):
    line_event = event["events"][0]
    message = line_event["message"]["text"]
    base_url = event["base_url"]
    api_key = event["api_key"]
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
    line_token = event["line_token"]
    reply_token = line_event["replyToken"]

    print(json.dumps(message_body))

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(line_token),
    }

    body = {
        "replyToken": reply_token,
        "messages": [message_body],
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
    message_body = get_bot_response(event)

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
