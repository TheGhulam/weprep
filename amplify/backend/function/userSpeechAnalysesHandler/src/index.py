import datetime
import json
import re
from collections import Counter

import boto3

# Transcript and Srt data
transcribe_client = boto3.client("transcribe")
s3_client = boto3.client("s3")
bucket_name = "weprep-user-audios"


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


def calculate_speech_speed(srt_data: str) -> float:
    """
    Calculate the speech speed (words per minute) based on the provided SRT data.

    Args:
        srt_data (str): The contents of the SRT file.

    Returns:
        float: The speech speed in words per minute.
    """
    lines = srt_data.strip().split("\n")
    text_lines = [
        line.strip() for line in lines if "-->" not in line and not line.isdigit()
    ]
    text = " ".join(text_lines)
    words_count = len(re.findall(r"\w+", text))

    timestamps = [line for line in lines if "-->" in line]

    start_time_str, _ = timestamps[0].split(" --> ")
    start_datetime = datetime.datetime.strptime(start_time_str, "%H:%M:%S,%f")

    _, end_time_str = timestamps[-1].split(" --> ")
    end_datetime = datetime.datetime.strptime(end_time_str, "%H:%M:%S,%f")

    total_duration = end_datetime - start_datetime
    total_seconds = total_duration.total_seconds()
    speed = words_count / (total_seconds / 60)

    return speed


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


def handler(event, context):
    print("received event:")
    print(event)

    # TODO: Get the transcript and srt data from the event
    transcript_data = "x"
    srt_data = "y"

    most_used_words = get_most_used_words(transcript_data)
    speech_speed = calculate_speech_speed(srt_data)
    hedging_word_count = count_hedging_words(transcript_data)
    pronunciation_words, filler_word_count = count_filler_words(transcript_data)

    response_data = {
        "most_used_words": most_used_words,
        "speech_speed": speech_speed,
        "hedging_word_count": hedging_word_count,
        "pronunciation_words": pronunciation_words,
        "filler_word_count": filler_word_count,
    }
    # TODO: save the response data to the database

    return {"statusCode": 200, "body": json.dumps(response_data)}
