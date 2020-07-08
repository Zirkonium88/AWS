"""
This module builds the stack for the static website
"""
import aws_cdk.aws_certificatemanager as certificatemanager
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codecommit as codecommit
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_route53_targets as route53_targets
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as _lambda
import aws_cdk.aws_iam as iam

from aws_cdk import core


class CertificateForCloudFrontStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        hosted_zone_id: str,
        hosted_zone_name: str,
        website_domain_name: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            hosted_zone_id=hosted_zone_id,
            zone_name=hosted_zone_name,
        )

        # SSL/TLS Certificate
        tls_cert = certificatemanager.DnsValidatedCertificate(
            self,
            "Certificate",
            hosted_zone=hosted_zone,
            domain_name=website_domain_name,
        )

        # Lambda at Edge for pretty URLs
        lambda_role = iam.Role(
            self,
            id="LambdaRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("lambda"), iam.ServicePrincipal("edgelambda")
            ),
        )

        lambda_at_edge = _lambda.Function(
            self,
            id="LambdaAtEdege",
            code=_lambda.Code.from_asset(path="./src/"),
            handler="index.handler",
            runtime=_lambda.Runtime.NODEJS_10_X,
            memory_size=128,
            role=lambda_role,
        )

        lambda_at_edge.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            )
        )

        core.CfnOutput(self, id="CertificateArn", value=tls_cert.certificate_arn)
        core.CfnOutput(self, id="LambdaArn", value=f"{lambda_at_edge.function_arn}:1")


def check_us_east_1(aws_arn: str):
    """Asserts that we get resource from us-east-1

    Arguments:
        aws_arn: ARN to check.
    """
    assert (
        aws_arn.split(":")[3] == "us-east-1"
    ), "We need a certificate in us-east-1 for CloudFront!"


class StaticWebsiteStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        id: str,
        lambda_at_edege_arn: str,
        hosted_zone_id: str,
        hosted_zone_name: str,
        website_domain_name: str,
        certificate_in_us_east_1_arn: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Raise an exception if we get a certificate that doesn't live in us-east-1
        check_us_east_1(certificate_in_us_east_1_arn)

        # The S3 Bucket that will store our website
        website_bucket = s3.Bucket(self, "WebsiteBucket")

        # The Origin Access Identity is a way to allow CloudFront Access to the Website Bucket
        origin_access_identity = cloudfront.OriginAccessIdentity(
            self, "OriginAccessIdentity", comment="Allows Read-Access from CloudFront"
        )

        # We tell the website bucket to allow access from CloudFront
        website_bucket.grant_read(origin_access_identity)

        # Import the cert from the arn we get as a parameter
        tls_cert = certificatemanager.Certificate.from_certificate_arn(
            self, "Certificate", certificate_arn=certificate_in_us_east_1_arn
        )

        # Raise an exception if we wet a Lambda that doesn't live in us-east-1
        check_us_east_1(lambda_at_edege_arn)

        # Reference Lambda
        # You need to deploy Lambda at Edege manually at the moment.
        # Go to the Lambda Console for this purpose.
        lambda_at_eddege = _lambda.Function.from_function_arn(
            self, id="LambdaAtEdege", function_arn=lambda_at_edege_arn
        )

        # We set up the CloudFront Distribution with the S3 Bucket as the origin and our certificate
        cloudfront_distribution = cloudfront.CloudFrontWebDistribution(
            self,
            "WebsiteDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=website_bucket,
                        origin_access_identity=origin_access_identity,
                    ),
                    behaviors=[
                        cloudfront.Behavior(
                            is_default_behavior=True,
                            lambda_function_associations=[
                                cloudfront.LambdaFunctionAssociation(
                                    event_type=cloudfront.LambdaEdgeEventType.ORIGIN_REQUEST,
                                    lambda_function=lambda_at_eddege,
                                )
                            ],
                            default_ttl=core.Duration.hours(1),
                        )
                    ],
                )
            ],
            error_configurations=[
                # Point CloudFront to our custom 404 error page when a 404 occurs
                cloudfront.CfnDistribution.CustomErrorResponseProperty(
                    error_code=404, response_code=404, response_page_path="/404.html"
                )
            ],
            viewer_certificate=cloudfront.ViewerCertificate.from_acm_certificate(
                certificate=tls_cert, aliases=[website_domain_name]
            ),
        )

        # Set the DNS Alias for CloudFront
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            hosted_zone_id=hosted_zone_id,
            zone_name=hosted_zone_name,
        )

        cloudfront_alias_record = route53.ARecord(
            self,
            "DNSAliasForCloudFront",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(cloudfront_distribution)
            ),
            record_name=website_domain_name,
        )

        # Repo for the website
        repository = codecommit.Repository(
            self,
            "Repository",
            repository_name=website_domain_name,
            description="Repository for the website {}".format(website_domain_name),
        )

        website_build_project = codebuild.PipelineProject(
            self,
            "WebsiteBuild",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_4_0
            ),
            environment_variables={
                "S3_BUCKET": codebuild.BuildEnvironmentVariable(
                    value=website_bucket.bucket_name
                ),
                "CLOUDFRONT_DISTRO_ID": codebuild.BuildEnvironmentVariable(
                    value=cloudfront_distribution.distribution_id
                ),
            },
        )
        website_bucket.grant_read_write(website_build_project.grant_principal)
        website_build_project.add_to_role_policy(
            statement=iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["cloudfront:CreateInvalidation"],
                resources=[
                    "arn:aws:cloudfront::{}:distribution/{}".format(
                        core.Aws.ACCOUNT_ID, cloudfront_distribution.distribution_id
                    )
                ],
            )
        )
        source_output = codepipeline.Artifact()

        website_build_pipeline = codepipeline.Pipeline(
            self,
            "WebsiteBuildPipeline",
            stages=[
                # Check Out the Code From the Repo
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeCommitSourceAction(
                            action_name="CheckoutCode",
                            repository=repository,
                            output=source_output,
                        )
                    ],
                ),
                # Build and deploy the Website to S3 (this uses the sync command with the delete option, which the codebuild action to deploy to S3 doesn't support)
                codepipeline.StageProps(
                    stage_name="BuildAndDeploy",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="BuildAndDeployWebsite",
                            project=website_build_project,
                            input=source_output,
                        )
                    ],
                ),
            ],
        )

        # Display the Repo Clone URLs as the Stack Output
        core.CfnOutput(
            self, id="RepositoryCloneUrlSSH", value=repository.repository_clone_url_ssh
        )
        core.CfnOutput(
            self,
            id="RepositoryCloneUrlHTTPS",
            value=repository.repository_clone_url_http,
        )

        # Display the website URL as the stack output
        core.CfnOutput(
            self, id="WebsiteUrl", value="https://{}/".format(website_domain_name)
        )
