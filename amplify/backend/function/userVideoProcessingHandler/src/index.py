import json

import boto3
from moviepy.editor import VideoFileClip

transcribe_client = boto3.client("transcribe")
s3_client = boto3.client("s3")
bucket_name = "weprep-user-videos"


def separate_audio_video(video_path, output_audio_path, output_video_path):
    """
    Separates the audio and video streams from a video file.

    Args:
        video_path (str): The path to the input video file in the S3 bucket.
        output_audio_path (str): The path to save the extracted audio file in the S3 bucket.
        output_video_path (str): The path to save the processed video file in the S3 bucket.

    Returns:
        None
    """
    # Download the video file from S3
    s3_client.download_file(bucket_name, video_path, "/tmp/input_video.mp4")

    # Load the video file
    video_clip = VideoFileClip("/tmp/input_video.mp4")

    # Extract the audio stream
    audio_clip = video_clip.audio

    # Write the audio stream to a file
    audio_clip.write_audiofile("/tmp/output_audio.mp3")

    # Upload the audio file to S3
    s3_client.upload_file("/tmp/output_audio.mp3", bucket_name, output_audio_path)

    # Write the processed video to a file
    video_clip.write_videofile("/tmp/output_video.mp4")

    # Upload the processed video file to S3
    s3_client.upload_file("/tmp/output_video.mp4", bucket_name, output_video_path)

    # Close the video clip
    video_clip.close()


def handler(event, context):
    print("received event:")
    print(event)

    # Get the video object information from the event
    video_key = event["Records"][0]["s3"]["object"]["key"]

    # Extract the user_id and video_id from the video_key
    user_id, _, video_id = video_key.split("/")

    # Construct the input and output paths
    input_video_path = f"{user_id}/raw/{video_id}"
    output_audio_path = f"{user_id}/processed/{video_id}_audio.mp3"
    output_video_path = f"{user_id}/processed/{video_id}_video.mp4"

    # Perform audio-video separation and processing
    separate_audio_video(input_video_path, output_audio_path, output_video_path)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(
            "Audio-video separation and processing completed successfully."
        ),
    }
