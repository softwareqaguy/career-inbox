# Career Inbox

A Python workflow that connects to a Yahoo mailbox through the Nylas API, reads recent emails, and filters job/recruiter-related messages for daily review.

## Current Features

- Classifies filtered emails into practical review categories:
  - Direct recruiter outreach
  - Job alert / automated posting
  - Interview or follow-up
  - Possible marketing/noise
  - General job-related

## Planned Features

- AI-assisted summary for each job-related email
- Suggested next action for manual review
- Optional draft response support without automatic sending

## Tech Stack

- Python
- Nylas API
- Yahoo Mail via IMAP
- python-dotenv
- requests

## Security Notes

This project uses a local `.env` file for private credentials. The `.env` file is excluded from GitHub using `.gitignore`.