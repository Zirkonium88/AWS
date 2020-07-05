import json
import os
import boto3
import logging


# Set log level
log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)


def create_bucket_policy(
    service_role_arn: str,
    s3_api_calls: list,
    bucket_name: str,
    access_key: str,
    secret_key: str,
    session_token: str,
):
    """Create and put a S3 Bucket Policy if bucket matches a name scheme.

    Args:
        service_role_arn: The IAM Role to allow communication to the specified Bucket
        s3_api_calls: The range of allowed S3 API calls
        bucket_name: The S3 Bucket name
        access_key: A temporary access key provided by Security Token Service (STS)
        secret_key: A temporary secret key key provided by Security Token Service (STS)
        session_token: A temporary session token provided by Security Token Service (STS)

    Returns:
        No returns
    """

    # Create client
    s3_client = boto3.client('s3')

    # Get bucket name from event
    bucket_name = event['detail']['requestParameters']['bucketName']

    # Check criteria
    if "KEY_WORD" in bucket_name:
        
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AddS3Permissions",
                "Action": s3_api_calls,
                "Effect": "Allow",
                "Resource": [
                    "arn:aws:s3:::{}".format(bucket_name),
                    "arn:aws:s3:::{}/*".format(bucket_name),
                ],
                "Principal": {"AWS": ["{}".format(service_role_arn)]},
            }
        ],
    }
    # Convert the policy from JSON dict to string
    bucket_policy = json.dumps(policy)
    try:
        s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
        logger.info("Put successfully bucket policy ...")
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchBucket":
            logger.error("The bucket you specified does not exists ... {}".format(e))
            raise e
        if e.response["Error"]["Code"] == "AccessDenied":
            logger.error("You are not allowed to perform this action ... {}".format(e))
            raise e
        else:
            logger.error("Error while putting Bucket Policy... {}".format(e))
            raise e
