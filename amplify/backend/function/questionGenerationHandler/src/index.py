import json
import time

import boto3
import requests

from .utils import system_prompt

bucket_name = "processed-cvs"
s3_client = boto3.client("s3")
api_token = "r8_PTUd7opDkDJMQYOzqALeOibvYNWClDD0DwkzL"
start_url = "https://api.replicate.com/v1/predictions"


def handler(event, context):
    user_id = event["pathParameters"]["user_id"]
    try:
        body = json.loads(event.get("body", ""))
        num_of_ques = body.get("numberOfQuestions")
        interviewer_tone = body.get("InterviewerTone")
    except json.JSONDecodeError:
        return response(400, "Invalid JSON format")
    objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{user_id}/")
    if "Contents" in objects:
        cv_file_key = objects["Contents"][0]["Key"]
        cv_object = s3_client.get_object(Bucket=bucket_name, Key=cv_file_key)
        cv_text = cv_object["Body"].read().decode("utf-8")
        form_data = f"Looking for questions related to the user's field of expertise. {num_of_ques} questions only."
        data = {
            "version": "02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            "input": {
                "debug": False,
                "top_k": 50,
                "top_p": 1,
                "prompt": f"{cv_text}{form_data}",
                "system_prompt": f"{system_prompt}. Keep your tone {interviewer_tone}.",
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
        if start_response.status_code != 200:
            return response(500, "Error starting prediction")
        start_result = start_response.json()
        get_url = start_result["urls"]["get"]
        for _ in range(30):
            poll_response = requests.get(get_url, headers=headers)
            poll_result = poll_response.json()
            if poll_result["status"] == "succeeded":
                result = join_tokens(poll_result["output"])
                return response(200, result)
            elif poll_result["status"] == "failed":
                return response(500, "Prediction failed")
            time.sleep(2)
        return response(408, "Request timed out")
    else:
        return response(404, "No CV found for the given user ID")


def join_tokens(tokens):
    text = ""
    for token in tokens:
        if token not in ["'", ".", ",", "!", "?", ";", ":"] and not text.endswith("'"):
            text += " "
        text += token
    return text.strip()


def response(status_code, message):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"message": message}),
    }
