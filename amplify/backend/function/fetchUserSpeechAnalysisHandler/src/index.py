import boto3
import simplejson as json

dynamodb = boto3.resource("dynamodb")
s3_client = boto3.client("s3")


def handler(event, context):
    print("received event:")
    print(event)

    video_id = event["pathParameters"]["video-id"]

    table_name = "userAudioDataTable-dev"
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={"videoId": video_id})
        item = response.get("Item")
        if item:
            # Extract the required fields from the item
            result = {
                "userId": item.get("userId"),
                "videoId": item.get("videoId"),
                "interviewId": item.get("interviewId"),
                "resumeId": item.get("resumeId"),
                "fillerWordCount": item.get("fillerWordCount"),
                "hedgingWordCount": item.get("hedgingWordCount"),
                "languagePositivity": item.get("langugagePositivity"),
                "mostUsedWords": item.get("mostUsedWords"),
                "pronunciationWords": item.get("pronunciationWords"),
                "speechSpeed": item.get("speechSpeed"),
                "feedbackAnalysis": item.get("feedbackAnalysis"),
                "summaryAnalysis": item.get("SummaryAnalysis"),
            }

        user_id = result["userId"]
        interview_id = result["interviewId"]
        object_key = f"{user_id}/{interview_id}/{video_id}.mp4"
        expiration = 3600
        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={"Bucket": "weprep-user-videos", "Key": object_key},
            ExpiresIn=expiration,
        )
        result["uploadUrl"] = upload_url
    except Exception as e:
        print(f"Error fetching data from DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to fetch data from DynamoDB"}),
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(result, use_decimal=True),
    }
