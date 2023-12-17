import json
import time

import boto3


def handler(event, context):
    s3_client = boto3.client("s3")
    textract_client = boto3.client("textract")

    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    file_key = event["Records"][0]["s3"]["object"]["key"]

    response = textract_client.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket_name, "Name": file_key}}
    )

    job_id = response["JobId"]

    while True:
        response = textract_client.get_document_text_detection(JobId=job_id)
        status = response["JobStatus"]
        if status in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(5)

    if status == "SUCCEEDED":
        extracted_text = ""
        for block in response["Blocks"]:
            if block["BlockType"] == "LINE":
                extracted_text += block["Text"] + "\n"

        output_bucket = "processed-cvs"
        output_key = file_key + ".json"
        s3_client.put_object(Body=extracted_text, Bucket=output_bucket, Key=output_key)

        return {
            "statusCode": 200,
            "body": json.dumps("Text extraction and saving successful."),
        }
    else:
        return {"statusCode": 500, "body": json.dumps("Text extraction failed.")}
