import datetime
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your mail'
SENDER_PASSWORD = 'your pass'
RECIPIENT_EMAIL = input("Enter the recipient's email address: ")

def send_email(subject, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print('Email notification sent successfully!')

        server.quit()
    except Exception as e:
        print('Error sending email notification:', e)

def main():
    while True:
        print("You will be notified daily by 23:19.")
        
        now = datetime.datetime.now()
        if now.hour == 23 and now.minute == 19:
            subject = 'Daily Notification'
            body = 'This is your daily notification. Have a great day!'
            send_email(subject, body)

            time.sleep(60)

        time.sleep(60)

if __name__ == '__main__':
    main()
