import json
import os
import boto3
import logging

# Get current iamgroup-name
GROUP_NAME = os.environ['iamgroup']

# Set log level
log_level = os.environ.get("LOG_LEVEL", "INFO")
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)


def create_iam_user(event, context):
    """Create a User within IAM if User not equal to FunctionalUser.

    Args:
        event: The event Lambda event object
        context: The event Lambda event context
    
    Returns:
        No returns
    """

    # Create client
    iam_client = boto3.client('iam')

    # Get user name from event
    user_name = event['detail']['requestParameters']['userName']
    create_date = event['detail']['responseElements']['user']['createDate']

    # Check criteria
    if "KEY_WORD" not in user_name:
        try:
            iam_client.add_user_to_group(
                GroupName=GROUP_NAME,
                UserName=user_name,
            )
            logger.info('Sucessfully created IAM User {}'.format(user_name))
        except Exception as e:
            logger.error('Error while creating created IAM User {}'.format(user_name))
            raise e

        # # For logging purpose
        # response = {
        #     "statusCode": 200,
        #     "User": json.dumps(user_name),
        #     "Group": json.dumps(GROUP_NAME),
        #     "Comment": json.dumps("Added user to group"),
        # }

        # print(response)
        # return response

    else:
        logger.info('No changes needed on FunctionalUser {}'.format(user_name))
