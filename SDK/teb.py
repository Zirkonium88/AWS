import boto3

BUCKET_NAME = 'trc-mw-resources'


def clientS3GetObjects():
    # High level level API
    s3_client = boto3.client('s3')
    bucket = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in bucket['Contents']:
        print(content['Key'], content['LastModified'])
    return


if __name__ == "__main__":
    clientS3GetObjects()
