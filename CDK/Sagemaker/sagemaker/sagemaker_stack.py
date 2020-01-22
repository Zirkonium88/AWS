from aws_cdk import core
from aws_cdk import aws_sagemaker as sagemaker
from aws_cdk import aws_glue as glue
from aws_cdk import aws_iam as iam


class SagemakerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        glue_role = iam.Role(
            self, 
            id="Glue_Role",
            assumed_by=iam.ServicePrincipal(
                service="glue.amazonaws.com"),
            role_name="Glue_Role",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AWSGlueConsoleFullAccess")]
        )

        dev_endpoint = glue.CfnDevEndpoint(
            self,
            id = "DemoDev",
            role_arn=glue_role.role_arn
        )

        sagemaker_role = iam.Role(
            self, 
            id="Sagemaker_Role",
            assumed_by=iam.ServicePrincipal(
                service="sagemaker.amazonaws.com"),
            role_name="Sagemaker_Role",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")]
        )

        sagemaker_pol = iam.Policy(
            self,
            "TaskSagemakerPol",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect('ALLOW'),
                    actions=[
                        "glue:GetDevEndpoint",
                        "glue:GetDevEndpoints",
                        "glue:UpdateDevEndpoint",
                        "glue:ListDevEndpoits"
                    ],
                    resources=[ 
                        "*"
                    ]
                )
            ]
        )

        sagemaker_pol.attach_to_role(sagemaker_role)
        
        notebook = sagemaker.CfnNotebookInstance(
            self,
            id = "Demo",
            instance_type="ml.t2.medium",
            notebook_instance_name="Demo",
            role_arn=sagemaker_role.role_arn
        )

        notebook.add_depends_on(dev_endpoint)
