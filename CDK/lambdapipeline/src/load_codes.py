# Load-Inventory Lambda function
#
# This function is triggered by an object being created in an Amazon S3 bucket.
# The file is downloaded and each line is inserted into a DynamoDB table.

import csv
import json
import urllib
import boto3
import os

# Connect to S3 and DynamoDB
s3 = boto3.resource("s3")
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get("TABLE_NAME")

# Connect to the DynamoDB tables
codesTables = dynamodb.Table(TABLE_NAME)

# This handler is executed every time the Lambda function is triggered


def load_codes(event, context):

    # Show the incoming event in the debug log
    print("Event received by Lambda function ... ")

    # Get the bucket and object key from the Event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])
    localFilename = "/tmp/codes.csv"

    # Download the file from S3 to the local filesystem
    try:
        s3.meta.client.download_file(bucket, key, localFilename)
    except Exception as e:
        print(e)
        print(
            "Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.".format(
                key, bucket
            )
        )
        raise e

    # Read the Inventory CSV file
    with open(localFilename) as csvfile:
        # Change delimiter accordingly
        reader = csv.DictReader(csvfile, delimiter=";")

        # Read each row in the file
        rowCount = 0
        for row in reader:
            rowCount += 1

            # Show the row in the debug log
            print(row)
            try:
                # Insert Store, Item and Count into the Inventory table
                item = {
                    "training": row["\ufefftraining"],
                    "id": row["name"],
                    "code": row["code"],
                }

                codesTables.put_item(Item=item)

            except Exception as e:
                print("Unable to insert data into DynamoDB table ... {}".format(e))

    # Finished!
    return "%d counts inserted" % rowCount
