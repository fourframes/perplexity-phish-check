# Perplexity Phish Check

**Perplexity Phish Check** is a Python-based tool that performs AI-driven phishing evaluations on emails using the **Perplexity API**. This tool connects to an IMAP server, retrieves unread emails, sends them to Perplexity AI for phishing analysis, and forwards the results to a predefined email address.

## How It Works

1. **Connects to an IMAP server**: The tool retrieves unread emails from a specified mailbox.
2. **Phishing evaluation**: It sends the email content to Perplexity AI, asking whether the message is a phishing attempt.
3. **Receives the response**: The analysis result from Perplexity AI is received.
4. **Forwards the result**: The phishing evaluation result is sent to a predefined email address.

## Setup Instructions

### 1. Set Up a Dedicated Email Address

You will need to set up a dedicated email address where you will forward emails that need phishing evaluation. The script can be configured to regularly check this mailbox for new messages and analyze them.

### 2. Install Dependencies

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

This will install all necessary Python packages listed in requirements.txt.

### 3. Configure Environment Variables

Copy the provided `sample.env` file, update the variables according to your setup, and rename it to `.env`. This file contains all the necessary configuration for connecting to your IMAP/SMTP servers and accessing the Perplexity API.

#### Environment Variables

| Variable               | Description                                                      |
|------------------------|------------------------------------------------------------------|
| `IMAP_SERVER`          | The address of your IMAP server (e.g., `imap.gmail.com`).         |
| `IMAP_USERNAME`        | Your email address or username for logging into the IMAP server. |
| `IMAP_PASSWORD`        | The password or app-specific password for logging into your IMAP account. |
| `SMTP_SERVER`          | The address of your SMTP server (e.g., `smtp.gmail.com`).         |
| `SMTP_USERNAME`        | Your email address or username for logging into the SMTP server. |
| `SMTP_PASSWORD`        | The password or app-specific password for logging into your SMTP account. |
| `SMTP_PORT`            | The port of your SMTP server (e.g., 587 for TLS).                |
| `PERPLEX_API_KEY`      | Your Perplexity API key for accessing their phishing detection service. |
| `SENDER_NAME`          | The email address used as the sender when sending phishing analysis results. |
| `RESPONSE_RECEIVER_MAIL` | The recipient email address where phishing evaluation results are sent. |

### 4. Schedule Regular Execution

To automate phishing checks, you can schedule the script to run at regular intervals using tools like cron jobs (Linux/macOS) or Task Scheduler (Windows). This ensures that new emails are regularly retrieved and evaluated.
Example Cron Job (Linux/macOS)

### Important Notes

- Email Retention: The script does not delete or move emails from the dedicated mailbox after processing them. You may need to manually manage or archive these emails based on your needs.
- Security: Ensure that sensitive information such as passwords and API keys are stored securely in your .env file and never hardcoded in the source code.

## Feature Ideas

- **Direct Response to Sender:** Instead of sending phishing evaluation results to a predefined email address, implement functionality to respond directly to the original sender of the email.
- **Whitelist Management:** Add support for maintaining a whitelist of email addresses or domains that are authorized to request phishing checks, ensuring only trusted sources can trigger evaluations.
- **Local email files:** Add support to analyze a local email file instead of polling emails from a server. 
