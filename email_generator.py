import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import pickle
from googleapiclient.discovery import build

from send_email import send_email
from summarize import summarize

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_service():
    token_path = "token.pickle"

    if os.environ.get("AWS_EXECUTION_ENV"):
        token_path = "/tmp/token.pickle"

    if not os.path.exists(token_path):
        raise RuntimeError("Gmail token not found")

    with open(token_path, "rb") as token:
        creds = pickle.load(token)

    return build("gmail", "v1", credentials=creds)



def fetch_recent_emails(max_results=15):
    service = get_service()

    results = (
        service.users()
        .messages()
        .list(userId="me", maxResults=max_results)
        .execute()
    )

    emails = []

    for msg in results.get("messages", []):
        data = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"])
            .execute()
        )

        headers = data["payload"]["headers"]

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"),
            "(No Subject)",
        )

        sender = next(
            (h["value"] for h in headers if h["name"] == "From"),
            "(Unknown Sender)",
        )

        emails.append((sender, subject))

    return emails


if __name__ == "__main__":

    emails = fetch_recent_emails(15)
    summary = summarize(emails)

    send_email(summary)
    print("✅ Summary sent to email")
