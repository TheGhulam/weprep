import base64
import io
import json
import os
import uuid

import boto3
from pydub import AudioSegment

lambda_client = boto3.client("lambda")


os.environ["PATH"] += os.pathsep + "/opt/bin"

s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")


def handler(event, context):
    print("received event:")
    print(event)

    # Get the user-id from the request path parameters
    user_id = event["user_id"]
    interview_id = event["interview_id"]
    json_body = event["json_body"]

    # Get the video-id and dialogues from the request body
    dialogues = json_body.get("dialogues")
    video_id = json_body["video-id"]
    resume_id = json_body["resume-id"]

    # Construct the S3 object key for the raw audio file
    raw_audio_key = f"{user_id}/{interview_id}/raw/{video_id}.mp3"

    # Download the raw audio file from S3
    try:
        response = s3.get_object(Bucket="weprep-user-audios", Key=raw_audio_key)
        audio_data = response["Body"].read()
    except Exception as e:
        print(f"Error downloading audio file from S3: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to download audio file"}),
        }
    if dialogues:
    # Load the audio file using pydub
        audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

        # Process each dialogue segment
        for dialogue in dialogues:
            title = dialogue["title"]
            start_time = dialogue["startTime"] * 1000
            end_time = dialogue["endTime"] * 1000

            # Extract the audio segment
            segment = audio[start_time:end_time]

            # Save the audio segment to S3
            segment_key = f"{user_id}/{interview_id}/processed/{video_id}_{title}.mp3"
            segment_data = segment.export(format="mp3").read()
            try:
                s3.put_object(
                    Body=segment_data,
                    Bucket="weprep-user-audios",
                    Key=segment_key,
                    ContentType="audio/mpeg",
                )
                print(f"Audio segment saved to S3: {segment_key}")
            except Exception as e:
                print(f"Error saving audio segment to S3: {str(e)}")
                return {
                    "statusCode": 500,
                    "headers": {
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                    "body": json.dumps({"error": "Failed to save audio segment"}),
                }

            # Run the transcription job
            try:
                job_name = f"{user_id}_{video_id}_{title}_{str(uuid.uuid4())}"
                transcribe.start_transcription_job(
                    TranscriptionJobName=job_name,
                    Media={"MediaFileUri": f"s3://weprep-user-audios/{segment_key}"},
                    MediaFormat="mp3",
                    LanguageCode="en-US",
                    OutputBucketName="weprep-user-audios",
                    OutputKey=f"{user_id}/{interview_id}/transcripts/{video_id}_{title}.json",
                )
                print(f"Transcription job started: {job_name}")
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
    request_body = {}
    request_body["user_id"] = user_id
    request_body["video_id"] = video_id
    request_body["interview_id"] = interview_id
    request_body["resume_id"] = resume_id
    lambda_client.invoke(
        FunctionName="userTranscriptAnalysisGenerationHandler-dev",
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
            {"message": "Audio processing and transcription started"}
        ),
    }
