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
        handle_get_request(event)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_get_request(event):

    user_id = event["pathParameters"]["user-id"]

    table = dynamodb.Table(DATABASE_NAME)

    try:
        # Fetch the user data from the database
        response = table.get_item(Key={"userId": user_id})
        user_data = response.get("Item", {})
        if user_data:
            user_data = {
                "userId": user_data.get("userId").get("S"),
                "confidenceScore": user_data.get("confidenceScore").get("N"),
                "clarityScore": user_data.get("clarityScore").get("N"),
                "fillerWordUsage": user_data.get("fillerWordUsage").get("N"),
                "emotionalScore": user_data.get("emotionalScore").get("N"),
                "attentionScore": user_data.get("attentionScore").get("N"),
            }

            body = json.dumps(user_data)
            status_code = 200
    except Exception as e:
        body = json.dumps({"error": str(e)})
        status_code = 500

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": body,
    }
