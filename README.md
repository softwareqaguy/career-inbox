# Career Inbox

Career Inbox is a Python workflow that helps organize job-search related emails from a Yahoo mailbox using the Nylas API. It reads recent inbox messages, filters for recruiter/job-related content, classifies the emails into practical categories, and saves a local review file for daily follow-up.

The project is designed as a personal job-search review workflow. It does not automatically respond to emails or make decisions. It helps surface relevant messages so they can be reviewed manually.

## Current Features

- Connects to Yahoo Mail through the Nylas API
- Reads recent inbox messages
- Formats email dates into a readable format
- Filters job-related emails using keyword matching
- Excludes obvious marketing/noise emails using exclude keywords
- Classifies filtered emails into review categories:
  - Direct recruiter outreach
  - Job alert / automated posting
  - Interview or follow-up
  - Possible marketing/noise
  - General job-related
- Generates a local job email review file
- Includes a manual review notes section for each email:
  - Role/company
  - Location/remote
  - Employment type
  - Pay/rate
  - Action needed
- Supports running locally through a Windows batch file
- Can be scheduled with Windows Task Scheduler
- Generated review files can sync through Google Drive Desktop for mobile access

## Tech Stack

- Python
- Nylas API
- Yahoo Mail via IMAP
- requests
- python-dotenv
- Windows Task Scheduler
- Google Drive Desktop

## Project Workflow

1. The script connects to the Nylas API using credentials stored locally in `.env`.
2. It retrieves recent Yahoo inbox messages.
3. Emails are filtered for job-search related content.
4. Obvious marketing/noise emails are excluded.
5. Remaining emails are classified into practical review categories.
6. A local review file is generated in the `job_email_reviews` folder.
7. The review file can sync to Google Drive Desktop for mobile access.
8. Windows Task Scheduler can run the workflow automatically on a recurring schedule.

## How to Run Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Create a `.env` file using `.env.example` as a guide:

``` env
NYLAS_API_KEY=your_nylas_api_key_here
NYLAS_GRANT_ID=your_nylas_grant_id_here
NYLAS_API_URI=https://api.us.nylas.com

Run the script:
python read_emails.py

The script creates a job email review file in the local job_email_reviews folder.