# MailSutra - Bulk Email Delivery System

MailSutra is a scalable and automated bulk email delivery system designed to send personalized daily email reminders using AWS services and SMTP. This project leverages AWS Lambda, Amazon S3, and SES SMTP to create a secure, reliable, and efficient communication tool for various applications, such as healthcare reminders, corporate campaigns, and educational updates.

---

## Features

- **Bulk Email Delivery:** Send emails to multiple recipients in a single operation.
- **AWS Integration:** Uses AWS S3 for recipient data storage and AWS Lambda for serverless execution.
- **Personalized Content:** Includes simple personalization with dynamic data.
- **Secure SMTP Configuration:** Employs TLS encryption for secure email transmission.
- **Scalable Design:** Handles thousands of recipients with minimal latency.
- **Error Handling:** Logs and handles errors to ensure reliability.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- **AWS Account:** To configure S3 and deploy the Lambda function.
- **SMTP Credentials:** For Amazon SES or any SMTP provider.
- **Python 3.x Environment:** For local testing and Lambda deployment.
- **AWS CLI Installed:** For managing AWS resources programmatically.

---

## Installation and Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/<username>/mailsutra.git
   cd mailsutra
## Installation and Setup

1. **Configure AWS S3 Bucket**  
   - Log in to your AWS Management Console.
   - Create an S3 bucket (e.g., `awsemailbucket123`) to store recipient data.
   - Upload a CSV file named `emails_data.csv` to the bucket. The file should have the following structure:
     ```csv
     Name,Email
     John Doe,john.doe@example.com
     Jane Smith,jane.smith@example.com
     ```
   - Ensure that the bucket has the necessary permissions to allow your Lambda function to access the file.

2. **Update Configuration**  
   - Open the `lambda_function.py` file in your editor.
   - Update the following variables with your details:
     ```python
     SMTP_USER = '<your-smtp-username>'
     SMTP_PASSWORD = '<your-smtp-password>'
     S3_BUCKET_NAME = 'awsemailbucket123'  # Replace with your bucket name
     S3_OBJECT_KEY = 'emails_data.csv'     # Ensure it matches the uploaded file name
     ```

3. **Deploy the Lambda Function**  
   - Zip the function code:
     ```bash
     zip function.zip lambda_function.py
     ```
   - Deploy the Lambda function using AWS CLI:
     ```bash
     aws lambda create-function \
       --function-name MailSutra \
       --runtime python3.x \
       --role <role-arn> \
       --handler lambda_function.lambda_handler \
       --timeout 30 \
       --zip-file fileb://function.zip
     ```
   - Replace `<role-arn>` with the ARN of the IAM role that has permissions to access S3 and SES.

4. **Set Up EventBridge for Scheduling (Optional)**  
   - Use AWS EventBridge to schedule the Lambda function for periodic execution:
     - Navigate to the EventBridge service in the AWS Console.
     - Create a new rule with a fixed schedule (e.g., daily at a specific time).
     - Attach the Lambda function to the rule.

5. **Test the Function**  
   - Trigger the function manually from the AWS Lambda Console:
     - Select your function from the list.
     - Click on the "Test" button and provide a test event (e.g., `{ "send_emails": true }`).
   - Verify that emails are sent to the recipients listed in the S3 CSV file.

---

## Usage

### Recipient Data

Ensure your recipient CSV file uploaded to the S3 bucket follows this structure:

```csv
Name,Email
John Doe,john.doe@example.com
Jane Smith,jane.smith@example.com
 ```

### Triggering the Function

You can trigger the Lambda function in the following ways:

1. **Manually via AWS Lambda Console:**  
   - Log in to the AWS Management Console and navigate to the Lambda service.
   - Select the `MailSutra` Lambda function from your list of functions.
   - Click the **Test** button at the top of the console.
   - Create a new test event with the following JSON payload:
     ```json
     {
       "send_emails": true
     }
     ```
   - Click **Save and Test** to execute the function. Verify the output and check the recipient's inbox to confirm email delivery.

2. **Using AWS CLI:**  
   - Execute the Lambda function using the AWS CLI with a test event:
     ```bash
     aws lambda invoke \
       --function-name MailSutra \
       --payload '{"send_emails": true}' \
       output.json
     ```
   - The results of the function will be saved in `output.json`. Check this file to verify the status of the execution.

3. **Automatically via AWS EventBridge (Recommended for Scheduling):**  
   - Navigate to the EventBridge service in the AWS Management Console.
   - Create a new rule for scheduling:
     - Choose **Schedule** and set a fixed rate or cron expression (e.g., `rate(1 day)` for daily execution).
   - Under the **Target** section, select the `MailSutra` Lambda function.
   - Save the rule to enable automatic daily email reminders.

---

## Example Email Output

Here’s an example of the email sent by MailSutra:

**Subject:** Daily Reminder  
**Body:**  
Hello, this is your daily reminder for the day! Here is some random info: 1234

Thank you for staying on track with your goals. If you have any questions or need assistance, feel free to reach out.

The email body is dynamically generated with a unique identifier (`1234` in this case) to add personalization. You can customize the subject line and body content to fit the specific use case, such as medical reminders, appointment notifications, or event updates.

---

## Troubleshooting

If the function fails to send emails or behaves unexpectedly, follow these steps to resolve common issues:

1. **Check AWS S3 Configuration:**  
   - Ensure the correct S3 bucket name and object key are provided in the Lambda function code.
   - Verify that the CSV file is properly formatted with valid email addresses.

2. **Validate SMTP Credentials:**  
   - Confirm that the `SMTP_USER` and `SMTP_PASSWORD` variables in the Lambda function are accurate.
   - Ensure that the SMTP server details (e.g., port and domain) match your provider’s configuration.

3. **Inspect Lambda Execution Logs:**  
   - Navigate to the AWS CloudWatch Logs service in the AWS Management Console.
   - Locate the logs for the `MailSutra` Lambda function and review recent entries for errors or warnings.

4. **Test Email Delivery:**  
   - Send a test email to your own address to confirm the function is correctly configured.
   - Check your spam/junk folder if the email does not appear in your inbox.

5. **Debug Rate Limits:**  
   - If you’re using Amazon SES, ensure you’re not exceeding your sending limits. You can request a limit increase from the AWS SES console if needed.

If issues persist, consult the AWS documentation for the services involved (e.g., Lambda, SES, S3) or create a GitHub issue for further support.

---

## Contributing

We welcome contributions to enhance the functionality of MailSutra. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push your branch (`git push origin feature-name`).
5. Open a pull request on GitHub.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

Special thanks to the AWS community and the contributors of Python libraries used in this project. Your support and resources make projects like MailSutra possible.

