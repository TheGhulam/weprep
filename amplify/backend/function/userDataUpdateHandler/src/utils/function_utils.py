import base64

import boto3

dynamodb = boto3.client("dynamodb")
s3 = boto3.client("s3")
cognito = boto3.client("cognito-idp")

USER_POOL_ID = "eu-central-1_WmsK5drsR"
TABLE_NAME = "userTable-dev"
BUCKET_NAME = "user-profile-picture-data"


def verify_cognito_user(email):
    try:
        response = cognito.list_users(
            UserPoolId=USER_POOL_ID,
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
    dynamodb.put_item(
        TableName=TABLE_NAME,
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
    file_name = f"{user_id}-profile-picture"
    s3.put_object(Body=picture_data, Bucket=BUCKET_NAME, Key=file_name)


def update_cognito_password(user_id, new_password):

    cognito.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=user_id,
        Password=new_password,
        Permanent=True,
    )


def fetch_user_from_database(user_id):
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={"userId": {"S": user_id}},
    )
    user_data = response.get("Item")
    if user_data:
        picture_url = user_data.pop("profilePictureURL", {}).get("S", None)
        if picture_url:
            picture_data = retrieve_picture_from_s3(picture_url)
            user_data["profilePictureData"] = picture_data
    user_data = {
        "phoneNumber": user_data.get("phoneNumber").get("S"),
        "lastName": user_data.get("lastName").get("S"),
        "userId": user_data.get("userId").get("S"),
        "skills": user_data.get("skills").get("SS"),
        "email": user_data.get("email").get("S"),
        "firstName": user_data.get("firstName").get("S"),
        "aboutMe": user_data.get("aboutMe").get("S"),
    }
    return user_data


def retrieve_picture_from_s3(picture_url):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=picture_url)
        print(response)
        picture_data = response["Body"].read()
        # Encode picture data as base64
        picture_data_base64 = base64.b64encode(picture_data).decode("utf-8")
        return picture_data_base64
    except Exception as e:
        print("Error retrieving picture from S3:", e)
        return None
