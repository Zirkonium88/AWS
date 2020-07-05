# Use IAM events to trigger a Lambda

If you want to trigger a Lambda on IAM, you probably noticed that Cloudwatch events is not supported, right?. You can not create them via console but via custom event via API call. You need to deploy this Lambda in us-east-1, where IAM is hosted.

Here you can find the [Lambda](https://github.com/Zirkonium88/AWS/tree/master/Lambda/AddUser/handler.py), which evaluates every new IAM user by `KEY_WORD`. If the users matches the criteria, he/she will be added to a IAM Group. The group name will be retrieved from the environment varibales:

```python
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
    else:
        logger.info('No changes needed on FunctionalUser {}'.format(user_name))
```


The [serverless.yaml](https://github.com/Zirkonium88/AWS/tree/master/Lambda/AddUser/serverless.yml) looks like this. It deploys the Lmabda and a Cloudwatch Event.

```yaml


service: AddUser # NOTE: update this with your service name

provider:
  name: aws
  runtime: python3.7
  stage: prod
  region: us-east-1

  iamRoleStatements:
    - Effect: "Allow"
      Action:
        - "iam:ListUsers" 
        - "iam:AddUserToGroup" 
      Resource: "*"
package:
  include:
    - adduser.py
  exclude:
    - event.json
    - venv/**

functions:
  AddUser:
    handler: adduser.lambda_handler
    name: adduser-prod
    environment: # Service wide environment variables
      iamgroup: 
        Ref: IAM-Group
    events:
      - cloudwatchEvent:
          event:
            source:
              - 'aws.iam'
            detail-type:
              - "AWS API Call via CloudTrail"
            detail: 
              eventSource: 
                - "iam.amazonaws.com"
              eventName:
                - "CreateUser"
                - "UpdateUser"
```
