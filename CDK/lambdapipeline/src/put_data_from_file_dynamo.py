# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into a DynamoDB table.

import csv
import json
import urllib
import os
import logging
import boto3

# Connect to the DynamoDB tables
TABLE_NAME = 'LambdaPipeTable'

# Set loglevel
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)

# Headers within in your csv you want to put exactly the same into DynamoDB
keys=['uuid', 'name', 'date']
# Naming the local file
TMP_DIR = '/tmp'
LOCAL_FILE_NAME = 'codes.csv'
joined_filename=TMP_DIR+'/'+LOCAL_FILE_NAME

def get_bucket_from_event(event: dict) -> str:
    '''Get the bucket from the event'''
    try: 
        bucket_name = event['Records'][0]['s3']['bucket']['name']
    except Exception as e:
        logger.info(e)
        logger.info('Error getting name the specified bucket. Make sure they exist and your bucket is in the same region as this function.')
        raise e
    return bucket_name

def get_key_from_event(event: dict) -> str:
    '''Get the file name from the event'''
    try:
        key_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        logger.info('key arrived in s3: {}'.format(key_name))
    except Exception as e:
        logger.info(e)
        logger.info('Error getting name the specified key')
        raise e
    return key_name

def download_csv_from_s3(bucket_name,key_name,joined_filename):
    '''Download CSV to /tmp in Lambda FS'''
    # Connect to s3
    s3 = boto3.client('s3')
    logger.info('copy file from s3 to ./tmp/codes.csv')
        # Download the file from S3 to the local filesystem
    try:
        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)
        s3.download_file(
            bucket_name, 
            key_name, 
            joined_filename
        )
    except Exception as e:
        logger.info(e)
        logger.info('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key_name, bucket_name))
        raise e
    return joined_filename

def put_item_into_db(keys,joined_filename):
    '''Load data from file into dynamodb'''
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    try: 
        logger.info('copy file content from ./tmp/codes.csv into dynamodb table: {}'.format(TABLE_NAME))
        
        codesTables = dynamodb.Table(TABLE_NAME)
        # Read the Inventory CSV file
        with open(joined_filename) as csvfile:
            # Change delimiter accordingly
            reader = csv.DictReader(csvfile, delimiter=';')
            # Read each row in the file
            rowCount = 0
            for row in reader:
                rowCount += 1
                try:
                    item={}
                    for m, n in zip(keys,row):
                        item[m] = row[n]
                    print(item)
                    codesTables.put_item(Item=item)
                except Exception as e:
                    logger.info(e)
                    logger.info('Unable to insert data into DynamoDB table: {}'.format(e))
                    raise e
    except Exception as e:
        logger.info(e)
        logger.info('Error putting items into dynamodb table: {}'.format(TABLE_NAME))
        raise e
    return logger.info('{} items inserted into dynamodb table: {}'.format(rowCount,TABLE_NAME))
        
# This handler is executed every time the Lambda function is triggered
def load_data_from_csv_to_dynamodb(event,context):
    '''Main function'''
    logger.info('Event recieved: {}'.format(json.dumps(event)))
    # Get neccessary vars
    bucket_name = get_bucket_from_event(event)
    key_name = get_key_from_event(event)
    try:
        download_path = download_csv_from_s3(
            bucket_name, 
            key_name, 
            joined_filename
        )
    except Exception as e:
        logger.info(e)
        logger.info('Error downloading files from s3')
        raise e
    # Put items from file into dynamodb
    try:
        put_item_into_db(
            joined_filename=download_path,
            keys=keys
        )

        response = {
            'message': 'Success putting items into dynamodb table: {}'.format(TABLE_NAME),
            'status': '200'
        }
        logger.info('Event successful processed: {}'.format(json.dumps(response)))
    except Exception as e:
        logger.info(e)
        logger.info('Error putting items into dynamodb {}'.format(TABLE_NAME))
        raise e

    return json.dumps(response)

    
