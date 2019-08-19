import json
import os

import boto3

# Get current iamgroup-name
GROUP_NAME = os.environ['iamgroup']


def lambda_handler(event, context):

    # Create client
    iam_client = boto3.client('iam')

    # Get user name from event
    user_name = event['detail']['requestParameters']['userName']
    create_date = event['detail']['responseElements']['user']['createDate']

    # Check criteria
    if "KEY_WORD" not in user_name:
        iam_client.add_user_to_group(
            GroupName=GROUP_NAME,
            UserName=user_name,
        )

        # For logging purpose
        response = {
            "statusCode": 200,
            "User": json.dumps(user_name),
            "Group": json.dumps(GROUP_NAME),
            "Comment": json.dumps("Added user to group"),
        }

        print(response)
        return response

    else:

        # For logging purpose
        response = {
            "statusCode": 400,
            "User": json.dumps(user_name),
            "Comment": json.dumps("No changes needed on functionalUserNasuni"),
        }
        print(response)
        return response
