#!/usr/bin/env python3

from aws_cdk import core

from sage_maker_glue.sage_maker_glue_stack import SageMakerGlueStack


app = core.App()
SageMakerGlueStack(app, "sage-maker-glue")

app.synth()
