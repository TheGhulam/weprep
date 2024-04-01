import json
import logging
import uuid

import boto3
from utils.function_utils import BUCKET_NAME, get_cv_url_from_s3

s3_client = boto3.client("s3")
allowed_file_types = {"pdf", "png", "jpg", "jpeg"}
dynamodb = boto3.client("dynamodb")

TABLE_NAME = "userCVsRecordTable-dev"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    http_method = event["httpMethod"]
    resource = event["resource"]

    if resource == "/cv-service/{user-id}/upload" and http_method == "POST":
        return handle_post_upload_cv_request(event)
    elif resource == "/cv-service/{user-id}/cv/{cv-id}" and http_method == "POST":
        return handle_post_upload_cv_data_request(event)

    elif http_method == "GET":
        return handle_get_request(event)
    elif http_method == "DELETE" and resource == "/cv-service/{user-id}/cv/{cv-id}":
        return handle_delete_request(event)
    else:
        return {"statusCode": 405, "body": json.dumps("Method Not Allowed")}


def handle_post_upload_cv_request(event):
    try:
        user_id = event["pathParameters"]["user-id"]

        file_content = event["body"]
        # file_content = base64.b64decode(file_content)

        cv_id = str(uuid.uuid4())

        file_name = f"{user_id}/{cv_id}"

        s3_client.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_content)

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

        body = json.loads(event.get("body"))
        cv_name = body["cvName"]

        dynamodb.put_item(
            TableName=TABLE_NAME,
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
                TableName=TABLE_NAME,
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
                TableName=TABLE_NAME,
                FilterExpression="#userId = :uid",
                ExpressionAttributeNames={"#userId": "userId"},
                ExpressionAttributeValues={":uid": {"S": user_id}},
            )

            items = response["Items"]
            if items:
                cv_files = []
                for item in items:
                    cv_id = item["cvId"]
                    print("This is the cv_id", cv_id)
                    cv_key = f"{user_id}/{cv_id}"
                    cv_url = get_cv_url_from_s3(cv_key)
                    cv_files.append(
                        {
                            "cvId": item.get("cvId").get("S"),
                            "cvName": item.get("cvId").get("S"),
                            "cvURL": cv_url,
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


def handle_delete_request(event):
    try:
        path_parameters = event.get("pathParameters", {})
        user_id = path_parameters.get("user-id")
        cv_id = path_parameters.get("cv-id")

        dynamodb.delete_item(
            TableName=TABLE_NAME,
            Key={"cvId": {"S": cv_id}},
        )

        cv_key = f"{user_id}/{cv_id}"
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=cv_key)
        return {"statusCode": 200, "body": {"message": "CV deleted successfully"}}

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error in deleting file."),
        }
