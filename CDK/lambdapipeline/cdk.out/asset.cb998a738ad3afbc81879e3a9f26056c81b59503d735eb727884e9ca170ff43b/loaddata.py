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

# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Set loglevel
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)

# Connect to the DynamoDB tables
codesTables = os.environ.get('TABLE_NAME')

def get_bucket_from_event(event: dict) -> str:
    '''Get the bucket from the event'''
    try: 
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        logger.info('file arrived on bucket = {}'.format(bucket_name))
    except Exception as e:
        print(e)
        logger.info('Error getting name the specified bucket. Make sure they exist and your bucket is in the same region as this function.')
        raise e
    return bucket_name

def get_key_from_event(event: dict) -> str:
    '''Get the file name from the event'''
    try:
        key_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        logger.info('key arrived in s3: {}'.format(key_name))
    except Exception as e:
        print(e)
        logger.info('Error getting name the specified key')
        raise e
    return key_name

def get_file_from_event(event: dict) -> str:
    '''Get the file name from the event'''
    try:
        key_name = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        file_name = key_name.split('/')[-1]
        logger.info('file arrived on s3! key = {} file = {}'.format(key_name,file_name))
    except Exception as e:
        logger.info(e)
        logger.info('Error getting name the specified file name')
        raise e
    return file_name

def put_item_into_db(local_filename: str, bucket_name: str, key_name: str):
    '''Load data from file into dynamodb'''
    try: 
        logger.info('copy file content into dynamodb table: {}'.format(codesTables))
        
        # Download the file from S3 to the local filesystem
        try:
            s3.meta.client.download_file(bucket_name, key_name,local_filename)
        except Exception as e:
            logger.info(e)
            logger.info('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e
        # Read the Inventory CSV file
        with open(local_filename) as csvfile:
            # Change delimiter accordingly
            reader = csv.DictReader(csvfile, delimiter=';')

            # Read each row in the file
            rowCount = 0
            for row in reader:
                rowCount += 1

                # Show the row in the debug log
                print(row['id'], row['code'], row['\data'])
                # print(row)
                try:
                    # Insert Store, Item and Count into the Inventory table
                    item = {'uuid': row['uuid'],
                            'name': row['name'],
                            'code': row['date']}

                    codesTables.put_item(Item=item)
                except Exception as e:
                    logger.info(e)
                    logger.info('Unable to insert data into DynamoDB table'.format(e))
                    raise e
    except Exception as e:
        logger.info(e)
        logger.info('Error putting items into dynamodb table: {}'.format(codesTables))
        raise e
    return logger.info('{} items inserted into dynamodb table: {}'.format(rowCount,codesTables))
        

# This handler is executed every time the Lambda function is triggered
def LoadData(event, context):
    '''Function entry'''
    logger.info('Event recieved: {}'.format(json.dumps(event)))

    # Get neccessary vars
    bucket = get_bucket_from_event(event)
    key = get_key_from_event(event)
    localFilename = '/tmp/codes.csv'

    # Put items frim file into dynamodb
    try:
        put_item_into_db(
            local_filename=localFilename,
            bucket_name=bucket,
            key_name=key
        )
    except Exception as e:
        logger.info(e)
        logger.info('Error putting items into dynamodb {}'.format(codesTables))
        raise e
    logger.info('Success putting items into dynamodb {}'.format(codesTables))

    
