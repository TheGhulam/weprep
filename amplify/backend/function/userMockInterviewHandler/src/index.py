import simplejson as json
import random
import uuid
from datetime import datetime, timezone


import boto3

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("mockInterviewSessionsTable-dev")
lambda_client = boto3.client("lambda")


def handler(event, context):
    print("received event:")
    print(event)
    http_method = event["httpMethod"]
    resource = event["resource"]
    if (
        http_method == "POST"
        and resource == "/user/mock-interview/{user-id}/upload"
    ):
        return handle_post_request_for_updating_db(event)
    elif (
        http_method == "GET"
        and resource
        == "/user/mock-interview/{user-id}/interview/{interview-id}"
    ):
        return handle_get_request_for_specific_interview(event)
    elif http_method == "GET" and resource == "/user/mock-interview/{user-id}":
        return handle_get_request_for_all_interviews(event)

    elif (
        http_method == "DELETE"
        and resource
        == "/user/mock-interview/{user-id}/interview/{interview-id}"
    ):
        return handle_delete_request(event)
    else:
        return {
            "statusCode": 405,
            "body": json.dumps("Method Not Allowed"),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
        }


def handle_post_request_for_updating_db(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        interview_id = str(uuid.uuid4())
        request_body = json.loads(event["body"])

        current_time_utc = datetime.now(timezone.utc)
        timestamp_str = current_time_utc.isoformat()
        video_id = str(uuid.uuid4())

        # Update the request body with additional data
        request_body["userId"] = user_id
        request_body["interviewId"] = interview_id
        request_body["createdAt"] = timestamp_str
        request_body["videoId"] = video_id

        # Assuming 'table' is initialized DynamoDB Table resource
        table.put_item(Item=request_body)

        # Invoke the other Lambda function asynchronously
        lambda_client.invoke(
            FunctionName="questionGenerationHandler-dev",
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps(request_body),  # Pass the updated request body
        )

        # Return the interviewId immediately to the caller
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
            "body": json.dumps(
                {"interviewId": interview_id, "videoId": video_id}
            ),
        }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
            "body": json.dumps("Error processing request"),
        }


def handle_get_request_for_all_interviews(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        response = table.query(
            KeyConditionExpression="userId = :userId",
            ExpressionAttributeValues={":userId": user_id},
        )
        interviews = response.get("Items", [])

        if interviews:
            s3 = boto3.client("s3")
            audio_table = boto3.resource("dynamodb").Table(
                "userAudioDataTable-dev"
            )

            interviews_details = []
            for interview in interviews:
                video_url = ""
                thumbnail_url = ""
                avg_meeting_score = 0
                status = ""
                interview_id = interview.get("interviewId")

                # Query the userAudioDataTable-dev to get the videoId
                audio_response = audio_table.scan(
                    FilterExpression="interviewId = :interviewId",
                    ExpressionAttributeValues={":interviewId": interview_id},
                )

                if audio_response.get("Items"):
                    video_id = audio_response["Items"][0].get("videoId")
                    avg_meeting_score = audio_response["Items"][0].get(
                        "averageMeetingScore", 0
                    )
                    status = audio_response["Items"][0].get(
                        "status", "processing"
                    )

                    if video_id:
                        video_key = f"{user_id}/{interview_id}/{video_id}.mp4"

                        # Generate presigned URL for the video
                        video_url = s3.generate_presigned_url(
                            "get_object",
                            Params={
                                "Bucket": "weprep-user-videos",
                                "Key": video_key,
                            },
                            ExpiresIn=600,  # URL expires in 10 minutes
                        )

                        # Generate presigned URL for the thumbnail
                        thumbnail_url = (
                            video_url + "?x-amz-process=video-thumbnail"
                        )

                interview_details = {
                    k: v for k, v in interview.items() if k != "userId"
                }
                interview_details["videoUrl"] = video_url
                interview_details["thumbnailUrl"] = thumbnail_url
                interview_details["avgScore"] = avg_meeting_score
                interview_details["duration"] = status
                interview_details["duration"] = ""

                interviews_details.append(interview_details)

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
                },
                "body": json.dumps(
                    {"userId": user_id, "interviewDetails": interviews_details}
                ),
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
                },
                "body": json.dumps(f"No interviews found for user {user_id}"),
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error processing request"),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
        }


def handle_get_request_for_specific_interview(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        interview_id = event["pathParameters"]["interview-id"]
        response = table.get_item(
            Key={"userId": user_id, "interviewId": interview_id}
        )
        interview = response.get("Item")
        video_url = ""
        thumbnail_url = ""

        if interview:
            s3 = boto3.client("s3")
            audio_table = boto3.resource("dynamodb").Table(
                "userAudioDataTable-dev"
            )

            # Query the userAudioDataTable-dev to get the videoId
            audio_response = audio_table.scan(
                FilterExpression="interviewId = :interviewId",
                ExpressionAttributeValues={":interviewId": interview_id},
            )

            if audio_response.get("Items"):
                video_id = audio_response["Items"][0].get("videoId")
                avg_meeting_score = audio_response["Items"][0].get(
                    "averageMeetingScore"
                )
                status = audio_response["Items"][0].get("status")

                if video_id:
                    video_key = f"{user_id}/{interview_id}/{video_id}.mp4"

                    # Generate presigned URL for the video
                    video_url = s3.generate_presigned_url(
                        "get_object",
                        Params={
                            "Bucket": "weprep-user-videos",
                            "Key": video_key,
                        },
                        ExpiresIn=600,  # URL expires in 10 minutes
                    )

                    # Generate presigned URL for the thumbnail
                    thumbnail_url = (
                        video_url + "?x-amz-process=video-thumbnail"
                    )

            interview["videoUrl"] = video_url
            interview["thumbnailUrl"] = thumbnail_url
            interview["avgScore"] = avg_meeting_score
            interview["duration"] = status
            interview["duration"] = ""

            return {
                "statusCode": 200,
                "body": json.dumps(interview),
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
                },
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                    "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
                },
                "body": json.dumps({"error": "Interview not found"}),
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": "Error getting interview details",
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
        }


def handle_delete_request(event):
    try:
        user_id = event["pathParameters"]["user-id"]
        interview_id = event["pathParameters"]["interview-id"]
        table.delete_item(Key={"userId": user_id, "interviewId": interview_id})

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
            "body": json.dumps({"message": "Interview deleted successfully"}),
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # or specify the allowed origin
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",  # specify the allowed HTTP methods
                "Access-Control-Allow-Headers": "Content-Type, Authorization",  # specify the allowed headers
            },
            "body": json.dumps("error while deleting interview"),
        }


def choose_random_number():
    numbers = [21, 44, 63, 73, 86, 95]
    return random.choice(numbers)
