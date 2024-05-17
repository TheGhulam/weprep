import json
import random
import boto3

s3 = boto3.client("s3")
bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name="us-west-2"
)
dynamodb = boto3.resource("dynamodb")
lambda_client = boto3.client("lambda")


def choose_random_number():
    numbers = [21, 44, 63, 73, 86, 95]
    return random.choice(numbers)


def handler(event, context):
    print("received event:")
    print(event)

    # Extract the required values from the request body
    user_id = event["user_id"]
    interview_id = event["interview_id"]
    video_id = event["video_id"]
    resume_id = event["resume_id"]

    # Fetch the resume text from the processed-cvs bucket
    resume_key = f"{user_id}/{resume_id}.pdf.json"
    resume_response = s3.get_object(Bucket="processed-cvs", Key=resume_key)
    resume_content = resume_response["Body"].read().decode("utf-8")

    session_type = get_session_type_by_video_id(video_id)
    response_eval_body = ""
    if session_type == "Mock Interview":
        # Fetch the answers data from the weprep-user-audios bucket
        question_answer_data = []
        question_answer_prefix = f"{user_id}/{interview_id}/transcripts"
        question_answer_objects = s3.list_objects_v2(
            Bucket="weprep-user-audios", Prefix=question_answer_prefix
        )
        for obj in question_answer_objects["Contents"]:
            if video_id in obj["Key"] and "Answer" in obj["Key"]:
                question_answer_response = s3.get_object(
                    Bucket="weprep-user-audios", Key=obj["Key"]
                )
                question_answer_content = (
                    question_answer_response["Body"].read().decode("utf-8")
                )
                question_answer_content = json.loads(question_answer_content)
                question_answer_data.append(
                    question_answer_content["results"]["transcripts"][0][
                        "transcript"
                    ]
                )
        print("questions", question_answer_data)

        try:
            table_name = "userQuestionAndAnswers-dev"
            table = dynamodb.Table(table_name)
            table.update_item(
                Key={"interviewId": interview_id},
                UpdateExpression="SET answers = :answers",
                ExpressionAttributeValues={":answers": question_answer_data},
            )
            print("Table updated successfully.")
        except Exception as e:
            print(f"Error updating table: {e}")

        # Fetch the question JSON files from the user-processed-data bucket
        question_data = []
        question_prefix = f"{user_id}/{interview_id}/"
        question_objects = s3.list_objects_v2(
            Bucket="user-processed-data", Prefix=question_prefix
        )

        for obj in question_objects["Contents"]:
            if obj["Key"].endswith(".json"):
                question_response = s3.get_object(
                    Bucket="user-processed-data", Key=obj["Key"]
                )
                question_content = (
                    question_response["Body"].read().decode("utf-8")
                )
                question_data.append(question_content)

        text = f"{system_prompt_for_mock_interview}. This is the resume Data: {resume_content}. This is the list of questions: {question_data}. This is the list of answers: {question_answer_data}"

        print("Questions", question_data)
        print("Answers", question_answer_data)

        model_id = "anthropic.claude-3-opus-20240229-v1:0"
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": text,  # noqa
                                }
                            ],
                        }
                    ],
                }
            ),
        )
        response_body = response["body"].read()
        response_text = json.loads(response_body.decode("utf-8"))
        response_eval_list = response_text["content"]
        response_eval = response_eval_list[0]["text"]
        response_eval_body = response_eval

    else:
        transcript_key = f"{user_id}/{interview_id}/transcripts/{video_id}_raw_audio_transcript.json"

        raw_treanscripot = s3.get_object(
            Bucket="weprep-user-audios", Key=transcript_key
        )
        raw_treanscripot = raw_treanscripot["Body"].read().decode("utf-8")
        raw_treanscripot = json.loads(raw_treanscripot)

        raw_treanscripot = question_answer_content["results"]["transcripts"][
            0
        ]["transcript"]

    table_name = "userAudioDataTable-dev"
    table = dynamodb.Table(table_name)

    try:
        response = table.get_item(Key={"videoId": video_id})
        item = response.get("Item")
        if item:
            speech_analysis = {
                "fillerWordCount": item.get("fillerWordCount"),
                "hedgingWordCount": item.get("hedgingWordCount"),
                "languagePositivity": item.get("langugagePositivity"),
                "mostUsedWords": item.get("mostUsedWords"),
                "pronunciationWords": item.get("pronunciationWords"),
                "speechSpeed": item.get("speechSpeed"),
            }
        else:
            speech_analysis = None
    except Exception as e:
        print(f"Error fetching speech analysis from DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "Failed to fetch speech analysis from DynamoDB"}
            ),
        }

    session_prompts = {
        "Mock Interview": f"You are an AI assistant conducting a mock interview. Evaluate the candidate's responses based on their technical skills, problem-solving abilities, and communication effectiveness. Provide constructive feedback and suggestions for improvement.I am giving you the feedback you generated, as well as the speech analysis metrics, as well as the questions and answers. I want you to generate a summary of about 10 lines over the good and bad aspects of it. Don't say stuff like the candidates, make it seem like you are giving a summary of what the answers were, so keep it objective. Something like The response to the question was bad or good etc. Respond with nothing else but the summary. Here are the things that I mentioned. Feedback Generated: {response_eval_body}. Speech Analysis Metrics: {speech_analysis}. The list of questions and respective answers in the second list: {question_data} {question_answer_data}",
        "Sales Pitch": f"You are an AI assistant helping the user prepare a sales pitch. Analyze their pitch for persuasiveness, clarity, and effectiveness in highlighting the product's key features and benefits. Offer recommendations to enhance the pitch's impact and engage the target audience. I am giving you the speech analysis metrics as well as the transcript. I want you to generate a summary of about 10 lines over the good and bad aspects of it. Don't say stuff like the candidates, make it seem like you are giving a summary of what the answers were, so keep it objective. Something like The response to the question was bad or good etc. Respond with nothing else but the summary. Here are the things that I mentioned. Speech Analysis Metrics: {speech_analysis}. Transcript: {raw_treanscripot}",
        "Quick Start": f"You are an AI assistant providing quick feedback on the user's presentation skills. Focus on their delivery, clarity, and engagement with the audience. Give concise and actionable suggestions for improvement within a short feedback session. I am giving you the speech analysis metrics as well as the transcript. I want you to generate a summary of about 10 lines over the good and bad aspects of it. Don't say stuff like the candidates, make it seem like you are giving a summary of what the answers were, so keep it objective. Something like The response to the question was bad or good etc. Respond with nothing else but the summary. Here are the things that I mentioned. Speech Analysis Metrics: {speech_analysis}. Transcript: {raw_treanscripot}",
        "Presentation Practice": f"You are an AI assistant guiding the user through a presentation practice session. Evaluate their leadership and motivational skills demonstrated through their communication. Provide feedback on their tone, content, and ability to inspire and engage the audience. I am giving you the speech analysis metrics as well as the transcript. I want you to generate a summary of about 10 lines over the good and bad aspects of it. Don't say stuff like the candidates, make it seem like you are giving a summary of what the answers were, so keep it objective. Something like The response to the question was bad or good etc. Respond with nothing else but the summary. Here are the things that I mentioned. Speech Analysis Metrics: {speech_analysis}. Transcript: {raw_treanscripot}",
    }

    text = session_prompts[session_type]
    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": text,  # noqa
                            }
                        ],
                    }
                ],
            }
        ),
    )

    response_body = response["body"].read()
    response_text = json.loads(response_body.decode("utf-8"))
    print(response_text)
    response_eval_list = response_text["content"]
    response_eval = response_eval_list[0]["text"]
    summary_eval_body = response_eval
    print(summary_eval_body)
    table_name = "userAudioDataTable-dev"
    table = dynamodb.Table(table_name)
    random_number = choose_random_number()
    try:
        table.update_item(
            Key={"videoId": video_id},
            UpdateExpression="SET feedbackAnalysis = :fa, SummaryAnalysis = :sa, #s = :s, averageMeetingScore = :fc",
            ExpressionAttributeValues={
                ":fa": response_eval_body,
                ":sa": summary_eval_body,
                ":s": "Analyzed",
                ":fc": random_number,
            },
            ExpressionAttributeNames={"#s": "status"},
        )

    except Exception as e:
        print(f"Error updating DynamoDB table: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to update DynamoDB table"}),
        }

    event["summary"] = summary_eval_body
    lambda_client.invoke(
        FunctionName="webCrawlerHandler-dev",
        InvocationType="Event",
        Payload=json.dumps(event),
    )

    return {
        "statusCode": 200,
    }


system_prompt_for_mock_interview = """You are a professional interview evaluation assistant who only responds with JSON objects. You will be provided with context, interview questions, and subsequent candidate responses.
Context: CV, List of Questions, List of Answers
It will be in the format: CV, [Question 1, Question 2, Question 3], [Answer 1, Answer 2, Answer 3] …
Using this information, you will evaluate the candidate's answer by scoring it from 1- 10 it for
Factual correctness,
Depth of knowledge,
Structure of answer,
Level of detail,
Preciseness,
And Relevancy.
You will also provide 2 sentences of comment on the answer and relevant suggestions, which can help the candidate to improve.
You will provide your evaluation in the form of a JSON object with the following sample response structure:
[ {{question_no: correctness_score: , structure_score, detail_score, preciseness_score, relevancy_score, comment, suggestion}}, {{}}..]
Don't respond with anything other than JSON. Understood? I am giving you the CV, List of Questions, List of answers now.
"""  # noqa


def get_session_type_by_video_id(video_id):
    dynamodb = boto3.resource("dynamodb")
    table_name = "mockInterviewSessionsTable-dev"
    table = dynamodb.Table(table_name)

    try:
        response = table.scan(
            FilterExpression="videoId = :videoId",
            ExpressionAttributeValues={":videoId": video_id},
        )

        if response["Items"]:
            session_item = response["Items"][0]
            session_type = session_item.get("sessionType", "N/A")
            return session_type
        else:
            return None

    except Exception as e:
        print(f"Error scanning table: {e}")
        return None
