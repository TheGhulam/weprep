import json
import uuid
from datetime import datetime, timezone

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
    elif http_method == "GET" and resource == "/user/mock-interview/{user-id}":
        return handle_get_request_for_all_interviews(event)

    elif (
        http_method == "DELETE"
        and resource == "/user/mock-interview/{user-id}/interview/{interview-id}"
    ):
        return handle_delete_request(event)
    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_post_request_for_updating_db(event):
    try:
        user_id = event["pathParameters"]["user-id"]

        interview_id = str(uuid.uuid4())

        request_body = json.loads(event["body"])

        current_time_utc = datetime.now(timezone.utc)
        timestamp_str = current_time_utc.isoformat()

        request_body["userId"] = user_id
        request_body["interviewId"] = interview_id
        request_body["createdAt"] = timestamp_str

        table.put_item(Item=request_body)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "interviewId": interview_id,
                }
            ),
        }
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("Error processing request")}


def handle_get_request_for_all_interviews(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        response = table.query(
            KeyConditionExpression="userId = :userId",
            ExpressionAttributeValues={":userId": user_id},
        )

        interviews = response.get("Items", [])
        if interviews:
            interviews_details = [
                {k: v for k, v in interview.items() if k != "userId"}
                for interview in interviews
            ]
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {"userId": user_id, "interviewDetails": interviews_details}
                ),
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps(f"No interviews found for user {user_id}"),
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error processing request"),
        }


def handle_get_request_for_specific_interview(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        interview_id = event["pathParameters"]["interview-id"]
        response = table.get_item(Key={"userId": user_id, "interviewId": interview_id})

        interview = response.get("Item")
        if interview:
            return {"statusCode": 200, "body": json.dumps(interview)}
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Interview not found"}),
            }

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": "Error getting interview details"}


def handle_delete_request(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        interview_id = event["pathParameters"]["interview-id"]
        table.delete_item(Key={"userId": user_id, "interviewId": interview_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Interview deleted successfully"}),
        }

    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("error while deleting interview")}
