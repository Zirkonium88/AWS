import datetime
import boto3
import os
import json

from botocore.exceptions import ClientError

# Set Logging Level
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)

# Set the global variables
keyAge = os.getenv('KeyAge')
SEC_OPS_TOPIC = os.getenv('SecOpsTopicArn')
usersWithOldKeys = {'Users':[],'Description':'List of users with Key Age greater than (>=) {} days'.format(keyAge),'KeyAgeCutOff':keyAge}

# Set clients
iamclient = boto3.iamclient('iam')
snsClient = boto3.iamclient('sns')

def GetIAMUser():
    '''Get all IAM Users'''
    try:
        usersList = iamclient.list_users()
    except Exception as e:
        print(e)
        logger.info(
            'Error: Make sure, that IAM User(s) exist and check Lambdas permissions.'
        )
        raise e
    return usersList

def InvalidateOutDatedKeys(keyAge,usersList):
    '''Invalidate all Keys older than keyAge and get a list of old keys'''
    try:
        timeLimit = datetime.datetime.now()-datetime.timedelta(days=keyAge)
        # Iterate through list of users and compare with `key_age` to flag old key owners
        for k in usersList['Users']:
            accessKeys = iamclient.list_access_keys(UserName=k['UserName'])
            # Iterate over all users
            for key in accessKeys['AccessKeyMetadata']:
                if key['CreateDate'].date() <= timeLimit.date():
                    usersWithOldKeys['Users'].append({ 
                        'UserName': k['UserName'],
                        'KeyAgeInDays': (datetime.date.today()-key['CreateDate'].date()).days 
                    })
                    iamclient.delete_access_key(
                        UserName=key['UserName'],
                        AccessKeyId=key['AccessKeyId']
                    )
        # If no users found with outdated keys, add message in response
        if not usersWithOldKeys['Users']:
            logger.info('Found 0 Keys that are outdated than {} days'.format(keyAge))
        else:
            logger.info('Found {0} Keys that are outdated than {1} days'.format(len(usersWithOldKeys['Users']),keyAge)
    except Exception as e:
        print(e)
        logger.info('Error: Something went wrong while listing the users and their keys.')
        raise e
    return usersWithOldKeys

def SendReport(usersWithOldKeys):
    '''Send a report of outdated keyse to SEC_OPS_TOPIC'''
    try:
        snsClient.publish(
            TopicArn = SEC_OPS_TOPIC,
            Message = json.dumps(usersWithOldKeys,indent=4) 
        )
    except Exception as e:
        print(e)
        logger.info('Error: Something went while sending the report.')
        raise e

def DailyUserCheck(event, context):
    logger.info('Starting daily IAM user check ...')
    usersList = GetIAMUser()
    usersWithOldKeys = InvalidateOutDatedKeys(keyAge,usersList)
    SendReport(usersWithOldKeys)
    logger.info('Finishing daily IAM user check ...')

if __name__ == '__main__':
    DailyUserCheck()