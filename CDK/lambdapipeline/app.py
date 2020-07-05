#!/usr/bin/env python3

from aws_cdk import core

from serverless_pipeline.serverless_pipeline_stack import ServerlessPipelineStack


app = core.App()
ServerlessPipelineStack(app, "import-codes")

app.synth()
