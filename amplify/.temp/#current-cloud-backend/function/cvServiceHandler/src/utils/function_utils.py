import boto3

s3_client = boto3.client("s3")
BUCKET_NAME = "user-cv173140-dev"


def get_cv_url_from_s3(cv_key):
    try:
        return generate_presigned_url(cv_key)
    except s3_client.exceptions.NoSuchKey:
        return None
    except Exception as e:
        print("Error:", e)
        return None


def generate_presigned_url(object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
        print("Error:", e)
        return None
    return response
