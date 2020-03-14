#!/usr/bin/env python3

from aws_cdk import core

from lambdapipe.lambdapipe_stack import LambdapipeStack


app = core.App()
LambdapipeStack(app, "lambdaPipeline")

app.synth()
