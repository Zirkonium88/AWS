from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as logs
from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import aws_cloudwatch_actions as actions
from aws_cdk import custom_resources as custom
from aws_cdk import aws_cloudformation as cfn
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets

class VpcSetupStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes her

        #####################
        # Customzied Basic VPC
        #####################

        vpc = ec2.Vpc(
            self,
            id="Basic_Vpc",
            max_azs=2,
            cidr='192.168.0.0/20',
            # configuration will create 2 groups in 2 AZs = 6 subnets.
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC,
                    name="Public",
                    cidr_mask=22
                ), 
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED,
                    name="Private",
                    cidr_mask=22
                )
            ],
            nat_gateways=0,
        )

        #####################
        # VPC Check Lambda
        #####################

        lambda_vpc_check = _lambda.Function(
            self,
            id="Delete_Default_VPC",
            handler="handler.DeleteDefaultVPC",
            code=_lambda.Code.asset("./lambda/vpc/"),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_7,
            function_name="Lambda_Daily_Delete_Default_VPC",
            timeout=core.Duration.seconds(300),
            retry_attempts=1,
            log_retention=logs.RetentionDays.FIVE_DAYS
        )

        lambda_vpc_check.add_to_role_policy(
            statement=iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ec2:DeleteSecurityGroup",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DescribeStaleSecurityGroups",
                        "ec2:DescribeRouteTables",
                        "ec2:DeleteRoute",
                        "ec2:DeleteRouteTable",
                        "ec2:DescribeNetworkAcls",
                        "ec2:DeleteNetworkAcl",
                        "ec2:DescribeSubnets",
                        "ec2:DeleteSubnet",  
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DetachNetworkInterface",
                        "ec2:DescribeVpcAttribute",
                        "ec2:DescribeVpcs",
                        "ec2:DeleteVpc",                    
                        "ec2:DescribeInternetGateways",
                        "ec2:DetachInternetGateway",
                        "ec2:DeleteInternetGateway",
                        "ec2:DescribeRegions",
                        "ec2:DescribeAccountAttributes"
                    ],
                    resources=["*"]
                )
        )

        vpc_check_rule = events.Rule(
            self,
            id="Schedule_VPC_Check_Lambda",
            schedule=events.Schedule.cron(
                    minute='0',
                    hour='22',
                    month='*',
                    week_day='*',
                    year='*'),
        )

        vpc_check_rule.add_target(targets.LambdaFunction(lambda_vpc_check))

        