import boto3

BUCKET = 'trc-mw-resources'


def clientGetObjects():
    # Use HIGH level API call
    s3client = boto3.client('s3')
    bucket = s3client.list_objects_v2(Bucket=BUCKET)
    for content in bucket['Contents']:
        print(content['Key'], content['LastModified'])
    return


def resourceGetObjects():
    #  Use LOW level API call
    s3resource = boto3.resource('s3')
    bucket = s3resource.Bucket(BUCKET)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)
    return


if __name__ == "__main__":
    print("Get content over HIGH level API calls")
    clientGetObjects()
    print("Get content over LOW level API calls")
    resourceGetObjects()
