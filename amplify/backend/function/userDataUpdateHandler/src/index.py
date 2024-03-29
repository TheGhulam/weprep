import base64
import json

import boto3

# Initialize DynamoDB client
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
        user_id = event["pathParameters"]["user_id"]

        user_data = fetch_user_from_database(user_id)

        user_password = get_cognito_password(user_id)

        user_data["password"] = user_password

        return {"statusCode": 200, "body": json.dumps(user_data)}
    except Exception as e:
        print("Error fetching user data:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to fetch user data"}),
        }


def handle_post_request(event):
    try:
        user_id = event["pathParameters"]["user_id"]

        body = json.loads(event["body"])
        password = body.get("password")
        first_name = body.get("firstName")
        last_name = body.get("lastName")
        email = body.get("email")
        about_me = body.get("aboutMe")
        skills = body.get("skills", [])
        phone_number = body.get("phoneNumber")

        picture_data_base64 = body.get("pictureData")
        if picture_data_base64:
            picture_data = base64.b64decode(picture_data_base64)

        save_user_to_s3(user_id, picture_data)
        update_cognito_password(user_id, password)

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
            "body": json.dumps({"message": "User data saved successfully"}),
        }
    except Exception as e:
        print("Error processing user data:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to process user data"}),
        }


def save_user_to_database(
    user_id,
    first_name,
    last_name,
    email,
    about_me,
    skills,
    phone_number,
):
    table_name = "userDataTable-dev"
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "userId": {"S": user_id},
            "firstName": {"S": first_name},
            "lastName": {"S": last_name},
            "email": {"S": email},
            "aboutMe": {"S": about_me},
            "skills": {"SS": skills},  # Assuming skills is a list of strings
            "phoneNumber": {"S": phone_number},
            "pictureURL": ({"S": f"{user_id}-profile-picture"}),
        },
    )


def save_user_to_s3(user_id, picture_data):
    bucket_name = "user-profile-picture-data"
    file_name = f"{user_id}-profile-picture"
    s3.put_object(Body=picture_data, Bucket=bucket_name, Key=file_name)


def update_cognito_password(user_id, new_password):

    cognito.admin_set_user_password(
        UserPoolId="eu-central-1_zua4po97J",
        Username=user_id,
        Password=new_password,
        Permanent=True,
    )


def fetch_user_from_database(user_id):
    response = dynamodb.get_item(
        TableName="userDataTable-dev", Key={"user_id": {"S": user_id}}
    )
    return response.get("Item", {})


def get_cognito_password(user_id):
    response = cognito.admin_get_user(
        UserPoolId="eu-central-1_zua4po97J", Username=user_id
    )
    return response["UserAttributes"][0]["Value"]
