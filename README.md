# AWS Glue Job Failure Notification to Slack

This AWS Lambda function is designed to send notifications to a Slack channel whenever an AWS Glue job fails. The function retrieves logs related to the Glue job from AWS CloudWatch Logs and formats them into a message for Slack.

## Prerequisites

Before you begin, ensure you have the following:

- AWS account with IAM permissions to create and manage Lambda functions, CloudWatch Logs, and Glue jobs.
- A Slack workspace with a channel where you want to send the notifications.
- A Slack webhook URL for the channel.

## Setup

### Step 1: Create a Slack Webhook URL

1. Go to your Slack workspace.
2. Navigate to the channel where you want to receive notifications.
3. Click on the channel name to open the channel settings.
4. Select "Integrations" and then "Add an app".
5. Search for "Incoming Webhooks" and add it to your workspace.
6. Follow the instructions to create a new webhook and copy the webhook URL.

### Step 2: Create the Lambda Function

1. Open the AWS Management Console.
2. Navigate to the Lambda service.
3. Click on "Create function".
4. Choose "Author from scratch".
5. Enter a function name (e.g., `GlueJobFailureNotification`).
6. Select a runtime (e.g., `Python 3.8`).
7. Choose or create an execution role with the necessary permissions:
   - Access to CloudWatch Logs (`logs:DescribeLogGroups`, `logs:DescribeLogStreams`, `logs:GetLogEvents`).
   - Access to send HTTP requests to Slack (`AWSLambdaBasicExecutionRole`).

### Step 3: Add Environment Variables

1. In the Lambda function configuration, go to the "Configuration" tab.
2. Select "Environment variables".
3. Add a new environment variable:
   - Key: `SLACK_WEBHOOK_URL`
   - Value: (paste your Slack webhook URL here)

### Step 4: Deploy the Lambda Function

1. Copy the following code from `lambda-notifications.py` into the Lambda function editor.

2. Click "Deploy" to save and deploy the function.

### Step 5: Configure AWS Glue to Trigger the Lambda Function

1. Navigate to the AWS Glue service in the AWS Management Console.
2. Create or edit an existing Glue job.
3. In the job configuration, go to the "Advanced properties" section.
4. Add a "Job bookmark" to enable retries.
5. In the "Script" section, add the following code to trigger the Lambda function on failure:

    ```python
    import boto3

    client = boto3.client('lambda')

    def send_failure_notification(job_name, log_stream_name, state):
        response = client.invoke(
            FunctionName='GlueJobFailureNotification',
            InvocationType='Event',
            Payload=json.dumps({
                'jobName': job_name,
                'logStreamName': log_stream_name,
                'state': state
            })
        )
    
    job_name = "your-glue-job-name"
    log_stream_name = "your-log-stream-name"
    state = "FAILED"
    
    if state == "FAILED":
        send_failure_notification(job_name, log_stream_name, state)
    ```

6. Save the job configuration.

### Step 6: Test the Setup

1. Run the Glue job and simulate a failure to test if the Lambda function gets triggered.
2. Check the Slack channel for the notification.

## Conclusion

You have successfully set up an AWS Lambda function to send notifications to Slack on AWS Glue job failures. This setup ensures you are promptly alerted whenever a Glue job fails, allowing you to take timely action.

## Troubleshooting

- Ensure the Lambda function has the necessary permissions to access CloudWatch Logs and send HTTP requests.
- Verify the Slack webhook URL is correctly set in the environment variables.
- Check the CloudWatch Logs for the Lambda function for any errors during execution.
