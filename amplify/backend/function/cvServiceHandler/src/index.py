import base64
import json
import logging
import uuid

import boto3

s3_client = boto3.client("s3")
bucket_name = "user-cv173140-dev"
allowed_file_types = {"pdf", "png", "jpg", "jpeg"}
dynamodb = boto3.client("dynamodb")

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    http_method = event["httpMethod"]
    resource = event["resource"]

    if resource == "/cv-service/{user-id}/upload" and http_method == "POST":
        # Logic for handling POST requests to /path1
        return handle_post_upload_cv_request(event)
    elif resource == "/cv-service/{user-id}/cv/{cv-id}" and http_method == "POST":
        # Logic for handling POST requests to /path2
        return handle_post_upload_cv_data_request(event)

    elif http_method == "GET":
        return handle_get_request(event)

    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_post_upload_cv_request(event):
    try:
        user_id = event["pathParameters"]["user-id"]

        # Extract file content and CV name from the event body
        file_content = event["body"]
        file_content = base64.b64decode(file_content)

        cv_id = str(uuid.uuid4())

        file_name = f"{user_id}/{cv_id}"

        # Upload the file to S3
        s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "File uploaded successfully.",
                    "cv_id": cv_id,
                }
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error in uploading file."),
        }


def handle_post_upload_cv_data_request(event):
    try:
        path_parameters = event.get("pathParameters", {})
        user_id = path_parameters.get("user-id")
        cv_id = path_parameters.get("cv-id")

        body = event.get("body")
        body = json.loads(base64.b64decode(body).decode("utf-8"))
        cv_name = body["cvName"]

        dynamodb.put_item(
            TableName="userCVsRecordTable-dev",
            Item={
                "userId": {"S": user_id},
                "cvId": {"S": cv_id},
                "cvName": {"S": cv_name},
            },
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "CV data saved successfully in DB"}),
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error in uploading CV Data."),
        }


def handle_get_request(event):
    try:
        path_parameters = event.get("pathParameters", {})
        user_id = path_parameters.get("user-id")
        cv_id = path_parameters.get("cv-id")

        if cv_id:
            response = dynamodb.scan(
                TableName="userCVsRecordTable-dev",
                FilterExpression="userId = :user_id_val AND cvId = :cv_id_val",
                ExpressionAttributeValues={
                    ":user_id_val": {"S": user_id},
                    ":cv_id_val": {"S": cv_id},
                },
            )
            item = response["Items"][0]

            if item:
                cv_key = f"{user_id}/{cv_id}"
                cv_url = get_cv_url_from_s3(cv_key)
                cv_details = {
                    "userId": item.get("userId").get("S"),
                    "cvId": item.get("cvId").get("S"),
                    "cvName": item.get("cvName").get("S"),
                    "cvURL": cv_url,
                }
                return {"statusCode": 200, "body": json.dumps(cv_details)}
            else:
                return {"statusCode": 404, "body": "CV not found"}
        else:
            response = dynamodb.scan(
                TableName="userCVsRecordTable-dev",
                FilterExpression="#userId = :uid",
                ExpressionAttributeNames={"#userId": "userId"},
                ExpressionAttributeValues={":uid": {"S": user_id}},
            )

            items = response["Items"]
            if items:
                cv_files = []
                for cv_detail in items:
                    cv_id = cv_detail["cvId"]
                    cv_key = f"{user_id}/{cv_id}"
                    cv_url = get_cv_url_from_s3(cv_key)
                    cv_files.append(
                        {
                            "cv_id": cv_id,
                            "cv_name": cv_detail["cvName"],
                            "cv_url": cv_url,
                        }
                    )
        return {
            "statusCode": 200,
            "body": json.dumps({"userId": user_id, "cvDetails": cv_files}),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error in fetching files."),
        }


def get_cv_url_from_s3(cv_key):
    try:
        return generate_presigned_url(cv_key)
    except s3_client.exceptions.NoSuchKey:
        return None  # CV file not found
    except Exception as e:
        print("Error:", e)
        return None


def generate_presigned_url(object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
        logger.error(f"Error generating presigned URL: {e}")
        return None
    return response
