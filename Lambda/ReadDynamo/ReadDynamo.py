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
