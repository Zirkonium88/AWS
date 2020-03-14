from aws_cdk import core
from aws_cdk import aws_appsync as _appsync
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_apigateway as _api
from aws_cdk import aws_cloudfront as _cf
from aws_cdk import aws_cognito as _cognito
from aws_cdk import aws_route53 as _r53
from aws_cdk import aws_route53_targets as _r53targets
from aws_cdk import aws_certificatemanager as _acm
from aws_cdk import aws_dynamodb as _dynamodb

class CdkVersionStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ################################################################
        # Input Parameter 
        ################################################################

        #===============================
        # Parameter for SSL
        acm_cf = core.CfnParameter(
            self,
            id="ACM_ARN_us",
            description="Enter the ARN of the correct ACM Certificate",
            type="String",
            default="arn:aws:acm:us-east-1:037732949416:certificate/b3ab7ca6-7203-431a-82bb-d5d8dc1b0a29"
        )

        acm_api = core.CfnParameter(
            self,
            id="ACM_ARN_eu",
            description="Enter the ARN of the correct ACM Certificate",
            type="String",
            default="arn:aws:acm:eu-central-1:037732949416:certificate/2a6b1b0b-a484-42a1-8298-3c124a2a0d15"
        )
        
        #===============================
        # Input Parameter for the url --> bucket needs to have the same name

        url_name = core.CfnParameter(
            self,
            id="URL_Name",
            description="Enter the name the URL you want to use",
            type="String",
            default="user.trctrainings.com"
        )

        prefix = core.CfnParameter(
            self,
            id="URL_Prefix",
            description="Enter the name the URL-Repfix you want to use",
            type="String",
            default="user"
        )

        #===============================
        # Input Parameter for the auth domain
        auth_domain = core.CfnParameter(
            self,
            id="Auth_Name",
            description="Enter the name for auth domain",
            type="String",
            default="auth-trctrainings"
        )

        ################################################################
        # Static Website Bucket with CORS
        ################################################################
 
        bucket = _s3.Bucket(
            self, 
            "Create_User_Frontend",
            bucket_name=url_name.value_as_string,
            website_index_document="index.html",
        )

        bucket.add_cors_rule(
            allowed_origins=["*"],
            allowed_methods=[
                _s3.HttpMethods.HEAD,
                _s3.HttpMethods.GET,
                _s3.HttpMethods.POST,
            ],
            allowed_headers=["*"],
        )

        ################################################################
        # Cloudfront Distribution and Origin Access
        ################################################################

        cf_origin_access = _cf.OriginAccessIdentity(
            self,
            id="CF_Origin_Access",
            comment="Allows CloudFront to reach to the bucket!"
        )

        cf_distribution = _cf.CloudFrontWebDistribution(
            self, 
            "CF_Create_User_Frontend",
            origin_configs=[
                _cf.SourceConfiguration(
                    s3_origin_source=_cf.S3OriginConfig(
                        s3_bucket_source=bucket,
                        origin_access_identity=cf_origin_access
                    ),
                    behaviors=[_cf.Behavior(is_default_behavior=True)]
                )   
            ],
            default_root_object="index.html",
            viewer_certificate=_cf.ViewerCertificate.from_acm_certificate(
                certificate=_acm.Certificate.from_certificate_arn(
                    self,
                    id="Imported_ACM_us",
                    certificate_arn=acm_cf.value_as_string
                ),
                aliases=[url_name.value_as_string]
            )            
        )

        ################################################################
        # Apply Bucket Policy
        ################################################################

        bucket.grant_read(cf_origin_access)

        ################################################################
        # DNS Settings
        ################################################################
        
        #================================================================
        # Use a preexisting one

        cf_alias = _r53targets.CloudFrontTarget(cf_distribution)

        hosted_zone = _r53.HostedZone.from_hosted_zone_attributes(
            self,
            id="Prexisting_HostedZone",
            zone_name="trctrainings.com",
            hosted_zone_id="Z3PP6TVU71INFN"
        )

        cf_target = _r53.RecordTarget.from_alias(cf_alias)

        a_record = _r53.ARecord(
            self,
            id="A_Record_Hosted_Zone_Create_User",
            zone=hosted_zone,
            target=cf_target,
            record_name=prefix.value_as_string
        )
    
        ################################################################
        # Cognito User Pool
        ################################################################

        user_pool = _cognito.UserPool(
            self,
            id="Create_Admin_User_Pool",
            user_pool_name="Create_Admin_User_Pool",
            sign_in_aliases=_cognito.SignInAliases.email
        )
        
        # #===============================
        # # Optional: This grouping ca be used to seprated permissions; 
        # user_group_admin = _cognito.CfnUserPoolGroup(
        #     self,
        #     id="Admin_User",
        #     user_pool_id=user_pool.user_pool_id,
        #     user_group_name="Netatwork_Windows_Admin"
        # )

        # user_group_3rd = _cognito.CfnUserPoolGroup(
        #     self,
        #     id="3rd_User",
        #     user_pool_id=user_pool.user_pool_id,
        #     user_group_name="3rd_Windows_Admin"
        # )

        #===============================

        #================================================================
        # Cognito App Client

        user_pool_app_client = _cognito.CfnUserPoolClient(
            self,
            id="User_Pool_App_Client",
            user_pool_id=user_pool.user_pool_id,
            supported_identity_providers=['COGNITO',user_identity_provider.provider_name],
            generate_secret=False,
            client_name="User_Pool_App_Client",
            allowed_o_auth_flows_user_pool_client=True,
            allowed_o_auth_scopes=["openid"],
            allowed_o_auth_flows=["code"],
            refresh_token_validity=1,
            callback_ur_ls=["https://"+url_name.value_as_string+"/"]
        )

        user_pool_app_client.add_depends_on(user_identity_provider)

        #================================================================
        # Cognito Auth Domain

        user_pool_auth_domain = _cognito.CfnUserPoolDomain(
            self,
            id="User_Pool_Atuh_Domain",
            domain=auth_domain.value_as_string,
            user_pool_id=user_pool.user_pool_id
        )

        ################################################################
        # DynamDB
        ################################################################

        items_table = _dynamodb.Table(
            self, 'ItemsTable',
            table_name=table_name,
            partition_key=Attribute(
                name=f'{table_name}Id',
                type=AttributeType.STRING
            ),
            billing_mode=_dynamodb.BillingMode.PAY_PER_REQUEST,
            stream=_dynamodb.StreamViewType.NEW_IMAGE,

            # The default removal policy is RETAIN, which means that cdk
            # destroy will not attempt to delete the new table, and it will
            # remain in your account until manually deleted. By setting the
            # policy to DESTROY, cdk destroy will delete the table (even if it
            # has data in it)
            removal_policy=core.RemovalPolicy.DESTROY # NOT recommended for production code
        )

        items_table_role = _iam.Role(
            self, 'ItemsDynamoDBRole',
            assumed_by=ServicePrincipal('appsync.amazonaws.com')
        )

        items_table_role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
            )
        )

        ################################################################
        # GrapQL API
        ################################################################ 
         
        items_graphql_api = _appsync.CfnGraphQLApi(
            self, 'ItemsApi',
            name='items-api',
            authentication_type='API_KEY'
        )

        _appsync.CfnApiKey(
            self, 'ItemsApiKey',
            api_id=items_graphql_api.attr_api_id
        )

        api_schema = _appsync.CfnGraphQLSchema(
            self, 'ItemsSchema',
            api_id=items_graphql_api.attr_api_id,
            definition=f"""\
                type {table_name} {{
                    {table_name}Id: ID!
                    name: String
                }}
                type Paginated{table_name} {{
                    items: [{table_name}!]!
                    nextToken: String
                }}
                type Query {{
                    all(limit: Int, nextToken: String): Paginated{table_name}!
                    getOne({table_name}Id: ID!): {table_name}
                }}
                type Mutation {{
                    save(name: String!): {table_name}
                    delete({table_name}Id: ID!): {table_name}
                }}
                type Schema {{
                    query: Query
                    mutation: Mutation
                }}"""
        )

        
        data_source = _appsync.CfnDataSource(
            self, 'ItemsDataSource',
            api_id=items_graphql_api.attr_api_id,
            name='ItemsDynamoDataSource',
            type='AMAZON_DYNAMODB',
            dynamo_db_config=CfnDataSource.DynamoDBConfigProperty(
                table_name=items_table.table_name,
                aws_region=self.region
            ),
            service_role_arn=items_table_role.role_arn
        )

        get_one_resolver = _appsync.CfnResolver(
            self, 'GetOneQueryResolver',
            api_id=items_graphql_api.attr_api_id,
            type_name='Query',
            field_name='getOne',
            data_source_name=data_source.name,
            request_mapping_template=f"""\
            {{
                "version": "2017-02-28",
                "operation": "GetItem",
                "key": {{
                "{table_name}Id": $util.dynamodb.toDynamoDBJson($ctx.args.{table_name}Id)
                }}
            }}""",
            response_mapping_template="$util.toJson($ctx.result)"
        )

        get_one_resolver.add_depends_on(api_schema)

        get_all_resolver = _appsync.CfnResolver(
            self, 'GetAllQueryResolver',
            api_id=items_graphql_api.attr_api_id,
            type_name='Query',
            field_name='all',
            data_source_name=data_source.name,
            request_mapping_template=f"""\
            {{
                "version": "2017-02-28",
                "operation": "Scan",
                "limit": $util.defaultIfNull($ctx.args.limit, 20),
                "nextToken": $util.toJson($util.defaultIfNullOrEmpty($ctx.args.nextToken, null))
            }}""",
            response_mapping_template="$util.toJson($ctx.result)"
        )

        get_all_resolver.add_depends_on(api_schema)

        save_resolver = _appsync.CfnResolver(
            self, 'SaveMutationResolver',
            api_id=items_graphql_api.attr_api_id,
            type_name='Mutation',
            field_name='save',
            data_source_name=data_source.name,
            request_mapping_template=f"""\
            {{
                "version": "2017-02-28",
                "operation": "PutItem",
                "key": {{
                    "{table_name}Id": {{ "S": "$util.autoId()" }}
                }},
                "attributeValues": {{
                    "name": $util.dynamodb.toDynamoDBJson($ctx.args.name)
                }}
            }}""",
            response_mapping_template="$util.toJson($ctx.result)"
        )

        save_resolver.add_depends_on(api_schema)

        delete_resolver = _appsync.CfnResolver(
            self, 'DeleteMutationResolver',
            api_id=items_graphql_api.attr_api_id,
            type_name='Mutation',
            field_name='delete',
            data_source_name=data_source.name,
            request_mapping_template=f"""\
            {{
                "version": "2017-02-28",
                "operation": "DeleteItem",
                "key": {{
                "{table_name}Id": $util.dynamodb.toDynamoDBJson($ctx.args.{table_name}Id)
                }}
            }}""",
            response_mapping_template="$util.toJson($ctx.result)"
        )

        delete_resolver.add_depends_on(api_schema)