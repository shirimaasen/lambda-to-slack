import json
import boto3
import os
import requests

logs_client = boto3.client('logs')

def lambda_handler(event, context):
    job_name = event['jobName']
    log_stream_name = event['logStreamName']
    state = event['state']
    
    log_group_name = '/aws-glue/jobs/logs/' + job_name
    
    response = logs_client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startFromHead=True
    )
    
    log_events = response['events']
    log_messages = [event['message'] for event in log_events]
    
    formatted_message = {
        "jobName": job_name,
        "state": state,
        "logMessages": log_messages
    }
    
    # Send logs to Slack
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
    slack_message = {
        "text": f"Glue Job {job_name} has failed.\nState: {state}\nLogs:\n{json.dumps(log_messages, indent=2)}"
    }
    requests.post(slack_webhook_url, data=json.dumps(slack_message))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully')
    }
