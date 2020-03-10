from aws_cdk import core
from aws_cdk import aws_iot as iot
from aws_cdk import aws_iam as iam
from aws_cdk import aws_kinesisfirehose as firehose


# IoT Topic Name
TOPIC_NAME = "IoT_TOPIC/recieve"

# Cloudformation cannot produce certificates for IoT Devices
CERTIFICATE ="arn:aws:iot:eu-central-1:037732949416:cert/437531efdb9b66ad7f36e7aa6a541984e55b896a8e3572a9b875f5dc7f9ab0df"

class IoTStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, delivery_stream_name: str, delivery_stream_arn: str, es_domain_name: str, es_domain_arn: str,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # IAM Role for IoT Topic Rule
        iot_topic_role_firehose = iam.Role(
            self,
            id="IoT_Topic_Role_Firehose",
            assumed_by=iam.ServicePrincipal(
                service="iot.amazonaws.com"
            )
        )

        iot_topic_role_es = iam.Role(
            self,
            id="IoT_Topic_Role_ES",
            assumed_by=iam.ServicePrincipal(
                service="iot.amazonaws.com"
            )
        )

        iot_topic_policy_firehose = iam.Policy(
            self,
            id="IoT_Topic_Policy_Firehose",
            policy_name="IoT_Topic_Policy_Firehose",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "firehose:PutRecord"
                    ],
                    resources=[
                        delivery_stream_arn
                    ]
                )
            ]  
        )

        iot_topic_policy_firehose.attach_to_role(iot_topic_role_firehose)

        iot_topic_policy_es = iam.Policy(
            self,
            id="IoT_Topic_Policy_ES",
            policy_name="IoT_Topic_Policy_ES",
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "es:ESHttpPut",
                    ],
                    resources=[
                        es_domain_arn+"/*"
                    ]
                )
            ]  
        )

        iot_topic_policy_es.attach_to_role(iot_topic_role_es)

        # IoT Thing
        thing = iot.CfnThing(
            self,
            id="IoT_Demo",
            thing_name="IoT_Demo"
        )

        # IoT Thing Policy
        policy = iot.CfnPolicy(
            self,
            id="Thing_Policy",
            policy_name="Connection_Policy",
            policy_document={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "iot:*",
                        "Resource": "*"
                    }
                ]
            },
        )

        # Connect Policy with Certificate
        principal_policy = iot.CfnPolicyPrincipalAttachment(
            self,
            id="Policy_Principal",
            policy_name=policy.policy_name,
            principal=CERTIFICATE
        )

        principal_policy.add_depends_on(thing)        

        # Connect IoT Thing with Certificate
        principal_thing = iot.CfnThingPrincipalAttachment(
            self,
            id="Thing_Principal",
            thing_name=thing.thing_name,
            principal=CERTIFICATE
        )

        principal_thing.add_depends_on(thing)

        # IoT Rule
        iot_rule = iot.CfnTopicRule(
            self,
            id="Iot_Demo_Topic_Rule",
            rule_name="Iot_Demo_Topic_Rule",
            topic_rule_payload={
                "ruleDisabled": False,
                "sql": "SELECT * FROM '{}'".format(TOPIC_NAME),
                "actions":[              
                    {
                        "firehose": {
                            "deliveryStreamName": delivery_stream_name,
                            "roleArn" : iot_topic_role_firehose.role_arn,
                            "separator" : "\n"
                        },
                    },
                    {
                        "elasticsearch": {
                            "endpoint": "https://"+es_domain_name,
                            "id": "${newuuid()}",
                            "index": "fanids",
                            "roleArn": iot_topic_role_es.role_arn,
                            "type" : "fanid"
                        },
                    },
                ]
            } 
        )

        # We assign the doamins's arn and name to a local variable for the Object.
        self._es_url = "https://"+es_domain_name+"/_plugin/kibana/"

    # Using the property decorator to export value delivery_arn
    @property
    def main_es_doamin(self):
        return self._es_url
