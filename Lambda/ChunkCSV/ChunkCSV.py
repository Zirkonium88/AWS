# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file will be downloaded and seprated to n files.
# Those n files will written to S3 again

import csv
import urllib
import os
import json
import shutil

import boto3

# Connect to S3
s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# This handler is executed every time the Lambda function is triggered
def lambda_handler(event, context):
    
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))

    # Check ENV_VAR
    if int(os.environ['NumberOfLines']) <= 0:
        raise Exception('NumberOfLines must be > 0')

    # Get the bucket and object key from the Event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    localFilename = '/tmp/codes.csv'

    # Download the file from S3 to the local filesystem
    try:
        s3_resource.meta.client.download_file(bucket, key, localFilename)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e

    # Some global vars    
    file_idx = 0
    outfile = None

    try:
        # Open the local file
        with open(localFilename, 'r') as infile:

            # Keep the header for each file
            header = next(infile)

            # Iterate over all lines
            for index, row in enumerate(infile):

                # Make the chunk
                if index % int(os.environ['NumberOfLines']) == 0:
                    if outfile is not None:

                        # Write the chunk as file
                        outfile.close()
                        
                        # Upload the current file to s3
                        s3_resource.meta.client.upload_file(
                            outfilename, 
                            bucket,
                            os.environ['Key']+outfilename.split('/tmp/')[1] 
                        )
                    
                    # Lambda is a read-only file system
                    # /tmp/ acts a write file system
                    outfilename = '/tmp/'+'smaller-{}.csv'.format(file_idx)
                    outfile = open(outfilename, 'w')

                    # Counter var
                    file_idx += 1

                    # Write the chunks header
                    outfile.write(header)

                # Write the chunks rows
                outfile.write(row)
    finally:
        # Write the last chunk as file
        if outfile is not None:
            outfile.close()

            # Upload last file to s3
            s3_resource.meta.client.upload_file(
                            outfilename, 
                            os.environ['Bucket'],
                            os.environ['Key']+outfilename.split('/tmp/')[1]
                        )

    # Logging porpuse
    # Avoid starting with zero and making possible to start with 1
    print("Seperated %s " % key, "into  %d files!" % file_idx)
    return "Seperated %s " % key + "into  %d files!" % file_idx
