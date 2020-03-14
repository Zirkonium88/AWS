from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_notifications as _s3_notification
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_dynamodb as _dynamo
from aws_cdk import aws_sqs as _sqs
from aws_cdk import aws_logs as _logs


class LambdapipeStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        bucket = _s3.Bucket(
            self,
            id="Pipe_Bucket",
            bucket_name="431892011317-pipe",
            encryption=_s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        dlq = _sqs.Queue(
            self,
            id="DLQ_LoadData_Lambda"
        )

        lambda_function = _lambda.Function(
            self,
            id="Pipe_Lambda",
            code=_lambda.Code.asset("./handlers"),
            handler="loaddata.LoadData",
            runtime=_lambda.Runtime.PYTHON_3_8,
            dead_letter_queue=dlq,
            log_retention=_logs.RetentionDays.ONE_DAY,
            memory_size=128,
            timeout=core.Duration.seconds(30),
            function_name="Lambda_Put_Data_from_File_into_DynamoDB",
            retry_attempts=1
        )

        lambda_function.add_to_role_policy(
            _iam.PolicyStatement(
                effect=_iam.Effect.ALLOW,
                actions=[
                    "s3:GetBucket*",
                    "s3:GetObject*",
                    "s3:List*",
                    "s3:Head*"
                ],
                resources=[
                    bucket.bucket_arn,
                    bucket.bucket_arn+"/*"
                ]
            )
        )

        bucket.add_event_notification(
            _s3.EventType.OBJECT_CREATED,
            _s3_notification.LambdaDestination(lambda_function),
            _s3.NotificationKeyFilter(
                prefix="data",
                suffix=".csv"
            )
        )

        results_db = _dynamo.Table(
            self,
            id="LoadData_Table",
            table_name="LambdaPipeTable",
            partition_key=_dynamo.Attribute(
                name="uuid",
                type=_dynamo.AttributeType.STRING
            ),
            sort_key=_dynamo.Attribute(
                name="name",
                type=_dynamo.AttributeType.STRING
            ),
            removal_policy=core.RemovalPolicy.DESTROY
        )

        lambda_function.add_environment(
            key="TABLE_NAME",
            value=results_db.table_name
        )

        results_db.grant_write_data(lambda_function)
