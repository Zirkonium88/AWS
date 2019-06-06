# Deploy your trainings website
# This template does not genrate a Route 53 domain oir a Cloudfront distribution!

import awacs.aws
import awacs.codebuild as cb
import awacs.codecommit as cm
import awacs.codepipeline as cp
from awacs.aws import Action, Allow, AWSPrincipal, Principal, Statement
from awacs.sts import AssumeRole
from troposphere import (AccountId, GetAtt, Join, Output, Parameter, Ref,
                         Region, Template)
from troposphere.codebuild import (Artifacts, Environment, Project,
                                   ProjectCache, Source)
from troposphere.codecommit import Repository, Trigger
from troposphere.codepipeline import (Actions, ActionTypeId, ArtifactStore,
                                      InputArtifacts, OutputArtifacts,
                                      Pipeline, Stages)
from troposphere.events import Rule, Target
from troposphere.iam import Policy, Role
from troposphere.s3 import Bucket, BucketPolicy, WebsiteConfiguration

PIPELINE_NAME = "TrainingsHomepageCICD"
PROJECT_NAME = "TrainingsHomepageProject"
BUILD_NAME = "TrainingsHomepageBuild"
ARTIFACT_BUCKET = "buildartifactsbucket"
WEBSITE_BUCKET = "awstrainingsbytecracer"
GIT_REPO = "TrainingsHomepage"
BRANCH_NAME = "master"
IAM_VERSION = "2012-10-17"
CFN_VERSION = "2010-09-09"

t = Template()
t.add_version(CFN_VERSION)

# Generate the bucket for storing build artifacts
WebsiteBucket = t.add_resource(Bucket(
    WEBSITE_BUCKET,
    AccessControl="PublicRead",
    WebsiteConfiguration=WebsiteConfiguration(
        IndexDocument="index.html",
        ErrorDocument="404.html"
    )
))

# Generate the bucketpolicy to allow user to access your static website
BucketPolicyStaticWebsite = t.add_resource(BucketPolicy(
    "BucketPolicyStaticWebsite",
    PolicyDocument={
        "Version": IAM_VERSION,
        "Statement": [
            {
                "Sid": "ReadOnly",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource":[
                    Join("", [
                        GetAtt(WebsiteBucket, "Arn"),
                        "/*"
                    ]
                    )
                ]
            }
        ]
    },
    Bucket=Ref(WebsiteBucket),
))

# Generate the bucket for storing build artifacts
BuildArtifacts = t.add_resource(Bucket(
    ARTIFACT_BUCKET
))


# Generate the codecommit repository
CodeCommit = t.add_resource(Repository(
    GIT_REPO,
    RepositoryName=GIT_REPO
))

# Generate the service policy and the service role for CodeBuild
CodeBuildServiceRole = t.add_resource(Role(
    "CodeBuildServiceRole",
    AssumeRolePolicyDocument=awacs.aws.Policy(
        Version=IAM_VERSION,
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
                Version=IAM_VERSION,
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
                            GetAtt(BuildArtifacts, "Arn"),
                            Join(
                                "/",
                                [GetAtt(BuildArtifacts, "Arn"), '*']
                            ),
                            GetAtt(WebsiteBucket, "Arn"),
                            Join(
                                "/",
                                [GetAtt(WebsiteBucket, "Arn"), '*']
                            )
                        ],
                    ),
                ],
            )
        ),
        Policy(
            PolicyName="WorkWithLogs",
            PolicyDocument=awacs.aws.Policy(
                Version=IAM_VERSION,
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
            PolicyName="WorkWithCloudfront",
            PolicyDocument=awacs.aws.Policy(
                Version=IAM_VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("cloudfront", "CreateInvalidation")
                        ],
                        Resource=["*"],
                    ),
                ],
            )
        )
    ]
))

# Generate the build porject
CodeBuildProject = t.add_resource(Project(
    BUILD_NAME,
    TimeoutInMinutes=60,
    Artifacts=Artifacts(
        Type='CODEPIPELINE'
    ),
    Cache=ProjectCache(
        Type='NO_CACHE'
    ),
    Environment=Environment(
        ComputeType='BUILD_GENERAL1_SMALL',
        Image='aws/codebuild/ubuntu-base:14.04',
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
        Version=IAM_VERSION,
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
                Version=IAM_VERSION,
                Statement=[
                    awacs.aws.Statement(
                        Effect=Allow,
                        Action=[
                            Action("iam", "PassRole"),
                            Action("codebuild", "BatchGetBuilds"),
                            Action("codebuild", "StartBuild"),
                            Action("codecommit", "CancelUploadArchive"),
                            Action("codecommit", "GetBranch"),
                            Action("codecommit", "GetUploadArchiveStatus"),
                            Action("codecommit", "GetCommit"),
                            Action("s3", "GetObject"),
                            Action("s3", "PutObject"),
                            Action("s3", "GetBucketAcl"),
                            Action("s3", "ListBucket"),
                            Action("s3", "GetBucketLocation"),
                            Action("s3", "GetObjectVersion"),
                            Action("codecommit", "UploadArchive"),
                        ],
                        Resource=['*']
                    )
                ],
            ),
        )
    ],
    Path='/'
))

# Generate the CICD pipeline
CodePipeline = t.add_resource(Pipeline(
    PIPELINE_NAME,
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
                        Provider="CodeCommit"
                    ),
                    OutputArtifacts=[
                        OutputArtifacts(
                            Name="SourceArtifact"
                        )
                    ],
                    Configuration={
                        "PollForSourceChanges": 'false',
                        "BranchName": BRANCH_NAME,
                        "RepositoryName": GIT_REPO,
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
    "StaticWebsiteEventRole",
    AssumeRolePolicyDocument=awacs.aws.Policy(
        Version=IAM_VERSION,
        Statement=[
            awacs.aws.Statement(
                Effect=Allow,
                Action=[Action("sts", "AssumeRole")],
                Principal=Principal("Service", ["events.amazonaws.com"])
            )
        ]
    ),
    Path="/",
    Policies=[
        Policy(
            PolicyName="cwe-pipeline-execution",
            PolicyDocument=awacs.aws.Policy(
                Version=IAM_VERSION,
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
    "StaticWebsiteEventRule",
    Name='codepipeline-StaticWebsiteEventRule',
    State='ENABLED',
    Description='Amazon CloudWatch Events rule to automatically start your pipeline when a change occurs in CodeCommit',
    EventPattern={
        "source": [
                "aws.codecommit"
        ],
        "detail-type": [
            "CodeCommit Repository State Change"
        ],
        "resources": [
            GetAtt(CodeCommit, "Arn")
        ],
        "detail": {
            "event": [
                "referenceCreated",
                "referenceUpdated"
            ],
            "referenceType": [
                "branch"
            ],
            "referenceName": [
                "master"
            ]
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

# Show cerated ressources
t.add_output([
    Output(
        "WebsiteURL",
        Value=GetAtt(WebsiteBucket, "WebsiteURL"),
        Description="URL for website hosted on S3"
    ),
    Output(
        "S3BucketSecureURL",
        Value=Join("", ["http://", GetAtt(WebsiteBucket, "DomainName")]),
        Description="Name of S3 bucket to hold website content"
    ),
])

# print(t.to_json())
print(t.to_yaml())

# Convert Skript to CFN template
# python DockerCICD.py > GoHugo.yml

# Check template
# aws cloudformation validate-template --template-body file://./GoHugo.yml

# Deploy template
# aws cloudformation deploy --template-file ./GoHugo.yml --stack-name my-aws-trainings-hp --capabilities CAPABILITY_NAMED_IAM

# Check errors
# aws cloudformation describe-stack-events --stack-name my-aws-trainings-hp

# Delete Stack
# aws cloudformation delete-stack --stack-name my-aws-trainings-hp
