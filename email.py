import smtplib
import datetime

email_address = input("Enter your email address: ")
email_password = "your pass"

smtp_server = "smtp.gmail.com"
smtp_port = 587

recipient_address = input("Enter the recipient's email address: ")

assignment_name = "Homework 1"
deadline = datetime.datetime(2024, 2, 24)

if datetime.datetime.now() > deadline:
    print(f"{assignment_name} is overdue!")
else:
    days_until_deadline = (deadline - datetime.datetime.now()).days

    if days_until_deadline < 3:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)

            message = f"From: {email_address}\r\nTo: {recipient_address}\r\nSubject: {assignment_name} Assignment Reminder\r\n\r\nThis is a reminder that the {assignment_name} assignment is due in {days_until_deadline} days."

            server.sendmail(email_address, recipient_address, message)

            print(f"Reminder email for {assignment_name} has been sent.")
    else:
        print(f"{assignment_name} is not due for another {days_until_deadline} days.")
