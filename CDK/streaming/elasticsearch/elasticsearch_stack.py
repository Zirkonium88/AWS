from aws_cdk import core
from aws_cdk import aws_elasticsearch as es

class ElasticSearchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        es_domain = es.CfnDomain(
            self,
            id="IoT_Demo_ES_Cluster",
            domain_name="iot-demo-trcmw-2020-02",
            elasticsearch_version="7.1",
            elasticsearch_cluster_config={
                "dedicatedMasterEnabled":True,
                "instanceCount":1,
                "zoneAwarenessEnabled":False, # = 1 Az
                "instanceType":"t2.medium.elasticsearch"                
            },
            ebs_options={
                "ebsEnabled":True,
                "iops":0,
                "volumeSize":10, # not smaller than 10
                "volumeType":"gp2"
            },
            snapshot_options={
                "automatedSnapshotStartHour":0
            },
            advanced_options={
                "rest.action.multi.allow_explicit_index":"true"
            },
            access_policies={
                "Version": "2012-10-17",
                "Statement": [
                    {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                        "*"
                        ]
                    },
                    "Action": [
                        "es:*"
                    ],
                    "Resource": "*"
                    }
                ]
            }
        )

        # We assign the doamins's arn and name to a local variable for the Object.
        self._es_domain_arn = es_domain.attr_arn
        self._es_endpoint = es_domain.attr_domain_endpoint

    # Using the property decorator to export value delivery_arn
    @property
    def main_es_props(self):
        return self._es_domain_arn, self._es_endpoint