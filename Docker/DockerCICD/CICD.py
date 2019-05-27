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
from troposphere import AccountId, GetAtt, Join, Output, Ref, Region, Template
from troposphere.codebuild import (Artifacts, Environment, Project,
                                   ProjectCache, Source)
from troposphere.codepipeline import (Actions, ActionTypeId, ArtifactStore,
                                      InputArtifacts, OutputArtifacts,
                                      Pipeline, Stages)
from troposphere.ecr import Repository
from troposphere.events import Rule, Target
from troposphere.iam import Policy, Role
from troposphere.s3 import Bucket, VersioningConfiguration

S3_OBJECT_Key = "docker.zip"
PROJECT_NAME = "dockerstaticwebsite"
BUILD_NAME = "dockerdeliverystaticwebsite"
S3_DELIVERY_BUCKET = "dockerstaticwebsite"
ARTIFACT_BUCKET = "buildartifactsbucket"
ECR_REPO = "dockerstaticwebsite"

t = Template()

t.set_description("This AWS CloudFormation Template deploys a S3-based CICD pipeline to deploy a docker image to Amazon ECR. The image needs to be upload to azuredropbucket ressource as zip. Docker build runs within the pipeline.")

# Generate two Buckets
IncommingBucket = t.add_resource(
    Bucket(
        S3_DELIVERY_BUCKET,
        VersioningConfiguration=VersioningConfiguration(
            Status="Enabled",
            )
        )
    )   

BuildArtifacts = t.add_resource(
    Bucket(
        ARTIFACT_BUCKET,
        )
    )

# Generate a ECR Repository
DockerStaticWebsiteRepo = t.add_resource(
    Repository(
        'DockerStaticWebsiteRepo',
        RepositoryName=ECR_REPO,
        RepositoryPolicyText=awacs.aws.Policy(
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
            PolicyName = "WorktwithS3",
            PolicyDocument=awacs.aws.Policy(
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
                            Join("/",
                                [GetAtt(IncommingBucket, "Arn"),'*']
                            ),
                            Join("/",
                                [GetAtt(BuildArtifacts, "Arn"),'*']
                            )
                        ],
                    ),
                ],
            )
        ),
    Policy(
            PolicyName = "WorkWithLogs",
            PolicyDocument=awacs.aws.Policy(
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
            PolicyName = "WorkWithECR",
            PolicyDocument=awacs.aws.Policy(
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
                        Resource=[GetAtt(DockerStaticWebsiteRepo, "Arn")],
                    ),
                ],
            )
        ), 
    ],
    Path='/'
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
            PolicyName = "CopyCodePipelineServicePolicy",
            PolicyDocument=awacs.aws.Policy(
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
        Type='S3'
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
                    RunOrder="1"
                )
            ]
        ),
        Stages(
            Name='Build',
            Actions=[
                Actions(
                    Name='Build',
                    ActionTypeId=ActionTypeId(
                        Category= 'Build',
                        Owner= 'AWS',
                        Provider= 'CodeBuild',
                        Version= '1'
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
            PolicyName = "StartPipeline",
            PolicyDocument=awacs.aws.Policy(
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("codepipeline", "StartPipelineExecution"),
                            ],
                        Resource=[Join(
                            "",
                            ['arn:aws:codepipeline:',Region,":",AccountId,":",BUILD_NAME]
                            )
                        ]
                    )
                ],
            ),
        )
    ],
    Path='/'
))

# Create the Event Rule
EventRule = t.add_resource(Rule(
    "DockerStaticWebsiteEventRule",
    Name='codepipeline-DockerStaticWebsiteEventRule',
    State='ENABLED',
    
    Description='Amazon CloudWatch Events rule to automatically start your pipeline when a change occurs in the Amazon S3 object key or S3 folder. Deleting this may prevent changes from being detected in that pipeline. Read more: http://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-about-starting.html',
    ScheduleExpression='',
    EventPattern={"source":["aws.s3"],"detail-type":["AWS API Call via CloudTrail"],"detail":{"eventSource":["s3.amazonaws.com"],"eventName":["PutObject","CompleteMultipartUpload","CopyObject"],"requestParameters":{"bucketName":["my-new-stack-azuredropbucket-zy6wv6dg4yic"],"key":["docker.zip"]}}},
    Targets=[
        Target(
            Arn=Join("",
                ['arn:aws:codepipeline:',Region,":",AccountId,":",BUILD_NAME]
            ),
            Id='CodePipelineTarget',
            RoleArn = GetAtt(EventRole,"Arn"),
        )
    ]
))

# Show cerated ressources
t.add_output(
    [   
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
                ['arn:aws:codepipeline:',Region,":",AccountId,":",BUILD_NAME]
            )
        ),
        Output(
            "ServiceRoleBuild",
            Description="CodeBuild IAM role",
            Value=GetAtt(CodeBuildServiceRole,"Arn")
        ),
        Output(
            "ServiceRolePipeline",
            Description="CodePipelind IAM role",
            Value=GetAtt(CodePipelineServiceRole,"Arn"),
        ),
        Output(
            "EventRule",
            Description="Cloudwatch Event Rule to trigger CodePipeline",
            Value=GetAtt(EventRule,"Arn")
        )
    ]
)

#print(t.to_json())
print(t.to_yaml())

# Convert Skript to CFN template
# python DockerCICD.py > DockerCICD.yml

# Check template
# aws cloudformation validate-template --template-body file://./DockerCICD.yml

# Deploy template
# aws cloudformation deploy --template-file ./DockerCICD.yml --stack-name my-new-stack --capabilities CAPABILITY_NAMED_IAM

# Check errors
# aws cloudformation describe-stack-events --stack-name my-new-stack

# Delete Stack
# aws cloudformation delete-stack --stack-name my-new-stack

# aws codepipeline retry-stage-execution --pipeline-name my-new-stack-DockerDelivery-13T6KR7HXMNO1 --stage-name Source --pipeline-execution-id 56bd1735-4f81-4621-aa58-f2429f71f259 --retry-mode FAILED_ACTIONS

# aws codepipeline get-job-details --job-id 56bd1735-4f81-4621-aa58-f2429f71f259
