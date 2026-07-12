# 📬 AWS Serverless Email Briefing System

A serverless automation that sends a daily email summary using AWS-native services.
The system runs on a schedule and classifies emails into **Needs Action** and **FYI**
using deterministic rule-based logic.

---

## 🧱 Architecture

- **Amazon EventBridge Scheduler** – Triggers the fetch stage on a cron schedule
- **AWS Lambda (Python) – Fetch stage** – Retrieves Gmail email metadata and enqueues it
- **Amazon SQS** – Decouples fetching from classification/delivery and buffers bursts of emails
- **AWS Lambda (Python) – Processing stage** – Triggered by SQS in batches; classifies emails and builds the summary
- **Amazon SES** – Sends the email briefing
- **Amazon S3** – Securely stores Gmail OAuth token
- **Amazon CloudWatch** – Logs execution and delivery status
- **IAM** – Least-privilege access control

---

## 🔄 Workflow

1. EventBridge Scheduler triggers the fetch Lambda (`fetch_handler.py`)
2. Fetch Lambda retrieves the Gmail OAuth token from S3
3. Recent email metadata (sender, subject) is fetched and pushed onto an SQS queue
   as a single message containing the full list for that run — this keeps a run's
   emails atomic so they're always classified and summarized together
4. SQS triggers the processing Lambda (`lambda_handler.py`), decoupling Gmail
   fetches from classification/delivery and buffering the queue if the processing
   side is briefly unavailable
5. Emails in the message are classified into actionable vs informational
6. A formatted summary is emailed via Amazon SES

### Fault tolerance

Because the two stages are decoupled by SQS, a failure in the processing Lambda
(e.g. a transient SES error) only affects the in-flight batch — SQS's visibility
timeout redelivers those messages for retry without re-fetching from Gmail. An
SQS redrive policy (dead-letter queue with `maxReceiveCount`) can be attached to
the queue so messages that repeatedly fail processing are captured for inspection
instead of being retried indefinitely.

---

## ⚠️ Email Deliverability Note

This project uses Amazon SES **without a custom domain**.
As a result, emails may be delivered to spam folders.
This is expected behavior when SPF, DKIM, and DMARC are not configured.

---

## 🛠 Technologies Used

- AWS Lambda (Python)
- Amazon EventBridge Scheduler
- Amazon SQS
- Amazon SES
- Amazon S3
- Amazon CloudWatch
- AWS IAM
- Gmail API

---

## ⚙️ Deployment Notes

This repo ships the two Lambda functions and no IaC template, so the queue and
triggers are wired up manually:

1. Create a standard SQS queue (e.g. `email-briefing-queue`) and, optionally, a
   dead-letter queue attached via a redrive policy.
2. Deploy `fetch_handler.py` as a Lambda with an EventBridge Scheduler trigger
   (cron) and an `SQS_QUEUE_URL` environment variable pointing at the queue.
3. Deploy `lambda_handler.py` as a second Lambda with an SQS trigger (event
   source mapping) on the same queue; leave the batch size at 1 so each queued
   message (one run's worth of emails) maps to exactly one summary email.
4. Grant the fetch Lambda `sqs:SendMessage` on the queue, and the processing
   Lambda `sqs:ReceiveMessage` / `sqs:DeleteMessage` / `sqs:GetQueueAttributes`.

---

## 🚀 Use Cases

- Daily work email briefing
- Serverless automation
- Event-driven AWS architecture demonstration
