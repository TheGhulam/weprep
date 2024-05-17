import json
import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    interview_id = event["pathParameters"]["interview-id"]
    video_id = event["pathParameters"]["video-id"]
    user_id = event["pathParameters"]["user-id"]

    object_key = f"{user_id}/{interview_id}/{video_id}.mp4"
    expiration = 3600
    upload_url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": "weprep-user-videos", "Key": object_key},
        ExpiresIn=expiration,
    )
    video_url = "to be generated through cloudfront"

    table_name = "userQuestionAndAnswers-dev"
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"interviewId": interview_id})
    questions_data = []
    if "Item" in response:
        item = response["Item"]
        questions_data = item.get("questions", [])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps(
            {
                "video_url": video_url,
                "questions": questions_data,
                "upload_url": upload_url,
            }
        ),
    }
