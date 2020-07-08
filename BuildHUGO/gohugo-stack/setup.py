import setuptools

CDK_VERSION = "1.49.1"

with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cdk_stack",
    version="0.0.1",
    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "cdk_stack"},
    packages=setuptools.find_packages(where="cdk_stack"),
    install_requires=[
        f"aws-cdk.core=={CDK_VERSION}",
        f"aws-cdk.aws-s3=={CDK_VERSION}",
        f"aws-cdk.aws-certificatemanager=={CDK_VERSION}",
        f"aws-cdk.aws-cloudfront=={CDK_VERSION}",
        f"aws-cdk.aws-route53-targets=={CDK_VERSION}",
        f"aws-cdk.aws-codecommit=={CDK_VERSION}",
        f"aws-cdk.aws-codebuild=={CDK_VERSION}",
        f"aws-cdk.aws-codepipeline=={CDK_VERSION}",
        f"aws-cdk.aws-codepipeline-actions=={CDK_VERSION}",
        f"aws-cdk.aws-ssm=={CDK_VERSION}",
        f"aws-cdk.aws-iam=={CDK_VERSION}",
        git - remote - codecommit,
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
