import json

import boto3
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from youtubesearchpython import VideosSearch

bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
dynamodb = boto3.resource("dynamodb")


def coursera_scrapper_helper(
    html_tags,
    tags_class,
    value,
    course_title,
    course_organization,
    course_details,
    course_link,
    query,
):
    url = (
        "https://www.coursera.org/search?query="
        + query
        + ("&sortBy=BEST_MATCH&index" "=prod_all_products_term_optimization")
    )
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    for j in range(0, value):
        x = soup.find_all(html_tags[0], class_=tags_class[0])[j].get_text()
        y = soup.find_all(html_tags[1], class_=tags_class[1])[j].get_text()
        while y[0] == "C":
            y = y[1:]

        z = soup.find_all(html_tags[1], class_=tags_class[2])[j].get_text()

        # v = soup.find_all(html_tags[1], class_ = tags_class[3])[j].get_text()
        f = (
            soup.find_all(
                html_tags[1],
                class_="cds-ProductCard-base cds-ProductCard-grid css-1gwppjr",
            )[j]
            .find("a")
            .get("href")
        )
        b = "https://www.coursera.org"
        f = b + f

        course_title.append(x)
        course_organization.append(y)
        course_details.append(z)
        course_link.append(f)


def scrap_Coursera(query):
    html_tags = ["h3", "div", "p"]
    tags_class = [
        "cds-CommonCard-title css-6ecy9b",
        "css-cxybwo cds-ProductCard-partners",
        "cds-CommonCard-metadata",
        "cds-CommonCard-bodyContent",
    ]

    course_title = []
    course_organization = []
    course_details = []
    course_link = []
    coursera_scrapper_helper(
        html_tags,
        tags_class,
        12,
        course_title,
        course_organization,
        course_details,
        course_link,
        query,
    )

    courses_data = []
    for i in range(len(course_title)):
        course_info = {
            "title": course_title[i],
            "course_organization": course_organization[i],
            "course_details": course_details[i],
            "url": course_link[i],
        }
        courses_data.append(course_info)

    # Convert the course data to JSON
    json.dumps(courses_data, indent=4)

    return courses_data


def scrape_youtube_videos(search_query):
    """
    Scrape YouTube videos based on a search query.
    Args:
        search_query (str): The search query to find relevant YouTube videos.
    Returns:
        list: A list of dictionaries containing information about the scraped YouTube videos.
    """
    # Create a VideosSearch object with the search query and limit the results to 12
    video_search = VideosSearch(search_query, limit=12)

    # Retrieve the list of video objects from the search results
    video_list = video_search.result()["result"]

    # Initialize an empty list to store video data
    video_data = []

    # Loop through the video list and extract relevant information for each video
    for video in video_list:
        video_info = {
            "title": video["title"],
            "url": f"https://www.youtube.com/watch?v={video['id']}",
            "views": video["viewCount"]["short"],
            "published": video["publishedTime"],
            "duration": video["duration"],
        }
        video_data.append(video_info)

    # Convert the video data list to JSON
    json.dumps(video_data, indent=4)

    return video_data


def google_search(query, num_results=12):
    """
    Perform a Google search and retrieve search results.
    Args:
        query (str): The search query.
        num_results (int, optional): Number of search results to retrieve. Defaults to 12.
    Returns:
        list: A list of dictionaries containing the URLs and titles of the search results.
    """
    # Perform the Google search
    search_results = search(query, num_results=num_results, advanced=True)

    # Initialize a list to store search result dictionaries
    search_data = []

    # Extract URLs and titles from search results and create dictionaries
    for result in search_results:
        search_info = {"url": result.url, "title": result.title}
        search_data.append(search_info)

    # Convert the search data to JSON
    json.dumps(search_data, indent=4)

    return search_data


def handler(event, context):
    print("received event:")
    print(event)

    user_id = event["user_id"]
    interview_id = event["interview_id"]
    video_id = event["video_id"]
    resume_id = event["resume_id"]

    summary = event["summary"]
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
                                "text": f"""I am giving you the summary that is generated for a user. Reply with only a query term and reason focusing on the weak points in the summary. Tell me the reason for it in 2 lines for each one over why and how looking into this topic will help the user improve. Keep it technical. Return me a list of JSON objects containing the query and the reason for it. Something like this: [{{query: some_query, reason: some_reason}}, {{query: some_query, reason: some_reason}}, ...]. Generate a total of 5 queries like this. Reply with only the JSON. Nothing else. Understood? Keep it 1 or 2 words but technical. Here is the summary: {summary}""",  # noqa
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
    queries = response_eval_list[0]["text"]
    queries = json.loads(queries)
    print(queries)

    merged_results = []

    for query_dict in queries:
        print(query_dict)
        query = query_dict["query"]
        reason = query_dict["reason"]
        google_results = google_search(query)
        coursera_results = scrap_Coursera(query)
        youtube_results = scrape_youtube_videos(query)

        merged_result = {
            "Query": query,
            "Reason": reason,
            "Google": google_results,
            "Coursera": coursera_results,
            "YouTube": youtube_results,
        }
        merged_results.append(merged_result)

    table_name = "userAudioDataTable-dev"
    table = dynamodb.Table(table_name)

    try:
        table.update_item(
            Key={"videoId": video_id},
            UpdateExpression="SET webCrawlerResults = :fa",
            ExpressionAttributeValues={":fa": merged_results},
        )

    except Exception as e:
        print(f"Error updating DynamoDB table: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Failed to update DynamoDB table"}),
        }

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(merged_results, indent=4),
    }
