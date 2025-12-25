# 📬 AWS Serverless Email Briefing System

A serverless automation that sends a daily email summary using AWS-native services.
The system runs on a schedule and classifies emails into **Needs Action** and **FYI**
using deterministic rule-based logic.

---

## 🧱 Architecture

- **Amazon EventBridge Scheduler** – Triggers execution on a cron schedule
- **AWS Lambda (Python)** – Fetches email metadata and generates summaries
- **Amazon SES** – Sends the email briefing
- **Amazon S3** – Securely stores Gmail OAuth token
- **Amazon CloudWatch** – Logs execution and delivery status
- **IAM** – Least-privilege access control

---

## 🔄 Workflow

1. EventBridge Scheduler triggers the Lambda function
2. Lambda retrieves Gmail OAuth token from S3
3. Recent email subjects are fetched
4. Emails are classified into actionable vs informational
5. A formatted summary is emailed via Amazon SES

---

## ⚠️ Email Deliverability Note

This project uses Amazon SES **without a custom domain**.
As a result, emails may be delivered to spam folders.
This is expected behavior when SPF, DKIM, and DMARC are not configured.

---

## 🛠 Technologies Used

- AWS Lambda (Python)
- Amazon EventBridge Scheduler
- Amazon SES
- Amazon S3
- Amazon CloudWatch
- AWS IAM
- Gmail API

---

## 🚀 Use Cases

- Daily work email briefing
- Serverless automation
- Event-driven AWS architecture demonstration
