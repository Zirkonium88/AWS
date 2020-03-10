from aws_cdk import core
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_s3 as s3
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
from aws_cdk import aws_cloudtrail as trail

LAMBDA_PWD_POLICY = open("./lambda/password/index.js", "r").read()
# LAMBDA_USER_KEY = open("./lambda/keyage/handler.py", "r").read()

class AccountSetupStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes her

        #####################
        # Password Policy Parameters
        #####################

        user_pwd_change = core.CfnParameter(
            self,
            id="Allow_Users_To_Change_Password",
            description='You can permit all IAM users in your account to use the IAM console to change their own passwords.',
            default=True,
            type="String",
            allowed_values=['true','false']
        )

        pwd_exp = core.CfnParameter(
            self,
            id="Hard_Expiry",
            description='You can prevent IAM users from choosing a new password after their current password has expired.',
            default=False,
            type="String",
            allowed_values=['true','false']
        )

        pwd_age = core.CfnParameter(
            self,
            id="Max_Password_Age",
            description='You can set IAM user passwords to be valid for only the specified number of days. Choose 0 if you don not want passwords to expire.',
            default="90",
            type="Number",
            constraint_description='Must be in the range [0-1095]',
            min_value=0,
            max_value=1095
        )

        pwd_length = core.CfnParameter(
            self,
            id="Minimum_Password_Length",
            description='You can specify the minimum number of characters allowed in an IAM user password.',
            default="16",
            type="Number",
            constraint_description='Must be in the range [6-128]',
            min_value=16,
            max_value=1095
        )

        pwd_reuse = core.CfnParameter(
            self,
            id="Password_Reuse_Prevention",
            description='You can prevent IAM users from reusing a specified number of previous passwords.',
            default="5",
            type="Number",
            constraint_description='Must be in the range [0-24]',
            min_value=0,
            max_value=24
        )

        pwd_lower_char = core.CfnParameter(
            self,
            id="Require_Lowercase_Characters",
            description='You can require that IAM user passwords contain at least one lowercase character from the ISO basic Latin alphabet (a to z).',
            default=True,
            type="String",
            allowed_values=['true','false']
        )

        pwd_number = core.CfnParameter(
            self,
            id="Require_Numbers_Characters",
            description='You can require that IAM user passwords contain at least one numeric character (0 to 9).',
            default=True,
            type="String",
            allowed_values=['true','false']
        )

        pwd_symbols = core.CfnParameter(
            self,
            id="Require_Symbols_Characters",
            description="You can require that IAM user passwords contain at least one of the following nonalphanumeric characters: '! @ # $ % ^ & * ( ) _ + - = [ ] {} |'",
            default=True,
            type="String",
            allowed_values=['true','false']
        )

        pwd_upper_char = core.CfnParameter(
            self,
            id="Require_Uppercase_Characters",
            description='You can require that IAM user passwords contain at least one uppercase character from the ISO basic Latin alphabet (A to Z).',
            default=True,
            type="String",
            allowed_values=['true','false']
        )

        #####################
        # Password Policy Lambda
        #####################

        lambda_pwd_pol = _lambda.Function(
            self,
            id="Set_Password_Policy",
            handler="index.handler",
            # code=_lambda.Code.from_asset(), --> Not working
            code=_lambda.Code.from_inline(code=LAMBDA_PWD_POLICY),
            memory_size=128,
            runtime=_lambda.Runtime.NODEJS_10_X,
            function_name="Lambda_Set_Password_Policy",
            timeout=core.Duration.seconds(30),
            retry_attempts=1,
            log_retention=logs.RetentionDays.FIVE_DAYS
        )

        lambda_pwd_pol.add_to_role_policy(
            statement=iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        'iam:GetAccountPasswordPolicy',
                        'iam:UpdateAccountPasswordPolicy',
                        'iam:DeleteAccountPasswordPolicy'
                    ],
                    resources=["*"]
                )
        )

        update_pwd_pol = cfn.CustomResource(
            self,
            id="Update_Password_Policy",
            provider=cfn.CustomResourceProvider.lambda_(lambda_pwd_pol),
            properties={
                "HardExpiry": pwd_exp.value_as_string,
                "AllowUsersToChangePassword": user_pwd_change.value_as_string,
                "MaxPasswordAge": pwd_age.value_as_number,
                "MinimumPasswordLength": pwd_length.value_as_number,
                "PasswordReusePrevention": pwd_reuse.value_as_number,
                "RequireLowercaseCharacters": pwd_lower_char.value_as_string,
                "RequireNumbers": pwd_number.value_as_string,
                "RequireSymbols": pwd_symbols.value_as_string,
                "RequireUppercaseCharacters": pwd_upper_char.value_as_string,
                "ServiceToken": lambda_pwd_pol.function_arn,
            }
        )

        #####################
        # Email for Alerts
        #####################

        user_email = core.CfnParameter(
            self,
            id="user_email",
            description="A valid email address",
            default="YOUR_EMAIL@exmaple.com.com",
            type="String"
        )

        #####################
        # Basic IAM Admin Group
        #####################

        sandbox_admin_group = iam.Group(
            self,
            id="SandBox_Admin_User_Group",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")],
        )

        #####################
        # Additional Policy for Admin
        #####################

        sandbox_admin_policy = iam.Policy(
            self,
            id="Limit_Sandbox_Admin_Group",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect("DENY"),
                    # effect=iam.Effect.ALLOW,
                    actions=[
                        "ec2:*Reserved*",
                        "dynamodb:*Reserved*",
                        "rds:*Reserved*",
                        "elasticache:*Reserved*",
                        "redshift:*Reserved*",
                        "elasticsearch:*Reserved*",
                        "cloudfront:*Reserved*",
                        "emr:*Reserved*",
                        # not working: Action '*:*Reserved*' is invalid. An action string consists of a service namespace
                        # "*:*Reserved*",
                    ],
                    resources=[
                        "*"
                    ]
                )
            ]
        )

        #####################
        # Attach additional Policy to Group
        #####################

        limited_sandbox_admin = sandbox_admin_group.attach_inline_policy(sandbox_admin_policy)

        #####################
        # Limit Cross Account Access
        #####################

        # limited_cross_account_role = cross_account_role.attach_inline_policy(sandbox_admin_policy)

        #####################
        # Billing Alert Topic
        #####################

        billing_topic = sns.Topic(
            self,
            id="Billing_Topic",
            topic_name="BillingAllertTopic",
            display_name="BillingAllertTopic",
        )

        #####################
        # User subscription
        #####################

        # not working

        #billing_topic.add_subscription(
        #    subscription=user_subscription
        #)

        #####################
        # Billing Topic Subscription
        #####################

        billing_sub = sns.CfnSubscription(
            self,
            id="Billing_Topic_Subscription",
            endpoint= user_email.value_as_string,
            protocol="email",
            topic_arn=billing_topic.topic_arn
        )

        #####################
        # The billing metric
        #####################

        billing_metric = cloudwatch.Metric(
            metric_name="Estimated_Charges",
            namespace="AWS/Billing",
            dimensions={
                "Currency": "USD"
            },
            statistic="Maximum"
        )

        #####################
        # 5 $ Alert
        #####################

        billing_alert_5Dollars = cloudwatch.Alarm(
            self,
            id="Billing_Alert5_Dollars",
            period=core.Duration.hours(6),
            threshold=5,
            metric=billing_metric,
            evaluation_periods=1,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
            alarm_description="If costs are greater then 5$ within 6 hours, this alarm will be triggered."
        )

        billing_alert_5Dollars.node.add_dependency(billing_topic)
        
        #####################
        # 5 $ Alert Action
        #####################

        billing_alert_action = actions.SnsAction(
            topic=billing_topic
        )

        billing_alert_5Dollars.add_alarm_action(billing_alert_action)

        #####################
        # User Check Topic
        #####################

        user_topic = sns.Topic(
            self,
            id="Check_User_Topic",
            topic_name="UserAccessKeyTopic",
            display_name="UserAccessKeyTopic",
        )

        #####################
        # User Check Topic Subscription
        #####################

        user_subscription = sns.CfnSubscription(
            self,
            id="User_Topic_Subscription",
            endpoint= user_email.value_as_string,
            protocol="email",
            topic_arn=user_topic.topic_arn
        )

        #####################
        # Key Check Lambda
        #####################

        lambda_key_check = _lambda.Function(
            self,
            id="Check_User_Keys",
            handler="handler.DailyUserCheck",
            code=_lambda.Code.asset("./lambda/keyage/"),
            memory_size=128,
            runtime=_lambda.Runtime.PYTHON_3_7,
            function_name="Lambda_User_Keys",
            timeout=core.Duration.seconds(30),
            retry_attempts=1,
            log_retention=logs.RetentionDays.FIVE_DAYS,
            environment={
                "SecOpsTopicArn": user_topic.topic_arn,
                "KeyAge": "90",
            },
        )

        lambda_key_check.add_to_role_policy(
            statement=iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        'iam:ListUsers',
                        'iam:ListAccessKeys'
                    ],
                    resources=["*"]
                )
        )

        user_topic.grant_publish(lambda_key_check)

        user_check_rule = events.Rule(
            self,
            id="Schedule_Check_Key_Lambda",
            schedule=events.Schedule.cron(
                minute='0',
                hour='18',
                month='*',
                week_day='*',
                year='*'
            ),
        )

        user_check_rule.add_target(targets.LambdaFunction(lambda_key_check))

        #####################
        # Root User Topic
        #####################

        root_user_topic = sns.Topic(
            self,
            id="Root_User_Topic",
            topic_name="RootUserAccessTopic",
            display_name="RootUserAccessTopic",
        )

        #####################
        # CloudTrail
        #####################

        cloudtrail_bucket = s3.Bucket(
            self,
            id="Cloudtrail_Bucket",
            bucket_name="431892011317-logs"
        )

        cloudtrail_bucket.add_lifecycle_rule(
            expiration=core.Duration.days(1),
        )

        cloudtrail = trail.Trail(
            self,
            id="Basic_Trail",
            cloud_watch_logs_retention=logs.RetentionDays.FIVE_DAYS,
            include_global_service_events=True,
            enable_file_validation=True,
            bucket=cloudtrail_bucket
        )

        #####################
        # Root User Check Topic Subscription
        #####################

        root_user_sub = sns.CfnSubscription(
            self,
            id="Root_User_Topic_Subscription",
            endpoint= user_email.value_as_string,
            protocol="email",
            topic_arn=root_user_topic.topic_arn,
        )

        root_user_rule = events.Rule(
            self,
            id="Root_Account_Usage",
            description="Events rule for monitoring root AWS Console Sign In activity",
            rule_name="Root_Activity_Rule",
            event_pattern=events.EventPattern(
                detail={
                    "userIdentity": {
                    "type": [
                        "Root"
                    ]
                    }
                },
                detail_type=["AWS Console Sign In via CloudTrail"]
            ),
            targets=[
                targets.SnsTopic(root_user_topic)
            ]
        )

        root_user_rule.node.add_dependency(root_user_topic)
