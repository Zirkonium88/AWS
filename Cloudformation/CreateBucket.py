# http://aws.amazon.com/cloudformation/aws-cloudformation-templates/

# Use troposphere to write your CloudFormation templates makes things easier.
# Steps: Install a venv and the the required packages (troposphere and awacs).

from troposphere import Output, Parameter, Ref, Template
from troposphere.s3 import (Bucket, LifecycleConfiguration, LifecycleRule,
                            LifecycleRuleTransition,
                            NoncurrentVersionTransition, PublicRead,
                            VersioningConfiguration)

t = Template()

t.add_description(
    "This AWS CloudFormation template creates two S3 Buckets."
    "One with simple settings and the other one with advanced settings to hold"
    "website content")

NamedBucket = t.add_parameter(Parameter(
    "DefaultBucket",
    Type="String",
    Description="Bucket with default settings."
))

# First Bucket
s3bucket = t.add_resource(Bucket(
    "DefaultS3Bucket",
    BucketName=Ref(NamedBucket)
))

# Second Bucket
s3bucket = t.add_resource(Bucket(
    "WebsiteS3Bucket",
    # Make public Read
    AccessControl=PublicRead,
    # Turn on Versioning to the whole S3 Bucket
    VersioningConfiguration=VersioningConfiguration(
        Status="Enabled",
    ),
    # Attach a LifeCycle Configuration
    LifecycleConfiguration=LifecycleConfiguration(Rules=[
        # Add a rule to
        LifecycleRule(
            # Rule attributes
            Id="S3BucketRule001",
            Prefix="/only-this-sub-dir",
            Status="Enabled",
            # Applies to current objects
            ExpirationInDays=3650,
            Transitions=[
                LifecycleRuleTransition(
                    StorageClass="STANDARD_IA",
                    TransitionInDays=60,
                ),
            ],
            # Applies to Non Current objects
            NoncurrentVersionExpirationInDays=365,
            NoncurrentVersionTransitions=[
                NoncurrentVersionTransition(
                    StorageClass="STANDARD_IA",
                    TransitionInDays=30,
                ),
                NoncurrentVersionTransition(
                    StorageClass="GLACIER",
                    TransitionInDays=120,
                ),
            ],
        ),
    ]),

))

t.add_output(Output(
    "DefaultBucketOutput",
    Value=Ref(s3bucket),
    Description="Name of S3 default bucket"
))

t.add_output(Output(
    "WebsiteBucketOutput",
    Value=Ref(s3bucket),
    Description="Name of S3 bucket to hold website content"
))

# print(t.to_json())
print(t.to_yaml())
