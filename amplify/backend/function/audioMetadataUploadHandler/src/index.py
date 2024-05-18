import base64
import json
import boto3

lambda_client = boto3.client("lambda")


def handler(event, context):
    print("received event:")
    print(event)

    # Get the user-id from the request path parameters
    user_id = event["pathParameters"]["user-id"]
    interview_id = event["pathParameters"]["interview-id"]

    # Parse the JSON request body
    json_body = base64.b64decode(event["body"])
    json_body = json.loads(json_body)

    event = {"user_id": user_id, "interview_id": interview_id, "json_body": json_body}


    lambda_client.invoke(
        FunctionName="userAudioUploadHandler-dev",
        InvocationType="Event",  # Asynchronous invocation
        Payload=json.dumps(event),  # Pass the updated request body
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET, POST",
        },
        "body": json.dumps(
            {"message": "Audio processing and transcription started"}
        ),
    }
