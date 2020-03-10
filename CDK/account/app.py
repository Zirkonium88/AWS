#!/usr/bin/env python3

from aws_cdk import core

from account_setup.account_setup_stack import AccountSetupStack
from account_setup.vpc_setup_stack import VpcSetupStack

env_USA = core.Environment(account="YOUR_ACCOUNT_ID", region="us-east-1")
env_EU = core.Environment(account="YOUR_ACCOUNT_ID", region="eu-central-1")

ACCOUNT_SETUP="Sets some basic accounts settings"
VPC_SETUP="Deletes all default VPCs and creates a new customized one"

app = core.App()

account = AccountSetupStack(app, "accountSetUp", description=ACCOUNT_SETUP, env=env_USA)
vpc = VpcSetupStack(app, "vpcSetUp", description=VPC_SETUP, env=env_EU)

# Deal with dependencies
vpc.add_dependency(account)

app.synth()
