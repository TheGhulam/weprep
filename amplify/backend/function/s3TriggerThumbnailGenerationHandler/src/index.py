import json
import boto3
import requests
from pydub import AudioSegment
def handler(event, context):
    # Get the bucket name and object key from the event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    object = event["Records"][0]["s3"]["object"]["key"]

    # Extract user_id, interview_id, and video_id from the object key
    key_parts = object.split("/")
    user_id = key_parts[0]
    interview_id = key_parts[1]
    video_id = key_parts[2].split(".")[0]

    # Construct the request body
    request_body = {
        "bucket": bucket,
        "key": f"{user_id}/{interview_id}/{video_id}",
        "local_path": "local",
    }

    # Define the endpoint URL
    endpoint_url = "http://3.79.205.170:80/analyze"

    try:
        requests.post(endpoint_url, json=request_body)
        print("Request to EC2 analyze endpoint was sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Request to EC2 analyze endpoint failed: {e}")

    s3 = boto3.client("s3")
    video_file = f"/tmp/{video_id}.mp4"
    s3.download_file(bucket, object, video_file)

    # Load the video file using pydub
    video = AudioSegment.from_file(video_file, format="mp4")

    # Calculate the duration of each frame (assuming 30 frames per second)
    frame_duration = 1000 // 30  # in milliseconds

    # Extract the 10th frame
    tenth_frame_start = (10 - 1) * frame_duration
    tenth_frame_end = tenth_frame_start + frame_duration
    tenth_frame = video[tenth_frame_start:tenth_frame_end]

    # Export the 10th frame as an image
    thumbnail_file = f"/tmp/{video_id}_thumbnail.png"
    tenth_frame.export(thumbnail_file, format="png")

    # Upload the thumbnail to a different S3 bucket
    thumbnail_bucket = "weprep-video-thumbnails"
    thumbnail_key = f"{user_id}/{interview_id}/{video_id}_thumbnail.png"
    s3.upload_file(thumbnail_file, thumbnail_bucket, thumbnail_key)

    return {
        "statusCode": 200,
        "body": json.dumps("Lambda function executed successfully"),
    }
