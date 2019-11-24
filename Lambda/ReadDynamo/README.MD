# Loading data from as CSV from thea DynamoDB table

In this example a [AWS Lambda](https://github.com/Zirkonium88/AWS/blob/master/Lambda/ReadDynamo/ReadDynamo.py) can be triggered by any event. This Lambda dumbs data from a DynamoDB table into CSV on S3.

```python

import boto3
from botocore.exceptions import ClientError
from pandas import DataFrame

from dynamodb_json import json_util as json

BUCKET_PATH = "s3://example-bucket/example.csv"
object_name = "example.csv"
bucket_name = "example-bucket"

TABLE_NAME = "SAMPLE_TABLE"


def lambda_handler(event, context):

    # Generate DynamoDB Object to read table
    dynamo_client = boto3.client('dynamodb')
    data = dynamo_client.scan(TableName=TABLE_NAME)

    # Save object as pandas dataFrame
    obj = DataFrame(json.loads(data['Items']))

    # Upload object to s3 as csv
    obj.to_csv(BUCKET_PATH, index=False)

    # Return response

    payload = {
        'Status': '200',
        'Bucket': bucket_name,
        'Key': object_name
    }

    print(payload)
    return payload


```
