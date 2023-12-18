import json
import logging
import time

import boto3
import requests
from utils.system_prompt import get_system_prompt

cv_bucket_name = "processed-cvs"
processed_questions_bucket_name = "user-processed-data"
s3_client = boto3.client("s3")
polly_client = boto3.client("polly")
api_token = "r8_PTUd7opDkDJMQYOzqALeOibvYNWClDD0DwkzL"
start_url = "https://api.replicate.com/v1/predictions"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    try:
        body = json.loads(event.get("body", ""))
        num_ques = body.get("numberOfQuestions")
        interviewer_tone = body.get("interviewerTone")
        interview_topic = body.get("interviewTopic")
    except json.JSONDecodeError:
        return response(400, "Invalid JSON format")
    objects = s3_client.list_objects_v2(Bucket=cv_bucket_name, Prefix=f"{user_id}/")
    if "Contents" in objects:
        cv_file_key = objects["Contents"][0]["Key"]
        cv_object = s3_client.get_object(Bucket=cv_bucket_name, Key=cv_file_key)
        cv_text = cv_object["Body"].read().decode("utf-8")
        logger.info(cv_text)
        data = {
            "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            "input": {
                "debug": False,
                "top_k": 50,
                "top_p": 1,
                "prompt": f"{cv_text}",
                "system_prompt": f"{get_system_prompt(num_ques, interview_topic)}. Keep your tone {interviewer_tone}.",
                "temperature": 0.5,
                "max_new_tokens": 500,
                "min_new_tokens": -1,
            },
        }
        headers = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json",
        }
        start_response = requests.post(
            start_url, headers=headers, data=json.dumps(data)
        )
        logger.info(start_response.text)

        start_result = start_response.json()
        get_url = start_result["urls"]["get"]
        for _ in range(30):
            poll_response = requests.get(get_url, headers=headers)
            poll_result = poll_response.json()
            logger.info(poll_result)

            if poll_result["status"] == "succeeded":
                result = join_tokens(poll_result["output"])
                audio_stream = text_to_speech(result, polly_client)
                save_to_s3(user_id, result, processed_questions_bucket_name)
                save_to_s3(
                    user_id,
                    audio_stream,
                    processed_questions_bucket_name,
                    file_name="questions.mp3",
                    is_audio=True,
                )
                audio_key = f"{user_id}/questions.mp3"
                presigned_url = generate_presigned_url(
                    processed_questions_bucket_name, audio_key
                )
                if presigned_url:
                    return response(200, {"url": presigned_url})
                else:
                    return response(500, {"message": "Error generating audio file URL"})
            elif poll_result["status"] == "failed":
                return response(500, "Prediction failed")
            time.sleep(2)
        return response(408, "Request timed out")
    else:
        return response(404, "No CV found for the given user ID")


def join_tokens(tokens):
    text = ""
    for token in tokens:
        text += token
    return text.strip()


def response(status_code, data):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            "Content-Type": "application/json",
        },
        "body": json.dumps(data),
    }


def save_to_s3(user_id, data, bucket_name, file_name="questions.json", is_audio=False):
    try:
        key = f"{user_id}/{file_name}"
        if is_audio:
            s3_client.put_object(
                Bucket=bucket_name, Key=key, Body=data, ContentType="audio/mpeg"
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
