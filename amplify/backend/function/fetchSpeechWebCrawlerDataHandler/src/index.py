import json

import boto3


def handler(event, context):
    print("received event:")
    print(event)

    # Get the video-id from the path parameters
    video_id = event["pathParameters"]["video-id"]

    # Create a DynamoDB client
    dynamodb = boto3.resource("dynamodb")

    # Specify the table name
    table_name = "userAudioDataTable-dev"

    # Get the table
    table = dynamodb.Table(table_name)

    try:
        # Fetch the item from the table using the video-id
        response = table.get_item(Key={"videoId": video_id})

        # Check if the item exists
        if "Item" in response:
            item = response["Item"]

            # Check if the webCrawlerResults attribute exists
            if "webCrawlerResults" in item:
                web_crawler_results = item["webCrawlerResults"]
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                    "body": json.dumps(web_crawler_results),
                }
            else:
                return {
                    "statusCode": 404,
                    "headers": {
                        "Access-Control-Allow-Headers": "*",
                        "Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                    },
                    "body": json.dumps(
                        "webCrawlerResults not found for the given video-id"
                    ),
                }
        else:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
                },
                "body": json.dumps("Item not found for the given video-id"),
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
            },
            "body": json.dumps(f"An error occurred: {str(e)}"),
        }
