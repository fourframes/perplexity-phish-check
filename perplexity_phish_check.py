import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from dotenv import load_dotenv
import os
from openai import OpenAI

# Loading environment variables
load_dotenv()
IMAP_SERVER=os.getenv('IMAP_SERVER')
IMAP_USERNAME=os.getenv('IMAP_USERNAME')
IMAP_PASSWORD=os.getenv('IMAP_PASSWORD')
SMTP_SERVER=os.getenv('SMTP_SERVER')
SMTP_USERNAME=os.getenv('SMTP_USERNAME')
SMTP_PASSWORD=os.getenv('SMTP_PASSWORD')
SMTP_PORT=os.getenv('SMTP_PORT')
PERPLEX_API_KEY=os.getenv('PERPLEX_API_KEY')
SENDER_NAME=os.getenv('SENDER_NAME')
REPONSE_RECEIVER_MAIL=os.getenv('REPONSE_RECEIVER_MAIL')

# Function to extract the plain text body from an email
def get_email_body(msg: str) -> str:
    """
    Gets the body of an email message.

    Parameters:
    msg (str): The E-Mail Body.

    Returns:
    str: The body of the email message
    """
    if msg.is_multipart():
        # Iterate over each part of the multipart message
        for part in msg.walk():
            # If the part is text/plain, return its payload (the message body)
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode()  # Decode if necessary
        return ''
    else:
        # If it's not multipart, just get the payload directly
        return msg.get_payload(decode=True).decode()


def get_unread_mails() -> list:
    """
    Gets unread mail messages.

    Parameters:
    imap_server (str): IMAP Server to connect to
    username (str): Username for the defined IMAP Server
    password (str): Password for the defined IMAP Server

    Returns:
    list: List of subject and message of each unread email.
    """
    
    # Connect to the server
    conn = imaplib.IMAP4_SSL(IMAP_SERVER)
    conn.login(IMAP_USERNAME, IMAP_PASSWORD)
    conn.select("inbox")
    emails = []
    
    # Search for unread emails
    status, messages = conn.search(None, 'UNSEEN')
    # Get the Subject and the Body Text of each email
    for message in messages[0].split():
        status, data = conn.fetch(message, '(RFC822)')
        email_message = email.message_from_bytes(data[0][1])
        subject = email_message['Subject']
        body = get_email_body(email_message)
        mail_body = (subject, body)
        emails.append(mail_body)
    # close connection
    conn.close()
    conn.logout()
    
    # return the list of unread messages
    return emails


def get_phish_evaluation(subject: str, mail: str) -> str:
    """
    Getting the AI phishing evaluation of an email

    Parameters:
    subject (str): Subject of the mail message
    mail (str): Content (body) of the mail message
    
    Returns: 
    str: AI Phishing evaluation
    """
    # Giving the context and request to the AI
    messages = [
    {
        "role": "system",
        "content": (
                "You are an artificial intelligence cybersecurity assistant and you need to detect phishing in emails. Please note that these e-mails have been forwarded before you receive them. "
        ),
    },
    {
        "role": "user",
        "content": (
                "The following email has been forwarded once and attachments might be removed in the process of forwarding. Do you think the initial first email is phishing? Please do not add any formatting to your response. "
                "The Subject is: " + subject +""
                "The Mail is: " + mail +""
        ),
    },
    ]
    # Connecting the client 
    client = OpenAI(api_key=PERPLEX_API_KEY, base_url="https://api.perplexity.ai")
    
    # Getting the response 
    response = client.chat.completions.create(
    model="llama-3.1-sonar-large-128k-online",
    messages=messages,
    )
    
    # Selecting the actual text from the response 
    completion_content = response.choices[0].message.content
    
    return completion_content

def send_email(subject: str, mail: str) -> None:
    """
    Sends an email message to a server

    Parameters:
    subject (str): Subject of the mail message
    mail (str): Content (body) of the mail message
    """
    # Create the email message
    message = MIMEMultipart()
    message['From'] = SMTP_USERNAME
    message['To'] = REPONSE_RECEIVER_MAIL
    message['Subject'] = subject

    # Email body
    message.attach(MIMEText(mail, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, 587)
        server.starttls()  # Secure the connection with TLS
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, REPONSE_RECEIVER_MAIL, message.as_string())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

def create_mail_response(initial_mail, ai_evaluation) -> str:
    """
    Create a new mail message response out of the initial mail 
    and the AI evaluation of the phishing status

    Parameters:
    initial_mail (str): The initial mail message body
    ai_evaluation (str): The AI evaluation of the given message
    
    Returns:
    str: Mail message response    
    """
    # Starting with the AI Evaluation
    response = "The evaluation of the phishing status is:\n"
    response += ai_evaluation +"\n"
    
    # Adding the initial mail message before ...
    response  += "The initial email was:\n"
    response += initial_mail+"\n"
    
    # ... returning
    return response

# Define the main function
def main():
    """
    Main Routine of the Script
    
    """
    
    # Getting unread mails
    mails = get_unread_mails()

    # Evaluating each message
    for mail in mails:
        # Getting the AI phishing evaluation 
        result = get_phish_evaluation(mail[0], mail[1])

        # Creating the response
        response = create_mail_response(mail[1], result)

        # Sending the response
        send_email('Phishing evaluation for: '+mail[0], response)

# The if __name__ == "__main__" block
if __name__ == "__main__":
    main()
