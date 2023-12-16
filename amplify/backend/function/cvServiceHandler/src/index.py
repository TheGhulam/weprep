import json

import boto3

s3_client = boto3.client("s3")
bucket_name = "user-cv173140-dev"


def handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "POST":
        return handle_post_request(event)

    elif http_method == "GET":
        return handle_get_request(event)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_post_request(event):
    try:
        # user_id = event['pathParameters']['userId']
        # file_content = event['body']
        # file_name = f"{user_id}/{uuid.uuid4()}.pdf"

        # s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return {"statusCode": 200, "body": json.dumps("File uploaded successfully.")}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("Error in uploading file.")}


def handle_get_request(event):
    try:
        user_id = event["pathParameters"]["userId"]
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=user_id + "/")
        files = [item["Key"] for item in response.get("Contents", [])]

        return {"statusCode": 200, "body": json.dumps(files)}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps("Error in fetching files.")}
