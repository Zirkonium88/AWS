from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_codecommit as _git

with open("./userdata.sh") as f:
    user_data = f.read()


class Ec2DevStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        ################################
        # Parameter section
        ################################

        #===============================
        # Parameter for EC2 Type
        ec2_type = core.CfnParameter(
            self,
            id="EC2_Type",
            description="Enter the instancetype",
            type="String",
            default="t2.micro"
        )

        #===============================
        # Parameter for EC2 Type
        bucket_name = core.CfnParameter(
            self,
            id="Deployment_Bucket_Param",
            description="Enter the instancetype",
            type="String",
            default="431892011317-deployment"
        )

        #===============================
        # Parameter for EC2 Type
        git_name = core.CfnParameter(
            self,
            id="Deployment_Git",
            description="Enter the instancetype",
            type="String",
            default="431892011317-git"
        )

        #===============================
        # Parameter for the instance name
        instance_name = core.CfnParameter(
            self,
            id="Instance_Name",
            description="Enter the instance name",
            type="String",
            default="ApacheWebServer"
        )

        #===============================
        # Parameter for key name
        key_name = core.CfnParameter(
            self,
            id="PEM_Key_Name",
            description="Enter the PEM file name",
            type="String",
            default="demo"
        )

        #===============================
        # Parameter for CIDR
        cidr_local = core.CfnParameter(
            self,
            id="CIDR",
            type="String",
            default="213.61.162.74/32",
            description="Source Ip from local machine"
        )

        ################################
        # Instantiate Dependencies
        ################################

        vpc = _ec2.Vpc.from_lookup(
            self,
            id="WWW-VPC",
            is_default=False,
            vpc_id="vpc-0e4f2f24a48b5d1d6"
        )

        dev_sg = _ec2.SecurityGroup(
            self,
            id="SG_DEV_EC2",
            vpc=vpc,
            security_group_name="Web_DMZ",
            description="SG for Webservers",
            allow_all_outbound=True
        )

        dev_sg.add_ingress_rule(
            peer=_ec2.Peer.ipv4(cidr_ip=cidr_local.value_as_string),
            connection=_ec2.Port.tcp(22),
            description="Allow ssh access"
        )

        dev_sg.add_ingress_rule(
            peer=_ec2.Peer.any_ipv4(),
            connection=_ec2.Port.tcp(80),
            description="Allow http access"
        )

        ami = _ec2.AmazonLinuxImage(
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            user_data=_ec2.UserData.custom(user_data),
            storage=_ec2.AmazonLinuxStorage.GENERAL_PURPOSE
        )
            
        
        ################################
        # S3 and Git
        ################################

        bucket = _s3.Bucket(
            self,
            id="Deployment_Bucket",
            bucket_name=bucket_name.value_as_string
        )

        git = _git.Repository(
            self,
            id="Deployment_Repository",
            repository_name=git_name.value_as_string
        )

        ec2_dev_role = _iam.Role(
            self,
            id="EC2_Dev_Role",
            assumed_by=_iam.ServicePrincipal(service="ec2.amazonaws.com")
        )

        git_policy = _iam.Policy(
            self,
            id="Dev_Instance_Git_Policy",
            policy_name="Dev_Instance_Git_Policy",
            statements=[
                _iam.PolicyStatement(
                    effect=_iam.Effect.ALLOW,
                    actions=[
                        "codecommit:AssociateApprovalRuleTemplateWithRepository",
                        "codecommit:BatchAssociateApprovalRuleTemplateWithRepositories",
                        "codecommit:BatchDisassociateApprovalRuleTemplateFromRepositories",
                        "codecommit:BatchGet*",
                        "codecommit:BatchDescribe*",
                        "codecommit:Create*",
                        "codecommit:DeleteBranch",
                        "codecommit:DeleteFile",
                        "codecommit:Describe*",
                        "codecommit:DisassociateApprovalRuleTemplateFromRepository",
                        "codecommit:EvaluatePullRequestApprovalRules",
                        "codecommit:Get*",
                        "codecommit:List*",
                        "codecommit:Merge*",
                        "codecommit:OverridePullRequestApprovalRules",
                        "codecommit:Put*",
                        "codecommit:Post*",
                        "codecommit:TagResource",
                        "codecommit:Test*",
                        "codecommit:UntagResource",
                        "codecommit:Update*",
                        "codecommit:GitPull",
                        "codecommit:GitPush"
                    ],
                    resources=[
                        git.repository_arn
                    ]
                )
            ]
        )

    
        dev_instance = _ec2.Instance(
            self, 
            id="Dev_EC2",
            vpc=vpc,
            instance_name=instance_name.value_as_string,
            instance_type=_ec2.InstanceType(instance_type_identifier=ec2_type.value_as_string),
            machine_image=ami,
            security_group=dev_sg,
            vpc_subnets=_ec2.SubnetSelection(subnet_type=_ec2.SubnetType.PUBLIC)
        )

        git_policy.attach_to_role(dev_instance.role)
         
        bucket.grant_read_write(dev_instance)
   
        core.CfnOutput(
            self, 
            id="Dev_Instance",
            value=dev_instance.instance_public_dns_name
        )