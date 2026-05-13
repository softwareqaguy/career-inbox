import os
import requests
from datetime import datetime, date 
from dotenv import load_dotenv
#from openai import OpenAI

load_dotenv()

NYLAS_API_KEY = os.getenv("NYLAS_API_KEY")
NYLAS_GRANT_ID = os.getenv("NYLAS_GRANT_ID")
NYLAS_API_URI = os.getenv("NYLAS_API_URI", "https://api.us.nylas.com")
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not NYLAS_API_KEY:
    raise ValueError("Missing NYLAS_API_KEY in .env")

if not NYLAS_GRANT_ID:
    raise ValueError("Missing NYLAS_GRANT_ID in .env")

'''if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in .env")'''

#client = OpenAI(api_key=OPENAI_API_KEY)

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

EXCLUDE_KEYWORDS = [
    "bath remodel",
    "bath remodeling",
    "blinds",
    "budget blinds",
    "free consultation",
    "in-home consultation",
    "insurance",
    "loan",
    "credit card",
    "save money",
    "discount",
    "promotion",
    "limited time",
    "unsubscribe",
]

def is_job_related(email):
    subject = email.get("subject", "") or ""
    snippet = email.get("snippet", "") or ""
    sender = str(email.get("from", "")) or ""

    searchable_text = f"{subject} {snippet} {sender}".lower()

    if any(keyword in searchable_text for keyword in EXCLUDE_KEYWORDS):
        return False

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
        "new job opportunities",
        "new positions",
        "new positions we just posted",
        "career site",
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
    "bath remodel",
    "bath remodeling",
    "blinds",
    "free consultation",
    "in-home consultation",
]):
        return "Possible marketing/noise"

    return "General job-related"

'''def generate_review_notes(email):
    subject = email.get("subject", "") or ""
    snippet = email.get("snippet", "") or ""
    sender = email.get("from", [])

    prompt = f"""
You are helping review job-search related emails.

Analyze this email and extract practical review notes.
Do not make assumptions. If something is not mentioned, write "Not mentioned".
Keep the response concise.

Email subject:
{subject}

Sender:
{sender}

Email snippet:
{snippet}

Return the result in this exact format:

- Role/company:
- Location/remote:
- Employment type:
- Pay/rate:
- Action needed:


    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    return response.output_text'''

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
print("\nRecent subjects checked:")
for email in emails:
    print("-", email.get("subject", "No subject"))
job_emails = [email for email in emails if is_job_related(email)]
print(f"Total emails checked: {len(emails)}")
print(f"Job-related emails found: {len(job_emails)}")
review_folder = "job_email_reviews"
os.makedirs(review_folder, exist_ok=True)

today = date.today().isoformat()
review_file = os.path.join(review_folder, f"job_email_review_{today}.txt")

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
            
            file.write("**Review Notes:**\n\n")
            file.write("- Role/company:\n")
            file.write("- Location/remote:\n")
            file.write("- Employment type:\n")
            file.write("- Pay/rate:\n")
            file.write("- Action needed:\n\n")
            
            '''file.write("**AI-Generated Review Notes:**\n\n")

            try:
                ai_notes = generate_review_notes(email)
                file.write(ai_notes)
                file.write("\n\n")
            except Exception as error:
                file.write("AI review could not be generated.\n\n")
                file.write(f"Error: {error}\n\n")'''
            
            file.write("---\n\n")

print(f"\nJob email review saved to: {review_file}")