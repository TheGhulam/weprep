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
    audio_data = event["body"]
    audio_data = base64.b64decode(audio_data)
    video_id = str(uuid.uuid4())
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
    try:
        transcription_job_name = (
            f"{user_id}_{interview_id}_{video_id}_raw_audio_transcription"
        )
        transcribe_client.start_transcription_job(
            TranscriptionJobName=transcription_job_name,
            Media={"MediaFileUri": f"s3://weprep-user-audios/{s3_key}"},
            MediaFormat="mp3",
            LanguageCode="en-US",
            OutputBucketName="weprep-user-audios",
            OutputKey=f"{user_id}/{interview_id}/transcripts/{video_id}_raw_audio_transcript.json",
        )
    except Exception as e:
        print(f"Error starting transcription job: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to start transcription job"}),
        }

    while True:
        status = transcribe_client.get_transcription_job(
            TranscriptionJobName=transcription_job_name
        )["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            break
        time.sleep(2)

    if status == "COMPLETED":
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
            "body": json.dumps(
                {"message": "Audio File Upload successful", "videoId": video_id}
            ),
        }

    else:
        print("Transcription job failed.")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Transcription job failed"}),
        }
