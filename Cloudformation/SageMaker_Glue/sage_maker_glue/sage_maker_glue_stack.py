from aws_cdk import core
from aws_cdk import aws_sagemaker as sagemaker
from aws_cdk import aws_glue as glue


class SageMakerGlueStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create sagemkaer notebook instance


