#!/usr/bin/env python3

from aws_cdk import core

from cdk_stack.cdk_stack import StaticWebsiteStack, CertificateForCloudFrontStack


app = core.App()

HOSTED_ZONE_ID = "YOUR_HOSTED_ZONE_ID"
HOSTED_ZONE_NAME = "YOUR_HOSTED_ZONE_NAME"
WEBSITE_DOMAIN_NAME = "YOUR_WEBSITE_DOMAIN_NAME"

# Insert the value for the certificate stack here
CLOUDFRONT_CERTIFICATE_ARN = "YOUR_CLOUDFRONT_CERTIFICATE_ARN"
PRETTY_URL_LAMBDA_VERSION_ARN = "YOUR_PRETTY_URL_LAMBDA_VERSION_ARN"

us_east_1 = core.Environment(region="us-east-1")
eu_central_1 = core.Environment(region="eu-central-1")

certificate_stack = CertificateForCloudFrontStack(
    app,
    "certificate-stack",
    hosted_zone_id=HOSTED_ZONE_ID,
    hosted_zone_name=HOSTED_ZONE_NAME,
    website_domain_name=WEBSITE_DOMAIN_NAME,
    env=us_east_1,
)

static_website_stack = StaticWebsiteStack(
    app,
    "www-stack",
    hosted_zone_id=HOSTED_ZONE_ID,
    hosted_zone_name=HOSTED_ZONE_NAME,
    website_domain_name=WEBSITE_DOMAIN_NAME,
    certificate_in_us_east_1_arn=CLOUDFRONT_CERTIFICATE_ARN,
    lambda_at_edege_arn=PRETTY_URL_LAMBDA_VERSION_ARN,
    env=eu_central_1,
)

static_website_stack.add_dependency(
    certificate_stack, reason="The certificate needs to exist in US-EAST-1!"
)

app.synth()
