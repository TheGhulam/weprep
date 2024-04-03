import base64
import json
import time
import uuid

import boto3

transcribe_client = boto3.client("transcribe")
s3_client = boto3.client("s3")
bucket_name = "user-processed-data"


def handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    audio_data = event["body"]
    audio_data = base64.b64decode(audio_data)

    audio_key = f"{user_id}/user_answers_audio.mp4"
    s3_client.put_object(Bucket=bucket_name, Key=audio_key, Body=audio_data)

    job_name = f"transcribe_{uuid.uuid4()}"
    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": f"s3://{bucket_name}/{audio_key}"},
        MediaFormat="mp4",
        LanguageCode="en-US",
        OutputBucketName=bucket_name,
        OutputKey=f"{user_id}/user_answers_audio.json",
    )

    transcription_result = poll_transcription_job_status(transcribe_client, job_name)
    if (
        transcription_result["TranscriptionJob"]["TranscriptionJobStatus"]
        == "COMPLETED"
    ):
        print("Transcription completed successfully.")
    elif transcription_result["TranscriptionJob"]["TranscriptionJobStatus"] == "FAILED":
        print("Transcription job failed.")
        return {"statusCode": 200, "body": json.dumps("User audio processing failed")}

    print(transcription_result)

    return {"statusCode": 200, "body": json.dumps("User audio processing successful")}


def poll_transcription_job_status(transcribe_client, job_name):
    while True:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            return response
        else:
            print(f"Waiting for transcription to complete. Current status: {status}")
            time.sleep(10)
