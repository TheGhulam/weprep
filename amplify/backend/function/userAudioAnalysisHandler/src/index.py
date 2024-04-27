import json
import logging

import boto3

user_processed_data_bucket_name = "user-processed-data"
s3_client = boto3.client("s3")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "GET":
        user_id = event["pathParameters"]["user_id"]
        audio_analysis_file_key = f"{user_id}/audio_analysis.json"

        user_analysis_audio = s3_client.get_object(
            Bucket=user_processed_data_bucket_name, Key=audio_analysis_file_key
        )

        user_analysis_audio = user_analysis_audio["Body"].read().decode("utf-8")
        return response(200, user_analysis_audio)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def response(status_code, data):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps(data),
    }
