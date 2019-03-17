# Load libraries
import boto3
import urllib
import json

# Set environment variables to avoid hard coded objects
# table_name = os.environ['TABLE_NAME']
table_name = "myLambdaFunctionTable"


# Set UP DynamoDB handler
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

    # Leave it or not: Say Hello from Lambda with status code 200
    return {
        'statusCode': 200,
        'Bucket': json.dumps(bucket),
        'Key': json.dumps(key)
    }
