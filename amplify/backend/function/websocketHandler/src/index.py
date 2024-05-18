import json
import boto3


def handler(event, context):
    if event["requestContext"]["eventType"] == "CONNECT":
        # Handle new WebSocket connection
        print("Client connected")
        return {"statusCode": 200}
    elif event["requestContext"]["eventType"] == "DISCONNECT":
        # Handle WebSocket disconnection
        print("Client disconnected")
        return {"statusCode": 200}
    elif event["requestContext"]["routeKey"] == "sendAnalysis":
        # Send analysis updates to connected clients
        connection_ids = get_connection_ids(event)
        analysis_data = {"message": "Video analysis is ready"}

        api_gateway = boto3.client(
            "apigatewaymanagementapi",
            endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}",
        )

        for connection_id in connection_ids:
            try:
                api_gateway.post_to_connection(
                    ConnectionId=connection_id, Data=json.dumps(analysis_data)
                )
            except Exception as e:
                print(e)

        return {"statusCode": 200}

    return {"statusCode": 404}


def get_connection_ids(event):
    api_gateway = boto3.client(
        "apigatewaymanagementapi",
        endpoint_url=f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}",
    )

    connection_ids = []
    next_token = None

    while True:
        params = {"NextToken": next_token} if next_token else {}
        response = api_gateway.get_connections(**params)
        connection_ids.extend(
            [item["ConnectionId"] for item in response.get("Items", [])]
        )
        next_token = response.get("NextToken")

        if not next_token:
            break

    return connection_ids
