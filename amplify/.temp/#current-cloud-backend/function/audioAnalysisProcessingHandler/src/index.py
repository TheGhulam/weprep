import json
import logging
import time

import boto3
import requests
from utils.system_prompt import get_system_prompt

s3_client = boto3.client("s3")

api_token = "r8_PTUd7opDkDJMQYOzqALeOibvYNWClDD0DwkzL"
start_url = "https://api.replicate.com/v1/predictions"

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_key = event["Records"][0]["s3"]["object"]["key"]

    if "user_answers_audio.json" in file_key:
        print(event)
        print(file_key)
        user_id = 1
        folder_prefix = f"{user_id}/"
        user_analysis_questions_key = f"{folder_prefix}questions.json"
        print(user_analysis_questions_key)
        user_analysis_questions_object = s3_client.get_object(
            Bucket=bucket_name, Key=user_analysis_questions_key
        )
        user_analysis_answers_object = s3_client.get_object(
            Bucket=bucket_name, Key=file_key
        )
        user_analysis_questions = (
            user_analysis_questions_object["Body"].read().decode("utf-8")
        )
        user_analysis_full_answers = (
            user_analysis_answers_object["Body"].read().decode("utf-8")
        )
        user_analysis_full_answers = json.loads(user_analysis_full_answers)

        user_analysis_transcript = user_analysis_full_answers["results"]["transcripts"][
            0
        ]["transcript"]
        prompt = (
            f"These are the interview questions {user_analysis_questions}."
            f"These are the interview answers {user_analysis_transcript}"
        )
        data = {
            "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            "input": {
                "debug": False,
                "top_k": 50,
                "top_p": 1,
                "prompt": prompt,
                "system_prompt": f"{get_system_prompt()}",
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
        while True:
            poll_response = requests.get(get_url, headers=headers)
            poll_result = poll_response.json()
            logger.info(poll_result)

            if poll_result["status"] == "succeeded":
                result = join_tokens(poll_result["output"])
                s3_client.put_object(
                    Bucket=bucket_name,
                    Key=f"{user_id}/audio_analysis.json",
                    Body=result,
                )
                return response(200, "Analysis successful")
            elif poll_result["status"] == "failed":
                return response(500, "Prediction failed")
            time.sleep(2)
    return response(500, "Wrong trigger file")


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
