import json

import boto3

s3_client = boto3.client("s3")
bucket_name = "processed-cvs"


def handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    folder_prefix = f"{user_id}/"

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        if "Contents" in response:
            object_key = response["Contents"][0]["Key"]

            # Retrieve the object
            object_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
            return {
                "statusCode": 200,
                "body": object_response["Body"].read().decode("utf-8"),
            }

        else:
            print(f"No files found for user id {user_id}.")
            return None
    except s3_client.exceptions.NoSuchKey:
        return {"statusCode": 500, "body": json.dumps("Text extraction failed.")}

    except Exception:
        return {"statusCode": 500, "body": json.dumps("Text extraction failed.")}
