import json
import logging

import boto3

from utils.system_prompt import (
    get_behavioral_prompt,
    get_conversational_prompt,
    get_stress_prompt,
    get_technical_prompt,
)

cv_bucket_name = "processed-cvs"
processed_questions_bucket_name = "user-processed-data"
s3_client = boto3.client("s3")
polly_client = boto3.client("polly")
bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name="us-west-2"
)
dynamodb = boto3.client("dynamodb")


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    user_id = event["userId"]
    resume_id = event.get("resumeId", "")
    interview_id = event.get("interviewId", "")
    interview_type = event.get("interviewType", "behavioral")
    interview_duration = event.get("interviewDuration", "short")
    interviewer_tone = event.get("interviewTone", "neutral")
    interview_topic = event.get("jobTitle", "")
    session_type = event.get("sessionType", "")

    logger.info("Processing interview data for user ID: %s", user_id)

    if session_type == "Mock Interview":
        if resume_id:
            cv_file_key = f"{user_id}/{resume_id}.pdf.json"
            logger.info(
                "Resume ID provided, attempting to fetch CV from S3 with key: %s",
                cv_file_key,
            )

            try:
                cv_object = s3_client.get_object(
                    Bucket=cv_bucket_name, Key=cv_file_key
                )
                cv_text = cv_object["Body"].read().decode("utf-8")
                logger.info("CV text fetched successfully: %s", cv_text)

                num_ques = get_num_questions(interview_duration)
                logger.info("Number of questions determined: %d", num_ques)

                system_prompt = get_system_prompt(
                    interview_type, num_ques, interview_topic
                )
                logger.info("Generated system prompt: %s", system_prompt)

                model_id = "anthropic.claude-3-opus-20240229-v1:0"
                logger.info("Invoking the language model with ID: %s", model_id)
                safe_cv_text = cv_text.replace("{", "{{").replace("}", "}}")
                safe_system_prompt = system_prompt.replace("{", "{{").replace(
                    "}", "}}"
                )
                response = bedrock_client.invoke_model(
                    modelId=model_id,
                    body=json.dumps(
                        {
                            "anthropic_version": "bedrock-2023-05-31",
                            "max_tokens": 1500,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": f"{safe_cv_text}\n\n The job description is {interview_topic}.{safe_system_prompt}. Keep your tone {interviewer_tone}.",  # noqa
                                        }
                                    ],
                                }
                            ],
                        }
                    ),
                )
                try:
                    response_body = response["body"].read()
                    response_text = response_body.decode("utf-8")
                    print(response_text)
                    result = json.loads(response_text, strict=False)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {str(e)}")
                    print(f"Error occurred at line {e.lineno}, column {e.colno}")
                    print(f"Error message: {e.msg}")
                    print(
                        f"Snippet of the invalid JSON: {response_text[e.pos:e.pos+20]}"
                    )
                logger.info("Model invocation successful")
                try:

                    output_list = result.get("content", [])
                    output = output_list[0]
                    questions_binary = output["text"]
                    print(questions_binary)
                    questions = json.loads(questions_binary, strict=False)
                    questions_data = []

                    for index, question in enumerate(questions["questions"]):
                        question_text = question["text"]

                        # Save question text to S3
                        file_name = f"question{index + 1}.json"
                        save_to_s3(
                            user_id,
                            interview_id,
                            question_text,
                            processed_questions_bucket_name,
                            file_name,
                        )

                        # Convert text to speech
                        audio_stream = text_to_speech(question_text, polly_client)

                        # Save audio to S3
                        audio_file_name = f"question{index + 1}.mp3"
                        save_to_s3(
                            user_id,
                            interview_id,
                            audio_stream,
                            processed_questions_bucket_name,
                            audio_file_name,
                            is_audio=True,
                        )

                        questions_data.append(
                            {
                                "question_id": f"question{index + 1}",
                                "text": question_text,
                            }
                        )
                except Exception as e:
                    logger.error(f"An error occurred: {str(e)}")
                    logger.error(
                        f"Error occurred at line {e.__traceback__.tb_lineno}"
                    )

                item = {
                    "interviewId": {"S": interview_id},
                    "userId": {"S": user_id},
                    "questions": {
                        "L": [
                            {
                                "M": {
                                    "question_id": {"S": q["question_id"]},
                                    "text": {"S": q["text"]},
                                }
                            }
                            for q in questions_data
                        ]
                    },
                }

                response = dynamodb.put_item(
                    TableName="userQuestionAndAnswers-dev", Item=item
                )

                # save_to_s3(
                #     user_id,
                #     interview_id,
                #     audio_stream,
                #     processed_questions_bucket_name,
                #     file_name="questions.mp3",
                #     is_audio=True,
                # )
                # logger.info("Audio stream saved to S3")

                # audio_key = f"{user_id}/questions.mp3"
                # presigned_url = generate_presigned_url(
                #     processed_questions_bucket_name, audio_key
                # )
                # logger.info("Generated presigned URL: %s", presigned_url)
                # if not presigned_url:
                #     logger.error("Error generating audio file URL")
            except Exception as e:
                logger.error(
                    "Error processing resume data for user ID: %s, error: %s",
                    user_id,
                    str(e),
                )
        else:
            logger.warning("No resume ID found for user ID: %s", user_id)


def get_num_questions(interview_duration):
    if interview_duration == "short":
        return 3
    elif interview_duration == "medium":
        return 5
    elif interview_duration == "long":
        return 7
    else:
        return 3


def get_system_prompt(interview_type, num_ques, interview_topic):
    if interview_type == "behavioral":
        prompt = get_behavioral_prompt(num_ques)
        return prompt
    elif interview_type == "technical":
        return get_technical_prompt(num_ques)
    elif interview_type == "conversational":
        return get_behavioral_prompt(num_ques)
    elif interview_type == "stress":
        return get_behavioral_prompt(num_ques)
    else:
        return get_behavioral_prompt(num_ques)


def save_to_s3(
    user_id,
    interview_id,
    data,
    bucket_name,
    file_name="questions.json",
    is_audio=False,
):
    try:
        key = f"{user_id}/{interview_id}/{file_name}"
        if is_audio:
            s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=data,
                ContentType="audio/mpeg",
            )
        else:
            s3_client.put_object(Bucket=bucket_name, Key=key, Body=data)
        logger.info(f"Data successfully saved to {bucket_name}/{key}")
    except Exception as e:
        logger.error(f"Error saving data to S3: {e}")
        raise


def text_to_speech(text, polly_client):
    try:
        response = polly_client.synthesize_speech(
            Engine="neural", Text=text, OutputFormat="mp3", VoiceId="Ruth"
        )
        return response["AudioStream"].read()
    except Exception as e:
        logger.error(f"Error in text-to-speech conversion: {e}")
        raise


def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
        logger.error(f"Error generating presigned URL: {e}")
        return None
    return response


# SAVE ALL 3 QUESTIONS TO S3 SEPERATELY
