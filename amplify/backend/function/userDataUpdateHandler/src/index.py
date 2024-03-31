import base64
import json

import boto3

# Initialize DynamoDB client
dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
cognito = boto3.client("cognito-idp")


def handler(event, context):
    print(event)
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

        # Check if required fields are present
        required_fields = ["email", "firstName", "lastName"]
        for field in required_fields:
            if field not in body:
                raise ValueError(
                    f"Required field '{field}' is missing in the request body"
                )

        # Extract required fields
        email = body["email"]
        first_name = body["firstName"]
        last_name = body["lastName"]

        # Verify email against Cognito
        cognito_user = verify_cognito_user(email)
        if not cognito_user:
            raise ValueError("Email does not match any user in Cognito")

        # Optional fields
        about_me = body.get("aboutMe")
        skills = body.get("skills", [])
        phone_number = body.get("phoneNumber")
        picture_data_base64 = body.get("profilePictureData")

        # Processing picture data if available
        if picture_data_base64:
            picture_data = base64.b64decode(picture_data_base64)
            save_user_to_s3(user_id, picture_data)

        # Saving user data to the database
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


def verify_cognito_user(email):
    try:
        response = cognito.list_users(
            UserPoolId="eu-central-1_zua4po97J",
            AttributesToGet=["email"],
            Filter=f'email = "{email}"',
        )
        if response["Users"]:
            return response["Users"][0]
        else:
            return None
    except Exception as e:
        print("Error verifying user in Cognito:", e)
        return None


def save_user_to_database(
    user_id,
    first_name,
    last_name,
    email,
    about_me,
    skills,
    phone_number,
):
    table_name = "userTable-dev"
    dynamodb.put_item(
        TableName=table_name,
        Item={
            "userId": {"S": user_id},
            "firstName": {"S": first_name},
            "lastName": {"S": last_name},
            "email": {"S": email},
            "aboutMe": {"S": about_me},
            "skills": {"SS": skills},
            "phoneNumber": {"S": phone_number},
            "profilePictureURL": ({"S": f"{user_id}-profile-picture"}),
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
        TableName="userTable-dev",
        Key={"userId": {"S": user_id}},
    )
    user_data = response.get("Item")
    if user_data:
        # Get picture data from S3 if available
        picture_url = user_data.pop("profilePictureURL", {}).get("S", None)
        if picture_url:
            # Retrieve picture data from S3
            picture_data = retrieve_picture_from_s3(picture_url)
            # Add picture data to user data
            user_data["profilePictureData"] = picture_data
    return user_data


def retrieve_picture_from_s3(picture_url):
    try:
        bucket_name = "user-profile-picture-data"
        # Extract bucket name and object key from picture URL
        # Retrieve picture data from S3
        response = s3.get_object(Bucket=bucket_name, Key=picture_url)
        print(response)
        picture_data = response["Body"].read()
        # Encode picture data as base64
        picture_data_base64 = base64.b64encode(picture_data).decode("utf-8")
        return picture_data_base64
    except Exception as e:
        print("Error retrieving picture from S3:", e)
        return None


# def hash_password(password):
#     salt = bcrypt.gensalt()
#     hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
#     return hashed_password
