import os
import pickle
import boto3

from email_generator import fetch_recent_emails
from summarize import summarize
from send_email import send_email

S3_BUCKET = "email-briefing-secrets-anuraag"

TOKEN_KEY = "token.pickle"

TMP_TOKEN_PATH = "/tmp/token.pickle"


def load_gmail_token():

    if not os.path.exists(TMP_TOKEN_PATH):
        s3 = boto3.client("s3")
        s3.download_file(S3_BUCKET, TOKEN_KEY, TMP_TOKEN_PATH)


def handler(event, context):

    load_gmail_token()

    emails = fetch_recent_emails(15)

    summary = summarize(emails)

    send_email(summary)

    return {
        "statusCode": 200,
        "body": "Email briefing sent successfully"
    }
