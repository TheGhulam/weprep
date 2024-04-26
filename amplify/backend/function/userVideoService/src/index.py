import json


def handler(event, context):
    video_id = event["pathParameters"]["interview-id"]
    base_url = "https://d38eh3vxny00rq.cloudfront.net/"
    video_url = f"{base_url}{video_id}.mp4"

    questions = [
        "I noticed on your resume that you've extensively used AWS services like Kubernetes, Lambdas, and S3 in your role at Spike Technologies. Can you describe a specific project where you implemented these technologies and the challenges you faced during deployment?",  # noqa
        "You've developed APIs using FastAPI and employed asynchronous techniques for handling large API calls at both Spike Technologies and Spiky.AI. Could you walk us through the design and development process of one of your most complex APIs, particularly how you managed data fetching and processing?",  # noqa
        "In your experience at Spiky.AI, you worked collaboratively using tools like Jira, Slack, and GitHub, and were involved in agile development. Can you discuss a particular instance where your team had to adapt or overcome a significant hurdle during a sprint, and how you contributed to resolving it?",  # noqa
    ]

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"video_url": video_url, "questions": questions}),
    }
