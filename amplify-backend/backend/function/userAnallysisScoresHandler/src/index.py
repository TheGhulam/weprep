import json

import boto3

# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb")


def handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "GET":
        return handle_get_request(event)
    else:
        return {
            "statusCode": 405,
            "body": f"HTTP method {http_method} is not supported",
        }


def handle_get_request(event):
    try:
        print("received event:")
        print(event)

        # Extract user-id from path parameters
        user_id = event["pathParameters"]["user-id"]

        # Query DynamoDB table for scores based on user-id
        scores = get_user_scores(user_id)

        # Return scores in the response body
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(scores),
        }
    except Exception as e:
        print("Error:", e)
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def get_user_scores(user_id):
    try:
        # Query DynamoDB table for scores based on user-id
        response = dynamodb.get_item(
            TableName="userAnalysisScoreTable-dev", Key={"userId": {"S": user_id}}
        )
        # Extract scores from the response
        scores = response.get("Item", {})
        return scores
    except Exception as e:
        print("Error retrieving scores from DynamoDB:", e)
        return []
