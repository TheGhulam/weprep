import io
import json
import os
import uuid

import boto3
from pydub import AudioSegment

os.environ["PATH"] += os.pathsep + "/opt/bin"

s3 = boto3.client("s3")
transcribe = boto3.client("transcribe")


def handler(event, context):
    print("received event:")
    print(event)

    # Get the user-id from the request path parameters
    user_id = event["pathParameters"]["user-id"]
    video_id = event["pathParameters"]["video-id"]

    # Parse the JSON request body
    json_body = json.loads(event["body"])

    # Get the video-id and dialogues from the request body
    dialogues = json_body["dialogues"]

    # Construct the S3 object key for the raw audio file
    raw_audio_key = f"{user_id}/raw/{video_id}.mp3"

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

    # Load the audio file using pydub
    audio = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")

    # Process each dialogue segment
    for dialogue in dialogues:
        title = dialogue["title"]
        start_time = dialogue["startTime"] * 1000  # Convert seconds to milliseconds
        end_time = dialogue["endTime"] * 1000

        # Extract the audio segment
        segment = audio[start_time:end_time]

        # Save the audio segment to S3
        segment_key = f"{user_id}/processed/{video_id}_{title}.mp3"
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
                OutputKey=f"{user_id}/transcripts/{video_id}_{title}.json",
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

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"message": "Audio processing and transcription started"}),
    }
