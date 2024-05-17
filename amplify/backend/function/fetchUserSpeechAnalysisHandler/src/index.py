import boto3
import simplejson as json
import random

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
        result = {}
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
                "status": item.get("status"),
                "averageMeetingScore": item.get("averageMeetingScore"),
            }

        user_id = result["userId"]
        interview_id = result["interviewId"]

        key = f"{user_id}/{interview_id}/transcripts/{video_id}_raw_audio_transcript.json"
        object_response = s3_client.get_object(
            Bucket="weprep-user-audios", Key=key
        )

        transcript = object_response["Body"].read().decode("utf-8")
        transcript = json.loads(transcript)
        result["transcript"] = transcript["results"]["transcripts"][0][
            "transcript"
        ]
        questions = []
        # try:
        #     table_name = "userQuestionAndAnswers-dev"
        #     table = dynamodb.Table(table_name)
        #     response = table.get_item(Key={"interviewId": interview_id})

        #     if "Item" in response:
        #         item = response["Item"]
        #         questions_data = item.get("questions", [])
        #         answers_data = item.get("answers", [])

        #         print(questions_data, answers_data)

        #         questions = []

        #         for i in range(min(len(questions_data), len(answers_data))):
        #             question = questions_data[i]["text"]
        #             answer = answers_data[i]

        #             question_answer_pair = {
        #                 "question": question,
        #                 "answer": answer,
        #             }

        #             questions.append(question_answer_pair)

        #         result["questions"] = questions

        # except Exception as e:
        #     result["questions"] = []

    except Exception as e:
        print(f"Error fetching data from DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(
                {"error": "Failed to fetch data from DynamoDB"}
            ),
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
