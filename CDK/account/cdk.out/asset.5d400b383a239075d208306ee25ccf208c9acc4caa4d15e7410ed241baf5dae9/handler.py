import boto3
import logging
import json
import os

from botocore.exceptions import ClientError

# Set Logging Level
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logging.root.setLevel(logging.getLevelName(log_level))  # type: ignore
logger = logging.getLogger(__name__)

def DeleteIGW(ec2, vpcId):
  '''Detach and delete the internet gateway'''

  arguments = {
    'Filters' : [
      {
        'Name' : 'attachment.vpc-id',
        'Values' : [vpcId]
      }
    ]
  }

  try:
    igw = ec2.describe_internet_gateways(**arguments)['InternetGateways']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  if igw:
    igwId = igw[0]['InternetGatewayId']

    try:
      result = ec2.detach_internet_gateway(InternetGatewayId=igwId, VpcId=vpcId)
    except ClientError as e:
      logger.info(e.response['Error']['Message'])

    try:
      result = ec2.delete_internet_gateway(InternetGatewayId=igwId)
    except ClientError as e:
      logger.info(e.response['Error']['Message'])

  return


def DeleteSubnets(ec2, arguments):
  '''Delete the subnets'''
  try:
    subnets = ec2.describe_subnets(**arguments)['Subnets']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  if subnets:
    for subnet in subnets:
      subnetId = sub['SubnetId']

      try:
        result = ec2.delete_subnet(SubnetId=subnetId)
      except ClientError as e:
        logger.info(e.response['Error']['Message'])

  return


def DeleteRouteTable(ec2, arguments):
  '''Delete the route tables'''

  try:
    routeTables = ec2.describe_route_tables(**arguments)['RouteTables']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  if routeTables:
    for routeTable in routeTables:
      main = 'false'
      for assoc in routeTable['Associations']:
        main = assoc['Main']
      if main == True:
        continue
      routeTableId = routeTable['RouteTableId']
        
      try:
        result = ec2.delete_route_table(RouteTableId=routeTableId)
      except ClientError as e:
        logger.info(e.response['Error']['Message'])

  return


def DeleteACLs(ec2, arguments):
  '''Delete the network access lists (NACLs)'''
  try:
    acls = ec2.describe_network_acls(**arguments)['NetworkAcls']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  if acls:
    for acl in acls:
      default = acl['IsDefault']
      if default == True:
        continue
      aclId = acl['NetworkAclId']

      try:
        result = ec2.delete_network_acl(NetworkAclId=aclId)
      except ClientError as e:
        logger.info(e.response['Error']['Message'])

  return


def DeleteSecurityGroups(ec2, arguments):
  '''Delete any security groups'''

  try:
    securityGroups = ec2.describe_security_groups(**arguments)['SecurityGroups']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  if securityGroups:
    for securityGroup in securityGroups:
      default = securityGroup['GroupName']
      if default == 'default':
        continue
      securityGroupId = securityGroup['GroupId']

      try:
        result = ec2.delete_security_group(GroupId=securityGroupId)
      except ClientError as e:
        logger.info(e.response['Error']['Message'])

  return


def DeleteVPCs(ec2, vpcId, region):
  '''Delete the VPC'''
  
  try:
    result = ec2.delete_vpc(VpcId=vpcId)
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  else:
    print('VPC {} has been deleted from the {} region.'.format(vpcId, region))

  return


def GetRegions(ec2):
  '''Return all AWS regions'''

  regions = []

  try:
    aws_regions = ec2.describe_regions()['Regions']
  except ClientError as e:
    logger.info(e.response['Error']['Message'])

  else:
    for region in aws_regions:
      regions.append(region['RegionName'])

  return regions


def DeleteDefaultVPC(event, context):
  """
  Do the work..
  Order of operation:
  1.) Delete the internet gateway
  2.) Delete subnets
  3.) Delete route tables
  4.) Delete network access lists
  5.) Delete security groups
  6.) Delete the VPC 
  """
  logger.info('Starting VPC Clean Up')

  ec2 = boto3.client('ec2')

  regions = GetRegions(ec2)

  for region in regions:
    try:
      attributs = ec2.describe_account_attributes(AttributeNames=['default-vpc'])['AccountAttributes']
    except ClientError as e:
      logger.info(e.response['Error']['Message'])
      return

    else:
      vpcId = attributs[0]['AttributeValues'][0]['AttributeValue']

    if vpcId == 'none':
      print('VPC (default) was not found in the {} region.'.format(region))
      continue

    # Are there any existing resources?  Since most resources attach an ENI, let's check..

    arguments = {
      'Filters' : [
        {
          'Name' : 'vpc-id',
          'Values' : [ vpcId ]
        }
      ]
    }

    try:
      eni = ec2.describe_network_interfaces(**arguments)['NetworkInterfaces']
    except ClientError as e:
      logger.info(e.response['Error']['Message'])
      return

    if eni:
      print('VPC {} has existing resources in the {} region.'.format(vpcId, region))
      continue

    DeleteIGW(ec2,vpcId)
    DeleteSubnets(ec2,arguments)
    DeleteRouteTable(ec2,arguments)
    DeleteACLs(ec2,arguments)
    DeleteSecurityGroups(ec2,arguments)
    DeleteVPCs(ec2,vpcId,region)

    logger.info('Finished VPC Clean Up')
