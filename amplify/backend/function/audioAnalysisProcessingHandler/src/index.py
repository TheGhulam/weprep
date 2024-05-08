import json
import logging

import boto3

s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    video_id = "TEMP VAR"
    user_id = "TEMP CART"
    bucket_name = "weprep-user-videos"
    object_key = f"{user_id}/{video_id}.mp4"
    expiration = 3600  # URL expiration time in seconds

    try:
        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )
        return response(200, upload_url)
    except Exception as e:
        # Handle any exceptions that may occur
        print(f"Error generating pre-signed URL: {e}")
        upload_url = None


def response(status_code, upload_url):

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"videoUploadUrl": upload_url}),
    }
