import json

from summarize import summarize
from send_email import send_email


def handler(event, context):

    emails = []

    for record in event.get("Records", []):
        body = json.loads(record["body"])
        emails.extend((item["sender"], item["subject"]) for item in body)

    if not emails:
        return {
            "statusCode": 200,
            "body": "No emails to process"
        }

    summary = summarize(emails)

    send_email(summary)

    return {
        "statusCode": 200,
        "body": f"Email briefing sent for {len(emails)} emails"
    }
