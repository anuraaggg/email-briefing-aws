import os
import json
import boto3

from email_generator import fetch_recent_emails

S3_BUCKET = "email-briefing-secrets-anuraag"

TOKEN_KEY = "token.pickle"

TMP_TOKEN_PATH = "/tmp/token.pickle"

QUEUE_URL = os.environ["SQS_QUEUE_URL"]


def load_gmail_token():

    if not os.path.exists(TMP_TOKEN_PATH):
        s3 = boto3.client("s3")
        s3.download_file(S3_BUCKET, TOKEN_KEY, TMP_TOKEN_PATH)


def handler(event, context):

    load_gmail_token()

    emails = fetch_recent_emails(15)

    sqs = boto3.client("sqs")

    for sender, subject in emails:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps({"sender": sender, "subject": subject}),
        )

    return {
        "statusCode": 200,
        "body": f"Queued {len(emails)} emails for processing"
    }
