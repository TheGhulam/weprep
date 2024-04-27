import json
import logging

import boto3

s3_client = boto3.client("s3")
bucket_name = "processed-cvs"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    folder_prefix = f"{user_id}/"
    logger.info(event)

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        logger.info(response)
        if "Contents" in response:
            object_key = response["Contents"][0]["Key"]

            object_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            return {
                "statusCode": 200,
                "body": json.dumps(
                    object_response["Body"].read().decode("utf-8"),
                ),
            }

        else:
            print(f"No files found for user id {user_id}.")
            return None
    except s3_client.exceptions.NoSuchKey:
        return {"statusCode": 500, "body": json.dumps("No such CV exists")}

    except Exception as e:
        logger.info(e)
        return {"statusCode": 500, "body": json.dumps("Text extraction failed.")}
