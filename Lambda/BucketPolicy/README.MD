# Use S3 events and Lambda to change BucketPolicies

This [Lambda](https://github.com/Zirkonium88/AWS/tree/master/Lambda/Bucketpolicy/handler.py) evaluates a Bucketname. If the name matches a key word, a Bucketpolicy is changed. In this case, the Bucketpolicy sets a Deny `DeleteBucket` and `DeleteObject`.  

```python
import json

import boto3


def lambda_handler(event, context):

    # Create client
    s3_client = boto3.client('s3')

    # Get bucket name from event
    bucket_name = event['detail']['requestParameters']['bucketName']

    # Check criteria
    if "KEY_WORD" in bucket_name:

        # Create a bucket policy

        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'SaveBucketContent',
                'Effect': 'Deny',
                'Principal': {'AWS': "*"},
                'Action': ['s3:DeleteBucket', 's3:DeleteObject'],
                'Resource': ["arn:aws:s3:::%s" % bucket_name, "arn:aws:s3:::%s/*" % bucket_name]
            }]
        }

        # Convert the policy to a JSON string
        bucket_policy = json.dumps(bucket_policy)

        # Set the new policy on the given bucket
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)

        # For logging purpose
        response = {
            "statusCode": 200,
            "Bucket": json.dumps(bucket_name),
            "Comment": json.dumps("Changed bucket policy accordingly"),
        }

        print(response)
        return response

    else:

        # For logging purpose
        response = {
            "statusCode": 400,
            "Bucket": json.dumps(bucket_name),
            "Comment": json.dumps("Nothing changed because bucket did not matched criteria"),
        }

        print(response)
        return response

```