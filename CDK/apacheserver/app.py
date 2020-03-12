#!/usr/bin/env python3

from aws_cdk import core

from ec2_dev.ec2_dev_stack import Ec2DevStack

env_EU = core.Environment(account="431892011317", region="eu-central-1")

app = core.App()
Ec2DevStack(app, "ec2Apache", env=env_EU)

app.synth()
