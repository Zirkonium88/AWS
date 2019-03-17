
# Load libraries
import os
import gzip
import json
import botocore
import shutil
import time
import boto3

# Get first timestamp for determing execution time. "end" is defined as default
start = time.time()
end = time.time()

# Initialise SQS services
sqs = boto3.client('sqs', region_name="eu-central-1")
queue_url = 'https://sqs.eu-central-1.amazonaws.com/XXX/Ec2Unzip'

# Counter variable for processed objects
i = 0

# Get all messages from the queue. Delete a message and the corresponding files after processing.
while True:
    response = sqs.receive_message(QueueUrl=queue_url,
                                   AttributeNames=['SentTimestamp'],
                                   MaxNumberOfMessages=1,
                                   MessageAttributeNames=['All'],
                                   VisibilityTimeout=0,
                                   WaitTimeSeconds=0)


    # If the queue gets empty, the response object decreases in character size
    if len(str(response)) < 300:
        print('')
        print(str(i) + ' Object(s) unzipped and uploaded in ' + str(round(end-start)) + ' s')
        print('')
        break

    else:
        message = response['Messages'][0]
        receipt_handle_msg = message['ReceiptHandle']
        body = message['Body']
        
        # Filter type of messages
        if 'Records' in body:
                body_js = json.loads(body)
                source_bucket = body_js['Records'][0]['s3']['bucket']['name']
                key = body_js['Records'][0]['s3']['object']['key']

                # Split file accordingly
                local_key = key.split('/')[1]
                local_key_unzipped = local_key.split('.gz')[0]

                # Define targets
                target_bucket = 'SAMPLE_BUCKET'
                target_directory = 'SAMPLE_BUCKET/Unzipped/'

                # Initialise s3 service
                s3 = boto3.resource('s3')

                try:
                    # Download files from S3
                    s3.Bucket(source_bucket).download_file(key, local_key)
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == "404":
                        print("The object does not exist.")
                    else:
                        raise

                # Unzip files to local drive
                with gzip.open(local_key, 'rb') as f_in:
                    with open(local_key_unzipped, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                # Upload unzipped files to S3
                s3.meta.client.upload_file(local_key, target_bucket, target_directory + local_key_unzipped)

                # Delete local files and count the number of objects
                os.remove(local_key)
                i = i + 1

                # Delete the queue message
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle_msg)

                # Get second timestamp for determing execution time
                end = time.time()
        else:
            # Delete messages different from 'Message'
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle_msg)