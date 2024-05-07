import datetime
import json
import re
import time
import urllib.request
import uuid
from collections import Counter

import boto3

s3 = boto3.client("s3")
transcribe_client = boto3.client("transcribe")
dynamodb = boto3.resource("dynamodb")


def handler(event, context):
    print("received event:")
    print(event)

    user_id = event["pathParameters"]["user-id"]
    audio_data = event["body"]
    video_id = str(uuid.uuid4())
    s3_key = f"{user_id}/raw/{video_id}.mp3"

    try:
        s3.put_object(
            Body=audio_data,
            Bucket="weprep-user-audios",
            Key=s3_key,
            ContentType="audio/mpeg",
        )
        print(f"Audio file uploaded to S3: {s3_key}")
    except Exception as e:
        print(f"Error uploading audio file to S3: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to upload audio file"}),
        }

    # Start the transcription job
    try:
        transcription_job_name = f"{user_id}_{video_id}_raw_audio_transcription"
        transcribe_client.start_transcription_job(
            TranscriptionJobName=transcription_job_name,
            Media={"MediaFileUri": f"s3://weprep-user-audios/{s3_key}"},
            MediaFormat="mp3",
            LanguageCode="en-US",
            OutputBucketName="weprep-user-audios",
            OutputKey=f"{user_id}/transcripts/{video_id}_raw_audio_transcript.json",
        )
    except Exception as e:
        print(f"Error starting transcription job: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to start transcription job"}),
        }

    while True:
        status = transcribe_client.get_transcription_job(
            TranscriptionJobName=transcription_job_name
        )["TranscriptionJob"]["TranscriptionJobStatus"]
        if status in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)

    if status == "COMPLETED":
        transcript_uri = transcribe_client.get_transcription_job(
            TranscriptionJobName=transcription_job_name
        )["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        transcript_data = json.loads(
            urllib.request.urlopen(transcript_uri).read().decode("utf-8")
        )
    else:
        print("Transcription job failed.")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Transcription job failed"}),
        }

    most_used_words = get_most_used_words(transcript_data)
    speech_speed = calculate_speech_speed(transcript_data)
    hedging_word_count = count_hedging_words(transcript_data)
    pronunciation_words, filler_word_count = count_filler_words(transcript_data)

    response_data = {
        "most_used_words": most_used_words,
        "speech_speed": speech_speed,
        "hedging_word_count": hedging_word_count,
        "pronunciation_words": pronunciation_words,
        "filler_word_count": filler_word_count,
    }

    table_name = "your_table_name"
    table = dynamodb.Table(table_name)

    try:
        table.put_item(
            Item={
                "userId": user_id,
                "videoId": video_id,
                "interviewId": event["interviewId"],
                "mostUsedWords": response_data["mostUsedWords"],
                "speechSpeed": response_data["speechSpeed"],
                "hedgingWordCount": response_data["hedgingWordCount"],
                "pronunciationWords": response_data["pronunciationWords"],
                "fillerWordCount": response_data["fillerWordCount"],
            }
        )
    except Exception as e:
        print(f"Error saving response data to DynamoDB: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps({"error": "Failed to save response data"}),
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps({"video-id": video_id}),
    }


def get_most_used_words(transcript_data, n=10):
    exclude_words = [
        "i",
        "we",
        "they",
        "a",
        "an",
        "the",
        "and",
        "or",
        "but",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "you",
        "it",
        "he",
        "she",
        "they",
        "we",
        "me",
        "him",
        "her",
        "us",
        "them",
        "my",
        "your",
        "his",
        "to",
        "of",
        "in",
        "on",
        "at",
        "by",
        "for",
        "with",
        "as",
        "from",
        "into",
        "onto",
    ]
    # Extract all "pronunciation" words
    pronunciation_words = [
        item["alternatives"][0]["content"].lower()
        for item in transcript_data["results"]["items"]
        if item["type"] == "pronunciation"
    ]

    # Remove punctuation and convert to lowercase
    clean_words = [re.sub(r"[^a-zA-Z]", "", word) for word in pronunciation_words]

    filtered_words = [word for word in clean_words if word.lower() not in exclude_words]

    # Count word frequencies
    word_counts = Counter(filtered_words)

    # Get the most common words
    most_common = word_counts.most_common(n)

    return most_common


def calculate_speech_speed(transcript_data: dict) -> int:
    """
    Calculate the speech speed (words per minute) based on the provided SRT data.

    Args:
        transcript_data (dict): The contents of the json file.

    Returns:
        float: The speech speed in words per minute.
    """
    first_word_start_time = transcript_data['results']['items'][0]['start_time']
    last_pronunciation_item = None
    word_count = 0
    for item in transcript_data['results']['items']:
        if item['type'] == 'pronunciation':
            last_pronunciation_item = item
            word_count += 1
    last_word_end_time = last_pronunciation_item['end_time']
    duration = float(last_word_end_time) - float(first_word_start_time)
    speech_speed = (word_count / duration) * 60
    return int(speech_speed)


def count_hedging_words(transcript_data: dict) -> int:
    """
    Count the number of hedging words in the transcript data.

    Args:
        transcript_data (dict): The transcript data as a dictionary.

    Returns:
        int: The count of hedging words.
    """
    hedging_words = [
        "maybe",
        "perhaps",
        "possibly",
        "probably",
        "likely",
        "apparently",
        "seems",
        "appears",
        "looks",
        "think",
        "believe",
        "suppose",
        "guess",
        "sort",
        "kind",
        "somewhat",
        "rather",
        "fairly",
        "relatively",
        "somewhat",
        "about",
        "around",
        "approximately",
        "almost",
        "nearly",
        "roughly",
        "like",
    ]

    print(hedging_words)

    transcript_text = " ".join(
        item["alternatives"][0]["content"].lower()
        for item in transcript_data["results"]["items"]
        if item["type"] == "pronunciation"
    )

    hedging_word_count = sum(
        re.search(rf"\b{word}\b", transcript_text) is not None for word in hedging_words
    )

    return hedging_word_count


def count_filler_words(transcript_data: dict) -> tuple[list[str], int]:
    """
    Count the number of filler words in the transcript data.

    Args:
        transcript_data (dict): The transcript data as a dictionary.

    Returns:
        tuple: A tuple containing:
            - A list of pronunciation words.
            - The count of filler words.
    """
    filler_words = [
        "um",
        "uh",
        "like",
        "you know",
        "so",
        "basically",
        "right",
        "well",
        "actually",
    ]

    pronunciation_words = [
        item["alternatives"][0]["content"].lower()
        for item in transcript_data["results"]["items"]
        if item["type"] == "pronunciation"
    ]

    filler_word_count = sum(word in filler_words for word in pronunciation_words)

    return pronunciation_words, filler_word_count


# FIGURE OUT WHERE SRT DATA IS COMING FROM
# ADD THE DATABASE TO SAVE THESE VALUES
# DEPLOY CHANGES AND PUSH TO CLOUD
