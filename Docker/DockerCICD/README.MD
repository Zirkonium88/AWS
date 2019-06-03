# A CICD piepline for Docker images

Using a automized CICD pipeline can save you hours of putting updated applications in the right place. If you can't use CodeCommit (e.g. to work together with Azure), a S3 Bucket with enabled `Versioning` option can used to emulated something like a Git. Going, one a the pipeline ends in ECR.

## Warning

The Cloudformation template deploys ressource within your account. You will get payed for them!

## Using Troposphere to generate a Cloudformation template

I very dislike bare debeloping of Cloudformation templates. An easy way to deal with this situation come up with [`troposphere`](https://github.com/cloudtools/troposphere). Here, the work gets done with Python and a very good documentation.

The following [Python file](DockerCICD/CICD.py) gets transformed with `python CICD.py > DockerCICD.yml` to our wanted Cloudformation YAML template.

````python
# Converted from CodePipeline example located at:
# http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codepipeline-pipeline.html # noqa

import awacs.aws
import awacs.codebuild as cb
import awacs.codepipeline as cp
import awacs.ecr as ecr
import awacs.logs as logs
import awacs.s3 as s3
from awacs.aws import Action, Allow, AWSPrincipal, Principal, Statement
from awacs.sts import AssumeRole
from troposphere import (AccountId, GetAtt, Join, Output, Parameter, Ref,
                         Region, Template)
from troposphere.cloudtrail import DataResource, EventSelector, Trail
from troposphere.codebuild import (Artifacts, Environment, Project,
                                   ProjectCache, Source)
from troposphere.codepipeline import (Actions, ActionTypeId, ArtifactStore,
                                      InputArtifacts, OutputArtifacts,
                                      Pipeline, Stages)
from troposphere.ecr import Repository
from troposphere.events import Rule, Target
from troposphere.iam import Policy, Role
from troposphere.s3 import Bucket, BucketPolicy, VersioningConfiguration

S3_OBJECT_Key = "docker.zip"
PROJECT_NAME = "cicdstaticwebsite"
BUILD_NAME = "dockerdeliverystaticwebsite"
S3_DELIVERY_BUCKET = "dockerstaticwebsite"
ARTIFACT_BUCKET = "buildartifactsbucket"
ECR_REPO = "dockerstaticwebsite"
VERSION = "2012-10-17"

t = Template()
t.add_version("2010-09-09")

ProjectName = t.add_parameter(Parameter(
    "AppName",
    Type="String",
    Description="Application Name",
    MinLength="1",
    MaxLength="255",
    Default=PROJECT_NAME,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

RepoName = t.add_parameter(Parameter(
    "RepName",
    Type="String",
    Description="ECR Repository Name",
    MinLength="1",
    MaxLength="255",
    Default=ECR_REPO,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

ObjectKey = t.add_parameter(Parameter(
    "S3ObjectKey",
    Type="String",
    Description="Uploaded Key",
    MinLength="1",
    MaxLength="255",
    Default=S3_OBJECT_Key,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

ArtifactBucket = t.add_parameter(Parameter(
    "ArtifactBucket",
    Type="String",
    Description="Artifact Bucket Name",
    MinLength="1",
    MaxLength="255",
    Default=ARTIFACT_BUCKET,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

DeliveryBucket = t.add_parameter(Parameter(
    "DeliveryBucket",
    Type="String",
    Description="Retrieval Bucket Name",
    MinLength="1",
    MaxLength="255",
    Default=S3_DELIVERY_BUCKET,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

BuildName = t.add_parameter(Parameter(
    "Key",
    Type="String",
    Description="CodeBuild Project Name",
    MinLength="1",
    MaxLength="255",
    Default=BUILD_NAME,
    AllowedPattern="[\\x20-\\x7E]*",
    ConstraintDescription="can contain only ASCII characters.",
))

t.set_description("This AWS CloudFormation Template deploys a S3-based CICD pipeline to deploy a docker image to Amazon ECR. The image needs to be upload to azuredropbucket ressource as zip. Docker build runs within the pipeline.")

# Generate two Buckets
IncommingBucket = t.add_resource(Bucket(
    S3_DELIVERY_BUCKET,
    VersioningConfiguration=VersioningConfiguration(
        Status="Enabled",
    )
))

BuildArtifacts = t.add_resource(Bucket(
    'buildartifactsbucket'
))

AWSCloudTrailBucket = t.add_resource(Bucket(
    'AWSCloudTrailBucket'
))

# Generate a ECR Repository
DockerStaticWebsiteRepo = t.add_resource(
    Repository(
        'DockerStaticWebsiteRepo',
        RepositoryName=Ref(RepoName),
        RepositoryPolicyText=awacs.aws.Policy(
            Version=VERSION,
            Statement=[
                awacs.aws.Statement(
                    Sid='AllowPushPull',
                    Effect=Allow,
                    Principal=AWSPrincipal('*'),
                    Action=[
                        ecr.GetDownloadUrlForLayer,
                        ecr.BatchGetImage,
                        ecr.BatchCheckLayerAvailability,
                        ecr.PutImage,
                        ecr.InitiateLayerUpload,
                        ecr.UploadLayerPart,
                        ecr.CompleteLayerUpload,
                    ],
                ),
            ]
        ),
    )
)

# Generate the service policy and the service role for CodeBuild
CodeBuildServiceRole = t.add_resource(Role(
    "CodeBuildServiceRole",
    AssumeRolePolicyDocument=awacs.aws.Policy(
        Version=VERSION,
        Statement=[
            awacs.aws.Statement(
                Effect=Allow,
                Action=[Action("sts", "AssumeRole")],
                Principal=Principal("Service", ["codebuild.amazonaws.com"])
            )
        ]
    ),
    Policies=[
        Policy(
            PolicyName="WorktwithS3",
            PolicyDocument=awacs.aws.Policy(
                Version=VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            # Action("s3", "*"),
                            Action("s3", "GetObject"),
                            Action("s3", "PutObject"),
                            Action("s3", "GetBucketAcl"),
                            Action("s3", "ListBucket"),
                            Action("s3", "GetBucketLocation"),
                            Action("s3", "GetObjectVersion")
                        ],
                        Resource=[
                            # '*'
                            GetAtt(IncommingBucket, "Arn"),
                            GetAtt(BuildArtifacts, "Arn"),
                            Join(
                                "/",
                                [GetAtt(IncommingBucket, "Arn"), '*']
                            ),
                            Join(
                                "/",
                                [GetAtt(BuildArtifacts, "Arn"), '*']
                            )
                        ],
                    ),
                ],
            )
        ),
        Policy(
            PolicyName="WorkWithLogs",
            PolicyDocument=awacs.aws.Policy(
                Version=VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("logs", "PutLogEvents"),
                            Action("logs", "CreateLogStream"),
                            Action("logs", "CreateLogGroup")
                        ],
                        Resource=["*"],
                    ),
                ],
            )
        ),
        Policy(
            PolicyName="WorkWithECR",
            PolicyDocument=awacs.aws.Policy(
                Version=VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("ecr", "CompleteLayerUpload"),
                            Action("ecr", "UploadLayerPart"),
                            Action("ecr", "GetAuthorizationToken"),
                            Action("ecr", "InitiateLayerUpload"),
                            Action("ecr", "BatchCheckLayerAvailability"),
                            Action("ecr", "PutImage")
                        ],
                        Resource=['*'],
                    ),
                ],
            )
        ),
    ]
))

# Generate the build porject
CodeBuildProject = t.add_resource(Project(
    "CodeBuildProjectDockerStaticWebsite",
    TimeoutInMinutes=60,
    Artifacts=Artifacts(
        Type='CODEPIPELINE'
    ),
    Cache=ProjectCache(
        Type='NO_CACHE'
    ),
    Environment=Environment(
        ComputeType='BUILD_GENERAL1_SMALL',
        Image='aws/codebuild/standard:2.0',
        Type='LINUX_CONTAINER',
        PrivilegedMode=True,
        ImagePullCredentialsType='CODEBUILD'
    ),
    ServiceRole=GetAtt(CodeBuildServiceRole, "Arn"),
    Name=PROJECT_NAME,
    Source=Source(
        Type='CODEPIPELINE',
        GitCloneDepth=1,
        InsecureSsl=False
    )
))

# Generate the service policy and the service role for CodePipeline
CodePipelineServiceRole = t.add_resource(Role(
    "CodePipelineServiceRole",
    AssumeRolePolicyDocument=awacs.aws.Policy(
        Version=VERSION,
        Statement=[
            awacs.aws.Statement(
                Effect=Allow,
                Action=[Action("sts", "AssumeRole")],
                Principal=Principal("Service", ["codepipeline.amazonaws.com"])
            )
        ]
    ),
    Policies=[
        Policy(
            PolicyName="CopyCodePipelineServicePolicy",
            PolicyDocument=awacs.aws.Policy(
                Version=VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("iam", "PassRole"),
                            Action("codebuild", "BatchGetBuilds"),
                            Action("codebuild", "StartBuild"),
                            Action("elasticbeanstalk", "*"),
                            Action("ec2", "*"),
                            Action("elasticloadbalancing", "*"),
                            Action("autoscaling", "*"),
                            Action("cloudwatch", "*"),
                            Action("s3", "*"),
                            Action("sns", "*"),
                            Action("cloudformation", "*"),
                            Action("rds", "*"),
                            Action("sqs", "*"),
                            Action("ecs", "*"),
                            Action("fargate", "*"),
                        ],
                        Resource=['*']
                    )
                ],
            ),
        )
    ],
    Path='/'
))

# Generate the CIDCD pipeline
CodePipeline = t.add_resource(Pipeline(
    "DockerStaticWebsitePipeline",
    ArtifactStore=ArtifactStore(
        Location=Ref(ARTIFACT_BUCKET),
        Type='S3',
    ),
    RoleArn=GetAtt(CodePipelineServiceRole, "Arn"),
    Name=BUILD_NAME,
    Stages=[
        Stages(
            Name="Source",
            Actions=[
                Actions(
                    Name="Source",
                    ActionTypeId=ActionTypeId(
                        Category="Source",
                        Owner="AWS",
                        Version="1",
                        Provider="S3"
                    ),
                    OutputArtifacts=[
                        OutputArtifacts(
                            Name="SourceArtifact"
                        )
                    ],
                    Configuration={
                        "PollForSourceChanges": 'false',
                        "S3Bucket": Ref(IncommingBucket),
                        "S3ObjectKey": S3_OBJECT_Key,
                    },
                    RunOrder=1,
                    Region=Region
                )
            ]
        ),
        Stages(
            Name='Build',
            Actions=[
                Actions(
                    Name='Build',
                    ActionTypeId=ActionTypeId(
                        Category='Build',
                        Owner='AWS',
                        Provider='CodeBuild',
                        Version='1'
                    ),
                    Configuration={
                        "ProjectName": PROJECT_NAME
                    },
                    Region=Region,
                    InputArtifacts=[
                        InputArtifacts(
                            Name="SourceArtifact"
                        )
                    ],
                    OutputArtifacts=[
                        OutputArtifacts(
                            Name="BuildArtifact"
                        )
                    ]
                )
            ]
        )
    ]
))

# Creat Event Rule role
EventRole = t.add_resource(Role(
    "DockerStaticWebsiteEventRole",
    AssumeRolePolicyDocument=awacs.aws.Policy(
        Version=VERSION,
        Statement=[
            awacs.aws.Statement(
                Effect=Allow,
                Action=[Action("sts", "AssumeRole")],
                Principal=Principal("Service", ["events.amazonaws.com"])
            )
        ]
    ),
    Policies=[
        Policy(
            PolicyName="DockerSaticWebsitePipeline",
            PolicyDocument=awacs.aws.Policy(
                Version=VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("codepipeline", "StartPipelineExecution"),
                        ],
                        Resource=[Join(
                            "",
                            ['arn:aws:codepipeline:', Region, ":",
                                AccountId, ":", Ref(CodePipeline)]
                        )
                        ]
                    )
                ],
            ),
        )
    ],
))


# Create the Event Rule
EventRule = t.add_resource(Rule(
    "DockerStaticWebsiteEventRule",
    Name='codepipeline-DockerStaticWebsiteEventRule',
    State='ENABLED',
    Description='Amazon CloudWatch Events rule to automatically start your pipeline when a change occurs in the Amazon S3 object key or S3 folder. Deleting this may prevent changes from being detected in that pipeline. Read more: http://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-about-starting.html',
    EventPattern={
        "source": [
                "aws.s3"
        ],
        "detail-type": [
            "AWS API Call via CloudTrail"
        ],
        "detail": {
            "eventSource": [
                "s3.amazonaws.com"
            ],
            "eventName": [
                "PutObject",
                "CompleteMultipartUpload",
                "CopyObject"
            ],
            "requestParameters": {
                "bucketName": [
                    {"Ref": S3_DELIVERY_BUCKET}
                ],
                "key": [
                    S3_OBJECT_Key
                ]
            }
        }
    },
    Targets=[
        Target(
            Arn=Join(
                "",
                ['arn:aws:codepipeline:', Region, ":", AccountId, ":", BUILD_NAME]
            ),
            Id='CodePipelineTarget',
            RoleArn=GetAtt(EventRole, "Arn"),
        )
    ]
))

BucketPolicy = t.add_resource(BucketPolicy(
    "BucketPolicy",
    PolicyDocument={
        "Statement": [
                {
                "Sid": "AWSCloudTrailAclCheck",
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                    "cloudtrail.amazonaws.com"
                    ]
                },
                "Action": "s3:GetBucketAcl",
                "Resource": {
                    "Fn::GetAtt": [
                    "AWSCloudTrailBucket",
                    "Arn"
                    ]
                }
                },
                {
                "Sid": "AWSCloudTrailWrite",
                "Effect": "Allow",
                "Principal": {
                    "Service": [
                    "cloudtrail.amazonaws.com"
                    ]
                },
                "Action": "s3:PutObject",
                "Resource": {
                    "Fn::Join": [
                    "",
                    [
                        {
                        "Fn::GetAtt": [
                            "AWSCloudTrailBucket",
                            "Arn"
                        ]
                        },
                        "/AWSLogs/",
                        {
                        "Ref": "AWS::AccountId"
                        },
                        "/*"
                    ]
                    ]
                },
                "Condition": {
                    "StringEquals": {
                    "s3:x-amz-acl": "bucket-owner-full-control"
                    }
                }
                }
            ]
    },
    Bucket=Ref(AWSCloudTrailBucket),
))

S3DeliveryTrail = t.add_resource(Trail(
    "S3DeliveryTrail",
    IsLogging=True,
    S3BucketName=Ref(AWSCloudTrailBucket),
    DependsOn=["BucketPolicy"],
    EventSelectors=[
        EventSelector(
            IncludeManagementEvents=True,
            DataResources=[
                DataResource(
                    Values=[
                        Join("",["arn:aws:s3:::",Ref(IncommingBucket),"/",S3_OBJECT_Key])
                    ],
                    Type="AWS::S3::Object",
                ),
            ],
            ReadWriteType="All",
        ),
    ],
))

# Show cerated ressources
t.add_output(
    [Output(
        "S3DeliveryTrail",
        Description="Cloudtrail to detect drift changes within S3",
        Value=GetAtt(S3DeliveryTrail, "Arn")
    ),
        Output(
            "IncommingBucket",
            Description="Incomming Bucket for docker.zip",
            Value=GetAtt(IncommingBucket, "Arn")
    ),
        Output(
            "BuildArtrifactsBucket",
            Description="Logging Bucket: Build process",
            Value=GetAtt(CodeBuildProject, "Arn")
    ),
        Output(
            "CodeBuildARN",
            Description="CodeBuild Arn",
            Value=GetAtt(CodeBuildProject, "Arn")
    ),
        Output(
            "CodePipelineARN",
            Description="CodePipeline Arn",
            Value=Join(
                "",
                ['arn:aws:codepipeline:', Region, ":", AccountId, ":", BUILD_NAME]
            )
    ),
        Output(
            "ServiceRoleBuild",
            Description="CodeBuild IAM role",
            Value=GetAtt(CodeBuildServiceRole, "Arn")
    ),
        Output(
            "ServiceRolePipeline",
            Description="CodePipelind IAM role",
            Value=GetAtt(CodePipelineServiceRole, "Arn"),
    ),
        Output(
            "EventRule",
            Description="Cloudwatch Event Rule to trigger CodePipeline",
            Value=GetAtt(EventRule, "Arn")
    )
    ]
)

# print(t.to_json())
print(t.to_yaml())

````
As you can see, JSON-script can be retrieve as well. First change

`````python
print(t.to_json())
#print(t.to_yaml())
`````

at the end of the CICD.py file. Second, use `python CICD.py > DockerCICD.json`to get a json.


## Deploying the Cloudformation template

First, validate the Cloudformation template with: 

````bash
aws cloudformation validate-template --template-body file://./DockerCICD.yml 
```` 

Afterwards, deploy the template with:

````bash
aws cloudformation deploy --template-file ./DockerCICD.yml --stack-name dockerstaticwebsite --capabilities CAPABILITY_NAMED_IAM
```` 

`--capabilities CAPABILITY_NAMED_IAMCAPABILITY_NAMED_IAM` is needed because you will deploy IAM ressources.

## Creat your buildspec.yml

Before uploading your Docker image, you need to create your `buildspec.yml`. It can look like this:

````bash
version: 0.2

env:
  variables:
    AWS_DEFAULT_REGION: "eu-central-1"
    AWS_ACCOUNT_ID: "037732949416"
    IMAGE_REPO_NAME: "dockerstaticwebsite"
    IMAGE_TAG: "latest"
    
phases:
  install:aws s3 
    runtime-versions:
      docker: 18
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - $(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...          
      - docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
      - docker tag $IMAGE_REPO_NAME:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG      
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker image...
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$IMAGE_REPO_NAME:$IMAGE_TAG
````

## Upload your docker image as zip file to S3

Gather all files (at least the `Dockerfile`, it dependencies and the `buildspec.yml`) together in one directory. Ready? Use `zip -r docker.zip .`, get the complete bucket name of your `dockerstaticwebsite`  and upload you zip-file to S3:

````bash
aws s3 ls
aws s3 cp foo.zip s3://dockerstaticwebsite+RANDOM_HASH

# RANDOM_HASH can be retrieved from Cloudformation outputs 
# or from your S3 console
````

Make sure you use the approciate key for your uploaded zip archive. The Cloudformations scripts uses `docker.zip`.