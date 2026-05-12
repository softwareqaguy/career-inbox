# Career Inbox

A Python workflow that connects to a Yahoo mailbox through the Nylas API, reads recent emails, and filters job/recruiter-related messages for daily review.

## Current Features

- Connects to the Nylas API
- Reads recent Yahoo inbox messages
- Formats email dates into a readable format
- Filters job-related emails using keywords
- Displays sender, subject, date, and snippet

## Planned Features

- Daily job-search email summary
- Priority classification
- AI-generated summary and suggested next action
- Optional draft response support for manual review

## Tech Stack

- Python
- Nylas API
- Yahoo Mail via IMAP
- python-dotenv
- requests

## Security Notes

This project uses a local `.env` file for private credentials. The `.env` file is excluded from GitHub using `.gitignore`.