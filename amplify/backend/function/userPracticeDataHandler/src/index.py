import json

import boto3

dynamodb = boto3.resource("dynamodb")
DATABASE_NAME = "userAnalysisScoreTable-dev"


def handler(event, context):
    print("received event:")
    print(event)
    http_method = event["httpMethod"]
    resource = event["resource"]

    if http_method == "GET" and resource == "/user/{user-id}/practice-data-scores":
        return handle_get_request(event)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_get_request(event):

    user_id = event["pathParameters"]["user-id"]

    table = dynamodb.Table(DATABASE_NAME)

    try:
        # Fetch the user data from the database
        response = table.get_item(Key={"userId": user_id})
        print(response)
        user_data = response.get("Item", {})
        if user_data:
            return {
                "statusCode": 200,
                "body": json.dumps(user_data),
                "headers": {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Credentials" : True
                },
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "User not found"}),
            }
    except Exception:
        return {
            "statusCode": 500,
            "body": json.dumps("Error in uploading file."),
        }
