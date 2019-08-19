import boto3

BUCKET_NAME = 'trc-mw-resources'


def clientS3GetOnjects():
    # User HIGH level API to retrieve obejcts within a bucket
    s3_client = boto3.client('s3')
    bucket = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in bucket['Contents']:
        print(content['Key'], content['LastModified'])
    return


def resourceS3GetObjects():
    # User LOW level API to retrieve obejcts within a bucket
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)
    return


if __name__ == "__main__":
    print("Used high level API")
    clientS3GetOnjects()
    print("Used low level APi")
    resourceS3GetObjects()
