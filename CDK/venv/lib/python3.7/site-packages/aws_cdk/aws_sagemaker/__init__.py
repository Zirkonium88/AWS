"""
## Amazon SageMaker Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
sagemaker = require("@aws-cdk/aws-sagemaker")
```
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sagemaker", "1.18.0", __name__, "aws-sagemaker@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.core.IInspectable)
class CfnCodeRepository(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnCodeRepository"):
    """A CloudFormation ``AWS::SageMaker::CodeRepository``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::CodeRepository
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, git_config: typing.Union["GitConfigProperty", aws_cdk.core.IResolvable], code_repository_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SageMaker::CodeRepository``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param git_config: ``AWS::SageMaker::CodeRepository.GitConfig``.
        :param code_repository_name: ``AWS::SageMaker::CodeRepository.CodeRepositoryName``.
        """
        props = CfnCodeRepositoryProps(git_config=git_config, code_repository_name=code_repository_name)

        jsii.create(CfnCodeRepository, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrCodeRepositoryName")
    def attr_code_repository_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CodeRepositoryName
        """
        return jsii.get(self, "attrCodeRepositoryName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="gitConfig")
    def git_config(self) -> typing.Union["GitConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::SageMaker::CodeRepository.GitConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html#cfn-sagemaker-coderepository-gitconfig
        """
        return jsii.get(self, "gitConfig")

    @git_config.setter
    def git_config(self, value: typing.Union["GitConfigProperty", aws_cdk.core.IResolvable]):
        return jsii.set(self, "gitConfig", value)

    @property
    @jsii.member(jsii_name="codeRepositoryName")
    def code_repository_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::CodeRepository.CodeRepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html#cfn-sagemaker-coderepository-coderepositoryname
        """
        return jsii.get(self, "codeRepositoryName")

    @code_repository_name.setter
    def code_repository_name(self, value: typing.Optional[str]):
        return jsii.set(self, "codeRepositoryName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnCodeRepository.GitConfigProperty", jsii_struct_bases=[], name_mapping={'repository_url': 'repositoryUrl', 'branch': 'branch', 'secret_arn': 'secretArn'})
    class GitConfigProperty():
        def __init__(self, *, repository_url: str, branch: typing.Optional[str]=None, secret_arn: typing.Optional[str]=None):
            """
            :param repository_url: ``CfnCodeRepository.GitConfigProperty.RepositoryUrl``.
            :param branch: ``CfnCodeRepository.GitConfigProperty.Branch``.
            :param secret_arn: ``CfnCodeRepository.GitConfigProperty.SecretArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-coderepository-gitconfig.html
            """
            self._values = {
                'repository_url': repository_url,
            }
            if branch is not None: self._values["branch"] = branch
            if secret_arn is not None: self._values["secret_arn"] = secret_arn

        @property
        def repository_url(self) -> str:
            """``CfnCodeRepository.GitConfigProperty.RepositoryUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-coderepository-gitconfig.html#cfn-sagemaker-coderepository-gitconfig-repositoryurl
            """
            return self._values.get('repository_url')

        @property
        def branch(self) -> typing.Optional[str]:
            """``CfnCodeRepository.GitConfigProperty.Branch``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-coderepository-gitconfig.html#cfn-sagemaker-coderepository-gitconfig-branch
            """
            return self._values.get('branch')

        @property
        def secret_arn(self) -> typing.Optional[str]:
            """``CfnCodeRepository.GitConfigProperty.SecretArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-coderepository-gitconfig.html#cfn-sagemaker-coderepository-gitconfig-secretarn
            """
            return self._values.get('secret_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GitConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnCodeRepositoryProps", jsii_struct_bases=[], name_mapping={'git_config': 'gitConfig', 'code_repository_name': 'codeRepositoryName'})
class CfnCodeRepositoryProps():
    def __init__(self, *, git_config: typing.Union["CfnCodeRepository.GitConfigProperty", aws_cdk.core.IResolvable], code_repository_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::SageMaker::CodeRepository``.

        :param git_config: ``AWS::SageMaker::CodeRepository.GitConfig``.
        :param code_repository_name: ``AWS::SageMaker::CodeRepository.CodeRepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html
        """
        self._values = {
            'git_config': git_config,
        }
        if code_repository_name is not None: self._values["code_repository_name"] = code_repository_name

    @property
    def git_config(self) -> typing.Union["CfnCodeRepository.GitConfigProperty", aws_cdk.core.IResolvable]:
        """``AWS::SageMaker::CodeRepository.GitConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html#cfn-sagemaker-coderepository-gitconfig
        """
        return self._values.get('git_config')

    @property
    def code_repository_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::CodeRepository.CodeRepositoryName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-coderepository.html#cfn-sagemaker-coderepository-coderepositoryname
        """
        return self._values.get('code_repository_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCodeRepositoryProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpoint(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnEndpoint"):
    """A CloudFormation ``AWS::SageMaker::Endpoint``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::Endpoint
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, endpoint_config_name: str, endpoint_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::SageMaker::Endpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param endpoint_config_name: ``AWS::SageMaker::Endpoint.EndpointConfigName``.
        :param endpoint_name: ``AWS::SageMaker::Endpoint.EndpointName``.
        :param tags: ``AWS::SageMaker::Endpoint.Tags``.
        """
        props = CfnEndpointProps(endpoint_config_name=endpoint_config_name, endpoint_name=endpoint_name, tags=tags)

        jsii.create(CfnEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrEndpointName")
    def attr_endpoint_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EndpointName
        """
        return jsii.get(self, "attrEndpointName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SageMaker::Endpoint.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="endpointConfigName")
    def endpoint_config_name(self) -> str:
        """``AWS::SageMaker::Endpoint.EndpointConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-endpointconfigname
        """
        return jsii.get(self, "endpointConfigName")

    @endpoint_config_name.setter
    def endpoint_config_name(self, value: str):
        return jsii.set(self, "endpointConfigName", value)

    @property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Endpoint.EndpointName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-endpointname
        """
        return jsii.get(self, "endpointName")

    @endpoint_name.setter
    def endpoint_name(self, value: typing.Optional[str]):
        return jsii.set(self, "endpointName", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnEndpointConfig(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfig"):
    """A CloudFormation ``AWS::SageMaker::EndpointConfig``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::EndpointConfig
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, production_variants: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ProductionVariantProperty"]]], endpoint_config_name: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None) -> None:
        """Create a new ``AWS::SageMaker::EndpointConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param production_variants: ``AWS::SageMaker::EndpointConfig.ProductionVariants``.
        :param endpoint_config_name: ``AWS::SageMaker::EndpointConfig.EndpointConfigName``.
        :param kms_key_id: ``AWS::SageMaker::EndpointConfig.KmsKeyId``.
        :param tags: ``AWS::SageMaker::EndpointConfig.Tags``.
        """
        props = CfnEndpointConfigProps(production_variants=production_variants, endpoint_config_name=endpoint_config_name, kms_key_id=kms_key_id, tags=tags)

        jsii.create(CfnEndpointConfig, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrEndpointConfigName")
    def attr_endpoint_config_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EndpointConfigName
        """
        return jsii.get(self, "attrEndpointConfigName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SageMaker::EndpointConfig.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="productionVariants")
    def production_variants(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ProductionVariantProperty"]]]:
        """``AWS::SageMaker::EndpointConfig.ProductionVariants``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-productionvariants
        """
        return jsii.get(self, "productionVariants")

    @production_variants.setter
    def production_variants(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ProductionVariantProperty"]]]):
        return jsii.set(self, "productionVariants", value)

    @property
    @jsii.member(jsii_name="endpointConfigName")
    def endpoint_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::EndpointConfig.EndpointConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-endpointconfigname
        """
        return jsii.get(self, "endpointConfigName")

    @endpoint_config_name.setter
    def endpoint_config_name(self, value: typing.Optional[str]):
        return jsii.set(self, "endpointConfigName", value)

    @property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::EndpointConfig.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]):
        return jsii.set(self, "kmsKeyId", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfig.ProductionVariantProperty", jsii_struct_bases=[], name_mapping={'initial_instance_count': 'initialInstanceCount', 'initial_variant_weight': 'initialVariantWeight', 'instance_type': 'instanceType', 'model_name': 'modelName', 'variant_name': 'variantName', 'accelerator_type': 'acceleratorType'})
    class ProductionVariantProperty():
        def __init__(self, *, initial_instance_count: jsii.Number, initial_variant_weight: jsii.Number, instance_type: str, model_name: str, variant_name: str, accelerator_type: typing.Optional[str]=None):
            """
            :param initial_instance_count: ``CfnEndpointConfig.ProductionVariantProperty.InitialInstanceCount``.
            :param initial_variant_weight: ``CfnEndpointConfig.ProductionVariantProperty.InitialVariantWeight``.
            :param instance_type: ``CfnEndpointConfig.ProductionVariantProperty.InstanceType``.
            :param model_name: ``CfnEndpointConfig.ProductionVariantProperty.ModelName``.
            :param variant_name: ``CfnEndpointConfig.ProductionVariantProperty.VariantName``.
            :param accelerator_type: ``CfnEndpointConfig.ProductionVariantProperty.AcceleratorType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html
            """
            self._values = {
                'initial_instance_count': initial_instance_count,
                'initial_variant_weight': initial_variant_weight,
                'instance_type': instance_type,
                'model_name': model_name,
                'variant_name': variant_name,
            }
            if accelerator_type is not None: self._values["accelerator_type"] = accelerator_type

        @property
        def initial_instance_count(self) -> jsii.Number:
            """``CfnEndpointConfig.ProductionVariantProperty.InitialInstanceCount``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-initialinstancecount
            """
            return self._values.get('initial_instance_count')

        @property
        def initial_variant_weight(self) -> jsii.Number:
            """``CfnEndpointConfig.ProductionVariantProperty.InitialVariantWeight``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-initialvariantweight
            """
            return self._values.get('initial_variant_weight')

        @property
        def instance_type(self) -> str:
            """``CfnEndpointConfig.ProductionVariantProperty.InstanceType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-instancetype
            """
            return self._values.get('instance_type')

        @property
        def model_name(self) -> str:
            """``CfnEndpointConfig.ProductionVariantProperty.ModelName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-modelname
            """
            return self._values.get('model_name')

        @property
        def variant_name(self) -> str:
            """``CfnEndpointConfig.ProductionVariantProperty.VariantName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-variantname
            """
            return self._values.get('variant_name')

        @property
        def accelerator_type(self) -> typing.Optional[str]:
            """``CfnEndpointConfig.ProductionVariantProperty.AcceleratorType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-endpointconfig-productionvariant.html#cfn-sagemaker-endpointconfig-productionvariant-acceleratortype
            """
            return self._values.get('accelerator_type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ProductionVariantProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointConfigProps", jsii_struct_bases=[], name_mapping={'production_variants': 'productionVariants', 'endpoint_config_name': 'endpointConfigName', 'kms_key_id': 'kmsKeyId', 'tags': 'tags'})
class CfnEndpointConfigProps():
    def __init__(self, *, production_variants: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointConfig.ProductionVariantProperty"]]], endpoint_config_name: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::SageMaker::EndpointConfig``.

        :param production_variants: ``AWS::SageMaker::EndpointConfig.ProductionVariants``.
        :param endpoint_config_name: ``AWS::SageMaker::EndpointConfig.EndpointConfigName``.
        :param kms_key_id: ``AWS::SageMaker::EndpointConfig.KmsKeyId``.
        :param tags: ``AWS::SageMaker::EndpointConfig.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html
        """
        self._values = {
            'production_variants': production_variants,
        }
        if endpoint_config_name is not None: self._values["endpoint_config_name"] = endpoint_config_name
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if tags is not None: self._values["tags"] = tags

    @property
    def production_variants(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnEndpointConfig.ProductionVariantProperty"]]]:
        """``AWS::SageMaker::EndpointConfig.ProductionVariants``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-productionvariants
        """
        return self._values.get('production_variants')

    @property
    def endpoint_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::EndpointConfig.EndpointConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-endpointconfigname
        """
        return self._values.get('endpoint_config_name')

    @property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::EndpointConfig.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-kmskeyid
        """
        return self._values.get('kms_key_id')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SageMaker::EndpointConfig.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpointconfig.html#cfn-sagemaker-endpointconfig-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEndpointConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnEndpointProps", jsii_struct_bases=[], name_mapping={'endpoint_config_name': 'endpointConfigName', 'endpoint_name': 'endpointName', 'tags': 'tags'})
class CfnEndpointProps():
    def __init__(self, *, endpoint_config_name: str, endpoint_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None):
        """Properties for defining a ``AWS::SageMaker::Endpoint``.

        :param endpoint_config_name: ``AWS::SageMaker::Endpoint.EndpointConfigName``.
        :param endpoint_name: ``AWS::SageMaker::Endpoint.EndpointName``.
        :param tags: ``AWS::SageMaker::Endpoint.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html
        """
        self._values = {
            'endpoint_config_name': endpoint_config_name,
        }
        if endpoint_name is not None: self._values["endpoint_name"] = endpoint_name
        if tags is not None: self._values["tags"] = tags

    @property
    def endpoint_config_name(self) -> str:
        """``AWS::SageMaker::Endpoint.EndpointConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-endpointconfigname
        """
        return self._values.get('endpoint_config_name')

    @property
    def endpoint_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Endpoint.EndpointName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-endpointname
        """
        return self._values.get('endpoint_name')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SageMaker::Endpoint.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-endpoint.html#cfn-sagemaker-endpoint-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnEndpointProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnModel(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnModel"):
    """A CloudFormation ``AWS::SageMaker::Model``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::Model
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, execution_role_arn: str, containers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ContainerDefinitionProperty"]]]]]=None, model_name: typing.Optional[str]=None, primary_container: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerDefinitionProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]=None) -> None:
        """Create a new ``AWS::SageMaker::Model``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param execution_role_arn: ``AWS::SageMaker::Model.ExecutionRoleArn``.
        :param containers: ``AWS::SageMaker::Model.Containers``.
        :param model_name: ``AWS::SageMaker::Model.ModelName``.
        :param primary_container: ``AWS::SageMaker::Model.PrimaryContainer``.
        :param tags: ``AWS::SageMaker::Model.Tags``.
        :param vpc_config: ``AWS::SageMaker::Model.VpcConfig``.
        """
        props = CfnModelProps(execution_role_arn=execution_role_arn, containers=containers, model_name=model_name, primary_container=primary_container, tags=tags, vpc_config=vpc_config)

        jsii.create(CfnModel, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrModelName")
    def attr_model_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ModelName
        """
        return jsii.get(self, "attrModelName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SageMaker::Model.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> str:
        """``AWS::SageMaker::Model.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: str):
        return jsii.set(self, "executionRoleArn", value)

    @property
    @jsii.member(jsii_name="containers")
    def containers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ContainerDefinitionProperty"]]]]]:
        """``AWS::SageMaker::Model.Containers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-containers
        """
        return jsii.get(self, "containers")

    @containers.setter
    def containers(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "ContainerDefinitionProperty"]]]]]):
        return jsii.set(self, "containers", value)

    @property
    @jsii.member(jsii_name="modelName")
    def model_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Model.ModelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-modelname
        """
        return jsii.get(self, "modelName")

    @model_name.setter
    def model_name(self, value: typing.Optional[str]):
        return jsii.set(self, "modelName", value)

    @property
    @jsii.member(jsii_name="primaryContainer")
    def primary_container(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerDefinitionProperty"]]]:
        """``AWS::SageMaker::Model.PrimaryContainer``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-primarycontainer
        """
        return jsii.get(self, "primaryContainer")

    @primary_container.setter
    def primary_container(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ContainerDefinitionProperty"]]]):
        return jsii.set(self, "primaryContainer", value)

    @property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]:
        """``AWS::SageMaker::Model.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["VpcConfigProperty"]]]):
        return jsii.set(self, "vpcConfig", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModel.ContainerDefinitionProperty", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_hostname': 'containerHostname', 'environment': 'environment', 'model_data_url': 'modelDataUrl'})
    class ContainerDefinitionProperty():
        def __init__(self, *, image: str, container_hostname: typing.Optional[str]=None, environment: typing.Any=None, model_data_url: typing.Optional[str]=None):
            """
            :param image: ``CfnModel.ContainerDefinitionProperty.Image``.
            :param container_hostname: ``CfnModel.ContainerDefinitionProperty.ContainerHostname``.
            :param environment: ``CfnModel.ContainerDefinitionProperty.Environment``.
            :param model_data_url: ``CfnModel.ContainerDefinitionProperty.ModelDataUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-containerdefinition.html
            """
            self._values = {
                'image': image,
            }
            if container_hostname is not None: self._values["container_hostname"] = container_hostname
            if environment is not None: self._values["environment"] = environment
            if model_data_url is not None: self._values["model_data_url"] = model_data_url

        @property
        def image(self) -> str:
            """``CfnModel.ContainerDefinitionProperty.Image``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-containerdefinition.html#cfn-sagemaker-model-containerdefinition-image
            """
            return self._values.get('image')

        @property
        def container_hostname(self) -> typing.Optional[str]:
            """``CfnModel.ContainerDefinitionProperty.ContainerHostname``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-containerdefinition.html#cfn-sagemaker-model-containerdefinition-containerhostname
            """
            return self._values.get('container_hostname')

        @property
        def environment(self) -> typing.Any:
            """``CfnModel.ContainerDefinitionProperty.Environment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-containerdefinition.html#cfn-sagemaker-model-containerdefinition-environment
            """
            return self._values.get('environment')

        @property
        def model_data_url(self) -> typing.Optional[str]:
            """``CfnModel.ContainerDefinitionProperty.ModelDataUrl``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-containerdefinition.html#cfn-sagemaker-model-containerdefinition-modeldataurl
            """
            return self._values.get('model_data_url')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ContainerDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModel.VpcConfigProperty", jsii_struct_bases=[], name_mapping={'security_group_ids': 'securityGroupIds', 'subnets': 'subnets'})
    class VpcConfigProperty():
        def __init__(self, *, security_group_ids: typing.List[str], subnets: typing.List[str]):
            """
            :param security_group_ids: ``CfnModel.VpcConfigProperty.SecurityGroupIds``.
            :param subnets: ``CfnModel.VpcConfigProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-vpcconfig.html
            """
            self._values = {
                'security_group_ids': security_group_ids,
                'subnets': subnets,
            }

        @property
        def security_group_ids(self) -> typing.List[str]:
            """``CfnModel.VpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-vpcconfig.html#cfn-sagemaker-model-vpcconfig-securitygroupids
            """
            return self._values.get('security_group_ids')

        @property
        def subnets(self) -> typing.List[str]:
            """``CfnModel.VpcConfigProperty.Subnets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-model-vpcconfig.html#cfn-sagemaker-model-vpcconfig-subnets
            """
            return self._values.get('subnets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'VpcConfigProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnModelProps", jsii_struct_bases=[], name_mapping={'execution_role_arn': 'executionRoleArn', 'containers': 'containers', 'model_name': 'modelName', 'primary_container': 'primaryContainer', 'tags': 'tags', 'vpc_config': 'vpcConfig'})
class CfnModelProps():
    def __init__(self, *, execution_role_arn: str, containers: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnModel.ContainerDefinitionProperty"]]]]]=None, model_name: typing.Optional[str]=None, primary_container: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnModel.ContainerDefinitionProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnModel.VpcConfigProperty"]]]=None):
        """Properties for defining a ``AWS::SageMaker::Model``.

        :param execution_role_arn: ``AWS::SageMaker::Model.ExecutionRoleArn``.
        :param containers: ``AWS::SageMaker::Model.Containers``.
        :param model_name: ``AWS::SageMaker::Model.ModelName``.
        :param primary_container: ``AWS::SageMaker::Model.PrimaryContainer``.
        :param tags: ``AWS::SageMaker::Model.Tags``.
        :param vpc_config: ``AWS::SageMaker::Model.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html
        """
        self._values = {
            'execution_role_arn': execution_role_arn,
        }
        if containers is not None: self._values["containers"] = containers
        if model_name is not None: self._values["model_name"] = model_name
        if primary_container is not None: self._values["primary_container"] = primary_container
        if tags is not None: self._values["tags"] = tags
        if vpc_config is not None: self._values["vpc_config"] = vpc_config

    @property
    def execution_role_arn(self) -> str:
        """``AWS::SageMaker::Model.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-executionrolearn
        """
        return self._values.get('execution_role_arn')

    @property
    def containers(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnModel.ContainerDefinitionProperty"]]]]]:
        """``AWS::SageMaker::Model.Containers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-containers
        """
        return self._values.get('containers')

    @property
    def model_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Model.ModelName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-modelname
        """
        return self._values.get('model_name')

    @property
    def primary_container(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnModel.ContainerDefinitionProperty"]]]:
        """``AWS::SageMaker::Model.PrimaryContainer``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-primarycontainer
        """
        return self._values.get('primary_container')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SageMaker::Model.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-tags
        """
        return self._values.get('tags')

    @property
    def vpc_config(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnModel.VpcConfigProperty"]]]:
        """``AWS::SageMaker::Model.VpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-model.html#cfn-sagemaker-model-vpcconfig
        """
        return self._values.get('vpc_config')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnModelProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNotebookInstance(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstance"):
    """A CloudFormation ``AWS::SageMaker::NotebookInstance``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::NotebookInstance
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, instance_type: str, role_arn: str, accelerator_types: typing.Optional[typing.List[str]]=None, additional_code_repositories: typing.Optional[typing.List[str]]=None, default_code_repository: typing.Optional[str]=None, direct_internet_access: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lifecycle_config_name: typing.Optional[str]=None, notebook_instance_name: typing.Optional[str]=None, root_access: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, volume_size_in_gb: typing.Optional[jsii.Number]=None) -> None:
        """Create a new ``AWS::SageMaker::NotebookInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param instance_type: ``AWS::SageMaker::NotebookInstance.InstanceType``.
        :param role_arn: ``AWS::SageMaker::NotebookInstance.RoleArn``.
        :param accelerator_types: ``AWS::SageMaker::NotebookInstance.AcceleratorTypes``.
        :param additional_code_repositories: ``AWS::SageMaker::NotebookInstance.AdditionalCodeRepositories``.
        :param default_code_repository: ``AWS::SageMaker::NotebookInstance.DefaultCodeRepository``.
        :param direct_internet_access: ``AWS::SageMaker::NotebookInstance.DirectInternetAccess``.
        :param kms_key_id: ``AWS::SageMaker::NotebookInstance.KmsKeyId``.
        :param lifecycle_config_name: ``AWS::SageMaker::NotebookInstance.LifecycleConfigName``.
        :param notebook_instance_name: ``AWS::SageMaker::NotebookInstance.NotebookInstanceName``.
        :param root_access: ``AWS::SageMaker::NotebookInstance.RootAccess``.
        :param security_group_ids: ``AWS::SageMaker::NotebookInstance.SecurityGroupIds``.
        :param subnet_id: ``AWS::SageMaker::NotebookInstance.SubnetId``.
        :param tags: ``AWS::SageMaker::NotebookInstance.Tags``.
        :param volume_size_in_gb: ``AWS::SageMaker::NotebookInstance.VolumeSizeInGB``.
        """
        props = CfnNotebookInstanceProps(instance_type=instance_type, role_arn=role_arn, accelerator_types=accelerator_types, additional_code_repositories=additional_code_repositories, default_code_repository=default_code_repository, direct_internet_access=direct_internet_access, kms_key_id=kms_key_id, lifecycle_config_name=lifecycle_config_name, notebook_instance_name=notebook_instance_name, root_access=root_access, security_group_ids=security_group_ids, subnet_id=subnet_id, tags=tags, volume_size_in_gb=volume_size_in_gb)

        jsii.create(CfnNotebookInstance, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrNotebookInstanceName")
    def attr_notebook_instance_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NotebookInstanceName
        """
        return jsii.get(self, "attrNotebookInstanceName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SageMaker::NotebookInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> str:
        """``AWS::SageMaker::NotebookInstance.InstanceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-instancetype
        """
        return jsii.get(self, "instanceType")

    @instance_type.setter
    def instance_type(self, value: str):
        return jsii.set(self, "instanceType", value)

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::SageMaker::NotebookInstance.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        return jsii.set(self, "roleArn", value)

    @property
    @jsii.member(jsii_name="acceleratorTypes")
    def accelerator_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.AcceleratorTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-acceleratortypes
        """
        return jsii.get(self, "acceleratorTypes")

    @accelerator_types.setter
    def accelerator_types(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "acceleratorTypes", value)

    @property
    @jsii.member(jsii_name="additionalCodeRepositories")
    def additional_code_repositories(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.AdditionalCodeRepositories``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-additionalcoderepositories
        """
        return jsii.get(self, "additionalCodeRepositories")

    @additional_code_repositories.setter
    def additional_code_repositories(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "additionalCodeRepositories", value)

    @property
    @jsii.member(jsii_name="defaultCodeRepository")
    def default_code_repository(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.DefaultCodeRepository``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-defaultcoderepository
        """
        return jsii.get(self, "defaultCodeRepository")

    @default_code_repository.setter
    def default_code_repository(self, value: typing.Optional[str]):
        return jsii.set(self, "defaultCodeRepository", value)

    @property
    @jsii.member(jsii_name="directInternetAccess")
    def direct_internet_access(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.DirectInternetAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-directinternetaccess
        """
        return jsii.get(self, "directInternetAccess")

    @direct_internet_access.setter
    def direct_internet_access(self, value: typing.Optional[str]):
        return jsii.set(self, "directInternetAccess", value)

    @property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]):
        return jsii.set(self, "kmsKeyId", value)

    @property
    @jsii.member(jsii_name="lifecycleConfigName")
    def lifecycle_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.LifecycleConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-lifecycleconfigname
        """
        return jsii.get(self, "lifecycleConfigName")

    @lifecycle_config_name.setter
    def lifecycle_config_name(self, value: typing.Optional[str]):
        return jsii.set(self, "lifecycleConfigName", value)

    @property
    @jsii.member(jsii_name="notebookInstanceName")
    def notebook_instance_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.NotebookInstanceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-notebookinstancename
        """
        return jsii.get(self, "notebookInstanceName")

    @notebook_instance_name.setter
    def notebook_instance_name(self, value: typing.Optional[str]):
        return jsii.set(self, "notebookInstanceName", value)

    @property
    @jsii.member(jsii_name="rootAccess")
    def root_access(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.RootAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-rootaccess
        """
        return jsii.get(self, "rootAccess")

    @root_access.setter
    def root_access(self, value: typing.Optional[str]):
        return jsii.set(self, "rootAccess", value)

    @property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "securityGroupIds", value)

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: typing.Optional[str]):
        return jsii.set(self, "subnetId", value)

    @property
    @jsii.member(jsii_name="volumeSizeInGb")
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        """``AWS::SageMaker::NotebookInstance.VolumeSizeInGB``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-volumesizeingb
        """
        return jsii.get(self, "volumeSizeInGb")

    @volume_size_in_gb.setter
    def volume_size_in_gb(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "volumeSizeInGb", value)


@jsii.implements(aws_cdk.core.IInspectable)
class CfnNotebookInstanceLifecycleConfig(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfig"):
    """A CloudFormation ``AWS::SageMaker::NotebookInstanceLifecycleConfig``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::NotebookInstanceLifecycleConfig
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, notebook_instance_lifecycle_config_name: typing.Optional[str]=None, on_create: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]=None, on_start: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]=None) -> None:
        """Create a new ``AWS::SageMaker::NotebookInstanceLifecycleConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param notebook_instance_lifecycle_config_name: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.NotebookInstanceLifecycleConfigName``.
        :param on_create: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnCreate``.
        :param on_start: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnStart``.
        """
        props = CfnNotebookInstanceLifecycleConfigProps(notebook_instance_lifecycle_config_name=notebook_instance_lifecycle_config_name, on_create=on_create, on_start=on_start)

        jsii.create(CfnNotebookInstanceLifecycleConfig, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrNotebookInstanceLifecycleConfigName")
    def attr_notebook_instance_lifecycle_config_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NotebookInstanceLifecycleConfigName
        """
        return jsii.get(self, "attrNotebookInstanceLifecycleConfigName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="notebookInstanceLifecycleConfigName")
    def notebook_instance_lifecycle_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.NotebookInstanceLifecycleConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-notebookinstancelifecycleconfigname
        """
        return jsii.get(self, "notebookInstanceLifecycleConfigName")

    @notebook_instance_lifecycle_config_name.setter
    def notebook_instance_lifecycle_config_name(self, value: typing.Optional[str]):
        return jsii.set(self, "notebookInstanceLifecycleConfigName", value)

    @property
    @jsii.member(jsii_name="onCreate")
    def on_create(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnCreate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-oncreate
        """
        return jsii.get(self, "onCreate")

    @on_create.setter
    def on_create(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]):
        return jsii.set(self, "onCreate", value)

    @property
    @jsii.member(jsii_name="onStart")
    def on_start(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnStart``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-onstart
        """
        return jsii.get(self, "onStart")

    @on_start.setter
    def on_start(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "NotebookInstanceLifecycleHookProperty"]]]]]):
        return jsii.set(self, "onStart", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty", jsii_struct_bases=[], name_mapping={'content': 'content'})
    class NotebookInstanceLifecycleHookProperty():
        def __init__(self, *, content: typing.Optional[str]=None):
            """
            :param content: ``CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty.Content``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-notebookinstancelifecycleconfig-notebookinstancelifecyclehook.html
            """
            self._values = {
            }
            if content is not None: self._values["content"] = content

        @property
        def content(self) -> typing.Optional[str]:
            """``CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty.Content``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-notebookinstancelifecycleconfig-notebookinstancelifecyclehook.html#cfn-sagemaker-notebookinstancelifecycleconfig-notebookinstancelifecyclehook-content
            """
            return self._values.get('content')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotebookInstanceLifecycleHookProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceLifecycleConfigProps", jsii_struct_bases=[], name_mapping={'notebook_instance_lifecycle_config_name': 'notebookInstanceLifecycleConfigName', 'on_create': 'onCreate', 'on_start': 'onStart'})
class CfnNotebookInstanceLifecycleConfigProps():
    def __init__(self, *, notebook_instance_lifecycle_config_name: typing.Optional[str]=None, on_create: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]]]=None, on_start: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]]]=None):
        """Properties for defining a ``AWS::SageMaker::NotebookInstanceLifecycleConfig``.

        :param notebook_instance_lifecycle_config_name: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.NotebookInstanceLifecycleConfigName``.
        :param on_create: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnCreate``.
        :param on_start: ``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnStart``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html
        """
        self._values = {
        }
        if notebook_instance_lifecycle_config_name is not None: self._values["notebook_instance_lifecycle_config_name"] = notebook_instance_lifecycle_config_name
        if on_create is not None: self._values["on_create"] = on_create
        if on_start is not None: self._values["on_start"] = on_start

    @property
    def notebook_instance_lifecycle_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.NotebookInstanceLifecycleConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-notebookinstancelifecycleconfigname
        """
        return self._values.get('notebook_instance_lifecycle_config_name')

    @property
    def on_create(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]]]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnCreate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-oncreate
        """
        return self._values.get('on_create')

    @property
    def on_start(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty"]]]]]:
        """``AWS::SageMaker::NotebookInstanceLifecycleConfig.OnStart``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstancelifecycleconfig.html#cfn-sagemaker-notebookinstancelifecycleconfig-onstart
        """
        return self._values.get('on_start')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNotebookInstanceLifecycleConfigProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnNotebookInstanceProps", jsii_struct_bases=[], name_mapping={'instance_type': 'instanceType', 'role_arn': 'roleArn', 'accelerator_types': 'acceleratorTypes', 'additional_code_repositories': 'additionalCodeRepositories', 'default_code_repository': 'defaultCodeRepository', 'direct_internet_access': 'directInternetAccess', 'kms_key_id': 'kmsKeyId', 'lifecycle_config_name': 'lifecycleConfigName', 'notebook_instance_name': 'notebookInstanceName', 'root_access': 'rootAccess', 'security_group_ids': 'securityGroupIds', 'subnet_id': 'subnetId', 'tags': 'tags', 'volume_size_in_gb': 'volumeSizeInGb'})
class CfnNotebookInstanceProps():
    def __init__(self, *, instance_type: str, role_arn: str, accelerator_types: typing.Optional[typing.List[str]]=None, additional_code_repositories: typing.Optional[typing.List[str]]=None, default_code_repository: typing.Optional[str]=None, direct_internet_access: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, lifecycle_config_name: typing.Optional[str]=None, notebook_instance_name: typing.Optional[str]=None, root_access: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, volume_size_in_gb: typing.Optional[jsii.Number]=None):
        """Properties for defining a ``AWS::SageMaker::NotebookInstance``.

        :param instance_type: ``AWS::SageMaker::NotebookInstance.InstanceType``.
        :param role_arn: ``AWS::SageMaker::NotebookInstance.RoleArn``.
        :param accelerator_types: ``AWS::SageMaker::NotebookInstance.AcceleratorTypes``.
        :param additional_code_repositories: ``AWS::SageMaker::NotebookInstance.AdditionalCodeRepositories``.
        :param default_code_repository: ``AWS::SageMaker::NotebookInstance.DefaultCodeRepository``.
        :param direct_internet_access: ``AWS::SageMaker::NotebookInstance.DirectInternetAccess``.
        :param kms_key_id: ``AWS::SageMaker::NotebookInstance.KmsKeyId``.
        :param lifecycle_config_name: ``AWS::SageMaker::NotebookInstance.LifecycleConfigName``.
        :param notebook_instance_name: ``AWS::SageMaker::NotebookInstance.NotebookInstanceName``.
        :param root_access: ``AWS::SageMaker::NotebookInstance.RootAccess``.
        :param security_group_ids: ``AWS::SageMaker::NotebookInstance.SecurityGroupIds``.
        :param subnet_id: ``AWS::SageMaker::NotebookInstance.SubnetId``.
        :param tags: ``AWS::SageMaker::NotebookInstance.Tags``.
        :param volume_size_in_gb: ``AWS::SageMaker::NotebookInstance.VolumeSizeInGB``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html
        """
        self._values = {
            'instance_type': instance_type,
            'role_arn': role_arn,
        }
        if accelerator_types is not None: self._values["accelerator_types"] = accelerator_types
        if additional_code_repositories is not None: self._values["additional_code_repositories"] = additional_code_repositories
        if default_code_repository is not None: self._values["default_code_repository"] = default_code_repository
        if direct_internet_access is not None: self._values["direct_internet_access"] = direct_internet_access
        if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
        if lifecycle_config_name is not None: self._values["lifecycle_config_name"] = lifecycle_config_name
        if notebook_instance_name is not None: self._values["notebook_instance_name"] = notebook_instance_name
        if root_access is not None: self._values["root_access"] = root_access
        if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
        if subnet_id is not None: self._values["subnet_id"] = subnet_id
        if tags is not None: self._values["tags"] = tags
        if volume_size_in_gb is not None: self._values["volume_size_in_gb"] = volume_size_in_gb

    @property
    def instance_type(self) -> str:
        """``AWS::SageMaker::NotebookInstance.InstanceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-instancetype
        """
        return self._values.get('instance_type')

    @property
    def role_arn(self) -> str:
        """``AWS::SageMaker::NotebookInstance.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-rolearn
        """
        return self._values.get('role_arn')

    @property
    def accelerator_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.AcceleratorTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-acceleratortypes
        """
        return self._values.get('accelerator_types')

    @property
    def additional_code_repositories(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.AdditionalCodeRepositories``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-additionalcoderepositories
        """
        return self._values.get('additional_code_repositories')

    @property
    def default_code_repository(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.DefaultCodeRepository``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-defaultcoderepository
        """
        return self._values.get('default_code_repository')

    @property
    def direct_internet_access(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.DirectInternetAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-directinternetaccess
        """
        return self._values.get('direct_internet_access')

    @property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-kmskeyid
        """
        return self._values.get('kms_key_id')

    @property
    def lifecycle_config_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.LifecycleConfigName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-lifecycleconfigname
        """
        return self._values.get('lifecycle_config_name')

    @property
    def notebook_instance_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.NotebookInstanceName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-notebookinstancename
        """
        return self._values.get('notebook_instance_name')

    @property
    def root_access(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.RootAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-rootaccess
        """
        return self._values.get('root_access')

    @property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::SageMaker::NotebookInstance.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-securitygroupids
        """
        return self._values.get('security_group_ids')

    @property
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::SageMaker::NotebookInstance.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-subnetid
        """
        return self._values.get('subnet_id')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SageMaker::NotebookInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-tags
        """
        return self._values.get('tags')

    @property
    def volume_size_in_gb(self) -> typing.Optional[jsii.Number]:
        """``AWS::SageMaker::NotebookInstance.VolumeSizeInGB``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-notebookinstance.html#cfn-sagemaker-notebookinstance-volumesizeingb
        """
        return self._values.get('volume_size_in_gb')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnNotebookInstanceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWorkteam(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sagemaker.CfnWorkteam"):
    """A CloudFormation ``AWS::SageMaker::Workteam``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html
    cloudformationResource:
    :cloudformationResource:: AWS::SageMaker::Workteam
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, description: typing.Optional[str]=None, member_definitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MemberDefinitionProperty"]]]]]=None, notification_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, workteam_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SageMaker::Workteam``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param description: ``AWS::SageMaker::Workteam.Description``.
        :param member_definitions: ``AWS::SageMaker::Workteam.MemberDefinitions``.
        :param notification_configuration: ``AWS::SageMaker::Workteam.NotificationConfiguration``.
        :param tags: ``AWS::SageMaker::Workteam.Tags``.
        :param workteam_name: ``AWS::SageMaker::Workteam.WorkteamName``.
        """
        props = CfnWorkteamProps(description=description, member_definitions=member_definitions, notification_configuration=notification_configuration, tags=tags, workteam_name=workteam_name)

        jsii.create(CfnWorkteam, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: aws_cdk.core.TreeInspector) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, props: typing.Mapping[str,typing.Any]) -> typing.Mapping[str,typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @property
    @jsii.member(jsii_name="attrWorkteamName")
    def attr_workteam_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: WorkteamName
        """
        return jsii.get(self, "attrWorkteamName")

    @property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::SageMaker::Workteam.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Workteam.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="memberDefinitions")
    def member_definitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MemberDefinitionProperty"]]]]]:
        """``AWS::SageMaker::Workteam.MemberDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-memberdefinitions
        """
        return jsii.get(self, "memberDefinitions")

    @member_definitions.setter
    def member_definitions(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "MemberDefinitionProperty"]]]]]):
        return jsii.set(self, "memberDefinitions", value)

    @property
    @jsii.member(jsii_name="notificationConfiguration")
    def notification_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]:
        """``AWS::SageMaker::Workteam.NotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-notificationconfiguration
        """
        return jsii.get(self, "notificationConfiguration")

    @notification_configuration.setter
    def notification_configuration(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationConfigurationProperty"]]]):
        return jsii.set(self, "notificationConfiguration", value)

    @property
    @jsii.member(jsii_name="workteamName")
    def workteam_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Workteam.WorkteamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-workteamname
        """
        return jsii.get(self, "workteamName")

    @workteam_name.setter
    def workteam_name(self, value: typing.Optional[str]):
        return jsii.set(self, "workteamName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnWorkteam.CognitoMemberDefinitionProperty", jsii_struct_bases=[], name_mapping={'cognito_client_id': 'cognitoClientId', 'cognito_user_group': 'cognitoUserGroup', 'cognito_user_pool': 'cognitoUserPool'})
    class CognitoMemberDefinitionProperty():
        def __init__(self, *, cognito_client_id: str, cognito_user_group: str, cognito_user_pool: str):
            """
            :param cognito_client_id: ``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoClientId``.
            :param cognito_user_group: ``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoUserGroup``.
            :param cognito_user_pool: ``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoUserPool``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-cognitomemberdefinition.html
            """
            self._values = {
                'cognito_client_id': cognito_client_id,
                'cognito_user_group': cognito_user_group,
                'cognito_user_pool': cognito_user_pool,
            }

        @property
        def cognito_client_id(self) -> str:
            """``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoClientId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-cognitomemberdefinition.html#cfn-sagemaker-workteam-cognitomemberdefinition-cognitoclientid
            """
            return self._values.get('cognito_client_id')

        @property
        def cognito_user_group(self) -> str:
            """``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoUserGroup``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-cognitomemberdefinition.html#cfn-sagemaker-workteam-cognitomemberdefinition-cognitousergroup
            """
            return self._values.get('cognito_user_group')

        @property
        def cognito_user_pool(self) -> str:
            """``CfnWorkteam.CognitoMemberDefinitionProperty.CognitoUserPool``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-cognitomemberdefinition.html#cfn-sagemaker-workteam-cognitomemberdefinition-cognitouserpool
            """
            return self._values.get('cognito_user_pool')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CognitoMemberDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnWorkteam.MemberDefinitionProperty", jsii_struct_bases=[], name_mapping={'cognito_member_definition': 'cognitoMemberDefinition'})
    class MemberDefinitionProperty():
        def __init__(self, *, cognito_member_definition: typing.Union[aws_cdk.core.IResolvable, "CfnWorkteam.CognitoMemberDefinitionProperty"]):
            """
            :param cognito_member_definition: ``CfnWorkteam.MemberDefinitionProperty.CognitoMemberDefinition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-memberdefinition.html
            """
            self._values = {
                'cognito_member_definition': cognito_member_definition,
            }

        @property
        def cognito_member_definition(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnWorkteam.CognitoMemberDefinitionProperty"]:
            """``CfnWorkteam.MemberDefinitionProperty.CognitoMemberDefinition``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-memberdefinition.html#cfn-sagemaker-workteam-memberdefinition-cognitomemberdefinition
            """
            return self._values.get('cognito_member_definition')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'MemberDefinitionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnWorkteam.NotificationConfigurationProperty", jsii_struct_bases=[], name_mapping={'notification_topic_arn': 'notificationTopicArn'})
    class NotificationConfigurationProperty():
        def __init__(self, *, notification_topic_arn: str):
            """
            :param notification_topic_arn: ``CfnWorkteam.NotificationConfigurationProperty.NotificationTopicArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-notificationconfiguration.html
            """
            self._values = {
                'notification_topic_arn': notification_topic_arn,
            }

        @property
        def notification_topic_arn(self) -> str:
            """``CfnWorkteam.NotificationConfigurationProperty.NotificationTopicArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sagemaker-workteam-notificationconfiguration.html#cfn-sagemaker-workteam-notificationconfiguration-notificationtopicarn
            """
            return self._values.get('notification_topic_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-sagemaker.CfnWorkteamProps", jsii_struct_bases=[], name_mapping={'description': 'description', 'member_definitions': 'memberDefinitions', 'notification_configuration': 'notificationConfiguration', 'tags': 'tags', 'workteam_name': 'workteamName'})
class CfnWorkteamProps():
    def __init__(self, *, description: typing.Optional[str]=None, member_definitions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWorkteam.MemberDefinitionProperty"]]]]]=None, notification_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnWorkteam.NotificationConfigurationProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.core.CfnTag]]=None, workteam_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::SageMaker::Workteam``.

        :param description: ``AWS::SageMaker::Workteam.Description``.
        :param member_definitions: ``AWS::SageMaker::Workteam.MemberDefinitions``.
        :param notification_configuration: ``AWS::SageMaker::Workteam.NotificationConfiguration``.
        :param tags: ``AWS::SageMaker::Workteam.Tags``.
        :param workteam_name: ``AWS::SageMaker::Workteam.WorkteamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html
        """
        self._values = {
        }
        if description is not None: self._values["description"] = description
        if member_definitions is not None: self._values["member_definitions"] = member_definitions
        if notification_configuration is not None: self._values["notification_configuration"] = notification_configuration
        if tags is not None: self._values["tags"] = tags
        if workteam_name is not None: self._values["workteam_name"] = workteam_name

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Workteam.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-description
        """
        return self._values.get('description')

    @property
    def member_definitions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnWorkteam.MemberDefinitionProperty"]]]]]:
        """``AWS::SageMaker::Workteam.MemberDefinitions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-memberdefinitions
        """
        return self._values.get('member_definitions')

    @property
    def notification_configuration(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnWorkteam.NotificationConfigurationProperty"]]]:
        """``AWS::SageMaker::Workteam.NotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-notificationconfiguration
        """
        return self._values.get('notification_configuration')

    @property
    def tags(self) -> typing.Optional[typing.List[aws_cdk.core.CfnTag]]:
        """``AWS::SageMaker::Workteam.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-tags
        """
        return self._values.get('tags')

    @property
    def workteam_name(self) -> typing.Optional[str]:
        """``AWS::SageMaker::Workteam.WorkteamName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sagemaker-workteam.html#cfn-sagemaker-workteam-workteamname
        """
        return self._values.get('workteam_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWorkteamProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnCodeRepository", "CfnCodeRepositoryProps", "CfnEndpoint", "CfnEndpointConfig", "CfnEndpointConfigProps", "CfnEndpointProps", "CfnModel", "CfnModelProps", "CfnNotebookInstance", "CfnNotebookInstanceLifecycleConfig", "CfnNotebookInstanceLifecycleConfigProps", "CfnNotebookInstanceProps", "CfnWorkteam", "CfnWorkteamProps", "__jsii_assembly__"]

publication.publish()
