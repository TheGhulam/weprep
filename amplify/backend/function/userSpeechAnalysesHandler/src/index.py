import datetime
import json
import re
from collections import Counter

import boto3

# Transcript data
transcribe_client = boto3.client("transcribe")
s3_client = boto3.client("s3")
bucket_name = "user-processed-data"


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


def calculate_speech_speed(transcript_data: dict) -> float:
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


def calculate_language_positivity(transcript_data):
    """
    Calculate the positivity percentage of the language used in the transcript data.

    Args:
        transcript_data (dict): The transcript data as a dictionary.

    Returns:
        float: The language positivity percentage, ranging from 0 (negative) to 100 (positive).
    """
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "brilliant", "superb",
                      "terrific"]
    negative_words = ["bad", "terrible", "awful", "horrible", "dreadful", "unpleasant", "nasty", "lousy", "poor"]

    transcript_text = " ".join(item["alternatives"][0]["content"].lower()
                               for item in transcript_data["results"]["items"]
                               if item["type"] == "pronunciation")

    positive_count = sum(re.search(rf"\b{word}\b", transcript_text) is not None for word in positive_words)
    negative_count = sum(re.search(rf"\b{word}\b", transcript_text) is not None for word in negative_words)

    total_words = positive_count + negative_count
    if total_words == 0:
        positivity_percentage = 50  # Neutral
    else:
        positivity_percentage = (positive_count / total_words) * 100

    return positivity_percentage


def handler(event, context):
    print("received event:")
    print(event)

    # TODO: Get the transcript data location from the event
    transcript_file = "x"
    with open(transcript_file, "r") as f:
        transcript_data = literal_eval(f.read())

    most_used_words = get_most_used_words(transcript_data)
    speech_speed = calculate_speech_speed(transcript_data)
    hedging_word_count = count_hedging_words(transcript_data)
    pronunciation_words, filler_word_count = count_filler_words(transcript_data)
    language_positivity_percentage = calculate_language_positivity(transcript_data)

    response_data = {
        "words_count": len(pronunciation_words),
        "filler_words_count": filler_word_count,
        "hedging_words_count": hedging_word_count,
        "speech_speed": speech_speed,
        "language_positivity_percentage": language_positivity_percentage,
        "most_used_words": most_used_words
    }
    # TODO: save the response data to the database

    return {"statusCode": 200, "body": json.dumps(response_data)}
