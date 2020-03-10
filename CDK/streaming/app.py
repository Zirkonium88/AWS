#!/usr/bin/env python3

from aws_cdk import core
from s3.s3_stack import S3Stack
from kinesis.kinesis_stack import KinesisStack
from iot.iot_stack import IoTStack
from elasticsearch.elasticsearch_stack import ElasticSearchStack

IOT_DESCRIPTION="Creates a IoT Thing and it's Policy and Certificate as well as a IoT Topic rule to save data in S3 via Firehose"
S3_DESCRIPTION="Creates a Bucket with KMS encryption"
FIREHOSE_DESCRIPTION="Creates a Firehose Delivery Stream with the S3 Bucket as destination"
ElasticSearch_DESCRIPTION="Creates a public ES-Cluster with Kibana 7.1 within the default VPC"

app = core.App()

bucket = S3Stack(app, "s3", description=S3_DESCRIPTION)
stream = KinesisStack(app, "firehose", bucket_arn=bucket._bucket_arn, description=FIREHOSE_DESCRIPTION)
es_domain = ElasticSearchStack(app, "es-cluster", description=ElasticSearch_DESCRIPTION)
iot = IoTStack(app, 
    "iot", 
    delivery_stream_arn=stream._delivery_stream_arn, 
    delivery_stream_name=stream._delivery_stream_name, 
    es_domain_arn=es_domain._es_domain_arn,
    es_domain_name=es_domain._es_endpoint, 
    description=IOT_DESCRIPTION
)

# Deal with dependencies
stream.add_dependency(bucket)
bucket.add_dependency(es_domain)
iot.add_dependency(es_domain)


app.synth()
