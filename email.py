////LAMDA FUNCTION FOR EMAIL USING SMTP

import smtplib
import random
import json
import os
import time
import boto3
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import StringIO

# Corrected SMTP configuration
SMTP_SERVER = 'email-smtp.eu-north-1.amazonaws.com'
SMTP_PORT = 587
SMTP_USER = 'your user name'
SMTP_PASSWORD = 'pass'

# AWS S3 Configuration
S3_BUCKET_NAME = 'bucket name'
S3_OBJECT_KEY = 'emails_data.csv'

def get_recipients_from_s3_csv(bucket_name, object_key): #fetches data from your s3 bucket
    """
    Retrieves the list of email recipients from an S3 CSV object.
    Assumes the CSV file contains two columns: Name and Email.
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        data = response['Body'].read().decode('utf-8')
        
        recipients = []
        csv_reader = csv.reader(StringIO(data))
        next(csv_reader, None)  # Skip header row if present
        
        for row in csv_reader:
            if len(row) >= 2:
                recipients.append(row[1].strip())  # Only collect email addresses
        
        return recipients
    except Exception as e:
        print(f"Error fetching recipient list from S3 CSV: {e}")
        return []

def send_bulk_email(subject, body, recipient_email):
    """
    Sends an email to a single recipient using SMTP.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = 'mailsutra@xyz.com' #example
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(msg['From'], recipient_email, msg.as_string())
        
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email to {recipient_email}: {e}")

def lambda_handler(event, context):
    """
    AWS Lambda function handler for sending daily reminder emails.
    """
    subject = 'Daily Reminder'
    base_body = 'Hello, this is your daily reminder for the day! Here is some random info: {}'

    recipient_list = get_recipients_from_s3_csv(S3_BUCKET_NAME, S3_OBJECT_KEY)
    if not recipient_list:
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to retrieve recipient list from S3.')
        }

    if not event.get('send_emails', False):
        return {
            'statusCode': 400,
            'body': json.dumps("Event does not contain required parameters.")
        }

    try:
        for recipient_email in recipient_list:
            random_data = random.randint(1000, 9999)  # Example of simple personalization
            personalized_body = base_body.format(random_data)
            send_bulk_email(subject, personalized_body, recipient_email)
            time.sleep(1)  # Optional rate-limiting delay

        return {
            'statusCode': 200,
            'body': json.dumps('Daily reminder emails sent successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {str(e)}")
        }

# Uncomment this to test locally
# if __name__ == "__main__":
#     lambda_handler(None, None)
