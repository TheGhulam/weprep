import json
import uuid

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("mockInterviewSessionsTable-dev")


def handler(event, context):
    print("received event:")
    print(event)
    http_method = event["httpMethod"]
    resource = event["resource"]
    if http_method == "POST" and resource == "/user/mock-interview/{user-id}/upload":
        handle_post_request_for_updating_db(event)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_post_request_for_updating_db(event):
    try:
        user_id = event["pathParameters"]["user-id"]

        interview_id = str(uuid.uuid4())

        request_body = json.loads(event["body"])

        request_body["userId"] = user_id
        request_body["mockInterviewId"] = interview_id

        table.put_item(Item=request_body)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "mockInterviewId": interview_id,
                }
            ),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
