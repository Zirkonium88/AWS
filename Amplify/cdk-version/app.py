#!/usr/bin/env python3

from aws_cdk import core

from cdk_version.cdk_version_stack import CdkVersionStack


app = core.App()
CdkVersionStack(app, "cdk-version")

app.synth()
