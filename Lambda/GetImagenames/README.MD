# Lambda pipeline with S3 and DynamoDB

This examples shows how AWS Lambda can be integrated with [Amazon S3](https://aws.amazon.com/s3/?nc1=h_ls) and [Amazon DynamoDB](https://aws.amazon.com/dynamodb/?nc1=h_ls). The Lambda extracts the bucket and image name of every upload and writes them to the DynamoDB table. A [sample event](https://github.com/Zirkonium88/AWS/blob/master/Lambda/GetImagenames/event.json) is given.

## Prerequisites

1. Create a S3 bucket.
2. Create a DynamoDB table.
3. Deploy the [GetImageNames Lambda](https://github.com/Zirkonium88/AWS/blob/master/Lambda/GetImagenames/handler.py) below via [Serverless](https://github.com/Zirkonium88/AWS/blob/master/Lambda/ServerlessDemo/README.MD) or AWS console.

```python
import boto3
import urllib
import json


# Set environment variables to avoid hard coded objects
# table_name = os.environ['TABLE_NAME']
table_name = "myLambdaFunctionTable"


# Set up DynamoDB service
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(table_name)

# Main Handler
def lambda_handler(event, context):
    
    # Get the Bucket name as object. Remember JSON-Objects from event are singular. Normally, 
    # you need to iterate over them.
    bucket = event['Records'][0]['s3']['bucket']['name']

    # Get the name of the uploaded file
    key = event['Records'][0]['s3']['object']['key']

    # Write the item object to DynamoDB
    # Partion key = object name
    # Value = Bucket name
    item = {'key': key, 'bucket': bucket}
    table.put_item(Item=item)
	
	# Leave it or not: Say "Hello" from Lambda with status code 200
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
```
4. Create an `All Object create` event within S3 pointing at your [GetImageNames Lambda](https://github.com/Zirkonium88/AWS/blob/master/Lambda/GetImagenames/handler.py).