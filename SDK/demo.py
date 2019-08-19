import boto3

BUCKET_NAME = 'trc-mw-resources'


def clientS3GetOnjects():
    # Use HIGH level API to retrieve obejcts within a bucket
    s3_client = boto3.client('s3')
    bucket = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in bucket['Contents']:
        print(content['Key'], content['LastModified'])
    return


def resourceS3GetObjects():
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)
    return


if __name__ == "__main__":
    print("HIGH Api")
    clientS3GetOnjects()
    print("LOW Api")
    resourceS3GetObjects()
