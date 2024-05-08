import json

import boto3

s3 = boto3.client("s3")
bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
dynamodb = boto3.resource("dynamodb")
lambda_client = boto3.client("lambda")


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

    # Fetch the answers data from the weprep-user-audios bucket
    question_answer_data = []
    question_answer_prefix = f"{user_id}/{interview_id}/transcripts"
    question_answer_objects = s3.list_objects_v2(
        Bucket="weprep-user-audios", Prefix=question_answer_prefix
    )
    for obj in question_answer_objects["Contents"]:
        if video_id in obj["Key"] and "Question" in obj["Key"]:
            question_answer_response = s3.get_object(
                Bucket="weprep-user-audios", Key=obj["Key"]
            )
            question_answer_content = (
                question_answer_response["Body"].read().decode("utf-8")
            )
            question_answer_content = json.loads(question_answer_content)
            question_answer_data.append(
                question_answer_content["results"]["transcripts"][0]["transcript"]
            )

    # Fetch the question JSON files from the user-processed-data bucket
    question_data = []
    question_prefix = f"{user_id}/{interview_id}/"
    question_objects = s3.list_objects_v2(
        Bucket="user-processed-data", Prefix=question_prefix
    )

    for obj in question_objects["Contents"]:
        if obj["Key"].endswith("question1.json"):
            question_response = s3.get_object(
                Bucket="user-processed-data", Key=obj["Key"]
            )
            question_content = question_response["Body"].read().decode("utf-8")
            question_data.append(question_content)

    model_id = "anthropic.claude-3-opus-20240229-v1:0"
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
                                "text": f"{system_prompt}. This is the resume Data: {resume_content}. This is the list of questions: {question_data}. This is the list of answers: {question_answer_data}",  # noqa
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
    response_eval_body = json.loads(response_eval)

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
                                "text": f"I am giving you the feedback you generated, as well as the speech analysis metrics, as well as the questions and answers. I want you to generate a summary of about 10 lines over the good and bad aspects of it. Don't say stuff like the candidates, make it seem like you are giving a summary of what the answers were, so keep it objective. Something like The response to the question was bad or good etc. Respond with nothing else but the summary. Here are the things that I mentioned. Feedback Generated: {response_eval_body}. Speech Analysis Metrics: {speech_analysis}. The list of questions and respective answers in the second list: {question_data} {question_answer_data}",  # noqa
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

    try:
        table.update_item(
            Key={"videoId": video_id},
            UpdateExpression="SET feedbackAnalysis = :fa, SummaryAnalysis = :sa",
            ExpressionAttributeValues={
                ":fa": response_eval_body,
                ":sa": summary_eval_body,
            },
        )

    except Exception as e:
        print(f"Error updating DynamoDB table: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to update DynamoDB table"}),
        }

    event["summary"] = summary_eval_body
    lambda_client.invoke(
        FunctionName="webCrawlerhandler-dev",
        InvocationType="Event",
        Payload=json.dumps(event),
    )

    return {
        "statusCode": 200,
    }


system_prompt = """You are a professional interview evaluation assistant who only responds with JSON objects. You will be provided with context, interview questions, and subsequent candidate responses.
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
