import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("userAudioAndVideoAnalysis")
s3 = boto3.client("s3")


def handler(event, context):
    print("received event:")
    print(event)

    user_id = event["pathParameters"]["user-id"]
    video_id = event["pathParameters"]["video-id"]

    try:
        # Fetch the specific record from DynamoDB using user_id and video_id
        response = table.query(
            KeyConditionExpression="userId = :user_id",
            FilterExpression="videoId = :video_id",
            ExpressionAttributeValues={
                ":user_id": user_id,
                ":video_id": video_id,
            },
            ProjectionExpression="interviewId, #s",
            ExpressionAttributeNames={"#s": "status"},
        )

        if "Items" in response and len(response["Items"]) > 0:
            item = response["Items"][0]
            interview_id = item.get("interviewId", "")
            status = item.get("status", "")

            # Fetch the audioAnalysis field from S3
            s3_key = f"{user_id}/{interview_id}/{video_id}_audio_analysis.json"
            try:
                s3_response = s3.get_object(
                    Bucket="video-audio-analysis-bucket", Key=s3_key
                )
                audio_analysis = json.loads(
                    s3_response["Body"].read().decode("utf-8")
                )
            except s3.exceptions.NoSuchKey:
                audio_analysis = {}

            s3_key = f"{user_id}/{interview_id}/{video_id}_engagement_analysis.json"
            try:
                s3_response = s3.get_object(
                    Bucket="video-audio-analysis-bucket", Key=s3_key
                )
                engagement_analysis = json.loads(
                    s3_response["Body"].read().decode("utf-8")
                )
            except s3.exceptions.NoSuchKey:
                engagement_analysis = {}

            s3_key = (
                f"{user_id}/{interview_id}/{video_id}_audio_emotion.json"
            )
            try:
                s3_response = s3.get_object(
                    Bucket="video-audio-analysis-bucket", Key=s3_key
                )
                emotion_analysis = json.loads(
                    s3_response["Body"].read().decode("utf-8")
                )
            except s3.exceptions.NoSuchKey:
                emotion_analysis = {}
            if audio_analysis and engagement_analysis and emotion_analysis:
            # Update the status field in DynamoDB

                table.update_item(
                    Key={
                        "userId": user_id,
                        "videoId": video_id,
                    },
                    UpdateExpression="SET #s = :status",
                    ExpressionAttributeNames={"#s": "status"},
                    ExpressionAttributeValues={":status": "analyzed"},
                )
                status = "analyzed"
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps(
                    {
                        "user_id": user_id,
                        "interview_id": interview_id,
                        "video_id": video_id,
                        "status": status,
                        "audioAnalysis": audio_analysis,
                        "engagementAnalysis": engagement_analysis,
                        "emotionAnalysis": emotion_analysis,
                    }
                ),
            }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps({"message": "Item not found"}),
            }
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"message": "Internal Server Error"}),
        }
