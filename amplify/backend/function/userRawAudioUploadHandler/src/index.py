import base64
import json
import time
import uuid

import boto3

s3 = boto3.client("s3")
transcribe_client = boto3.client("transcribe")
dynamodb = boto3.resource("dynamodb")
lambda_client = boto3.client("lambda")


def handler(event, context):
    print("received event:")
    print(event)

    user_id = event["pathParameters"]["user-id"]
    interview_id = event["pathParameters"]["interview-id"]

    resume_id = event.get("queryStringParameters", {}).get("resume-id", "")
    video_id = event.get("queryStringParameters", {}).get("video-id", "")

    audio_data = event["body"]
    audio_data = base64.b64decode(audio_data)

    table_name = "userAudioDataTable-dev"
    table = dynamodb.Table(table_name)

    try:
        table.put_item(
            Item={
                "userId": user_id,
                "videoId": video_id,
                "interviewId": interview_id,
                "resumeId": resume_id,
                "mostUsedWords": [],
                "speechSpeed": None,
                "hedgingWordCount": None,
                "pronunciationWords": [],
                "fillerWordCount": None,
                "langugagePositivity": None,
                "feedbackAnalysis": [],
                "SummaryAnalysis": None,
                "webCrawlerResults": [],
                "status": "Processing",
            }
        )
        print("Initial item inserted successfully.")
    except Exception as e:
        print(f"Error inserting initial item: {e}")

    s3_key = f"{user_id}/{interview_id}/raw/{video_id}.mp3"

    try:
        s3.put_object(
            Body=audio_data,
            Bucket="weprep-user-audios",
            Key=s3_key,
            ContentType="audio/mpeg",
        )
        print(f"Audio file uploaded to S3: {s3_key}")
    except Exception as e:
        print(f"Error uploading audio file to S3: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to upload audio file"}),
        }

    # Start the transcription job



    request_body = {}
    request_body["user_id"] = user_id
    request_body["video_id"] = video_id
    request_body["interview_id"] = interview_id
    request_body["resume_id"] = resume_id

    lambda_client.invoke(
        FunctionName="userSpeechAnalysesHandler-dev",
        InvocationType="Event",  # Asynchronous invocation
        Payload=json.dumps(request_body),  # Pass the updated request body
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"message": "Audio File Upload successful"}),
    }
