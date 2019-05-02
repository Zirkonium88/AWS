# Loading data from a CSV into a DynamoDB table

In this example a [AWS Lambda](https://github.com/Zirkonium88/AWS/blob/master/Lambda/LoadData/handler.py) is trigerd by an S3 event. This Lambda loads data from a CSV into a [DynamoDB](https://aws.amazon.com/dynamodb/?nc1=h_ls) table.

```python

# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into a DynamoDB table.

# Load libs
import json, urllib, boto3, csv

# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
codesTables = dynamodb.Table('SAMPLE_TABLE');

# This handler is executed every time the Lambda function is triggered
def lambda_handler(event, context):

    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))

    # Get the bucket and object key from the Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    localFilename = '/tmp/codes.csv'

    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, localFilename)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # Read the Inventory CSV file
    with open(localFilename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';') # Change delimiter accordingly

        # Read each row in the file
        rowCount = 0
        for row in reader:
            rowCount += 1
            
            # Show the row in the debug log
            print(row['id'], row['code'], row['\data'])
            #print(row)
            try:
                # Insert Store, Item and Count into the Inventory table
                item = {'training': row['\data'],
                        'id': row['id'], 
                        'code': row['code']}

                codesTables.put_item(Item=item)
            

            except Exception as e:
                print(e)
                print("Unable to insert data into DynamoDB table".format(e))

    # Finished!
    return "%d counts inserted" % rowCount



```




