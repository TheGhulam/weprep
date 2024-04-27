# fmt: off
import base64
import json

import boto3
from utils.function_utils import (fetch_user_from_database,
                                  save_user_to_database, save_user_to_s3,
                                  verify_cognito_user)

# fmt: on
dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
cognito = boto3.client("cognito-idp")


def handler(event, context):
    http_method = event["httpMethod"]

    if http_method == "GET":
        return handle_get_request(event)
    elif http_method == "POST":
        return handle_post_request(event)
    else:
        return {
            "statusCode": 405,
            "body": f"HTTP method {http_method} is not supported",
        }


def handle_get_request(event):

    try:
        user_id = event["pathParameters"]["user-id"]

        user_data = fetch_user_from_database(user_id)

        return {"statusCode": 200, "body": json.dumps(user_data)}
    except Exception as e:
        print("Error fetching user data:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch user data"}),
        }


def handle_post_request(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        body = json.loads(event.get("body"))

        required_fields = ["email", "firstName", "lastName"]
        for field in required_fields:
            if field not in body:
                raise ValueError(
                    f"Required field '{field}' is missing in the request body"
                )

        email = body["email"]
        first_name = body["firstName"]
        last_name = body["lastName"]

        cognito_user = verify_cognito_user(email)
        if not cognito_user:
            raise ValueError("Email does not match any user in Cognito")

        about_me = body.get("aboutMe")
        skills = body.get("skills", [])
        phone_number = body.get("phoneNumber")
        picture_data_base64 = body.get("profilePictureData")

        if picture_data_base64:
            picture_data = base64.b64decode(picture_data_base64)
            save_user_to_s3(user_id, picture_data)

        save_user_to_database(
            user_id,
            first_name,
            last_name,
            email,
            about_me,
            skills,
            phone_number,
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "User data saved successfully in DB"}),
        }
    except Exception as e:
        print("Error processing user data:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
