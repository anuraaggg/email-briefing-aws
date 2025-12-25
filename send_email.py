import boto3

SENDER = "anuraagshnkr@gmail.com"   
RECIPIENT = "anuraagshnkr@gmail.com"

def send_email(summary):
    ses = boto3.client("ses", region_name="ap-south-1")

    ses.send_email(
        Source=SENDER,
        Destination={"ToAddresses": [RECIPIENT]},
        Message={
            "Subject": {"Data": "📬 Work Email Briefing"},
            "Body": {
                "Text": {"Data": summary}
            }
        }
    )
