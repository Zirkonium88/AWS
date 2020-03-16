import unittest 
import os 
import json
import boto3 
import botocore

from unittest.mock import patch, ANY

import src.put_data_from_file_dynamo as h

# Test vars
BUCKET_NAME = "431892011317-pipe"
KEY_NAME = "data/codes.csv"
TABLE_NAME = 'LambdaPipeTable'
TMP_DIR = './tmp'
TMP_DIR_LAMBDA_FS = '/tmp'
LOCAL_FILE_NAME = 'codes.csv'
joined_filename=TMP_DIR+'/'+LOCAL_FILE_NAME
joined_filename_lambda_fs=TMP_DIR_LAMBDA_FS+'/'+LOCAL_FILE_NAME

# Connect to S3 and DynamoDB
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


# Headers within in your csv you want to put exactly the same into DynamoDB
keys_list=['uuid', 'name', 'date']

# Test event
with open('./event/event.json', 'r') as f:
    EVENT_FILE = json.load(f)

with open('./event/event.json', 'r') as f:
    CONTEXT_FILE = json.load(f)

class Test_PutDataFromFileDynamo(unittest.TestCase):
    
    # Get Bucket Name
    def test_get_bucket_from_event(self,event=EVENT_FILE):
        '''Test: Fetching bucket from test event.'''
        self.assertEqual(h.get_bucket_from_event(event),BUCKET_NAME)
    
    # Get Key Name
    def test_get_key_from_event(self,event=EVENT_FILE):
        '''Test: Fetching keye from test event.'''
        self.assertEqual(h.get_key_from_event(event),KEY_NAME)
    
    # Download CSV
    def test_download_csv_from_s3(self,event=EVENT_FILE):
        '''Test: Download CSV to /tmp in Lambda FS.'''
        
        bucket_name = h.get_bucket_from_event(event)
        key_name = h.get_key_from_event(event)

        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)
        
        with patch("src.put_data_from_file_dynamo.boto3.client") as boto_mock:
            h.download_csv_from_s3(
                bucket_name, 
                key_name, 
                joined_filename
            )
            # call boto3.client("s3")
            boto_mock.assert_called_once_with("s3")
            # call s3.download_file(key_name,local_filename)
            boto_mock.return_value.download_file.assert_called_once_with(
                bucket_name, 
                key_name, 
                joined_filename
            )
    
    # Put items to dynamodb
    def test_put_item_into_db(self,event=EVENT_FILE):
        '''Test: Load data from file into dynamodb'''
        keys=keys_list
        bucket_name = h.get_bucket_from_event(event)
        key_name = h.get_key_from_event(event)
        with patch("src.put_data_from_file_dynamo.boto3.resource") as boto_mock:
            h.put_item_into_db(
                keys,
                joined_filename
            )
            # call boto3.resource("dynamodb")
            boto_mock.assert_called_once_with("dynamodb")
            # call dynamodb.Table(TABLE_NAME)
            boto_mock.return_value.Table.assert_called_once_with(TABLE_NAME)
            # call Table.put_item(key_name,joined_filename)
            boto_mock.return_value.Table.return_value.put_item.assert_called()
    
    def test_load_data_from_csv_to_dynamodb(self,event=EVENT_FILE):
        '''Test: Main function'''
        with patch("src.put_data_from_file_dynamo.download_csv_from_s3") as download_mock, \
            patch("src.put_data_from_file_dynamo.put_item_into_db") as put_mock:
            
            response = json.loads(h.load_data_from_csv_to_dynamodb(event=EVENT_FILE, context=CONTEXT_FILE))

            bucket_name = h.get_bucket_from_event(event)
            key_name = h.get_key_from_event(event)

            download_mock.assert_called_once_with(
                bucket_name, 
                key_name, 
                joined_filename_lambda_fs
            )

            response = json.loads(h.load_data_from_csv_to_dynamodb(event=EVENT_FILE, context=CONTEXT_FILE))
            put_mock.assert_called()

            assert isinstance(response, dict)
            assert response['status'] == '200'

if __name__ == "__main__":
    unittest.main()