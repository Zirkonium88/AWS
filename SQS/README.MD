# SQS demo: Unzip large files from S3 with EC2 and Python

In some UseCases your are not able to use AWS Lambda to react on S3 events. Maybe you need to unzip large gzip-files (unzipped file size > 512 mb). In this situation Lambda is not appropriate due to [service limitations](https://docs.aws.amazon.com/lambda/latest/dg/limits.html). 

1. Create an **Amazon Linux 2** instance combined with a **IAM role** allowing to read and write files from and to **S3** as well as **SQS**. 

2. Prepare your instance.
    ```bash
    sudo yum install python37
    curl -O https://bootstrap.pypa.io/get-pip.py
    sudo su
    python get-pip.py
    pip install boto3
    ```

3. Copy the [EC2Unzip.py](AWS/SQS/EC2Unzip.py) file to your instance.

    ```python
    # Load libraries
    import os
    import gzip
    import json
    import botocore
    import shutil
    import time
    import boto3

    # Get first timestamp for determing execution time. Give `end` a default value, if SQS message queue is empty.
    start = time.time()
    end = time.time()

    # Initialise the SQS service
    sqs = boto3.client('sqs', region_name="eu-central-1")
    queue_url = 'https://sqs.eu-central-1.amazonaws.com/XXX/Ec2Unzip' # XXX = Your account-id

    # Counter variable for processed objects
    i = 0

    # Get all messages from the queue. Delete a message and the corresponding files after processing.
    while True:
        response = sqs.receive_message(QueueUrl=queue_url,
                                    AttributeNames=['SentTimestamp'],
                                    MaxNumberOfMessages=1,
                                    MessageAttributeNames=['All'],
                                    VisibilityTimeout=0, # Change accordingly for VisibilityTimeOut and LongPolling features of SQS
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

                    # Get a second timestamp for determing execution time
                    end = time.time()
            else:
                # Delete messages different from 'Message'
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle_msg)
    ```

4. Creat an **S3-Event** for your `SAMPLE_BUCKET` (**PUT** or **All Obejct create**).

5. Upload a sample file to **S3**.

6. On your EC2 instance run: 
    ```bash
    python EC2unzip.py
    ``` 

    You will see something like this: 

    ```bash
    1 Object(s) unzipped and uploaded in 5 s
    ```

7. Going further: 
    - Create an **AMI** of your instance. Now, you can use the length of your **SQS** message queue as [AutoScaling trigger](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-using-sqs-queue.html).
    - Load the current version of your Python file from **S3** via **UserData**. Everytime an **EC2 instance** is starting, the **AWS CLI** copies the Python script from **S3**
    
    ``` bash
    aws s3 cp s3://SAMPLE_BUCKET/EC2Unzip.py EC2Unzip.py
    ```