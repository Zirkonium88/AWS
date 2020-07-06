import boto3

BUCKET_NAME = "www-stack-websitebucket75c24d94-fvr9vrhsz9wb"


def clientS3GetOnjects():
    """Use HIGH level API to retrieve obejcts within a bucket"""
    s3_client = boto3.client("s3")
    bucket = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    for content in bucket["Contents"]:
        print(content["Key"], content["LastModified"])
    return


def resourceS3GetObjects():
    """Use LOW level API to retrieve obejcts within a bucket"""
    s3_resource = boto3.resource("s3")
    bucket = s3_resource.Bucket(BUCKET_NAME)
    for object in bucket.objects.all():
        print(object.key, object.last_modified)
    return


def create_presigned_url(bucket, object_key, expiration_time):
    """Generate a presigned URL to share a S3 object.

    Args:
        bucket: The destination S3 bucket.
        object_key: The object key within S3.
        expiration_time: The expiration time for the URL in seconds.

    Returns:
        presigned_url: The presigned URL.
    """
    s3_client = boto3.client("s3")
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_key},
            ExpiresIn=expiration_time,
        )
    except Exception as e:
        raise e
    return presigned_url


if __name__ == "__main__":
    # print("Used high level API")
    # clientS3GetOnjects()
    # print("Used low level APi")
    # resourceS3GetObjects()
    print("Create a presigned URL for object")
    url = create_presigned_url(
        bucket=BUCKET_NAME, object_key="index.html", expiration_time=3600
    )
    print(url)
