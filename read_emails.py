import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NYLAS_API_KEY = os.getenv("NYLAS_API_KEY")
NYLAS_GRANT_ID = os.getenv("NYLAS_GRANT_ID")
NYLAS_API_URI = os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")

if not NYLAS_API_KEY:
    raise ValueError("Missing NYLAS_API_KEY in .env")

if not NYLAS_GRANT_ID:
    raise ValueError("Missing NYLAS_GRANT_ID in .env")

JOB_KEYWORDS = ["recruiter", "hiring", "interview", "w2", "contract", "quality assurance", "qa analyst", "qa lead", "test analyst", "business analyst", "technical analyst", "application support", "production support", "databricks"]

def is_job_related(email):
    subject = email.get("subject", "") or ""
    snippet = email.get("snippet", "") or ""
    searchable_text = f"{subject} {snippet}".lower()

    return any(keyword in searchable_text for keyword in JOB_KEYWORDS)

headers = {
    "Authorization": f"Bearer {NYLAS_API_KEY}",
    "Accept": "application/json"
}

url = f"{NYLAS_API_URI}/v3/grants/{NYLAS_GRANT_ID}/messages"

params = {
    "limit": 10
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

emails = response.json().get("data", [])
job_emails = [email for email in emails if is_job_related(email)]

print("\nCareer Inbox - Job Related Emails")
print("=" * 70)

if not job_emails:
    print("No job-related emails found.")
else:
    for index, email in enumerate(job_emails, start=1):
        subject = email.get("subject", "No subject")
        sender = email.get("from", [])
        raw_date = email.get("date")
        snippet = email.get("snippet", "")
        if raw_date:
            formatted_date = datetime.fromtimestamp(raw_date).strftime("%Y-%m-%d %I:%M:%S %p")
        else:            
            formatted_date = "No Date"

        print(f"\n{index}. {subject}")
        print(f"From: {sender}")
        print(f"Date: {formatted_date}")

        if snippet:
            print(f"Snippet: {snippet}")


        print("-" * 70)