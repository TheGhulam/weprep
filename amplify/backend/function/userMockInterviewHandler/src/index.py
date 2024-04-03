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
        return handle_post_request_for_updating_db(event)
    elif (
        http_method == "GET"
        and resource == "/user/mock-interview/{user-id}/interview/{interview-id}"
    ):
        return handle_get_request_for_specific_interview(event)
    elif (
        http_method == "GET" and resource == "/user/mock-interview/{user-id}/interview"
    ):
        return handle_get_request_for_all_interviews(event)
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
        print(e)
        return {"statusCode": 500, "body": json.dumps("Error processing request")}


def handle_get_request_for_all_interviews(event):
    try:
        # user_id = event["pathParameters"]["user-id"]

        return {
            "statusCode": 200,
            # "body": json.dumps(
            #     {
            #         "mockInterviewId": interview_id,
            #     }
            # ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error processing request"),
        }


def handle_get_request_for_specific_interview(event):
    pass
