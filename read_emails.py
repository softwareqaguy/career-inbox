import os
import requests
from datetime import datetime, date 
from dotenv import load_dotenv

load_dotenv()

NYLAS_API_KEY = os.getenv("NYLAS_API_KEY")
NYLAS_GRANT_ID = os.getenv("NYLAS_GRANT_ID")
NYLAS_API_URI = os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")

if not NYLAS_API_KEY:
    raise ValueError("Missing NYLAS_API_KEY in .env")

if not NYLAS_GRANT_ID:
    raise ValueError("Missing NYLAS_GRANT_ID in .env")

JOB_KEYWORDS = [
    "recruiter",
    "hiring",
    "interview",
    "job",
    "position",
    "opportunity",
    "contract",
    "w2",
    "remote",
    "hybrid",
    "onsite",
    "qa",
    "quality assurance",
    "qa analyst",
    "qa engineer",
    "test analyst",
    "performance test",
    "automation",
    "software tester",
    "business analyst",
    "technical analyst",
    "application support",
    "production support",
    "databricks",
    "sql",
    "python",
    "resume",
    "background",
    "experience",
    "available",
    "availability",
]

def is_job_related(email):
    subject = email.get("subject", "") or ""
    snippet = email.get("snippet", "") or ""
    searchable_text = f"{subject} {snippet}".lower()

    return any(keyword in searchable_text for keyword in JOB_KEYWORDS)

def classify_email(email):
    subject = email.get("subject", "") or ""
    snippet = email.get("snippet", "") or ""
    sender = str(email.get("from", "")) or ""

    text = f"{subject} {snippet} {sender}".lower()

    if any(keyword in text for keyword in [
        "interview",
        "schedule a call",
        "phone screen",
        "video interview",
        "next steps",
        "availability",
        "available for a call",
        "follow up",
        "following up",
    ]):
        return "Interview or follow-up"

    if any(keyword in text for keyword in [
        "recruiter",
        "talent acquisition",
        "staffing",
        "w2 contract",
        "contract role",
        "contract position",
        "hiring for",
        "i came across your profile",
        "your background",
        "your experience",
    ]):
        return "Direct recruiter outreach"

    if any(keyword in text for keyword in [
        "job alert",
        "new jobs",
        "recommended jobs",
        "jobs you may be interested in",
        "linkedin job",
        "indeed",
        "ziprecruiter",
        "glassdoor",
        "dice",
    ]):
        return "Job alert / automated posting"

    if any(keyword in text for keyword in [
        "insurance",
        "save",
        "discount",
        "unsubscribe",
        "promotion",
        "limited time",
        "offer",
        "credit",
        "loan",
    ]):
        return "Possible marketing/noise"

    return "General job-related"

headers = {
    "Authorization": f"Bearer {NYLAS_API_KEY}",
    "Accept": "application/json"
}

url = f"{NYLAS_API_URI}/v3/grants/{NYLAS_GRANT_ID}/messages"

params = {
    "limit": 50
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

emails = response.json().get("data", [])
job_emails = [email for email in emails if is_job_related(email)]
print(f"Total emails checked: {len(emails)}")
print(f"Job-related emails found: {len(job_emails)}")
review_folder = "job_email_reviews"
os.makedirs(review_folder, exist_ok=True)

today = date.today().isoformat()
review_file = os.path.join(review_folder, f"job_email_review_{today}.md")

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
        category = classify_email(email)
        if raw_date:
            formatted_date = datetime.fromtimestamp(raw_date).strftime("%Y-%m-%d %I:%M:%S %p")
        else:            
            formatted_date = "No Date"

        print(f"\n{index}. {subject}")
        print(f"From: {sender}")
        print(f"Date: {formatted_date}")
        print(f"Category: {category}")

        if snippet:
            print(f"Snippet: {snippet}")


        print("-" * 70)

with open(review_file, "w", encoding="utf-8") as file:
    file.write(f"# Job Email Review - {today}\n\n")

    if not job_emails:
        file.write("No job-related emails found.\n")
    else:
        file.write(f"Found {len(job_emails)} job-related email(s).\n\n")

        for index, email in enumerate(job_emails, start=1):
            subject = email.get("subject", "No subject")
            sender = email.get("from", [])
            raw_date = email.get("date")
            snippet = email.get("snippet", "")
            category = classify_email(email)

            if raw_date:
                formatted_date = datetime.fromtimestamp(raw_date).strftime("%Y-%m-%d %I:%M:%S %p")
            else:
                formatted_date = "No date"

            file.write(f"## {index}. {subject}\n\n")
            file.write(f"**From:** {sender}\n\n")
            file.write(f"**Date:** {formatted_date}\n\n")
            file.write(f"**Category:** {category}\n\n")

            if snippet:
                file.write(f"**Snippet:** {snippet}\n\n")

            file.write("---\n\n")

print(f"\nJob email review saved to: {review_file}")