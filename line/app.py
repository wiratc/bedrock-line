import json

import requests
import os

import boto3


def lambda_handler(event, context):

    function_name = dict(os.environ)["LINE_REPLY_FUNCTION_ARN"]

    print(json.dumps(event))

    body = json.loads(event["body"])
    config = json.load(open("config.json"))

    userId = body["destination"]
    bot_config = config[userId]

    body["bot_config"] = bot_config
    lambda_client = boto3.client("lambda")

    response = lambda_client.invoke(
        FunctionName=function_name, InvocationType="Event", Payload=json.dumps(body)
    )

    print(response)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                "environ": dict(os.environ),
                "event": event,
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
