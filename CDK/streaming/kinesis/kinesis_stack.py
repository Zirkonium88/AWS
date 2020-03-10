from aws_cdk import core
from aws_cdk import aws_kinesisfirehose as firehose
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3

class KinesisStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, bucket_arn: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # Referenced Bucket
        referenced_bucket = s3.Bucket.from_bucket_arn(
            self,
            id="Ref_Iot_Data_Bucket",
            bucket_arn=bucket_arn
        )

        # IAM Role for Firehose
        firehose_role = iam.Role(
            self,
            id="Firehose_Role",
            assumed_by=iam.ServicePrincipal(
                service="firehose.amazonaws.com"
            )
        )

        delivery_policy = iam.Policy(
            self,
            id="Firehose_Policy",
            policy_name="Firehose_Policy",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "s3:AbortMultipartUpload",
                        "s3:GetBucketLocation",
                        "s3:GetObject",
                        "s3:ListBucket",
                        "s3:ListBucketMultipartUploads",
                        "s3:PutObject"
                    ],
                    resources=[
                        referenced_bucket.bucket_arn,
                        referenced_bucket.bucket_arn+"/*"
                    ]
                )
            ]               
        )

        delivery_policy.attach_to_role(firehose_role)

        # Firehose stream
        delivery_stream = firehose.CfnDeliveryStream(
            self,
            id="IoT_Batch_Layer_Stream",
            delivery_stream_name="IoT_Data_Batch_Stream",
            s3_destination_configuration={
                "bucketArn": referenced_bucket.bucket_arn,
                "bufferingHints": {
                    "intervalInSeconds": 60,
                    "sizeInMBs": 50
                },
                "compressionFormat": "UNCOMPRESSED",
                "roleArn": firehose_role.role_arn
            }
        )     

        # delivery_stream.add_depends_on(firehose_role)

        # We assign the stream's arn and name to a local variable for the Object.
        self._delivery_stream_name = delivery_stream.delivery_stream_name
        self._delivery_stream_arn = delivery_stream.attr_arn
    
    # Using the property decorator to export value delivery_arn
    @property
    def main_delivery_stream_props(self):
        return self._delivery_stream_name, self._delivery_stream_arn