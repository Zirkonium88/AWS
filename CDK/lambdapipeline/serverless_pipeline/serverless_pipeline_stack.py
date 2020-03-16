from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_s3_notifications as _s3_notification
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_dynamodb as _dynamo
from aws_cdk import aws_sqs as _sqs
from aws_cdk import aws_logs as _logs


class ServerlessPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        ################################################################
        # Create a Bucket
        ################################################################

        bucket = _s3.Bucket(
            self,
            id="Pipe_Bucket",
            bucket_name="431892011317-pipe",
            encryption=_s3.BucketEncryption.S3_MANAGED,
            removal_policy=core.RemovalPolicy.DESTROY,
        )

        ################################################################
        # Create a Dead Letter Queue for Lambda_Put_Data_from_File_into_DynamoDB
        ################################################################

        dlq = _sqs.Queue(
            self,
            id="DLQ_LoadData_Lambda"
        )

        ################################################################
        # Create a Lambda fucntion: Lambda_Put_Data_from_File_into_DynamoDB
        ################################################################

        lambda_function = _lambda.Function(
            self,
            id="Pipe_Lambda",
            code=_lambda.Code.asset("./src"),
            handler="put_data_from_file_dynamo.load_data_from_csv_to_dynamodb",
            runtime=_lambda.Runtime.PYTHON_3_8,
            dead_letter_queue=dlq,
            dead_letter_queue_enabled=True,
            log_retention=_logs.RetentionDays.ONE_DAY,
            memory_size=128,
            timeout=core.Duration.seconds(30),
            function_name="Lambda_Put_Data_from_File_into_DynamoDB",
            retry_attempts=0,

        )

        ################################################################
        # Permissions for the Lambda fucntion: Lambda_Put_Data_from_File_into_DynamoDB
        ################################################################

        #dlq.grant_send_messages(lambda_function)

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

        ################################################################
        # Allow the S3 bucket to send event to Lambda fucntion: Lambda_Put_Data_from_File_into_DynamoDB
        ################################################################

        bucket.add_event_notification(
            _s3.EventType.OBJECT_CREATED,
            _s3_notification.LambdaDestination(lambda_function),
            _s3.NotificationKeyFilter(
                prefix="data",
                suffix=".csv"
            )
        )

        ################################################################
        # Create a DynamoDB table: LambdaPipeTable
        ################################################################

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

        ################################################################
        # Add the DynamoDB table name as ENV_VAR to Lambda fucntion: Lambda_Put_Data_from_File_into_DynamoDB
        ################################################################

        lambda_function.add_environment(
            key="TABLE_NAME",
            value=results_db.table_name
        )

        ################################################################
        # Allow the Lambda fucntion: Lambda_Put_Data_from_File_into_DynamoDB to write data to DynamoDB table: LambdaPipeTable
        ################################################################

        results_db.grant_write_data(lambda_function)