"""
## AWS Glue Construct Library

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

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

### Database

A `Database` is a logical grouping of `Tables` in the Glue Catalog.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Database(stack, "MyDatabase",
    database_name="my_database"
)
```

By default, a S3 bucket is created and the Database is stored under  `s3://<bucket-name>/`, but you can manually specify another location:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Database(stack, "MyDatabase",
    database_name="my_database",
    location_uri="s3://explicit-bucket/some-path/"
)
```

### Table

A Glue table describes a table of data in S3: its structure (column names and types), location of data (S3 objects with a common prefix in a S3 bucket), and format for the files (Json, Avro, Parquet, etc.):

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    database=my_database,
    table_name="my_table",
    columns=[{
        "name": "col1",
        "type": glue.Schema.string
    }, {
        "name": "col2",
        "type": glue.Schema.array(Schema.string),
        "comment": "col2 is an array of strings"
    }],
    data_format=glue.DataFormat.Json
)
```

By default, a S3 bucket will be created to store the table's data but you can manually pass the `bucket` and `s3Prefix`:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    bucket=my_bucket,
    s3_prefix="my-table/", ...
)
```

#### Partitions

To improve query performance, a table can specify `partitionKeys` on which data is stored and queried separately. For example, you might partition a table by `year` and `month` to optimize queries based on a time window:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    database=my_database,
    table_name="my_table",
    columns=[{
        "name": "col1",
        "type": glue.Schema.string
    }],
    partition_keys=[{
        "name": "year",
        "type": glue.Schema.smallint
    }, {
        "name": "month",
        "type": glue.Schema.smallint
    }],
    data_format=glue.DataFormat.Json
)
```

### [Encryption](https://docs.aws.amazon.com/athena/latest/ug/encryption.html)

You can enable encryption on a Table's data:

* `Unencrypted` - files are not encrypted. The default encryption setting.
* [S3Managed](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html) - Server side encryption (`SSE-S3`) with an Amazon S3-managed key.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.S3Managed, ...
)
```

* [Kms](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html) - Server-side encryption (`SSE-KMS`) with an AWS KMS Key managed by the account owner.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# KMS key is created automatically
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.Kms, ...
)

# with an explicit KMS key
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.Kms,
    encryption_key=kms.Key(stack, "MyKey"), ...
)
```

* [KmsManaged](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html) - Server-side encryption (`SSE-KMS`), like `Kms`, except with an AWS KMS Key managed by the AWS Key Management Service.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.KmsManaged, ...
)
```

* [ClientSideKms](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html#client-side-encryption-kms-managed-master-key-intro) - Client-side encryption (`CSE-KMS`) with an AWS KMS Key managed by the account owner.

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
# KMS key is created automatically
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.ClientSideKms, ...
)

# with an explicit KMS key
glue.Table(stack, "MyTable",
    encryption=glue.TableEncryption.ClientSideKms,
    encryption_key=kms.Key(stack, "MyKey"), ...
)
```

*Note: you cannot provide a `Bucket` when creating the `Table` if you wish to use server-side encryption (`Kms`, `KmsManaged` or `S3Managed`)*.

### Types

A table's schema is a collection of columns, each of which have a `name` and a `type`. Types are recursive structures, consisting of primitive and complex types:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
glue.Table(stack, "MyTable",
    columns=[{
        "name": "primitive_column",
        "type": glue.Schema.string
    }, {
        "name": "array_column",
        "type": glue.Schema.array(glue.Schema.integer),
        "comment": "array<integer>"
    }, {
        "name": "map_column",
        "type": glue.Schema.map(glue.Schema.string, glue.Schema.timestamp),
        "comment": "map<string,string>"
    }, {
        "name": "struct_column",
        "type": glue.Schema.struct([
            name="nested_column",
            type=glue.Schema.date,
            comment="nested comment"
        ]),
        "comment": "struct<nested_column:date COMMENT 'nested comment'>"
    }], ...
)
```

#### Primitive

Numeric:

* `bigint`
* `float`
* `integer`
* `smallint`
* `tinyint`

Date and Time:

* `date`
* `timestamp`

String Types:

* `string`
* `decimal`
* `char`
* `varchar`

Misc:

* `boolean`
* `binary`

#### Complex

* `array` - array of some other type
* `map` - map of some primitive key type to any value type.
* `struct` - nested structure containing individually named and typed columns.
"""
import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_s3
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-glue", "1.18.0", __name__, "aws-glue@1.18.0.jsii.tgz")
@jsii.implements(aws_cdk.core.IInspectable)
class CfnClassifier(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnClassifier"):
    """A CloudFormation ``AWS::Glue::Classifier``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Classifier
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, csv_classifier: typing.Optional[typing.Union[typing.Optional["CsvClassifierProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, grok_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GrokClassifierProperty"]]]=None, json_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JsonClassifierProperty"]]]=None, xml_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["XMLClassifierProperty"]]]=None) -> None:
        """Create a new ``AWS::Glue::Classifier``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param csv_classifier: ``AWS::Glue::Classifier.CsvClassifier``.
        :param grok_classifier: ``AWS::Glue::Classifier.GrokClassifier``.
        :param json_classifier: ``AWS::Glue::Classifier.JsonClassifier``.
        :param xml_classifier: ``AWS::Glue::Classifier.XMLClassifier``.
        """
        props = CfnClassifierProps(csv_classifier=csv_classifier, grok_classifier=grok_classifier, json_classifier=json_classifier, xml_classifier=xml_classifier)

        jsii.create(CfnClassifier, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="csvClassifier")
    def csv_classifier(self) -> typing.Optional[typing.Union[typing.Optional["CsvClassifierProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Glue::Classifier.CsvClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-csvclassifier
        """
        return jsii.get(self, "csvClassifier")

    @csv_classifier.setter
    def csv_classifier(self, value: typing.Optional[typing.Union[typing.Optional["CsvClassifierProperty"], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "csvClassifier", value)

    @property
    @jsii.member(jsii_name="grokClassifier")
    def grok_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GrokClassifierProperty"]]]:
        """``AWS::Glue::Classifier.GrokClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-grokclassifier
        """
        return jsii.get(self, "grokClassifier")

    @grok_classifier.setter
    def grok_classifier(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["GrokClassifierProperty"]]]):
        return jsii.set(self, "grokClassifier", value)

    @property
    @jsii.member(jsii_name="jsonClassifier")
    def json_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JsonClassifierProperty"]]]:
        """``AWS::Glue::Classifier.JsonClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-jsonclassifier
        """
        return jsii.get(self, "jsonClassifier")

    @json_classifier.setter
    def json_classifier(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["JsonClassifierProperty"]]]):
        return jsii.set(self, "jsonClassifier", value)

    @property
    @jsii.member(jsii_name="xmlClassifier")
    def xml_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["XMLClassifierProperty"]]]:
        """``AWS::Glue::Classifier.XMLClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-xmlclassifier
        """
        return jsii.get(self, "xmlClassifier")

    @xml_classifier.setter
    def xml_classifier(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["XMLClassifierProperty"]]]):
        return jsii.set(self, "xmlClassifier", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.CsvClassifierProperty", jsii_struct_bases=[], name_mapping={'allow_single_column': 'allowSingleColumn', 'contains_header': 'containsHeader', 'delimiter': 'delimiter', 'disable_value_trimming': 'disableValueTrimming', 'header': 'header', 'name': 'name', 'quote_symbol': 'quoteSymbol'})
    class CsvClassifierProperty():
        def __init__(self, *, allow_single_column: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, contains_header: typing.Optional[str]=None, delimiter: typing.Optional[str]=None, disable_value_trimming: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, header: typing.Optional[typing.List[str]]=None, name: typing.Optional[str]=None, quote_symbol: typing.Optional[str]=None):
            """
            :param allow_single_column: ``CfnClassifier.CsvClassifierProperty.AllowSingleColumn``.
            :param contains_header: ``CfnClassifier.CsvClassifierProperty.ContainsHeader``.
            :param delimiter: ``CfnClassifier.CsvClassifierProperty.Delimiter``.
            :param disable_value_trimming: ``CfnClassifier.CsvClassifierProperty.DisableValueTrimming``.
            :param header: ``CfnClassifier.CsvClassifierProperty.Header``.
            :param name: ``CfnClassifier.CsvClassifierProperty.Name``.
            :param quote_symbol: ``CfnClassifier.CsvClassifierProperty.QuoteSymbol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html
            """
            self._values = {
            }
            if allow_single_column is not None: self._values["allow_single_column"] = allow_single_column
            if contains_header is not None: self._values["contains_header"] = contains_header
            if delimiter is not None: self._values["delimiter"] = delimiter
            if disable_value_trimming is not None: self._values["disable_value_trimming"] = disable_value_trimming
            if header is not None: self._values["header"] = header
            if name is not None: self._values["name"] = name
            if quote_symbol is not None: self._values["quote_symbol"] = quote_symbol

        @property
        def allow_single_column(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnClassifier.CsvClassifierProperty.AllowSingleColumn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-allowsinglecolumn
            """
            return self._values.get('allow_single_column')

        @property
        def contains_header(self) -> typing.Optional[str]:
            """``CfnClassifier.CsvClassifierProperty.ContainsHeader``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-containsheader
            """
            return self._values.get('contains_header')

        @property
        def delimiter(self) -> typing.Optional[str]:
            """``CfnClassifier.CsvClassifierProperty.Delimiter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-delimiter
            """
            return self._values.get('delimiter')

        @property
        def disable_value_trimming(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnClassifier.CsvClassifierProperty.DisableValueTrimming``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-disablevaluetrimming
            """
            return self._values.get('disable_value_trimming')

        @property
        def header(self) -> typing.Optional[typing.List[str]]:
            """``CfnClassifier.CsvClassifierProperty.Header``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-header
            """
            return self._values.get('header')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnClassifier.CsvClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-name
            """
            return self._values.get('name')

        @property
        def quote_symbol(self) -> typing.Optional[str]:
            """``CfnClassifier.CsvClassifierProperty.QuoteSymbol``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-csvclassifier.html#cfn-glue-classifier-csvclassifier-quotesymbol
            """
            return self._values.get('quote_symbol')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CsvClassifierProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.GrokClassifierProperty", jsii_struct_bases=[], name_mapping={'classification': 'classification', 'grok_pattern': 'grokPattern', 'custom_patterns': 'customPatterns', 'name': 'name'})
    class GrokClassifierProperty():
        def __init__(self, *, classification: str, grok_pattern: str, custom_patterns: typing.Optional[str]=None, name: typing.Optional[str]=None):
            """
            :param classification: ``CfnClassifier.GrokClassifierProperty.Classification``.
            :param grok_pattern: ``CfnClassifier.GrokClassifierProperty.GrokPattern``.
            :param custom_patterns: ``CfnClassifier.GrokClassifierProperty.CustomPatterns``.
            :param name: ``CfnClassifier.GrokClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html
            """
            self._values = {
                'classification': classification,
                'grok_pattern': grok_pattern,
            }
            if custom_patterns is not None: self._values["custom_patterns"] = custom_patterns
            if name is not None: self._values["name"] = name

        @property
        def classification(self) -> str:
            """``CfnClassifier.GrokClassifierProperty.Classification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-classification
            """
            return self._values.get('classification')

        @property
        def grok_pattern(self) -> str:
            """``CfnClassifier.GrokClassifierProperty.GrokPattern``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-grokpattern
            """
            return self._values.get('grok_pattern')

        @property
        def custom_patterns(self) -> typing.Optional[str]:
            """``CfnClassifier.GrokClassifierProperty.CustomPatterns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-custompatterns
            """
            return self._values.get('custom_patterns')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnClassifier.GrokClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-grokclassifier.html#cfn-glue-classifier-grokclassifier-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GrokClassifierProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.JsonClassifierProperty", jsii_struct_bases=[], name_mapping={'json_path': 'jsonPath', 'name': 'name'})
    class JsonClassifierProperty():
        def __init__(self, *, json_path: str, name: typing.Optional[str]=None):
            """
            :param json_path: ``CfnClassifier.JsonClassifierProperty.JsonPath``.
            :param name: ``CfnClassifier.JsonClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html
            """
            self._values = {
                'json_path': json_path,
            }
            if name is not None: self._values["name"] = name

        @property
        def json_path(self) -> str:
            """``CfnClassifier.JsonClassifierProperty.JsonPath``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html#cfn-glue-classifier-jsonclassifier-jsonpath
            """
            return self._values.get('json_path')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnClassifier.JsonClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-jsonclassifier.html#cfn-glue-classifier-jsonclassifier-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JsonClassifierProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifier.XMLClassifierProperty", jsii_struct_bases=[], name_mapping={'classification': 'classification', 'row_tag': 'rowTag', 'name': 'name'})
    class XMLClassifierProperty():
        def __init__(self, *, classification: str, row_tag: str, name: typing.Optional[str]=None):
            """
            :param classification: ``CfnClassifier.XMLClassifierProperty.Classification``.
            :param row_tag: ``CfnClassifier.XMLClassifierProperty.RowTag``.
            :param name: ``CfnClassifier.XMLClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html
            """
            self._values = {
                'classification': classification,
                'row_tag': row_tag,
            }
            if name is not None: self._values["name"] = name

        @property
        def classification(self) -> str:
            """``CfnClassifier.XMLClassifierProperty.Classification``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-classification
            """
            return self._values.get('classification')

        @property
        def row_tag(self) -> str:
            """``CfnClassifier.XMLClassifierProperty.RowTag``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-rowtag
            """
            return self._values.get('row_tag')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnClassifier.XMLClassifierProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-classifier-xmlclassifier.html#cfn-glue-classifier-xmlclassifier-name
            """
            return self._values.get('name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'XMLClassifierProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnClassifierProps", jsii_struct_bases=[], name_mapping={'csv_classifier': 'csvClassifier', 'grok_classifier': 'grokClassifier', 'json_classifier': 'jsonClassifier', 'xml_classifier': 'xmlClassifier'})
class CfnClassifierProps():
    def __init__(self, *, csv_classifier: typing.Optional[typing.Union[typing.Optional["CfnClassifier.CsvClassifierProperty"], typing.Optional[aws_cdk.core.IResolvable]]]=None, grok_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.GrokClassifierProperty"]]]=None, json_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.JsonClassifierProperty"]]]=None, xml_classifier: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.XMLClassifierProperty"]]]=None):
        """Properties for defining a ``AWS::Glue::Classifier``.

        :param csv_classifier: ``AWS::Glue::Classifier.CsvClassifier``.
        :param grok_classifier: ``AWS::Glue::Classifier.GrokClassifier``.
        :param json_classifier: ``AWS::Glue::Classifier.JsonClassifier``.
        :param xml_classifier: ``AWS::Glue::Classifier.XMLClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html
        """
        self._values = {
        }
        if csv_classifier is not None: self._values["csv_classifier"] = csv_classifier
        if grok_classifier is not None: self._values["grok_classifier"] = grok_classifier
        if json_classifier is not None: self._values["json_classifier"] = json_classifier
        if xml_classifier is not None: self._values["xml_classifier"] = xml_classifier

    @property
    def csv_classifier(self) -> typing.Optional[typing.Union[typing.Optional["CfnClassifier.CsvClassifierProperty"], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Glue::Classifier.CsvClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-csvclassifier
        """
        return self._values.get('csv_classifier')

    @property
    def grok_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.GrokClassifierProperty"]]]:
        """``AWS::Glue::Classifier.GrokClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-grokclassifier
        """
        return self._values.get('grok_classifier')

    @property
    def json_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.JsonClassifierProperty"]]]:
        """``AWS::Glue::Classifier.JsonClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-jsonclassifier
        """
        return self._values.get('json_classifier')

    @property
    def xml_classifier(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnClassifier.XMLClassifierProperty"]]]:
        """``AWS::Glue::Classifier.XMLClassifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-classifier.html#cfn-glue-classifier-xmlclassifier
        """
        return self._values.get('xml_classifier')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnClassifierProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnConnection(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnConnection"):
    """A CloudFormation ``AWS::Glue::Connection``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Connection
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, catalog_id: str, connection_input: typing.Union[aws_cdk.core.IResolvable, "ConnectionInputProperty"]) -> None:
        """Create a new ``AWS::Glue::Connection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param catalog_id: ``AWS::Glue::Connection.CatalogId``.
        :param connection_input: ``AWS::Glue::Connection.ConnectionInput``.
        """
        props = CfnConnectionProps(catalog_id=catalog_id, connection_input=connection_input)

        jsii.create(CfnConnection, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """``AWS::Glue::Connection.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-catalogid
        """
        return jsii.get(self, "catalogId")

    @catalog_id.setter
    def catalog_id(self, value: str):
        return jsii.set(self, "catalogId", value)

    @property
    @jsii.member(jsii_name="connectionInput")
    def connection_input(self) -> typing.Union[aws_cdk.core.IResolvable, "ConnectionInputProperty"]:
        """``AWS::Glue::Connection.ConnectionInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-connectioninput
        """
        return jsii.get(self, "connectionInput")

    @connection_input.setter
    def connection_input(self, value: typing.Union[aws_cdk.core.IResolvable, "ConnectionInputProperty"]):
        return jsii.set(self, "connectionInput", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnection.ConnectionInputProperty", jsii_struct_bases=[], name_mapping={'connection_properties': 'connectionProperties', 'connection_type': 'connectionType', 'description': 'description', 'match_criteria': 'matchCriteria', 'name': 'name', 'physical_connection_requirements': 'physicalConnectionRequirements'})
    class ConnectionInputProperty():
        def __init__(self, *, connection_properties: typing.Any, connection_type: str, description: typing.Optional[str]=None, match_criteria: typing.Optional[typing.List[str]]=None, name: typing.Optional[str]=None, physical_connection_requirements: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnConnection.PhysicalConnectionRequirementsProperty"]]]=None):
            """
            :param connection_properties: ``CfnConnection.ConnectionInputProperty.ConnectionProperties``.
            :param connection_type: ``CfnConnection.ConnectionInputProperty.ConnectionType``.
            :param description: ``CfnConnection.ConnectionInputProperty.Description``.
            :param match_criteria: ``CfnConnection.ConnectionInputProperty.MatchCriteria``.
            :param name: ``CfnConnection.ConnectionInputProperty.Name``.
            :param physical_connection_requirements: ``CfnConnection.ConnectionInputProperty.PhysicalConnectionRequirements``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html
            """
            self._values = {
                'connection_properties': connection_properties,
                'connection_type': connection_type,
            }
            if description is not None: self._values["description"] = description
            if match_criteria is not None: self._values["match_criteria"] = match_criteria
            if name is not None: self._values["name"] = name
            if physical_connection_requirements is not None: self._values["physical_connection_requirements"] = physical_connection_requirements

        @property
        def connection_properties(self) -> typing.Any:
            """``CfnConnection.ConnectionInputProperty.ConnectionProperties``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectionproperties
            """
            return self._values.get('connection_properties')

        @property
        def connection_type(self) -> str:
            """``CfnConnection.ConnectionInputProperty.ConnectionType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype
            """
            return self._values.get('connection_type')

        @property
        def description(self) -> typing.Optional[str]:
            """``CfnConnection.ConnectionInputProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-description
            """
            return self._values.get('description')

        @property
        def match_criteria(self) -> typing.Optional[typing.List[str]]:
            """``CfnConnection.ConnectionInputProperty.MatchCriteria``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-matchcriteria
            """
            return self._values.get('match_criteria')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnConnection.ConnectionInputProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-name
            """
            return self._values.get('name')

        @property
        def physical_connection_requirements(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnConnection.PhysicalConnectionRequirementsProperty"]]]:
            """``CfnConnection.ConnectionInputProperty.PhysicalConnectionRequirements``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-physicalconnectionrequirements
            """
            return self._values.get('physical_connection_requirements')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConnectionInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnection.PhysicalConnectionRequirementsProperty", jsii_struct_bases=[], name_mapping={'availability_zone': 'availabilityZone', 'security_group_id_list': 'securityGroupIdList', 'subnet_id': 'subnetId'})
    class PhysicalConnectionRequirementsProperty():
        def __init__(self, *, availability_zone: typing.Optional[str]=None, security_group_id_list: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None):
            """
            :param availability_zone: ``CfnConnection.PhysicalConnectionRequirementsProperty.AvailabilityZone``.
            :param security_group_id_list: ``CfnConnection.PhysicalConnectionRequirementsProperty.SecurityGroupIdList``.
            :param subnet_id: ``CfnConnection.PhysicalConnectionRequirementsProperty.SubnetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html
            """
            self._values = {
            }
            if availability_zone is not None: self._values["availability_zone"] = availability_zone
            if security_group_id_list is not None: self._values["security_group_id_list"] = security_group_id_list
            if subnet_id is not None: self._values["subnet_id"] = subnet_id

        @property
        def availability_zone(self) -> typing.Optional[str]:
            """``CfnConnection.PhysicalConnectionRequirementsProperty.AvailabilityZone``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-availabilityzone
            """
            return self._values.get('availability_zone')

        @property
        def security_group_id_list(self) -> typing.Optional[typing.List[str]]:
            """``CfnConnection.PhysicalConnectionRequirementsProperty.SecurityGroupIdList``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-securitygroupidlist
            """
            return self._values.get('security_group_id_list')

        @property
        def subnet_id(self) -> typing.Optional[str]:
            """``CfnConnection.PhysicalConnectionRequirementsProperty.SubnetId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-physicalconnectionrequirements.html#cfn-glue-connection-physicalconnectionrequirements-subnetid
            """
            return self._values.get('subnet_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PhysicalConnectionRequirementsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnConnectionProps", jsii_struct_bases=[], name_mapping={'catalog_id': 'catalogId', 'connection_input': 'connectionInput'})
class CfnConnectionProps():
    def __init__(self, *, catalog_id: str, connection_input: typing.Union[aws_cdk.core.IResolvable, "CfnConnection.ConnectionInputProperty"]):
        """Properties for defining a ``AWS::Glue::Connection``.

        :param catalog_id: ``AWS::Glue::Connection.CatalogId``.
        :param connection_input: ``AWS::Glue::Connection.ConnectionInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html
        """
        self._values = {
            'catalog_id': catalog_id,
            'connection_input': connection_input,
        }

    @property
    def catalog_id(self) -> str:
        """``AWS::Glue::Connection.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-catalogid
        """
        return self._values.get('catalog_id')

    @property
    def connection_input(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnConnection.ConnectionInputProperty"]:
        """``AWS::Glue::Connection.ConnectionInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-connection.html#cfn-glue-connection-connectioninput
        """
        return self._values.get('connection_input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnConnectionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnCrawler(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnCrawler"):
    """A CloudFormation ``AWS::Glue::Crawler``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Crawler
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, role: str, targets: typing.Union[aws_cdk.core.IResolvable, "TargetsProperty"], classifiers: typing.Optional[typing.List[str]]=None, configuration: typing.Optional[str]=None, crawler_security_configuration: typing.Optional[str]=None, database_name: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schedule: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ScheduleProperty"]]]=None, schema_change_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SchemaChangePolicyProperty"]]]=None, table_prefix: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::Glue::Crawler``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param role: ``AWS::Glue::Crawler.Role``.
        :param targets: ``AWS::Glue::Crawler.Targets``.
        :param classifiers: ``AWS::Glue::Crawler.Classifiers``.
        :param configuration: ``AWS::Glue::Crawler.Configuration``.
        :param crawler_security_configuration: ``AWS::Glue::Crawler.CrawlerSecurityConfiguration``.
        :param database_name: ``AWS::Glue::Crawler.DatabaseName``.
        :param description: ``AWS::Glue::Crawler.Description``.
        :param name: ``AWS::Glue::Crawler.Name``.
        :param schedule: ``AWS::Glue::Crawler.Schedule``.
        :param schema_change_policy: ``AWS::Glue::Crawler.SchemaChangePolicy``.
        :param table_prefix: ``AWS::Glue::Crawler.TablePrefix``.
        :param tags: ``AWS::Glue::Crawler.Tags``.
        """
        props = CfnCrawlerProps(role=role, targets=targets, classifiers=classifiers, configuration=configuration, crawler_security_configuration=crawler_security_configuration, database_name=database_name, description=description, name=name, schedule=schedule, schema_change_policy=schema_change_policy, table_prefix=table_prefix, tags=tags)

        jsii.create(CfnCrawler, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Glue::Crawler.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        """``AWS::Glue::Crawler.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: str):
        return jsii.set(self, "role", value)

    @property
    @jsii.member(jsii_name="targets")
    def targets(self) -> typing.Union[aws_cdk.core.IResolvable, "TargetsProperty"]:
        """``AWS::Glue::Crawler.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-targets
        """
        return jsii.get(self, "targets")

    @targets.setter
    def targets(self, value: typing.Union[aws_cdk.core.IResolvable, "TargetsProperty"]):
        return jsii.set(self, "targets", value)

    @property
    @jsii.member(jsii_name="classifiers")
    def classifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Glue::Crawler.Classifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-classifiers
        """
        return jsii.get(self, "classifiers")

    @classifiers.setter
    def classifiers(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "classifiers", value)

    @property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Configuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-configuration
        """
        return jsii.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: typing.Optional[str]):
        return jsii.set(self, "configuration", value)

    @property
    @jsii.member(jsii_name="crawlerSecurityConfiguration")
    def crawler_security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.CrawlerSecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-crawlersecurityconfiguration
        """
        return jsii.get(self, "crawlerSecurityConfiguration")

    @crawler_security_configuration.setter
    def crawler_security_configuration(self, value: typing.Optional[str]):
        return jsii.set(self, "crawlerSecurityConfiguration", value)

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter
    def database_name(self, value: typing.Optional[str]):
        return jsii.set(self, "databaseName", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ScheduleProperty"]]]:
        """``AWS::Glue::Crawler.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ScheduleProperty"]]]):
        return jsii.set(self, "schedule", value)

    @property
    @jsii.member(jsii_name="schemaChangePolicy")
    def schema_change_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SchemaChangePolicyProperty"]]]:
        """``AWS::Glue::Crawler.SchemaChangePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schemachangepolicy
        """
        return jsii.get(self, "schemaChangePolicy")

    @schema_change_policy.setter
    def schema_change_policy(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["SchemaChangePolicyProperty"]]]):
        return jsii.set(self, "schemaChangePolicy", value)

    @property
    @jsii.member(jsii_name="tablePrefix")
    def table_prefix(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.TablePrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tableprefix
        """
        return jsii.get(self, "tablePrefix")

    @table_prefix.setter
    def table_prefix(self, value: typing.Optional[str]):
        return jsii.set(self, "tablePrefix", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.CatalogTargetProperty", jsii_struct_bases=[], name_mapping={'database_name': 'databaseName', 'tables': 'tables'})
    class CatalogTargetProperty():
        def __init__(self, *, database_name: typing.Optional[str]=None, tables: typing.Optional[typing.List[str]]=None):
            """
            :param database_name: ``CfnCrawler.CatalogTargetProperty.DatabaseName``.
            :param tables: ``CfnCrawler.CatalogTargetProperty.Tables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html
            """
            self._values = {
            }
            if database_name is not None: self._values["database_name"] = database_name
            if tables is not None: self._values["tables"] = tables

        @property
        def database_name(self) -> typing.Optional[str]:
            """``CfnCrawler.CatalogTargetProperty.DatabaseName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-databasename
            """
            return self._values.get('database_name')

        @property
        def tables(self) -> typing.Optional[typing.List[str]]:
            """``CfnCrawler.CatalogTargetProperty.Tables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-catalogtarget.html#cfn-glue-crawler-catalogtarget-tables
            """
            return self._values.get('tables')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CatalogTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.DynamoDBTargetProperty", jsii_struct_bases=[], name_mapping={'path': 'path'})
    class DynamoDBTargetProperty():
        def __init__(self, *, path: typing.Optional[str]=None):
            """
            :param path: ``CfnCrawler.DynamoDBTargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html
            """
            self._values = {
            }
            if path is not None: self._values["path"] = path

        @property
        def path(self) -> typing.Optional[str]:
            """``CfnCrawler.DynamoDBTargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-dynamodbtarget.html#cfn-glue-crawler-dynamodbtarget-path
            """
            return self._values.get('path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DynamoDBTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.JdbcTargetProperty", jsii_struct_bases=[], name_mapping={'connection_name': 'connectionName', 'exclusions': 'exclusions', 'path': 'path'})
    class JdbcTargetProperty():
        def __init__(self, *, connection_name: typing.Optional[str]=None, exclusions: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None):
            """
            :param connection_name: ``CfnCrawler.JdbcTargetProperty.ConnectionName``.
            :param exclusions: ``CfnCrawler.JdbcTargetProperty.Exclusions``.
            :param path: ``CfnCrawler.JdbcTargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html
            """
            self._values = {
            }
            if connection_name is not None: self._values["connection_name"] = connection_name
            if exclusions is not None: self._values["exclusions"] = exclusions
            if path is not None: self._values["path"] = path

        @property
        def connection_name(self) -> typing.Optional[str]:
            """``CfnCrawler.JdbcTargetProperty.ConnectionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-connectionname
            """
            return self._values.get('connection_name')

        @property
        def exclusions(self) -> typing.Optional[typing.List[str]]:
            """``CfnCrawler.JdbcTargetProperty.Exclusions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-exclusions
            """
            return self._values.get('exclusions')

        @property
        def path(self) -> typing.Optional[str]:
            """``CfnCrawler.JdbcTargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-jdbctarget.html#cfn-glue-crawler-jdbctarget-path
            """
            return self._values.get('path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JdbcTargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.S3TargetProperty", jsii_struct_bases=[], name_mapping={'exclusions': 'exclusions', 'path': 'path'})
    class S3TargetProperty():
        def __init__(self, *, exclusions: typing.Optional[typing.List[str]]=None, path: typing.Optional[str]=None):
            """
            :param exclusions: ``CfnCrawler.S3TargetProperty.Exclusions``.
            :param path: ``CfnCrawler.S3TargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html
            """
            self._values = {
            }
            if exclusions is not None: self._values["exclusions"] = exclusions
            if path is not None: self._values["path"] = path

        @property
        def exclusions(self) -> typing.Optional[typing.List[str]]:
            """``CfnCrawler.S3TargetProperty.Exclusions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-exclusions
            """
            return self._values.get('exclusions')

        @property
        def path(self) -> typing.Optional[str]:
            """``CfnCrawler.S3TargetProperty.Path``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-s3target.html#cfn-glue-crawler-s3target-path
            """
            return self._values.get('path')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3TargetProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.ScheduleProperty", jsii_struct_bases=[], name_mapping={'schedule_expression': 'scheduleExpression'})
    class ScheduleProperty():
        def __init__(self, *, schedule_expression: typing.Optional[str]=None):
            """
            :param schedule_expression: ``CfnCrawler.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schedule.html
            """
            self._values = {
            }
            if schedule_expression is not None: self._values["schedule_expression"] = schedule_expression

        @property
        def schedule_expression(self) -> typing.Optional[str]:
            """``CfnCrawler.ScheduleProperty.ScheduleExpression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schedule.html#cfn-glue-crawler-schedule-scheduleexpression
            """
            return self._values.get('schedule_expression')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ScheduleProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.SchemaChangePolicyProperty", jsii_struct_bases=[], name_mapping={'delete_behavior': 'deleteBehavior', 'update_behavior': 'updateBehavior'})
    class SchemaChangePolicyProperty():
        def __init__(self, *, delete_behavior: typing.Optional[str]=None, update_behavior: typing.Optional[str]=None):
            """
            :param delete_behavior: ``CfnCrawler.SchemaChangePolicyProperty.DeleteBehavior``.
            :param update_behavior: ``CfnCrawler.SchemaChangePolicyProperty.UpdateBehavior``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html
            """
            self._values = {
            }
            if delete_behavior is not None: self._values["delete_behavior"] = delete_behavior
            if update_behavior is not None: self._values["update_behavior"] = update_behavior

        @property
        def delete_behavior(self) -> typing.Optional[str]:
            """``CfnCrawler.SchemaChangePolicyProperty.DeleteBehavior``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-deletebehavior
            """
            return self._values.get('delete_behavior')

        @property
        def update_behavior(self) -> typing.Optional[str]:
            """``CfnCrawler.SchemaChangePolicyProperty.UpdateBehavior``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-schemachangepolicy.html#cfn-glue-crawler-schemachangepolicy-updatebehavior
            """
            return self._values.get('update_behavior')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SchemaChangePolicyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawler.TargetsProperty", jsii_struct_bases=[], name_mapping={'catalog_targets': 'catalogTargets', 'dynamo_db_targets': 'dynamoDbTargets', 'jdbc_targets': 'jdbcTargets', 's3_targets': 's3Targets'})
    class TargetsProperty():
        def __init__(self, *, catalog_targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.CatalogTargetProperty"]]]]]=None, dynamo_db_targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.DynamoDBTargetProperty"]]]]]=None, jdbc_targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.JdbcTargetProperty"]]]]]=None, s3_targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.S3TargetProperty"]]]]]=None):
            """
            :param catalog_targets: ``CfnCrawler.TargetsProperty.CatalogTargets``.
            :param dynamo_db_targets: ``CfnCrawler.TargetsProperty.DynamoDBTargets``.
            :param jdbc_targets: ``CfnCrawler.TargetsProperty.JdbcTargets``.
            :param s3_targets: ``CfnCrawler.TargetsProperty.S3Targets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html
            """
            self._values = {
            }
            if catalog_targets is not None: self._values["catalog_targets"] = catalog_targets
            if dynamo_db_targets is not None: self._values["dynamo_db_targets"] = dynamo_db_targets
            if jdbc_targets is not None: self._values["jdbc_targets"] = jdbc_targets
            if s3_targets is not None: self._values["s3_targets"] = s3_targets

        @property
        def catalog_targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.CatalogTargetProperty"]]]]]:
            """``CfnCrawler.TargetsProperty.CatalogTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-catalogtargets
            """
            return self._values.get('catalog_targets')

        @property
        def dynamo_db_targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.DynamoDBTargetProperty"]]]]]:
            """``CfnCrawler.TargetsProperty.DynamoDBTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-dynamodbtargets
            """
            return self._values.get('dynamo_db_targets')

        @property
        def jdbc_targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.JdbcTargetProperty"]]]]]:
            """``CfnCrawler.TargetsProperty.JdbcTargets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-jdbctargets
            """
            return self._values.get('jdbc_targets')

        @property
        def s3_targets(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.S3TargetProperty"]]]]]:
            """``CfnCrawler.TargetsProperty.S3Targets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-crawler-targets.html#cfn-glue-crawler-targets-s3targets
            """
            return self._values.get('s3_targets')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TargetsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnCrawlerProps", jsii_struct_bases=[], name_mapping={'role': 'role', 'targets': 'targets', 'classifiers': 'classifiers', 'configuration': 'configuration', 'crawler_security_configuration': 'crawlerSecurityConfiguration', 'database_name': 'databaseName', 'description': 'description', 'name': 'name', 'schedule': 'schedule', 'schema_change_policy': 'schemaChangePolicy', 'table_prefix': 'tablePrefix', 'tags': 'tags'})
class CfnCrawlerProps():
    def __init__(self, *, role: str, targets: typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.TargetsProperty"], classifiers: typing.Optional[typing.List[str]]=None, configuration: typing.Optional[str]=None, crawler_security_configuration: typing.Optional[str]=None, database_name: typing.Optional[str]=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, schedule: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCrawler.ScheduleProperty"]]]=None, schema_change_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCrawler.SchemaChangePolicyProperty"]]]=None, table_prefix: typing.Optional[str]=None, tags: typing.Any=None):
        """Properties for defining a ``AWS::Glue::Crawler``.

        :param role: ``AWS::Glue::Crawler.Role``.
        :param targets: ``AWS::Glue::Crawler.Targets``.
        :param classifiers: ``AWS::Glue::Crawler.Classifiers``.
        :param configuration: ``AWS::Glue::Crawler.Configuration``.
        :param crawler_security_configuration: ``AWS::Glue::Crawler.CrawlerSecurityConfiguration``.
        :param database_name: ``AWS::Glue::Crawler.DatabaseName``.
        :param description: ``AWS::Glue::Crawler.Description``.
        :param name: ``AWS::Glue::Crawler.Name``.
        :param schedule: ``AWS::Glue::Crawler.Schedule``.
        :param schema_change_policy: ``AWS::Glue::Crawler.SchemaChangePolicy``.
        :param table_prefix: ``AWS::Glue::Crawler.TablePrefix``.
        :param tags: ``AWS::Glue::Crawler.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html
        """
        self._values = {
            'role': role,
            'targets': targets,
        }
        if classifiers is not None: self._values["classifiers"] = classifiers
        if configuration is not None: self._values["configuration"] = configuration
        if crawler_security_configuration is not None: self._values["crawler_security_configuration"] = crawler_security_configuration
        if database_name is not None: self._values["database_name"] = database_name
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name
        if schedule is not None: self._values["schedule"] = schedule
        if schema_change_policy is not None: self._values["schema_change_policy"] = schema_change_policy
        if table_prefix is not None: self._values["table_prefix"] = table_prefix
        if tags is not None: self._values["tags"] = tags

    @property
    def role(self) -> str:
        """``AWS::Glue::Crawler.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-role
        """
        return self._values.get('role')

    @property
    def targets(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnCrawler.TargetsProperty"]:
        """``AWS::Glue::Crawler.Targets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-targets
        """
        return self._values.get('targets')

    @property
    def classifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Glue::Crawler.Classifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-classifiers
        """
        return self._values.get('classifiers')

    @property
    def configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Configuration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-configuration
        """
        return self._values.get('configuration')

    @property
    def crawler_security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.CrawlerSecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-crawlersecurityconfiguration
        """
        return self._values.get('crawler_security_configuration')

    @property
    def database_name(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-databasename
        """
        return self._values.get('database_name')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-description
        """
        return self._values.get('description')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-name
        """
        return self._values.get('name')

    @property
    def schedule(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCrawler.ScheduleProperty"]]]:
        """``AWS::Glue::Crawler.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schedule
        """
        return self._values.get('schedule')

    @property
    def schema_change_policy(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnCrawler.SchemaChangePolicyProperty"]]]:
        """``AWS::Glue::Crawler.SchemaChangePolicy``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-schemachangepolicy
        """
        return self._values.get('schema_change_policy')

    @property
    def table_prefix(self) -> typing.Optional[str]:
        """``AWS::Glue::Crawler.TablePrefix``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tableprefix
        """
        return self._values.get('table_prefix')

    @property
    def tags(self) -> typing.Any:
        """``AWS::Glue::Crawler.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-crawler.html#cfn-glue-crawler-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnCrawlerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDataCatalogEncryptionSettings(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnDataCatalogEncryptionSettings"):
    """A CloudFormation ``AWS::Glue::DataCatalogEncryptionSettings``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::DataCatalogEncryptionSettings
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, catalog_id: str, data_catalog_encryption_settings: typing.Union[aws_cdk.core.IResolvable, "DataCatalogEncryptionSettingsProperty"]) -> None:
        """Create a new ``AWS::Glue::DataCatalogEncryptionSettings``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param catalog_id: ``AWS::Glue::DataCatalogEncryptionSettings.CatalogId``.
        :param data_catalog_encryption_settings: ``AWS::Glue::DataCatalogEncryptionSettings.DataCatalogEncryptionSettings``.
        """
        props = CfnDataCatalogEncryptionSettingsProps(catalog_id=catalog_id, data_catalog_encryption_settings=data_catalog_encryption_settings)

        jsii.create(CfnDataCatalogEncryptionSettings, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """``AWS::Glue::DataCatalogEncryptionSettings.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-catalogid
        """
        return jsii.get(self, "catalogId")

    @catalog_id.setter
    def catalog_id(self, value: str):
        return jsii.set(self, "catalogId", value)

    @property
    @jsii.member(jsii_name="dataCatalogEncryptionSettings")
    def data_catalog_encryption_settings(self) -> typing.Union[aws_cdk.core.IResolvable, "DataCatalogEncryptionSettingsProperty"]:
        """``AWS::Glue::DataCatalogEncryptionSettings.DataCatalogEncryptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings
        """
        return jsii.get(self, "dataCatalogEncryptionSettings")

    @data_catalog_encryption_settings.setter
    def data_catalog_encryption_settings(self, value: typing.Union[aws_cdk.core.IResolvable, "DataCatalogEncryptionSettingsProperty"]):
        return jsii.set(self, "dataCatalogEncryptionSettings", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty", jsii_struct_bases=[], name_mapping={'kms_key_id': 'kmsKeyId', 'return_connection_password_encrypted': 'returnConnectionPasswordEncrypted'})
    class ConnectionPasswordEncryptionProperty():
        def __init__(self, *, kms_key_id: typing.Optional[str]=None, return_connection_password_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param kms_key_id: ``CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty.KmsKeyId``.
            :param return_connection_password_encrypted: ``CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty.ReturnConnectionPasswordEncrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html
            """
            self._values = {
            }
            if kms_key_id is not None: self._values["kms_key_id"] = kms_key_id
            if return_connection_password_encrypted is not None: self._values["return_connection_password_encrypted"] = return_connection_password_encrypted

        @property
        def kms_key_id(self) -> typing.Optional[str]:
            """``CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty.KmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html#cfn-glue-datacatalogencryptionsettings-connectionpasswordencryption-kmskeyid
            """
            return self._values.get('kms_key_id')

        @property
        def return_connection_password_encrypted(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty.ReturnConnectionPasswordEncrypted``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-connectionpasswordencryption.html#cfn-glue-datacatalogencryptionsettings-connectionpasswordencryption-returnconnectionpasswordencrypted
            """
            return self._values.get('return_connection_password_encrypted')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConnectionPasswordEncryptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty", jsii_struct_bases=[], name_mapping={'connection_password_encryption': 'connectionPasswordEncryption', 'encryption_at_rest': 'encryptionAtRest'})
    class DataCatalogEncryptionSettingsProperty():
        def __init__(self, *, connection_password_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty"]]]=None, encryption_at_rest: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty"]]]=None):
            """
            :param connection_password_encryption: ``CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty.ConnectionPasswordEncryption``.
            :param encryption_at_rest: ``CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty.EncryptionAtRest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html
            """
            self._values = {
            }
            if connection_password_encryption is not None: self._values["connection_password_encryption"] = connection_password_encryption
            if encryption_at_rest is not None: self._values["encryption_at_rest"] = encryption_at_rest

        @property
        def connection_password_encryption(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDataCatalogEncryptionSettings.ConnectionPasswordEncryptionProperty"]]]:
            """``CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty.ConnectionPasswordEncryption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings-connectionpasswordencryption
            """
            return self._values.get('connection_password_encryption')

        @property
        def encryption_at_rest(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty"]]]:
            """``CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty.EncryptionAtRest``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings-encryptionatrest
            """
            return self._values.get('encryption_at_rest')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DataCatalogEncryptionSettingsProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty", jsii_struct_bases=[], name_mapping={'catalog_encryption_mode': 'catalogEncryptionMode', 'sse_aws_kms_key_id': 'sseAwsKmsKeyId'})
    class EncryptionAtRestProperty():
        def __init__(self, *, catalog_encryption_mode: typing.Optional[str]=None, sse_aws_kms_key_id: typing.Optional[str]=None):
            """
            :param catalog_encryption_mode: ``CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty.CatalogEncryptionMode``.
            :param sse_aws_kms_key_id: ``CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty.SseAwsKmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html
            """
            self._values = {
            }
            if catalog_encryption_mode is not None: self._values["catalog_encryption_mode"] = catalog_encryption_mode
            if sse_aws_kms_key_id is not None: self._values["sse_aws_kms_key_id"] = sse_aws_kms_key_id

        @property
        def catalog_encryption_mode(self) -> typing.Optional[str]:
            """``CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty.CatalogEncryptionMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html#cfn-glue-datacatalogencryptionsettings-encryptionatrest-catalogencryptionmode
            """
            return self._values.get('catalog_encryption_mode')

        @property
        def sse_aws_kms_key_id(self) -> typing.Optional[str]:
            """``CfnDataCatalogEncryptionSettings.EncryptionAtRestProperty.SseAwsKmsKeyId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-datacatalogencryptionsettings-encryptionatrest.html#cfn-glue-datacatalogencryptionsettings-encryptionatrest-sseawskmskeyid
            """
            return self._values.get('sse_aws_kms_key_id')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionAtRestProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDataCatalogEncryptionSettingsProps", jsii_struct_bases=[], name_mapping={'catalog_id': 'catalogId', 'data_catalog_encryption_settings': 'dataCatalogEncryptionSettings'})
class CfnDataCatalogEncryptionSettingsProps():
    def __init__(self, *, catalog_id: str, data_catalog_encryption_settings: typing.Union[aws_cdk.core.IResolvable, "CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty"]):
        """Properties for defining a ``AWS::Glue::DataCatalogEncryptionSettings``.

        :param catalog_id: ``AWS::Glue::DataCatalogEncryptionSettings.CatalogId``.
        :param data_catalog_encryption_settings: ``AWS::Glue::DataCatalogEncryptionSettings.DataCatalogEncryptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html
        """
        self._values = {
            'catalog_id': catalog_id,
            'data_catalog_encryption_settings': data_catalog_encryption_settings,
        }

    @property
    def catalog_id(self) -> str:
        """``AWS::Glue::DataCatalogEncryptionSettings.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-catalogid
        """
        return self._values.get('catalog_id')

    @property
    def data_catalog_encryption_settings(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnDataCatalogEncryptionSettings.DataCatalogEncryptionSettingsProperty"]:
        """``AWS::Glue::DataCatalogEncryptionSettings.DataCatalogEncryptionSettings``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-datacatalogencryptionsettings.html#cfn-glue-datacatalogencryptionsettings-datacatalogencryptionsettings
        """
        return self._values.get('data_catalog_encryption_settings')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDataCatalogEncryptionSettingsProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDatabase(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnDatabase"):
    """A CloudFormation ``AWS::Glue::Database``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Database
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, catalog_id: str, database_input: typing.Union[aws_cdk.core.IResolvable, "DatabaseInputProperty"]) -> None:
        """Create a new ``AWS::Glue::Database``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param catalog_id: ``AWS::Glue::Database.CatalogId``.
        :param database_input: ``AWS::Glue::Database.DatabaseInput``.
        """
        props = CfnDatabaseProps(catalog_id=catalog_id, database_input=database_input)

        jsii.create(CfnDatabase, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """``AWS::Glue::Database.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-catalogid
        """
        return jsii.get(self, "catalogId")

    @catalog_id.setter
    def catalog_id(self, value: str):
        return jsii.set(self, "catalogId", value)

    @property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Union[aws_cdk.core.IResolvable, "DatabaseInputProperty"]:
        """``AWS::Glue::Database.DatabaseInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-databaseinput
        """
        return jsii.get(self, "databaseInput")

    @database_input.setter
    def database_input(self, value: typing.Union[aws_cdk.core.IResolvable, "DatabaseInputProperty"]):
        return jsii.set(self, "databaseInput", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDatabase.DatabaseInputProperty", jsii_struct_bases=[], name_mapping={'description': 'description', 'location_uri': 'locationUri', 'name': 'name', 'parameters': 'parameters'})
    class DatabaseInputProperty():
        def __init__(self, *, description: typing.Optional[str]=None, location_uri: typing.Optional[str]=None, name: typing.Optional[str]=None, parameters: typing.Any=None):
            """
            :param description: ``CfnDatabase.DatabaseInputProperty.Description``.
            :param location_uri: ``CfnDatabase.DatabaseInputProperty.LocationUri``.
            :param name: ``CfnDatabase.DatabaseInputProperty.Name``.
            :param parameters: ``CfnDatabase.DatabaseInputProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html
            """
            self._values = {
            }
            if description is not None: self._values["description"] = description
            if location_uri is not None: self._values["location_uri"] = location_uri
            if name is not None: self._values["name"] = name
            if parameters is not None: self._values["parameters"] = parameters

        @property
        def description(self) -> typing.Optional[str]:
            """``CfnDatabase.DatabaseInputProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-description
            """
            return self._values.get('description')

        @property
        def location_uri(self) -> typing.Optional[str]:
            """``CfnDatabase.DatabaseInputProperty.LocationUri``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-locationuri
            """
            return self._values.get('location_uri')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnDatabase.DatabaseInputProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-name
            """
            return self._values.get('name')

        @property
        def parameters(self) -> typing.Any:
            """``CfnDatabase.DatabaseInputProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html#cfn-glue-database-databaseinput-parameters
            """
            return self._values.get('parameters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'DatabaseInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDatabaseProps", jsii_struct_bases=[], name_mapping={'catalog_id': 'catalogId', 'database_input': 'databaseInput'})
class CfnDatabaseProps():
    def __init__(self, *, catalog_id: str, database_input: typing.Union[aws_cdk.core.IResolvable, "CfnDatabase.DatabaseInputProperty"]):
        """Properties for defining a ``AWS::Glue::Database``.

        :param catalog_id: ``AWS::Glue::Database.CatalogId``.
        :param database_input: ``AWS::Glue::Database.DatabaseInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html
        """
        self._values = {
            'catalog_id': catalog_id,
            'database_input': database_input,
        }

    @property
    def catalog_id(self) -> str:
        """``AWS::Glue::Database.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-catalogid
        """
        return self._values.get('catalog_id')

    @property
    def database_input(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnDatabase.DatabaseInputProperty"]:
        """``AWS::Glue::Database.DatabaseInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-database.html#cfn-glue-database-databaseinput
        """
        return self._values.get('database_input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDatabaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnDevEndpoint(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnDevEndpoint"):
    """A CloudFormation ``AWS::Glue::DevEndpoint``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::DevEndpoint
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, role_arn: str, arguments: typing.Any=None, endpoint_name: typing.Optional[str]=None, extra_jars_s3_path: typing.Optional[str]=None, extra_python_libs_s3_path: typing.Optional[str]=None, glue_version: typing.Optional[str]=None, number_of_nodes: typing.Optional[jsii.Number]=None, number_of_workers: typing.Optional[jsii.Number]=None, public_key: typing.Optional[str]=None, security_configuration: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Any=None, worker_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Glue::DevEndpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param role_arn: ``AWS::Glue::DevEndpoint.RoleArn``.
        :param arguments: ``AWS::Glue::DevEndpoint.Arguments``.
        :param endpoint_name: ``AWS::Glue::DevEndpoint.EndpointName``.
        :param extra_jars_s3_path: ``AWS::Glue::DevEndpoint.ExtraJarsS3Path``.
        :param extra_python_libs_s3_path: ``AWS::Glue::DevEndpoint.ExtraPythonLibsS3Path``.
        :param glue_version: ``AWS::Glue::DevEndpoint.GlueVersion``.
        :param number_of_nodes: ``AWS::Glue::DevEndpoint.NumberOfNodes``.
        :param number_of_workers: ``AWS::Glue::DevEndpoint.NumberOfWorkers``.
        :param public_key: ``AWS::Glue::DevEndpoint.PublicKey``.
        :param security_configuration: ``AWS::Glue::DevEndpoint.SecurityConfiguration``.
        :param security_group_ids: ``AWS::Glue::DevEndpoint.SecurityGroupIds``.
        :param subnet_id: ``AWS::Glue::DevEndpoint.SubnetId``.
        :param tags: ``AWS::Glue::DevEndpoint.Tags``.
        :param worker_type: ``AWS::Glue::DevEndpoint.WorkerType``.
        """
        props = CfnDevEndpointProps(role_arn=role_arn, arguments=arguments, endpoint_name=endpoint_name, extra_jars_s3_path=extra_jars_s3_path, extra_python_libs_s3_path=extra_python_libs_s3_path, glue_version=glue_version, number_of_nodes=number_of_nodes, number_of_workers=number_of_workers, public_key=public_key, security_configuration=security_configuration, security_group_ids=security_group_ids, subnet_id=subnet_id, tags=tags, worker_type=worker_type)

        jsii.create(CfnDevEndpoint, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Glue::DevEndpoint.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="arguments")
    def arguments(self) -> typing.Any:
        """``AWS::Glue::DevEndpoint.Arguments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-arguments
        """
        return jsii.get(self, "arguments")

    @arguments.setter
    def arguments(self, value: typing.Any):
        return jsii.set(self, "arguments", value)

    @property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::Glue::DevEndpoint.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str):
        return jsii.set(self, "roleArn", value)

    @property
    @jsii.member(jsii_name="endpointName")
    def endpoint_name(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.EndpointName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-endpointname
        """
        return jsii.get(self, "endpointName")

    @endpoint_name.setter
    def endpoint_name(self, value: typing.Optional[str]):
        return jsii.set(self, "endpointName", value)

    @property
    @jsii.member(jsii_name="extraJarsS3Path")
    def extra_jars_s3_path(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.ExtraJarsS3Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrajarss3path
        """
        return jsii.get(self, "extraJarsS3Path")

    @extra_jars_s3_path.setter
    def extra_jars_s3_path(self, value: typing.Optional[str]):
        return jsii.set(self, "extraJarsS3Path", value)

    @property
    @jsii.member(jsii_name="extraPythonLibsS3Path")
    def extra_python_libs_s3_path(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.ExtraPythonLibsS3Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrapythonlibss3path
        """
        return jsii.get(self, "extraPythonLibsS3Path")

    @extra_python_libs_s3_path.setter
    def extra_python_libs_s3_path(self, value: typing.Optional[str]):
        return jsii.set(self, "extraPythonLibsS3Path", value)

    @property
    @jsii.member(jsii_name="glueVersion")
    def glue_version(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.GlueVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-glueversion
        """
        return jsii.get(self, "glueVersion")

    @glue_version.setter
    def glue_version(self, value: typing.Optional[str]):
        return jsii.set(self, "glueVersion", value)

    @property
    @jsii.member(jsii_name="numberOfNodes")
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::DevEndpoint.NumberOfNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofnodes
        """
        return jsii.get(self, "numberOfNodes")

    @number_of_nodes.setter
    def number_of_nodes(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "numberOfNodes", value)

    @property
    @jsii.member(jsii_name="numberOfWorkers")
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::DevEndpoint.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofworkers
        """
        return jsii.get(self, "numberOfWorkers")

    @number_of_workers.setter
    def number_of_workers(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "numberOfWorkers", value)

    @property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.PublicKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-publickey
        """
        return jsii.get(self, "publicKey")

    @public_key.setter
    def public_key(self, value: typing.Optional[str]):
        return jsii.set(self, "publicKey", value)

    @property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.SecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securityconfiguration
        """
        return jsii.get(self, "securityConfiguration")

    @security_configuration.setter
    def security_configuration(self, value: typing.Optional[str]):
        return jsii.set(self, "securityConfiguration", value)

    @property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Glue::DevEndpoint.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securitygroupids
        """
        return jsii.get(self, "securityGroupIds")

    @security_group_ids.setter
    def security_group_ids(self, value: typing.Optional[typing.List[str]]):
        return jsii.set(self, "securityGroupIds", value)

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-subnetid
        """
        return jsii.get(self, "subnetId")

    @subnet_id.setter
    def subnet_id(self, value: typing.Optional[str]):
        return jsii.set(self, "subnetId", value)

    @property
    @jsii.member(jsii_name="workerType")
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-workertype
        """
        return jsii.get(self, "workerType")

    @worker_type.setter
    def worker_type(self, value: typing.Optional[str]):
        return jsii.set(self, "workerType", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnDevEndpointProps", jsii_struct_bases=[], name_mapping={'role_arn': 'roleArn', 'arguments': 'arguments', 'endpoint_name': 'endpointName', 'extra_jars_s3_path': 'extraJarsS3Path', 'extra_python_libs_s3_path': 'extraPythonLibsS3Path', 'glue_version': 'glueVersion', 'number_of_nodes': 'numberOfNodes', 'number_of_workers': 'numberOfWorkers', 'public_key': 'publicKey', 'security_configuration': 'securityConfiguration', 'security_group_ids': 'securityGroupIds', 'subnet_id': 'subnetId', 'tags': 'tags', 'worker_type': 'workerType'})
class CfnDevEndpointProps():
    def __init__(self, *, role_arn: str, arguments: typing.Any=None, endpoint_name: typing.Optional[str]=None, extra_jars_s3_path: typing.Optional[str]=None, extra_python_libs_s3_path: typing.Optional[str]=None, glue_version: typing.Optional[str]=None, number_of_nodes: typing.Optional[jsii.Number]=None, number_of_workers: typing.Optional[jsii.Number]=None, public_key: typing.Optional[str]=None, security_configuration: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Any=None, worker_type: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Glue::DevEndpoint``.

        :param role_arn: ``AWS::Glue::DevEndpoint.RoleArn``.
        :param arguments: ``AWS::Glue::DevEndpoint.Arguments``.
        :param endpoint_name: ``AWS::Glue::DevEndpoint.EndpointName``.
        :param extra_jars_s3_path: ``AWS::Glue::DevEndpoint.ExtraJarsS3Path``.
        :param extra_python_libs_s3_path: ``AWS::Glue::DevEndpoint.ExtraPythonLibsS3Path``.
        :param glue_version: ``AWS::Glue::DevEndpoint.GlueVersion``.
        :param number_of_nodes: ``AWS::Glue::DevEndpoint.NumberOfNodes``.
        :param number_of_workers: ``AWS::Glue::DevEndpoint.NumberOfWorkers``.
        :param public_key: ``AWS::Glue::DevEndpoint.PublicKey``.
        :param security_configuration: ``AWS::Glue::DevEndpoint.SecurityConfiguration``.
        :param security_group_ids: ``AWS::Glue::DevEndpoint.SecurityGroupIds``.
        :param subnet_id: ``AWS::Glue::DevEndpoint.SubnetId``.
        :param tags: ``AWS::Glue::DevEndpoint.Tags``.
        :param worker_type: ``AWS::Glue::DevEndpoint.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html
        """
        self._values = {
            'role_arn': role_arn,
        }
        if arguments is not None: self._values["arguments"] = arguments
        if endpoint_name is not None: self._values["endpoint_name"] = endpoint_name
        if extra_jars_s3_path is not None: self._values["extra_jars_s3_path"] = extra_jars_s3_path
        if extra_python_libs_s3_path is not None: self._values["extra_python_libs_s3_path"] = extra_python_libs_s3_path
        if glue_version is not None: self._values["glue_version"] = glue_version
        if number_of_nodes is not None: self._values["number_of_nodes"] = number_of_nodes
        if number_of_workers is not None: self._values["number_of_workers"] = number_of_workers
        if public_key is not None: self._values["public_key"] = public_key
        if security_configuration is not None: self._values["security_configuration"] = security_configuration
        if security_group_ids is not None: self._values["security_group_ids"] = security_group_ids
        if subnet_id is not None: self._values["subnet_id"] = subnet_id
        if tags is not None: self._values["tags"] = tags
        if worker_type is not None: self._values["worker_type"] = worker_type

    @property
    def role_arn(self) -> str:
        """``AWS::Glue::DevEndpoint.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-rolearn
        """
        return self._values.get('role_arn')

    @property
    def arguments(self) -> typing.Any:
        """``AWS::Glue::DevEndpoint.Arguments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-arguments
        """
        return self._values.get('arguments')

    @property
    def endpoint_name(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.EndpointName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-endpointname
        """
        return self._values.get('endpoint_name')

    @property
    def extra_jars_s3_path(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.ExtraJarsS3Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrajarss3path
        """
        return self._values.get('extra_jars_s3_path')

    @property
    def extra_python_libs_s3_path(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.ExtraPythonLibsS3Path``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-extrapythonlibss3path
        """
        return self._values.get('extra_python_libs_s3_path')

    @property
    def glue_version(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.GlueVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-glueversion
        """
        return self._values.get('glue_version')

    @property
    def number_of_nodes(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::DevEndpoint.NumberOfNodes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofnodes
        """
        return self._values.get('number_of_nodes')

    @property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::DevEndpoint.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-numberofworkers
        """
        return self._values.get('number_of_workers')

    @property
    def public_key(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.PublicKey``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-publickey
        """
        return self._values.get('public_key')

    @property
    def security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.SecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securityconfiguration
        """
        return self._values.get('security_configuration')

    @property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Glue::DevEndpoint.SecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-securitygroupids
        """
        return self._values.get('security_group_ids')

    @property
    def subnet_id(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.SubnetId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-subnetid
        """
        return self._values.get('subnet_id')

    @property
    def tags(self) -> typing.Any:
        """``AWS::Glue::DevEndpoint.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-tags
        """
        return self._values.get('tags')

    @property
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::DevEndpoint.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-devendpoint.html#cfn-glue-devendpoint-workertype
        """
        return self._values.get('worker_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnDevEndpointProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnJob(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnJob"):
    """A CloudFormation ``AWS::Glue::Job``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Job
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, command: typing.Union[aws_cdk.core.IResolvable, "JobCommandProperty"], role: str, allocated_capacity: typing.Optional[jsii.Number]=None, connections: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionsListProperty"]]]=None, default_arguments: typing.Any=None, description: typing.Optional[str]=None, execution_property: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ExecutionPropertyProperty"]]]=None, glue_version: typing.Optional[str]=None, log_uri: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, notification_property: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationPropertyProperty"]]]=None, number_of_workers: typing.Optional[jsii.Number]=None, security_configuration: typing.Optional[str]=None, tags: typing.Any=None, timeout: typing.Optional[jsii.Number]=None, worker_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Glue::Job``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param command: ``AWS::Glue::Job.Command``.
        :param role: ``AWS::Glue::Job.Role``.
        :param allocated_capacity: ``AWS::Glue::Job.AllocatedCapacity``.
        :param connections: ``AWS::Glue::Job.Connections``.
        :param default_arguments: ``AWS::Glue::Job.DefaultArguments``.
        :param description: ``AWS::Glue::Job.Description``.
        :param execution_property: ``AWS::Glue::Job.ExecutionProperty``.
        :param glue_version: ``AWS::Glue::Job.GlueVersion``.
        :param log_uri: ``AWS::Glue::Job.LogUri``.
        :param max_capacity: ``AWS::Glue::Job.MaxCapacity``.
        :param max_retries: ``AWS::Glue::Job.MaxRetries``.
        :param name: ``AWS::Glue::Job.Name``.
        :param notification_property: ``AWS::Glue::Job.NotificationProperty``.
        :param number_of_workers: ``AWS::Glue::Job.NumberOfWorkers``.
        :param security_configuration: ``AWS::Glue::Job.SecurityConfiguration``.
        :param tags: ``AWS::Glue::Job.Tags``.
        :param timeout: ``AWS::Glue::Job.Timeout``.
        :param worker_type: ``AWS::Glue::Job.WorkerType``.
        """
        props = CfnJobProps(command=command, role=role, allocated_capacity=allocated_capacity, connections=connections, default_arguments=default_arguments, description=description, execution_property=execution_property, glue_version=glue_version, log_uri=log_uri, max_capacity=max_capacity, max_retries=max_retries, name=name, notification_property=notification_property, number_of_workers=number_of_workers, security_configuration=security_configuration, tags=tags, timeout=timeout, worker_type=worker_type)

        jsii.create(CfnJob, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Glue::Job.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Union[aws_cdk.core.IResolvable, "JobCommandProperty"]:
        """``AWS::Glue::Job.Command``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-command
        """
        return jsii.get(self, "command")

    @command.setter
    def command(self, value: typing.Union[aws_cdk.core.IResolvable, "JobCommandProperty"]):
        return jsii.set(self, "command", value)

    @property
    @jsii.member(jsii_name="defaultArguments")
    def default_arguments(self) -> typing.Any:
        """``AWS::Glue::Job.DefaultArguments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-defaultarguments
        """
        return jsii.get(self, "defaultArguments")

    @default_arguments.setter
    def default_arguments(self, value: typing.Any):
        return jsii.set(self, "defaultArguments", value)

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        """``AWS::Glue::Job.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: str):
        return jsii.set(self, "role", value)

    @property
    @jsii.member(jsii_name="allocatedCapacity")
    def allocated_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.AllocatedCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-allocatedcapacity
        """
        return jsii.get(self, "allocatedCapacity")

    @allocated_capacity.setter
    def allocated_capacity(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "allocatedCapacity", value)

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionsListProperty"]]]:
        """``AWS::Glue::Job.Connections``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-connections
        """
        return jsii.get(self, "connections")

    @connections.setter
    def connections(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ConnectionsListProperty"]]]):
        return jsii.set(self, "connections", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="executionProperty")
    def execution_property(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ExecutionPropertyProperty"]]]:
        """``AWS::Glue::Job.ExecutionProperty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-executionproperty
        """
        return jsii.get(self, "executionProperty")

    @execution_property.setter
    def execution_property(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["ExecutionPropertyProperty"]]]):
        return jsii.set(self, "executionProperty", value)

    @property
    @jsii.member(jsii_name="glueVersion")
    def glue_version(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.GlueVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-glueversion
        """
        return jsii.get(self, "glueVersion")

    @glue_version.setter
    def glue_version(self, value: typing.Optional[str]):
        return jsii.set(self, "glueVersion", value)

    @property
    @jsii.member(jsii_name="logUri")
    def log_uri(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.LogUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-loguri
        """
        return jsii.get(self, "logUri")

    @log_uri.setter
    def log_uri(self, value: typing.Optional[str]):
        return jsii.set(self, "logUri", value)

    @property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxcapacity
        """
        return jsii.get(self, "maxCapacity")

    @max_capacity.setter
    def max_capacity(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "maxCapacity", value)

    @property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.MaxRetries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxretries
        """
        return jsii.get(self, "maxRetries")

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "maxRetries", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="notificationProperty")
    def notification_property(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationPropertyProperty"]]]:
        """``AWS::Glue::Job.NotificationProperty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-notificationproperty
        """
        return jsii.get(self, "notificationProperty")

    @notification_property.setter
    def notification_property(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["NotificationPropertyProperty"]]]):
        return jsii.set(self, "notificationProperty", value)

    @property
    @jsii.member(jsii_name="numberOfWorkers")
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-numberofworkers
        """
        return jsii.get(self, "numberOfWorkers")

    @number_of_workers.setter
    def number_of_workers(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "numberOfWorkers", value)

    @property
    @jsii.member(jsii_name="securityConfiguration")
    def security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.SecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-securityconfiguration
        """
        return jsii.get(self, "securityConfiguration")

    @security_configuration.setter
    def security_configuration(self, value: typing.Optional[str]):
        return jsii.set(self, "securityConfiguration", value)

    @property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "timeout", value)

    @property
    @jsii.member(jsii_name="workerType")
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-workertype
        """
        return jsii.get(self, "workerType")

    @worker_type.setter
    def worker_type(self, value: typing.Optional[str]):
        return jsii.set(self, "workerType", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.ConnectionsListProperty", jsii_struct_bases=[], name_mapping={'connections': 'connections'})
    class ConnectionsListProperty():
        def __init__(self, *, connections: typing.Optional[typing.List[str]]=None):
            """
            :param connections: ``CfnJob.ConnectionsListProperty.Connections``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-connectionslist.html
            """
            self._values = {
            }
            if connections is not None: self._values["connections"] = connections

        @property
        def connections(self) -> typing.Optional[typing.List[str]]:
            """``CfnJob.ConnectionsListProperty.Connections``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-connectionslist.html#cfn-glue-job-connectionslist-connections
            """
            return self._values.get('connections')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConnectionsListProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.ExecutionPropertyProperty", jsii_struct_bases=[], name_mapping={'max_concurrent_runs': 'maxConcurrentRuns'})
    class ExecutionPropertyProperty():
        def __init__(self, *, max_concurrent_runs: typing.Optional[jsii.Number]=None):
            """
            :param max_concurrent_runs: ``CfnJob.ExecutionPropertyProperty.MaxConcurrentRuns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-executionproperty.html
            """
            self._values = {
            }
            if max_concurrent_runs is not None: self._values["max_concurrent_runs"] = max_concurrent_runs

        @property
        def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
            """``CfnJob.ExecutionPropertyProperty.MaxConcurrentRuns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-executionproperty.html#cfn-glue-job-executionproperty-maxconcurrentruns
            """
            return self._values.get('max_concurrent_runs')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ExecutionPropertyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.JobCommandProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'python_version': 'pythonVersion', 'script_location': 'scriptLocation'})
    class JobCommandProperty():
        def __init__(self, *, name: typing.Optional[str]=None, python_version: typing.Optional[str]=None, script_location: typing.Optional[str]=None):
            """
            :param name: ``CfnJob.JobCommandProperty.Name``.
            :param python_version: ``CfnJob.JobCommandProperty.PythonVersion``.
            :param script_location: ``CfnJob.JobCommandProperty.ScriptLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if python_version is not None: self._values["python_version"] = python_version
            if script_location is not None: self._values["script_location"] = script_location

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnJob.JobCommandProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-name
            """
            return self._values.get('name')

        @property
        def python_version(self) -> typing.Optional[str]:
            """``CfnJob.JobCommandProperty.PythonVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-pythonversion
            """
            return self._values.get('python_version')

        @property
        def script_location(self) -> typing.Optional[str]:
            """``CfnJob.JobCommandProperty.ScriptLocation``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-jobcommand.html#cfn-glue-job-jobcommand-scriptlocation
            """
            return self._values.get('script_location')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JobCommandProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJob.NotificationPropertyProperty", jsii_struct_bases=[], name_mapping={'notify_delay_after': 'notifyDelayAfter'})
    class NotificationPropertyProperty():
        def __init__(self, *, notify_delay_after: typing.Optional[jsii.Number]=None):
            """
            :param notify_delay_after: ``CfnJob.NotificationPropertyProperty.NotifyDelayAfter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-notificationproperty.html
            """
            self._values = {
            }
            if notify_delay_after is not None: self._values["notify_delay_after"] = notify_delay_after

        @property
        def notify_delay_after(self) -> typing.Optional[jsii.Number]:
            """``CfnJob.NotificationPropertyProperty.NotifyDelayAfter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-job-notificationproperty.html#cfn-glue-job-notificationproperty-notifydelayafter
            """
            return self._values.get('notify_delay_after')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationPropertyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnJobProps", jsii_struct_bases=[], name_mapping={'command': 'command', 'role': 'role', 'allocated_capacity': 'allocatedCapacity', 'connections': 'connections', 'default_arguments': 'defaultArguments', 'description': 'description', 'execution_property': 'executionProperty', 'glue_version': 'glueVersion', 'log_uri': 'logUri', 'max_capacity': 'maxCapacity', 'max_retries': 'maxRetries', 'name': 'name', 'notification_property': 'notificationProperty', 'number_of_workers': 'numberOfWorkers', 'security_configuration': 'securityConfiguration', 'tags': 'tags', 'timeout': 'timeout', 'worker_type': 'workerType'})
class CfnJobProps():
    def __init__(self, *, command: typing.Union[aws_cdk.core.IResolvable, "CfnJob.JobCommandProperty"], role: str, allocated_capacity: typing.Optional[jsii.Number]=None, connections: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.ConnectionsListProperty"]]]=None, default_arguments: typing.Any=None, description: typing.Optional[str]=None, execution_property: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.ExecutionPropertyProperty"]]]=None, glue_version: typing.Optional[str]=None, log_uri: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, notification_property: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.NotificationPropertyProperty"]]]=None, number_of_workers: typing.Optional[jsii.Number]=None, security_configuration: typing.Optional[str]=None, tags: typing.Any=None, timeout: typing.Optional[jsii.Number]=None, worker_type: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Glue::Job``.

        :param command: ``AWS::Glue::Job.Command``.
        :param role: ``AWS::Glue::Job.Role``.
        :param allocated_capacity: ``AWS::Glue::Job.AllocatedCapacity``.
        :param connections: ``AWS::Glue::Job.Connections``.
        :param default_arguments: ``AWS::Glue::Job.DefaultArguments``.
        :param description: ``AWS::Glue::Job.Description``.
        :param execution_property: ``AWS::Glue::Job.ExecutionProperty``.
        :param glue_version: ``AWS::Glue::Job.GlueVersion``.
        :param log_uri: ``AWS::Glue::Job.LogUri``.
        :param max_capacity: ``AWS::Glue::Job.MaxCapacity``.
        :param max_retries: ``AWS::Glue::Job.MaxRetries``.
        :param name: ``AWS::Glue::Job.Name``.
        :param notification_property: ``AWS::Glue::Job.NotificationProperty``.
        :param number_of_workers: ``AWS::Glue::Job.NumberOfWorkers``.
        :param security_configuration: ``AWS::Glue::Job.SecurityConfiguration``.
        :param tags: ``AWS::Glue::Job.Tags``.
        :param timeout: ``AWS::Glue::Job.Timeout``.
        :param worker_type: ``AWS::Glue::Job.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html
        """
        self._values = {
            'command': command,
            'role': role,
        }
        if allocated_capacity is not None: self._values["allocated_capacity"] = allocated_capacity
        if connections is not None: self._values["connections"] = connections
        if default_arguments is not None: self._values["default_arguments"] = default_arguments
        if description is not None: self._values["description"] = description
        if execution_property is not None: self._values["execution_property"] = execution_property
        if glue_version is not None: self._values["glue_version"] = glue_version
        if log_uri is not None: self._values["log_uri"] = log_uri
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if max_retries is not None: self._values["max_retries"] = max_retries
        if name is not None: self._values["name"] = name
        if notification_property is not None: self._values["notification_property"] = notification_property
        if number_of_workers is not None: self._values["number_of_workers"] = number_of_workers
        if security_configuration is not None: self._values["security_configuration"] = security_configuration
        if tags is not None: self._values["tags"] = tags
        if timeout is not None: self._values["timeout"] = timeout
        if worker_type is not None: self._values["worker_type"] = worker_type

    @property
    def command(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnJob.JobCommandProperty"]:
        """``AWS::Glue::Job.Command``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-command
        """
        return self._values.get('command')

    @property
    def role(self) -> str:
        """``AWS::Glue::Job.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-role
        """
        return self._values.get('role')

    @property
    def allocated_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.AllocatedCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-allocatedcapacity
        """
        return self._values.get('allocated_capacity')

    @property
    def connections(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.ConnectionsListProperty"]]]:
        """``AWS::Glue::Job.Connections``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-connections
        """
        return self._values.get('connections')

    @property
    def default_arguments(self) -> typing.Any:
        """``AWS::Glue::Job.DefaultArguments``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-defaultarguments
        """
        return self._values.get('default_arguments')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-description
        """
        return self._values.get('description')

    @property
    def execution_property(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.ExecutionPropertyProperty"]]]:
        """``AWS::Glue::Job.ExecutionProperty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-executionproperty
        """
        return self._values.get('execution_property')

    @property
    def glue_version(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.GlueVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-glueversion
        """
        return self._values.get('glue_version')

    @property
    def log_uri(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.LogUri``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-loguri
        """
        return self._values.get('log_uri')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxcapacity
        """
        return self._values.get('max_capacity')

    @property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.MaxRetries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-maxretries
        """
        return self._values.get('max_retries')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-name
        """
        return self._values.get('name')

    @property
    def notification_property(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnJob.NotificationPropertyProperty"]]]:
        """``AWS::Glue::Job.NotificationProperty``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-notificationproperty
        """
        return self._values.get('notification_property')

    @property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-numberofworkers
        """
        return self._values.get('number_of_workers')

    @property
    def security_configuration(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.SecurityConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-securityconfiguration
        """
        return self._values.get('security_configuration')

    @property
    def tags(self) -> typing.Any:
        """``AWS::Glue::Job.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-tags
        """
        return self._values.get('tags')

    @property
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::Job.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-timeout
        """
        return self._values.get('timeout')

    @property
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::Job.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-job.html#cfn-glue-job-workertype
        """
        return self._values.get('worker_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnJobProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnMLTransform(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnMLTransform"):
    """A CloudFormation ``AWS::Glue::MLTransform``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::MLTransform
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, input_record_tables: typing.Union[aws_cdk.core.IResolvable, "InputRecordTablesProperty"], role: str, transform_parameters: typing.Union[aws_cdk.core.IResolvable, "TransformParametersProperty"], description: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, number_of_workers: typing.Optional[jsii.Number]=None, timeout: typing.Optional[jsii.Number]=None, worker_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Glue::MLTransform``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param input_record_tables: ``AWS::Glue::MLTransform.InputRecordTables``.
        :param role: ``AWS::Glue::MLTransform.Role``.
        :param transform_parameters: ``AWS::Glue::MLTransform.TransformParameters``.
        :param description: ``AWS::Glue::MLTransform.Description``.
        :param max_capacity: ``AWS::Glue::MLTransform.MaxCapacity``.
        :param max_retries: ``AWS::Glue::MLTransform.MaxRetries``.
        :param name: ``AWS::Glue::MLTransform.Name``.
        :param number_of_workers: ``AWS::Glue::MLTransform.NumberOfWorkers``.
        :param timeout: ``AWS::Glue::MLTransform.Timeout``.
        :param worker_type: ``AWS::Glue::MLTransform.WorkerType``.
        """
        props = CfnMLTransformProps(input_record_tables=input_record_tables, role=role, transform_parameters=transform_parameters, description=description, max_capacity=max_capacity, max_retries=max_retries, name=name, number_of_workers=number_of_workers, timeout=timeout, worker_type=worker_type)

        jsii.create(CfnMLTransform, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="inputRecordTables")
    def input_record_tables(self) -> typing.Union[aws_cdk.core.IResolvable, "InputRecordTablesProperty"]:
        """``AWS::Glue::MLTransform.InputRecordTables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-inputrecordtables
        """
        return jsii.get(self, "inputRecordTables")

    @input_record_tables.setter
    def input_record_tables(self, value: typing.Union[aws_cdk.core.IResolvable, "InputRecordTablesProperty"]):
        return jsii.set(self, "inputRecordTables", value)

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> str:
        """``AWS::Glue::MLTransform.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-role
        """
        return jsii.get(self, "role")

    @role.setter
    def role(self, value: str):
        return jsii.set(self, "role", value)

    @property
    @jsii.member(jsii_name="transformParameters")
    def transform_parameters(self) -> typing.Union[aws_cdk.core.IResolvable, "TransformParametersProperty"]:
        """``AWS::Glue::MLTransform.TransformParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-transformparameters
        """
        return jsii.get(self, "transformParameters")

    @transform_parameters.setter
    def transform_parameters(self, value: typing.Union[aws_cdk.core.IResolvable, "TransformParametersProperty"]):
        return jsii.set(self, "transformParameters", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxcapacity
        """
        return jsii.get(self, "maxCapacity")

    @max_capacity.setter
    def max_capacity(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "maxCapacity", value)

    @property
    @jsii.member(jsii_name="maxRetries")
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.MaxRetries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxretries
        """
        return jsii.get(self, "maxRetries")

    @max_retries.setter
    def max_retries(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "maxRetries", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="numberOfWorkers")
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-numberofworkers
        """
        return jsii.get(self, "numberOfWorkers")

    @number_of_workers.setter
    def number_of_workers(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "numberOfWorkers", value)

    @property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-timeout
        """
        return jsii.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "timeout", value)

    @property
    @jsii.member(jsii_name="workerType")
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-workertype
        """
        return jsii.get(self, "workerType")

    @worker_type.setter
    def worker_type(self, value: typing.Optional[str]):
        return jsii.set(self, "workerType", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnMLTransform.FindMatchesParametersProperty", jsii_struct_bases=[], name_mapping={'primary_key_column_name': 'primaryKeyColumnName', 'accuracy_cost_tradeoff': 'accuracyCostTradeoff', 'enforce_provided_labels': 'enforceProvidedLabels', 'precision_recall_tradeoff': 'precisionRecallTradeoff'})
    class FindMatchesParametersProperty():
        def __init__(self, *, primary_key_column_name: str, accuracy_cost_tradeoff: typing.Optional[jsii.Number]=None, enforce_provided_labels: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, precision_recall_tradeoff: typing.Optional[jsii.Number]=None):
            """
            :param primary_key_column_name: ``CfnMLTransform.FindMatchesParametersProperty.PrimaryKeyColumnName``.
            :param accuracy_cost_tradeoff: ``CfnMLTransform.FindMatchesParametersProperty.AccuracyCostTradeoff``.
            :param enforce_provided_labels: ``CfnMLTransform.FindMatchesParametersProperty.EnforceProvidedLabels``.
            :param precision_recall_tradeoff: ``CfnMLTransform.FindMatchesParametersProperty.PrecisionRecallTradeoff``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters-findmatchesparameters.html
            """
            self._values = {
                'primary_key_column_name': primary_key_column_name,
            }
            if accuracy_cost_tradeoff is not None: self._values["accuracy_cost_tradeoff"] = accuracy_cost_tradeoff
            if enforce_provided_labels is not None: self._values["enforce_provided_labels"] = enforce_provided_labels
            if precision_recall_tradeoff is not None: self._values["precision_recall_tradeoff"] = precision_recall_tradeoff

        @property
        def primary_key_column_name(self) -> str:
            """``CfnMLTransform.FindMatchesParametersProperty.PrimaryKeyColumnName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters-findmatchesparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters-primarykeycolumnname
            """
            return self._values.get('primary_key_column_name')

        @property
        def accuracy_cost_tradeoff(self) -> typing.Optional[jsii.Number]:
            """``CfnMLTransform.FindMatchesParametersProperty.AccuracyCostTradeoff``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters-findmatchesparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters-accuracycosttradeoff
            """
            return self._values.get('accuracy_cost_tradeoff')

        @property
        def enforce_provided_labels(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnMLTransform.FindMatchesParametersProperty.EnforceProvidedLabels``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters-findmatchesparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters-enforceprovidedlabels
            """
            return self._values.get('enforce_provided_labels')

        @property
        def precision_recall_tradeoff(self) -> typing.Optional[jsii.Number]:
            """``CfnMLTransform.FindMatchesParametersProperty.PrecisionRecallTradeoff``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters-findmatchesparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters-precisionrecalltradeoff
            """
            return self._values.get('precision_recall_tradeoff')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'FindMatchesParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnMLTransform.GlueTablesProperty", jsii_struct_bases=[], name_mapping={'database_name': 'databaseName', 'table_name': 'tableName', 'catalog_id': 'catalogId', 'connection_name': 'connectionName'})
    class GlueTablesProperty():
        def __init__(self, *, database_name: str, table_name: str, catalog_id: typing.Optional[str]=None, connection_name: typing.Optional[str]=None):
            """
            :param database_name: ``CfnMLTransform.GlueTablesProperty.DatabaseName``.
            :param table_name: ``CfnMLTransform.GlueTablesProperty.TableName``.
            :param catalog_id: ``CfnMLTransform.GlueTablesProperty.CatalogId``.
            :param connection_name: ``CfnMLTransform.GlueTablesProperty.ConnectionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables-gluetables.html
            """
            self._values = {
                'database_name': database_name,
                'table_name': table_name,
            }
            if catalog_id is not None: self._values["catalog_id"] = catalog_id
            if connection_name is not None: self._values["connection_name"] = connection_name

        @property
        def database_name(self) -> str:
            """``CfnMLTransform.GlueTablesProperty.DatabaseName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables-gluetables.html#cfn-glue-mltransform-inputrecordtables-gluetables-databasename
            """
            return self._values.get('database_name')

        @property
        def table_name(self) -> str:
            """``CfnMLTransform.GlueTablesProperty.TableName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables-gluetables.html#cfn-glue-mltransform-inputrecordtables-gluetables-tablename
            """
            return self._values.get('table_name')

        @property
        def catalog_id(self) -> typing.Optional[str]:
            """``CfnMLTransform.GlueTablesProperty.CatalogId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables-gluetables.html#cfn-glue-mltransform-inputrecordtables-gluetables-catalogid
            """
            return self._values.get('catalog_id')

        @property
        def connection_name(self) -> typing.Optional[str]:
            """``CfnMLTransform.GlueTablesProperty.ConnectionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables-gluetables.html#cfn-glue-mltransform-inputrecordtables-gluetables-connectionname
            """
            return self._values.get('connection_name')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'GlueTablesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnMLTransform.InputRecordTablesProperty", jsii_struct_bases=[], name_mapping={'glue_tables': 'glueTables'})
    class InputRecordTablesProperty():
        def __init__(self, *, glue_tables: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.GlueTablesProperty"]]]]]=None):
            """
            :param glue_tables: ``CfnMLTransform.InputRecordTablesProperty.GlueTables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables.html
            """
            self._values = {
            }
            if glue_tables is not None: self._values["glue_tables"] = glue_tables

        @property
        def glue_tables(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.GlueTablesProperty"]]]]]:
            """``CfnMLTransform.InputRecordTablesProperty.GlueTables``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-inputrecordtables.html#cfn-glue-mltransform-inputrecordtables-gluetables
            """
            return self._values.get('glue_tables')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'InputRecordTablesProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnMLTransform.TransformParametersProperty", jsii_struct_bases=[], name_mapping={'transform_type': 'transformType', 'find_matches_parameters': 'findMatchesParameters'})
    class TransformParametersProperty():
        def __init__(self, *, transform_type: str, find_matches_parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnMLTransform.FindMatchesParametersProperty"]]]=None):
            """
            :param transform_type: ``CfnMLTransform.TransformParametersProperty.TransformType``.
            :param find_matches_parameters: ``CfnMLTransform.TransformParametersProperty.FindMatchesParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html
            """
            self._values = {
                'transform_type': transform_type,
            }
            if find_matches_parameters is not None: self._values["find_matches_parameters"] = find_matches_parameters

        @property
        def transform_type(self) -> str:
            """``CfnMLTransform.TransformParametersProperty.TransformType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html#cfn-glue-mltransform-transformparameters-transformtype
            """
            return self._values.get('transform_type')

        @property
        def find_matches_parameters(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnMLTransform.FindMatchesParametersProperty"]]]:
            """``CfnMLTransform.TransformParametersProperty.FindMatchesParameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-mltransform-transformparameters.html#cfn-glue-mltransform-transformparameters-findmatchesparameters
            """
            return self._values.get('find_matches_parameters')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TransformParametersProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnMLTransformProps", jsii_struct_bases=[], name_mapping={'input_record_tables': 'inputRecordTables', 'role': 'role', 'transform_parameters': 'transformParameters', 'description': 'description', 'max_capacity': 'maxCapacity', 'max_retries': 'maxRetries', 'name': 'name', 'number_of_workers': 'numberOfWorkers', 'timeout': 'timeout', 'worker_type': 'workerType'})
class CfnMLTransformProps():
    def __init__(self, *, input_record_tables: typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.InputRecordTablesProperty"], role: str, transform_parameters: typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.TransformParametersProperty"], description: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, max_retries: typing.Optional[jsii.Number]=None, name: typing.Optional[str]=None, number_of_workers: typing.Optional[jsii.Number]=None, timeout: typing.Optional[jsii.Number]=None, worker_type: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Glue::MLTransform``.

        :param input_record_tables: ``AWS::Glue::MLTransform.InputRecordTables``.
        :param role: ``AWS::Glue::MLTransform.Role``.
        :param transform_parameters: ``AWS::Glue::MLTransform.TransformParameters``.
        :param description: ``AWS::Glue::MLTransform.Description``.
        :param max_capacity: ``AWS::Glue::MLTransform.MaxCapacity``.
        :param max_retries: ``AWS::Glue::MLTransform.MaxRetries``.
        :param name: ``AWS::Glue::MLTransform.Name``.
        :param number_of_workers: ``AWS::Glue::MLTransform.NumberOfWorkers``.
        :param timeout: ``AWS::Glue::MLTransform.Timeout``.
        :param worker_type: ``AWS::Glue::MLTransform.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html
        """
        self._values = {
            'input_record_tables': input_record_tables,
            'role': role,
            'transform_parameters': transform_parameters,
        }
        if description is not None: self._values["description"] = description
        if max_capacity is not None: self._values["max_capacity"] = max_capacity
        if max_retries is not None: self._values["max_retries"] = max_retries
        if name is not None: self._values["name"] = name
        if number_of_workers is not None: self._values["number_of_workers"] = number_of_workers
        if timeout is not None: self._values["timeout"] = timeout
        if worker_type is not None: self._values["worker_type"] = worker_type

    @property
    def input_record_tables(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.InputRecordTablesProperty"]:
        """``AWS::Glue::MLTransform.InputRecordTables``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-inputrecordtables
        """
        return self._values.get('input_record_tables')

    @property
    def role(self) -> str:
        """``AWS::Glue::MLTransform.Role``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-role
        """
        return self._values.get('role')

    @property
    def transform_parameters(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnMLTransform.TransformParametersProperty"]:
        """``AWS::Glue::MLTransform.TransformParameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-transformparameters
        """
        return self._values.get('transform_parameters')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-description
        """
        return self._values.get('description')

    @property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.MaxCapacity``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxcapacity
        """
        return self._values.get('max_capacity')

    @property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.MaxRetries``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-maxretries
        """
        return self._values.get('max_retries')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-name
        """
        return self._values.get('name')

    @property
    def number_of_workers(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.NumberOfWorkers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-numberofworkers
        """
        return self._values.get('number_of_workers')

    @property
    def timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::Glue::MLTransform.Timeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-timeout
        """
        return self._values.get('timeout')

    @property
    def worker_type(self) -> typing.Optional[str]:
        """``AWS::Glue::MLTransform.WorkerType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-mltransform.html#cfn-glue-mltransform-workertype
        """
        return self._values.get('worker_type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnMLTransformProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnPartition(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnPartition"):
    """A CloudFormation ``AWS::Glue::Partition``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Partition
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, catalog_id: str, database_name: str, partition_input: typing.Union[aws_cdk.core.IResolvable, "PartitionInputProperty"], table_name: str) -> None:
        """Create a new ``AWS::Glue::Partition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param catalog_id: ``AWS::Glue::Partition.CatalogId``.
        :param database_name: ``AWS::Glue::Partition.DatabaseName``.
        :param partition_input: ``AWS::Glue::Partition.PartitionInput``.
        :param table_name: ``AWS::Glue::Partition.TableName``.
        """
        props = CfnPartitionProps(catalog_id=catalog_id, database_name=database_name, partition_input=partition_input, table_name=table_name)

        jsii.create(CfnPartition, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """``AWS::Glue::Partition.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-catalogid
        """
        return jsii.get(self, "catalogId")

    @catalog_id.setter
    def catalog_id(self, value: str):
        return jsii.set(self, "catalogId", value)

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        """``AWS::Glue::Partition.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter
    def database_name(self, value: str):
        return jsii.set(self, "databaseName", value)

    @property
    @jsii.member(jsii_name="partitionInput")
    def partition_input(self) -> typing.Union[aws_cdk.core.IResolvable, "PartitionInputProperty"]:
        """``AWS::Glue::Partition.PartitionInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-partitioninput
        """
        return jsii.get(self, "partitionInput")

    @partition_input.setter
    def partition_input(self, value: typing.Union[aws_cdk.core.IResolvable, "PartitionInputProperty"]):
        return jsii.set(self, "partitionInput", value)

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """``AWS::Glue::Partition.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-tablename
        """
        return jsii.get(self, "tableName")

    @table_name.setter
    def table_name(self, value: str):
        return jsii.set(self, "tableName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.ColumnProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'comment': 'comment', 'type': 'type'})
    class ColumnProperty():
        def __init__(self, *, name: str, comment: typing.Optional[str]=None, type: typing.Optional[str]=None):
            """
            :param name: ``CfnPartition.ColumnProperty.Name``.
            :param comment: ``CfnPartition.ColumnProperty.Comment``.
            :param type: ``CfnPartition.ColumnProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html
            """
            self._values = {
                'name': name,
            }
            if comment is not None: self._values["comment"] = comment
            if type is not None: self._values["type"] = type

        @property
        def name(self) -> str:
            """``CfnPartition.ColumnProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-name
            """
            return self._values.get('name')

        @property
        def comment(self) -> typing.Optional[str]:
            """``CfnPartition.ColumnProperty.Comment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-comment
            """
            return self._values.get('comment')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnPartition.ColumnProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-column.html#cfn-glue-partition-column-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ColumnProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.OrderProperty", jsii_struct_bases=[], name_mapping={'column': 'column', 'sort_order': 'sortOrder'})
    class OrderProperty():
        def __init__(self, *, column: str, sort_order: typing.Optional[jsii.Number]=None):
            """
            :param column: ``CfnPartition.OrderProperty.Column``.
            :param sort_order: ``CfnPartition.OrderProperty.SortOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html
            """
            self._values = {
                'column': column,
            }
            if sort_order is not None: self._values["sort_order"] = sort_order

        @property
        def column(self) -> str:
            """``CfnPartition.OrderProperty.Column``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html#cfn-glue-partition-order-column
            """
            return self._values.get('column')

        @property
        def sort_order(self) -> typing.Optional[jsii.Number]:
            """``CfnPartition.OrderProperty.SortOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-order.html#cfn-glue-partition-order-sortorder
            """
            return self._values.get('sort_order')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OrderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.PartitionInputProperty", jsii_struct_bases=[], name_mapping={'values': 'values', 'parameters': 'parameters', 'storage_descriptor': 'storageDescriptor'})
    class PartitionInputProperty():
        def __init__(self, *, values: typing.List[str], parameters: typing.Any=None, storage_descriptor: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.StorageDescriptorProperty"]]]=None):
            """
            :param values: ``CfnPartition.PartitionInputProperty.Values``.
            :param parameters: ``CfnPartition.PartitionInputProperty.Parameters``.
            :param storage_descriptor: ``CfnPartition.PartitionInputProperty.StorageDescriptor``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html
            """
            self._values = {
                'values': values,
            }
            if parameters is not None: self._values["parameters"] = parameters
            if storage_descriptor is not None: self._values["storage_descriptor"] = storage_descriptor

        @property
        def values(self) -> typing.List[str]:
            """``CfnPartition.PartitionInputProperty.Values``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-values
            """
            return self._values.get('values')

        @property
        def parameters(self) -> typing.Any:
            """``CfnPartition.PartitionInputProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-parameters
            """
            return self._values.get('parameters')

        @property
        def storage_descriptor(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.StorageDescriptorProperty"]]]:
            """``CfnPartition.PartitionInputProperty.StorageDescriptor``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-partitioninput.html#cfn-glue-partition-partitioninput-storagedescriptor
            """
            return self._values.get('storage_descriptor')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PartitionInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.SerdeInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'parameters': 'parameters', 'serialization_library': 'serializationLibrary'})
    class SerdeInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None, parameters: typing.Any=None, serialization_library: typing.Optional[str]=None):
            """
            :param name: ``CfnPartition.SerdeInfoProperty.Name``.
            :param parameters: ``CfnPartition.SerdeInfoProperty.Parameters``.
            :param serialization_library: ``CfnPartition.SerdeInfoProperty.SerializationLibrary``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if parameters is not None: self._values["parameters"] = parameters
            if serialization_library is not None: self._values["serialization_library"] = serialization_library

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnPartition.SerdeInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-name
            """
            return self._values.get('name')

        @property
        def parameters(self) -> typing.Any:
            """``CfnPartition.SerdeInfoProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-parameters
            """
            return self._values.get('parameters')

        @property
        def serialization_library(self) -> typing.Optional[str]:
            """``CfnPartition.SerdeInfoProperty.SerializationLibrary``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-serdeinfo.html#cfn-glue-partition-serdeinfo-serializationlibrary
            """
            return self._values.get('serialization_library')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SerdeInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.SkewedInfoProperty", jsii_struct_bases=[], name_mapping={'skewed_column_names': 'skewedColumnNames', 'skewed_column_value_location_maps': 'skewedColumnValueLocationMaps', 'skewed_column_values': 'skewedColumnValues'})
    class SkewedInfoProperty():
        def __init__(self, *, skewed_column_names: typing.Optional[typing.List[str]]=None, skewed_column_value_location_maps: typing.Any=None, skewed_column_values: typing.Optional[typing.List[str]]=None):
            """
            :param skewed_column_names: ``CfnPartition.SkewedInfoProperty.SkewedColumnNames``.
            :param skewed_column_value_location_maps: ``CfnPartition.SkewedInfoProperty.SkewedColumnValueLocationMaps``.
            :param skewed_column_values: ``CfnPartition.SkewedInfoProperty.SkewedColumnValues``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html
            """
            self._values = {
            }
            if skewed_column_names is not None: self._values["skewed_column_names"] = skewed_column_names
            if skewed_column_value_location_maps is not None: self._values["skewed_column_value_location_maps"] = skewed_column_value_location_maps
            if skewed_column_values is not None: self._values["skewed_column_values"] = skewed_column_values

        @property
        def skewed_column_names(self) -> typing.Optional[typing.List[str]]:
            """``CfnPartition.SkewedInfoProperty.SkewedColumnNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnnames
            """
            return self._values.get('skewed_column_names')

        @property
        def skewed_column_value_location_maps(self) -> typing.Any:
            """``CfnPartition.SkewedInfoProperty.SkewedColumnValueLocationMaps``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnvaluelocationmaps
            """
            return self._values.get('skewed_column_value_location_maps')

        @property
        def skewed_column_values(self) -> typing.Optional[typing.List[str]]:
            """``CfnPartition.SkewedInfoProperty.SkewedColumnValues``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-skewedinfo.html#cfn-glue-partition-skewedinfo-skewedcolumnvalues
            """
            return self._values.get('skewed_column_values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SkewedInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartition.StorageDescriptorProperty", jsii_struct_bases=[], name_mapping={'bucket_columns': 'bucketColumns', 'columns': 'columns', 'compressed': 'compressed', 'input_format': 'inputFormat', 'location': 'location', 'number_of_buckets': 'numberOfBuckets', 'output_format': 'outputFormat', 'parameters': 'parameters', 'serde_info': 'serdeInfo', 'skewed_info': 'skewedInfo', 'sort_columns': 'sortColumns', 'stored_as_sub_directories': 'storedAsSubDirectories'})
    class StorageDescriptorProperty():
        def __init__(self, *, bucket_columns: typing.Optional[typing.List[str]]=None, columns: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPartition.ColumnProperty"]]]]]=None, compressed: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, input_format: typing.Optional[str]=None, location: typing.Optional[str]=None, number_of_buckets: typing.Optional[jsii.Number]=None, output_format: typing.Optional[str]=None, parameters: typing.Any=None, serde_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.SerdeInfoProperty"]]]=None, skewed_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.SkewedInfoProperty"]]]=None, sort_columns: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPartition.OrderProperty"]]]]]=None, stored_as_sub_directories: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param bucket_columns: ``CfnPartition.StorageDescriptorProperty.BucketColumns``.
            :param columns: ``CfnPartition.StorageDescriptorProperty.Columns``.
            :param compressed: ``CfnPartition.StorageDescriptorProperty.Compressed``.
            :param input_format: ``CfnPartition.StorageDescriptorProperty.InputFormat``.
            :param location: ``CfnPartition.StorageDescriptorProperty.Location``.
            :param number_of_buckets: ``CfnPartition.StorageDescriptorProperty.NumberOfBuckets``.
            :param output_format: ``CfnPartition.StorageDescriptorProperty.OutputFormat``.
            :param parameters: ``CfnPartition.StorageDescriptorProperty.Parameters``.
            :param serde_info: ``CfnPartition.StorageDescriptorProperty.SerdeInfo``.
            :param skewed_info: ``CfnPartition.StorageDescriptorProperty.SkewedInfo``.
            :param sort_columns: ``CfnPartition.StorageDescriptorProperty.SortColumns``.
            :param stored_as_sub_directories: ``CfnPartition.StorageDescriptorProperty.StoredAsSubDirectories``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html
            """
            self._values = {
            }
            if bucket_columns is not None: self._values["bucket_columns"] = bucket_columns
            if columns is not None: self._values["columns"] = columns
            if compressed is not None: self._values["compressed"] = compressed
            if input_format is not None: self._values["input_format"] = input_format
            if location is not None: self._values["location"] = location
            if number_of_buckets is not None: self._values["number_of_buckets"] = number_of_buckets
            if output_format is not None: self._values["output_format"] = output_format
            if parameters is not None: self._values["parameters"] = parameters
            if serde_info is not None: self._values["serde_info"] = serde_info
            if skewed_info is not None: self._values["skewed_info"] = skewed_info
            if sort_columns is not None: self._values["sort_columns"] = sort_columns
            if stored_as_sub_directories is not None: self._values["stored_as_sub_directories"] = stored_as_sub_directories

        @property
        def bucket_columns(self) -> typing.Optional[typing.List[str]]:
            """``CfnPartition.StorageDescriptorProperty.BucketColumns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-bucketcolumns
            """
            return self._values.get('bucket_columns')

        @property
        def columns(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPartition.ColumnProperty"]]]]]:
            """``CfnPartition.StorageDescriptorProperty.Columns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-columns
            """
            return self._values.get('columns')

        @property
        def compressed(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnPartition.StorageDescriptorProperty.Compressed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-compressed
            """
            return self._values.get('compressed')

        @property
        def input_format(self) -> typing.Optional[str]:
            """``CfnPartition.StorageDescriptorProperty.InputFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-inputformat
            """
            return self._values.get('input_format')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnPartition.StorageDescriptorProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-location
            """
            return self._values.get('location')

        @property
        def number_of_buckets(self) -> typing.Optional[jsii.Number]:
            """``CfnPartition.StorageDescriptorProperty.NumberOfBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-numberofbuckets
            """
            return self._values.get('number_of_buckets')

        @property
        def output_format(self) -> typing.Optional[str]:
            """``CfnPartition.StorageDescriptorProperty.OutputFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-outputformat
            """
            return self._values.get('output_format')

        @property
        def parameters(self) -> typing.Any:
            """``CfnPartition.StorageDescriptorProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-parameters
            """
            return self._values.get('parameters')

        @property
        def serde_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.SerdeInfoProperty"]]]:
            """``CfnPartition.StorageDescriptorProperty.SerdeInfo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-serdeinfo
            """
            return self._values.get('serde_info')

        @property
        def skewed_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnPartition.SkewedInfoProperty"]]]:
            """``CfnPartition.StorageDescriptorProperty.SkewedInfo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-skewedinfo
            """
            return self._values.get('skewed_info')

        @property
        def sort_columns(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnPartition.OrderProperty"]]]]]:
            """``CfnPartition.StorageDescriptorProperty.SortColumns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-sortcolumns
            """
            return self._values.get('sort_columns')

        @property
        def stored_as_sub_directories(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnPartition.StorageDescriptorProperty.StoredAsSubDirectories``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-partition-storagedescriptor.html#cfn-glue-partition-storagedescriptor-storedassubdirectories
            """
            return self._values.get('stored_as_sub_directories')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StorageDescriptorProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnPartitionProps", jsii_struct_bases=[], name_mapping={'catalog_id': 'catalogId', 'database_name': 'databaseName', 'partition_input': 'partitionInput', 'table_name': 'tableName'})
class CfnPartitionProps():
    def __init__(self, *, catalog_id: str, database_name: str, partition_input: typing.Union[aws_cdk.core.IResolvable, "CfnPartition.PartitionInputProperty"], table_name: str):
        """Properties for defining a ``AWS::Glue::Partition``.

        :param catalog_id: ``AWS::Glue::Partition.CatalogId``.
        :param database_name: ``AWS::Glue::Partition.DatabaseName``.
        :param partition_input: ``AWS::Glue::Partition.PartitionInput``.
        :param table_name: ``AWS::Glue::Partition.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html
        """
        self._values = {
            'catalog_id': catalog_id,
            'database_name': database_name,
            'partition_input': partition_input,
            'table_name': table_name,
        }

    @property
    def catalog_id(self) -> str:
        """``AWS::Glue::Partition.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-catalogid
        """
        return self._values.get('catalog_id')

    @property
    def database_name(self) -> str:
        """``AWS::Glue::Partition.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-databasename
        """
        return self._values.get('database_name')

    @property
    def partition_input(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnPartition.PartitionInputProperty"]:
        """``AWS::Glue::Partition.PartitionInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-partitioninput
        """
        return self._values.get('partition_input')

    @property
    def table_name(self) -> str:
        """``AWS::Glue::Partition.TableName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-partition.html#cfn-glue-partition-tablename
        """
        return self._values.get('table_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnPartitionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnSecurityConfiguration(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnSecurityConfiguration"):
    """A CloudFormation ``AWS::Glue::SecurityConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::SecurityConfiguration
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, encryption_configuration: typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigurationProperty"], name: str) -> None:
        """Create a new ``AWS::Glue::SecurityConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param encryption_configuration: ``AWS::Glue::SecurityConfiguration.EncryptionConfiguration``.
        :param name: ``AWS::Glue::SecurityConfiguration.Name``.
        """
        props = CfnSecurityConfigurationProps(encryption_configuration=encryption_configuration, name=name)

        jsii.create(CfnSecurityConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(self) -> typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigurationProperty"]:
        """``AWS::Glue::SecurityConfiguration.EncryptionConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration
        """
        return jsii.get(self, "encryptionConfiguration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: typing.Union[aws_cdk.core.IResolvable, "EncryptionConfigurationProperty"]):
        return jsii.set(self, "encryptionConfiguration", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Glue::SecurityConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnSecurityConfiguration.CloudWatchEncryptionProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_encryption_mode': 'cloudWatchEncryptionMode', 'kms_key_arn': 'kmsKeyArn'})
    class CloudWatchEncryptionProperty():
        def __init__(self, *, cloud_watch_encryption_mode: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None):
            """
            :param cloud_watch_encryption_mode: ``CfnSecurityConfiguration.CloudWatchEncryptionProperty.CloudWatchEncryptionMode``.
            :param kms_key_arn: ``CfnSecurityConfiguration.CloudWatchEncryptionProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html
            """
            self._values = {
            }
            if cloud_watch_encryption_mode is not None: self._values["cloud_watch_encryption_mode"] = cloud_watch_encryption_mode
            if kms_key_arn is not None: self._values["kms_key_arn"] = kms_key_arn

        @property
        def cloud_watch_encryption_mode(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.CloudWatchEncryptionProperty.CloudWatchEncryptionMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html#cfn-glue-securityconfiguration-cloudwatchencryption-cloudwatchencryptionmode
            """
            return self._values.get('cloud_watch_encryption_mode')

        @property
        def kms_key_arn(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.CloudWatchEncryptionProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-cloudwatchencryption.html#cfn-glue-securityconfiguration-cloudwatchencryption-kmskeyarn
            """
            return self._values.get('kms_key_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'CloudWatchEncryptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnSecurityConfiguration.EncryptionConfigurationProperty", jsii_struct_bases=[], name_mapping={'cloud_watch_encryption': 'cloudWatchEncryption', 'job_bookmarks_encryption': 'jobBookmarksEncryption', 's3_encryptions': 's3Encryptions'})
    class EncryptionConfigurationProperty():
        def __init__(self, *, cloud_watch_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecurityConfiguration.CloudWatchEncryptionProperty"]]]=None, job_bookmarks_encryption: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecurityConfiguration.JobBookmarksEncryptionProperty"]]]=None, s3_encryptions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSecurityConfiguration.S3EncryptionProperty"]]]]]=None):
            """
            :param cloud_watch_encryption: ``CfnSecurityConfiguration.EncryptionConfigurationProperty.CloudWatchEncryption``.
            :param job_bookmarks_encryption: ``CfnSecurityConfiguration.EncryptionConfigurationProperty.JobBookmarksEncryption``.
            :param s3_encryptions: ``CfnSecurityConfiguration.EncryptionConfigurationProperty.S3Encryptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html
            """
            self._values = {
            }
            if cloud_watch_encryption is not None: self._values["cloud_watch_encryption"] = cloud_watch_encryption
            if job_bookmarks_encryption is not None: self._values["job_bookmarks_encryption"] = job_bookmarks_encryption
            if s3_encryptions is not None: self._values["s3_encryptions"] = s3_encryptions

        @property
        def cloud_watch_encryption(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecurityConfiguration.CloudWatchEncryptionProperty"]]]:
            """``CfnSecurityConfiguration.EncryptionConfigurationProperty.CloudWatchEncryption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-cloudwatchencryption
            """
            return self._values.get('cloud_watch_encryption')

        @property
        def job_bookmarks_encryption(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnSecurityConfiguration.JobBookmarksEncryptionProperty"]]]:
            """``CfnSecurityConfiguration.EncryptionConfigurationProperty.JobBookmarksEncryption``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-jobbookmarksencryption
            """
            return self._values.get('job_bookmarks_encryption')

        @property
        def s3_encryptions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnSecurityConfiguration.S3EncryptionProperty"]]]]]:
            """``CfnSecurityConfiguration.EncryptionConfigurationProperty.S3Encryptions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-encryptionconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration-s3encryptions
            """
            return self._values.get('s3_encryptions')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'EncryptionConfigurationProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnSecurityConfiguration.JobBookmarksEncryptionProperty", jsii_struct_bases=[], name_mapping={'job_bookmarks_encryption_mode': 'jobBookmarksEncryptionMode', 'kms_key_arn': 'kmsKeyArn'})
    class JobBookmarksEncryptionProperty():
        def __init__(self, *, job_bookmarks_encryption_mode: typing.Optional[str]=None, kms_key_arn: typing.Optional[str]=None):
            """
            :param job_bookmarks_encryption_mode: ``CfnSecurityConfiguration.JobBookmarksEncryptionProperty.JobBookmarksEncryptionMode``.
            :param kms_key_arn: ``CfnSecurityConfiguration.JobBookmarksEncryptionProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html
            """
            self._values = {
            }
            if job_bookmarks_encryption_mode is not None: self._values["job_bookmarks_encryption_mode"] = job_bookmarks_encryption_mode
            if kms_key_arn is not None: self._values["kms_key_arn"] = kms_key_arn

        @property
        def job_bookmarks_encryption_mode(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.JobBookmarksEncryptionProperty.JobBookmarksEncryptionMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html#cfn-glue-securityconfiguration-jobbookmarksencryption-jobbookmarksencryptionmode
            """
            return self._values.get('job_bookmarks_encryption_mode')

        @property
        def kms_key_arn(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.JobBookmarksEncryptionProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-jobbookmarksencryption.html#cfn-glue-securityconfiguration-jobbookmarksencryption-kmskeyarn
            """
            return self._values.get('kms_key_arn')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'JobBookmarksEncryptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnSecurityConfiguration.S3EncryptionProperty", jsii_struct_bases=[], name_mapping={'kms_key_arn': 'kmsKeyArn', 's3_encryption_mode': 's3EncryptionMode'})
    class S3EncryptionProperty():
        def __init__(self, *, kms_key_arn: typing.Optional[str]=None, s3_encryption_mode: typing.Optional[str]=None):
            """
            :param kms_key_arn: ``CfnSecurityConfiguration.S3EncryptionProperty.KmsKeyArn``.
            :param s3_encryption_mode: ``CfnSecurityConfiguration.S3EncryptionProperty.S3EncryptionMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html
            """
            self._values = {
            }
            if kms_key_arn is not None: self._values["kms_key_arn"] = kms_key_arn
            if s3_encryption_mode is not None: self._values["s3_encryption_mode"] = s3_encryption_mode

        @property
        def kms_key_arn(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.S3EncryptionProperty.KmsKeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html#cfn-glue-securityconfiguration-s3encryption-kmskeyarn
            """
            return self._values.get('kms_key_arn')

        @property
        def s3_encryption_mode(self) -> typing.Optional[str]:
            """``CfnSecurityConfiguration.S3EncryptionProperty.S3EncryptionMode``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-securityconfiguration-s3encryption.html#cfn-glue-securityconfiguration-s3encryption-s3encryptionmode
            """
            return self._values.get('s3_encryption_mode')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'S3EncryptionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnSecurityConfigurationProps", jsii_struct_bases=[], name_mapping={'encryption_configuration': 'encryptionConfiguration', 'name': 'name'})
class CfnSecurityConfigurationProps():
    def __init__(self, *, encryption_configuration: typing.Union[aws_cdk.core.IResolvable, "CfnSecurityConfiguration.EncryptionConfigurationProperty"], name: str):
        """Properties for defining a ``AWS::Glue::SecurityConfiguration``.

        :param encryption_configuration: ``AWS::Glue::SecurityConfiguration.EncryptionConfiguration``.
        :param name: ``AWS::Glue::SecurityConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html
        """
        self._values = {
            'encryption_configuration': encryption_configuration,
            'name': name,
        }

    @property
    def encryption_configuration(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnSecurityConfiguration.EncryptionConfigurationProperty"]:
        """``AWS::Glue::SecurityConfiguration.EncryptionConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-encryptionconfiguration
        """
        return self._values.get('encryption_configuration')

    @property
    def name(self) -> str:
        """``AWS::Glue::SecurityConfiguration.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-securityconfiguration.html#cfn-glue-securityconfiguration-name
        """
        return self._values.get('name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnSecurityConfigurationProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTable(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnTable"):
    """A CloudFormation ``AWS::Glue::Table``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Table
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, catalog_id: str, database_name: str, table_input: typing.Union[aws_cdk.core.IResolvable, "TableInputProperty"]) -> None:
        """Create a new ``AWS::Glue::Table``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param catalog_id: ``AWS::Glue::Table.CatalogId``.
        :param database_name: ``AWS::Glue::Table.DatabaseName``.
        :param table_input: ``AWS::Glue::Table.TableInput``.
        """
        props = CfnTableProps(catalog_id=catalog_id, database_name=database_name, table_input=table_input)

        jsii.create(CfnTable, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """``AWS::Glue::Table.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-catalogid
        """
        return jsii.get(self, "catalogId")

    @catalog_id.setter
    def catalog_id(self, value: str):
        return jsii.set(self, "catalogId", value)

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        """``AWS::Glue::Table.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter
    def database_name(self, value: str):
        return jsii.set(self, "databaseName", value)

    @property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Union[aws_cdk.core.IResolvable, "TableInputProperty"]:
        """``AWS::Glue::Table.TableInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-tableinput
        """
        return jsii.get(self, "tableInput")

    @table_input.setter
    def table_input(self, value: typing.Union[aws_cdk.core.IResolvable, "TableInputProperty"]):
        return jsii.set(self, "tableInput", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.ColumnProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'comment': 'comment', 'type': 'type'})
    class ColumnProperty():
        def __init__(self, *, name: str, comment: typing.Optional[str]=None, type: typing.Optional[str]=None):
            """
            :param name: ``CfnTable.ColumnProperty.Name``.
            :param comment: ``CfnTable.ColumnProperty.Comment``.
            :param type: ``CfnTable.ColumnProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html
            """
            self._values = {
                'name': name,
            }
            if comment is not None: self._values["comment"] = comment
            if type is not None: self._values["type"] = type

        @property
        def name(self) -> str:
            """``CfnTable.ColumnProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-name
            """
            return self._values.get('name')

        @property
        def comment(self) -> typing.Optional[str]:
            """``CfnTable.ColumnProperty.Comment``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-comment
            """
            return self._values.get('comment')

        @property
        def type(self) -> typing.Optional[str]:
            """``CfnTable.ColumnProperty.Type``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-column.html#cfn-glue-table-column-type
            """
            return self._values.get('type')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ColumnProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.OrderProperty", jsii_struct_bases=[], name_mapping={'column': 'column', 'sort_order': 'sortOrder'})
    class OrderProperty():
        def __init__(self, *, column: str, sort_order: jsii.Number):
            """
            :param column: ``CfnTable.OrderProperty.Column``.
            :param sort_order: ``CfnTable.OrderProperty.SortOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html
            """
            self._values = {
                'column': column,
                'sort_order': sort_order,
            }

        @property
        def column(self) -> str:
            """``CfnTable.OrderProperty.Column``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html#cfn-glue-table-order-column
            """
            return self._values.get('column')

        @property
        def sort_order(self) -> jsii.Number:
            """``CfnTable.OrderProperty.SortOrder``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-order.html#cfn-glue-table-order-sortorder
            """
            return self._values.get('sort_order')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'OrderProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.SerdeInfoProperty", jsii_struct_bases=[], name_mapping={'name': 'name', 'parameters': 'parameters', 'serialization_library': 'serializationLibrary'})
    class SerdeInfoProperty():
        def __init__(self, *, name: typing.Optional[str]=None, parameters: typing.Any=None, serialization_library: typing.Optional[str]=None):
            """
            :param name: ``CfnTable.SerdeInfoProperty.Name``.
            :param parameters: ``CfnTable.SerdeInfoProperty.Parameters``.
            :param serialization_library: ``CfnTable.SerdeInfoProperty.SerializationLibrary``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html
            """
            self._values = {
            }
            if name is not None: self._values["name"] = name
            if parameters is not None: self._values["parameters"] = parameters
            if serialization_library is not None: self._values["serialization_library"] = serialization_library

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnTable.SerdeInfoProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-name
            """
            return self._values.get('name')

        @property
        def parameters(self) -> typing.Any:
            """``CfnTable.SerdeInfoProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-parameters
            """
            return self._values.get('parameters')

        @property
        def serialization_library(self) -> typing.Optional[str]:
            """``CfnTable.SerdeInfoProperty.SerializationLibrary``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-serdeinfo.html#cfn-glue-table-serdeinfo-serializationlibrary
            """
            return self._values.get('serialization_library')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SerdeInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.SkewedInfoProperty", jsii_struct_bases=[], name_mapping={'skewed_column_names': 'skewedColumnNames', 'skewed_column_value_location_maps': 'skewedColumnValueLocationMaps', 'skewed_column_values': 'skewedColumnValues'})
    class SkewedInfoProperty():
        def __init__(self, *, skewed_column_names: typing.Optional[typing.List[str]]=None, skewed_column_value_location_maps: typing.Any=None, skewed_column_values: typing.Optional[typing.List[str]]=None):
            """
            :param skewed_column_names: ``CfnTable.SkewedInfoProperty.SkewedColumnNames``.
            :param skewed_column_value_location_maps: ``CfnTable.SkewedInfoProperty.SkewedColumnValueLocationMaps``.
            :param skewed_column_values: ``CfnTable.SkewedInfoProperty.SkewedColumnValues``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html
            """
            self._values = {
            }
            if skewed_column_names is not None: self._values["skewed_column_names"] = skewed_column_names
            if skewed_column_value_location_maps is not None: self._values["skewed_column_value_location_maps"] = skewed_column_value_location_maps
            if skewed_column_values is not None: self._values["skewed_column_values"] = skewed_column_values

        @property
        def skewed_column_names(self) -> typing.Optional[typing.List[str]]:
            """``CfnTable.SkewedInfoProperty.SkewedColumnNames``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnnames
            """
            return self._values.get('skewed_column_names')

        @property
        def skewed_column_value_location_maps(self) -> typing.Any:
            """``CfnTable.SkewedInfoProperty.SkewedColumnValueLocationMaps``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnvaluelocationmaps
            """
            return self._values.get('skewed_column_value_location_maps')

        @property
        def skewed_column_values(self) -> typing.Optional[typing.List[str]]:
            """``CfnTable.SkewedInfoProperty.SkewedColumnValues``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-skewedinfo.html#cfn-glue-table-skewedinfo-skewedcolumnvalues
            """
            return self._values.get('skewed_column_values')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'SkewedInfoProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.StorageDescriptorProperty", jsii_struct_bases=[], name_mapping={'bucket_columns': 'bucketColumns', 'columns': 'columns', 'compressed': 'compressed', 'input_format': 'inputFormat', 'location': 'location', 'number_of_buckets': 'numberOfBuckets', 'output_format': 'outputFormat', 'parameters': 'parameters', 'serde_info': 'serdeInfo', 'skewed_info': 'skewedInfo', 'sort_columns': 'sortColumns', 'stored_as_sub_directories': 'storedAsSubDirectories'})
    class StorageDescriptorProperty():
        def __init__(self, *, bucket_columns: typing.Optional[typing.List[str]]=None, columns: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ColumnProperty"]]]]]=None, compressed: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, input_format: typing.Optional[str]=None, location: typing.Optional[str]=None, number_of_buckets: typing.Optional[jsii.Number]=None, output_format: typing.Optional[str]=None, parameters: typing.Any=None, serde_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.SerdeInfoProperty"]]]=None, skewed_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.SkewedInfoProperty"]]]=None, sort_columns: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.OrderProperty"]]]]]=None, stored_as_sub_directories: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None):
            """
            :param bucket_columns: ``CfnTable.StorageDescriptorProperty.BucketColumns``.
            :param columns: ``CfnTable.StorageDescriptorProperty.Columns``.
            :param compressed: ``CfnTable.StorageDescriptorProperty.Compressed``.
            :param input_format: ``CfnTable.StorageDescriptorProperty.InputFormat``.
            :param location: ``CfnTable.StorageDescriptorProperty.Location``.
            :param number_of_buckets: ``CfnTable.StorageDescriptorProperty.NumberOfBuckets``.
            :param output_format: ``CfnTable.StorageDescriptorProperty.OutputFormat``.
            :param parameters: ``CfnTable.StorageDescriptorProperty.Parameters``.
            :param serde_info: ``CfnTable.StorageDescriptorProperty.SerdeInfo``.
            :param skewed_info: ``CfnTable.StorageDescriptorProperty.SkewedInfo``.
            :param sort_columns: ``CfnTable.StorageDescriptorProperty.SortColumns``.
            :param stored_as_sub_directories: ``CfnTable.StorageDescriptorProperty.StoredAsSubDirectories``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html
            """
            self._values = {
            }
            if bucket_columns is not None: self._values["bucket_columns"] = bucket_columns
            if columns is not None: self._values["columns"] = columns
            if compressed is not None: self._values["compressed"] = compressed
            if input_format is not None: self._values["input_format"] = input_format
            if location is not None: self._values["location"] = location
            if number_of_buckets is not None: self._values["number_of_buckets"] = number_of_buckets
            if output_format is not None: self._values["output_format"] = output_format
            if parameters is not None: self._values["parameters"] = parameters
            if serde_info is not None: self._values["serde_info"] = serde_info
            if skewed_info is not None: self._values["skewed_info"] = skewed_info
            if sort_columns is not None: self._values["sort_columns"] = sort_columns
            if stored_as_sub_directories is not None: self._values["stored_as_sub_directories"] = stored_as_sub_directories

        @property
        def bucket_columns(self) -> typing.Optional[typing.List[str]]:
            """``CfnTable.StorageDescriptorProperty.BucketColumns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-bucketcolumns
            """
            return self._values.get('bucket_columns')

        @property
        def columns(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ColumnProperty"]]]]]:
            """``CfnTable.StorageDescriptorProperty.Columns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-columns
            """
            return self._values.get('columns')

        @property
        def compressed(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTable.StorageDescriptorProperty.Compressed``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-compressed
            """
            return self._values.get('compressed')

        @property
        def input_format(self) -> typing.Optional[str]:
            """``CfnTable.StorageDescriptorProperty.InputFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-inputformat
            """
            return self._values.get('input_format')

        @property
        def location(self) -> typing.Optional[str]:
            """``CfnTable.StorageDescriptorProperty.Location``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-location
            """
            return self._values.get('location')

        @property
        def number_of_buckets(self) -> typing.Optional[jsii.Number]:
            """``CfnTable.StorageDescriptorProperty.NumberOfBuckets``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-numberofbuckets
            """
            return self._values.get('number_of_buckets')

        @property
        def output_format(self) -> typing.Optional[str]:
            """``CfnTable.StorageDescriptorProperty.OutputFormat``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-outputformat
            """
            return self._values.get('output_format')

        @property
        def parameters(self) -> typing.Any:
            """``CfnTable.StorageDescriptorProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-parameters
            """
            return self._values.get('parameters')

        @property
        def serde_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.SerdeInfoProperty"]]]:
            """``CfnTable.StorageDescriptorProperty.SerdeInfo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-serdeinfo
            """
            return self._values.get('serde_info')

        @property
        def skewed_info(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.SkewedInfoProperty"]]]:
            """``CfnTable.StorageDescriptorProperty.SkewedInfo``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-skewedinfo
            """
            return self._values.get('skewed_info')

        @property
        def sort_columns(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.OrderProperty"]]]]]:
            """``CfnTable.StorageDescriptorProperty.SortColumns``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-sortcolumns
            """
            return self._values.get('sort_columns')

        @property
        def stored_as_sub_directories(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
            """``CfnTable.StorageDescriptorProperty.StoredAsSubDirectories``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-storagedescriptor.html#cfn-glue-table-storagedescriptor-storedassubdirectories
            """
            return self._values.get('stored_as_sub_directories')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'StorageDescriptorProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTable.TableInputProperty", jsii_struct_bases=[], name_mapping={'description': 'description', 'name': 'name', 'owner': 'owner', 'parameters': 'parameters', 'partition_keys': 'partitionKeys', 'retention': 'retention', 'storage_descriptor': 'storageDescriptor', 'table_type': 'tableType', 'view_expanded_text': 'viewExpandedText', 'view_original_text': 'viewOriginalText'})
    class TableInputProperty():
        def __init__(self, *, description: typing.Optional[str]=None, name: typing.Optional[str]=None, owner: typing.Optional[str]=None, parameters: typing.Any=None, partition_keys: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ColumnProperty"]]]]]=None, retention: typing.Optional[jsii.Number]=None, storage_descriptor: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.StorageDescriptorProperty"]]]=None, table_type: typing.Optional[str]=None, view_expanded_text: typing.Optional[str]=None, view_original_text: typing.Optional[str]=None):
            """
            :param description: ``CfnTable.TableInputProperty.Description``.
            :param name: ``CfnTable.TableInputProperty.Name``.
            :param owner: ``CfnTable.TableInputProperty.Owner``.
            :param parameters: ``CfnTable.TableInputProperty.Parameters``.
            :param partition_keys: ``CfnTable.TableInputProperty.PartitionKeys``.
            :param retention: ``CfnTable.TableInputProperty.Retention``.
            :param storage_descriptor: ``CfnTable.TableInputProperty.StorageDescriptor``.
            :param table_type: ``CfnTable.TableInputProperty.TableType``.
            :param view_expanded_text: ``CfnTable.TableInputProperty.ViewExpandedText``.
            :param view_original_text: ``CfnTable.TableInputProperty.ViewOriginalText``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html
            """
            self._values = {
            }
            if description is not None: self._values["description"] = description
            if name is not None: self._values["name"] = name
            if owner is not None: self._values["owner"] = owner
            if parameters is not None: self._values["parameters"] = parameters
            if partition_keys is not None: self._values["partition_keys"] = partition_keys
            if retention is not None: self._values["retention"] = retention
            if storage_descriptor is not None: self._values["storage_descriptor"] = storage_descriptor
            if table_type is not None: self._values["table_type"] = table_type
            if view_expanded_text is not None: self._values["view_expanded_text"] = view_expanded_text
            if view_original_text is not None: self._values["view_original_text"] = view_original_text

        @property
        def description(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-description
            """
            return self._values.get('description')

        @property
        def name(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-name
            """
            return self._values.get('name')

        @property
        def owner(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.Owner``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-owner
            """
            return self._values.get('owner')

        @property
        def parameters(self) -> typing.Any:
            """``CfnTable.TableInputProperty.Parameters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
            """
            return self._values.get('parameters')

        @property
        def partition_keys(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTable.ColumnProperty"]]]]]:
            """``CfnTable.TableInputProperty.PartitionKeys``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-partitionkeys
            """
            return self._values.get('partition_keys')

        @property
        def retention(self) -> typing.Optional[jsii.Number]:
            """``CfnTable.TableInputProperty.Retention``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-retention
            """
            return self._values.get('retention')

        @property
        def storage_descriptor(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTable.StorageDescriptorProperty"]]]:
            """``CfnTable.TableInputProperty.StorageDescriptor``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-storagedescriptor
            """
            return self._values.get('storage_descriptor')

        @property
        def table_type(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.TableType``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-tabletype
            """
            return self._values.get('table_type')

        @property
        def view_expanded_text(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.ViewExpandedText``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-viewexpandedtext
            """
            return self._values.get('view_expanded_text')

        @property
        def view_original_text(self) -> typing.Optional[str]:
            """``CfnTable.TableInputProperty.ViewOriginalText``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-vieworiginaltext
            """
            return self._values.get('view_original_text')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'TableInputProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTableProps", jsii_struct_bases=[], name_mapping={'catalog_id': 'catalogId', 'database_name': 'databaseName', 'table_input': 'tableInput'})
class CfnTableProps():
    def __init__(self, *, catalog_id: str, database_name: str, table_input: typing.Union[aws_cdk.core.IResolvable, "CfnTable.TableInputProperty"]):
        """Properties for defining a ``AWS::Glue::Table``.

        :param catalog_id: ``AWS::Glue::Table.CatalogId``.
        :param database_name: ``AWS::Glue::Table.DatabaseName``.
        :param table_input: ``AWS::Glue::Table.TableInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html
        """
        self._values = {
            'catalog_id': catalog_id,
            'database_name': database_name,
            'table_input': table_input,
        }

    @property
    def catalog_id(self) -> str:
        """``AWS::Glue::Table.CatalogId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-catalogid
        """
        return self._values.get('catalog_id')

    @property
    def database_name(self) -> str:
        """``AWS::Glue::Table.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-databasename
        """
        return self._values.get('database_name')

    @property
    def table_input(self) -> typing.Union[aws_cdk.core.IResolvable, "CfnTable.TableInputProperty"]:
        """``AWS::Glue::Table.TableInput``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-table.html#cfn-glue-table-tableinput
        """
        return self._values.get('table_input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTableProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnTrigger(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnTrigger"):
    """A CloudFormation ``AWS::Glue::Trigger``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Trigger
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]], type: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None, predicate: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PredicateProperty"]]]=None, schedule: typing.Optional[str]=None, start_on_creation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Any=None, workflow_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Glue::Trigger``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param actions: ``AWS::Glue::Trigger.Actions``.
        :param type: ``AWS::Glue::Trigger.Type``.
        :param description: ``AWS::Glue::Trigger.Description``.
        :param name: ``AWS::Glue::Trigger.Name``.
        :param predicate: ``AWS::Glue::Trigger.Predicate``.
        :param schedule: ``AWS::Glue::Trigger.Schedule``.
        :param start_on_creation: ``AWS::Glue::Trigger.StartOnCreation``.
        :param tags: ``AWS::Glue::Trigger.Tags``.
        :param workflow_name: ``AWS::Glue::Trigger.WorkflowName``.
        """
        props = CfnTriggerProps(actions=actions, type=type, description=description, name=name, predicate=predicate, schedule=schedule, start_on_creation=start_on_creation, tags=tags, workflow_name=workflow_name)

        jsii.create(CfnTrigger, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Glue::Trigger.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]]:
        """``AWS::Glue::Trigger.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-actions
        """
        return jsii.get(self, "actions")

    @actions.setter
    def actions(self, value: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "ActionProperty"]]]):
        return jsii.set(self, "actions", value)

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> str:
        """``AWS::Glue::Trigger.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-type
        """
        return jsii.get(self, "type")

    @type.setter
    def type(self, value: str):
        return jsii.set(self, "type", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)

    @property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PredicateProperty"]]]:
        """``AWS::Glue::Trigger.Predicate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-predicate
        """
        return jsii.get(self, "predicate")

    @predicate.setter
    def predicate(self, value: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["PredicateProperty"]]]):
        return jsii.set(self, "predicate", value)

    @property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: typing.Optional[str]):
        return jsii.set(self, "schedule", value)

    @property
    @jsii.member(jsii_name="startOnCreation")
    def start_on_creation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Glue::Trigger.StartOnCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-startoncreation
        """
        return jsii.get(self, "startOnCreation")

    @start_on_creation.setter
    def start_on_creation(self, value: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]):
        return jsii.set(self, "startOnCreation", value)

    @property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.WorkflowName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-workflowname
        """
        return jsii.get(self, "workflowName")

    @workflow_name.setter
    def workflow_name(self, value: typing.Optional[str]):
        return jsii.set(self, "workflowName", value)

    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.ActionProperty", jsii_struct_bases=[], name_mapping={'arguments': 'arguments', 'crawler_name': 'crawlerName', 'job_name': 'jobName', 'notification_property': 'notificationProperty', 'security_configuration': 'securityConfiguration', 'timeout': 'timeout'})
    class ActionProperty():
        def __init__(self, *, arguments: typing.Any=None, crawler_name: typing.Optional[str]=None, job_name: typing.Optional[str]=None, notification_property: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTrigger.NotificationPropertyProperty"]]]=None, security_configuration: typing.Optional[str]=None, timeout: typing.Optional[jsii.Number]=None):
            """
            :param arguments: ``CfnTrigger.ActionProperty.Arguments``.
            :param crawler_name: ``CfnTrigger.ActionProperty.CrawlerName``.
            :param job_name: ``CfnTrigger.ActionProperty.JobName``.
            :param notification_property: ``CfnTrigger.ActionProperty.NotificationProperty``.
            :param security_configuration: ``CfnTrigger.ActionProperty.SecurityConfiguration``.
            :param timeout: ``CfnTrigger.ActionProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html
            """
            self._values = {
            }
            if arguments is not None: self._values["arguments"] = arguments
            if crawler_name is not None: self._values["crawler_name"] = crawler_name
            if job_name is not None: self._values["job_name"] = job_name
            if notification_property is not None: self._values["notification_property"] = notification_property
            if security_configuration is not None: self._values["security_configuration"] = security_configuration
            if timeout is not None: self._values["timeout"] = timeout

        @property
        def arguments(self) -> typing.Any:
            """``CfnTrigger.ActionProperty.Arguments``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-arguments
            """
            return self._values.get('arguments')

        @property
        def crawler_name(self) -> typing.Optional[str]:
            """``CfnTrigger.ActionProperty.CrawlerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-crawlername
            """
            return self._values.get('crawler_name')

        @property
        def job_name(self) -> typing.Optional[str]:
            """``CfnTrigger.ActionProperty.JobName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-jobname
            """
            return self._values.get('job_name')

        @property
        def notification_property(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTrigger.NotificationPropertyProperty"]]]:
            """``CfnTrigger.ActionProperty.NotificationProperty``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-notificationproperty
            """
            return self._values.get('notification_property')

        @property
        def security_configuration(self) -> typing.Optional[str]:
            """``CfnTrigger.ActionProperty.SecurityConfiguration``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-securityconfiguration
            """
            return self._values.get('security_configuration')

        @property
        def timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnTrigger.ActionProperty.Timeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-action.html#cfn-glue-trigger-action-timeout
            """
            return self._values.get('timeout')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ActionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.ConditionProperty", jsii_struct_bases=[], name_mapping={'crawler_name': 'crawlerName', 'crawl_state': 'crawlState', 'job_name': 'jobName', 'logical_operator': 'logicalOperator', 'state': 'state'})
    class ConditionProperty():
        def __init__(self, *, crawler_name: typing.Optional[str]=None, crawl_state: typing.Optional[str]=None, job_name: typing.Optional[str]=None, logical_operator: typing.Optional[str]=None, state: typing.Optional[str]=None):
            """
            :param crawler_name: ``CfnTrigger.ConditionProperty.CrawlerName``.
            :param crawl_state: ``CfnTrigger.ConditionProperty.CrawlState``.
            :param job_name: ``CfnTrigger.ConditionProperty.JobName``.
            :param logical_operator: ``CfnTrigger.ConditionProperty.LogicalOperator``.
            :param state: ``CfnTrigger.ConditionProperty.State``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html
            """
            self._values = {
            }
            if crawler_name is not None: self._values["crawler_name"] = crawler_name
            if crawl_state is not None: self._values["crawl_state"] = crawl_state
            if job_name is not None: self._values["job_name"] = job_name
            if logical_operator is not None: self._values["logical_operator"] = logical_operator
            if state is not None: self._values["state"] = state

        @property
        def crawler_name(self) -> typing.Optional[str]:
            """``CfnTrigger.ConditionProperty.CrawlerName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlername
            """
            return self._values.get('crawler_name')

        @property
        def crawl_state(self) -> typing.Optional[str]:
            """``CfnTrigger.ConditionProperty.CrawlState``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-crawlstate
            """
            return self._values.get('crawl_state')

        @property
        def job_name(self) -> typing.Optional[str]:
            """``CfnTrigger.ConditionProperty.JobName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-jobname
            """
            return self._values.get('job_name')

        @property
        def logical_operator(self) -> typing.Optional[str]:
            """``CfnTrigger.ConditionProperty.LogicalOperator``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-logicaloperator
            """
            return self._values.get('logical_operator')

        @property
        def state(self) -> typing.Optional[str]:
            """``CfnTrigger.ConditionProperty.State``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-condition.html#cfn-glue-trigger-condition-state
            """
            return self._values.get('state')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'ConditionProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.NotificationPropertyProperty", jsii_struct_bases=[], name_mapping={'notify_delay_after': 'notifyDelayAfter'})
    class NotificationPropertyProperty():
        def __init__(self, *, notify_delay_after: typing.Optional[jsii.Number]=None):
            """
            :param notify_delay_after: ``CfnTrigger.NotificationPropertyProperty.NotifyDelayAfter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html
            """
            self._values = {
            }
            if notify_delay_after is not None: self._values["notify_delay_after"] = notify_delay_after

        @property
        def notify_delay_after(self) -> typing.Optional[jsii.Number]:
            """``CfnTrigger.NotificationPropertyProperty.NotifyDelayAfter``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-notificationproperty.html#cfn-glue-trigger-notificationproperty-notifydelayafter
            """
            return self._values.get('notify_delay_after')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'NotificationPropertyProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


    @jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTrigger.PredicateProperty", jsii_struct_bases=[], name_mapping={'conditions': 'conditions', 'logical': 'logical'})
    class PredicateProperty():
        def __init__(self, *, conditions: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTrigger.ConditionProperty"]]]]]=None, logical: typing.Optional[str]=None):
            """
            :param conditions: ``CfnTrigger.PredicateProperty.Conditions``.
            :param logical: ``CfnTrigger.PredicateProperty.Logical``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html
            """
            self._values = {
            }
            if conditions is not None: self._values["conditions"] = conditions
            if logical is not None: self._values["logical"] = logical

        @property
        def conditions(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional[typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTrigger.ConditionProperty"]]]]]:
            """``CfnTrigger.PredicateProperty.Conditions``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-conditions
            """
            return self._values.get('conditions')

        @property
        def logical(self) -> typing.Optional[str]:
            """``CfnTrigger.PredicateProperty.Logical``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-trigger-predicate.html#cfn-glue-trigger-predicate-logical
            """
            return self._values.get('logical')

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return 'PredicateProperty(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())



@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnTriggerProps", jsii_struct_bases=[], name_mapping={'actions': 'actions', 'type': 'type', 'description': 'description', 'name': 'name', 'predicate': 'predicate', 'schedule': 'schedule', 'start_on_creation': 'startOnCreation', 'tags': 'tags', 'workflow_name': 'workflowName'})
class CfnTriggerProps():
    def __init__(self, *, actions: typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTrigger.ActionProperty"]]], type: str, description: typing.Optional[str]=None, name: typing.Optional[str]=None, predicate: typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTrigger.PredicateProperty"]]]=None, schedule: typing.Optional[str]=None, start_on_creation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]=None, tags: typing.Any=None, workflow_name: typing.Optional[str]=None):
        """Properties for defining a ``AWS::Glue::Trigger``.

        :param actions: ``AWS::Glue::Trigger.Actions``.
        :param type: ``AWS::Glue::Trigger.Type``.
        :param description: ``AWS::Glue::Trigger.Description``.
        :param name: ``AWS::Glue::Trigger.Name``.
        :param predicate: ``AWS::Glue::Trigger.Predicate``.
        :param schedule: ``AWS::Glue::Trigger.Schedule``.
        :param start_on_creation: ``AWS::Glue::Trigger.StartOnCreation``.
        :param tags: ``AWS::Glue::Trigger.Tags``.
        :param workflow_name: ``AWS::Glue::Trigger.WorkflowName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html
        """
        self._values = {
            'actions': actions,
            'type': type,
        }
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name
        if predicate is not None: self._values["predicate"] = predicate
        if schedule is not None: self._values["schedule"] = schedule
        if start_on_creation is not None: self._values["start_on_creation"] = start_on_creation
        if tags is not None: self._values["tags"] = tags
        if workflow_name is not None: self._values["workflow_name"] = workflow_name

    @property
    def actions(self) -> typing.Union[aws_cdk.core.IResolvable, typing.List[typing.Union[aws_cdk.core.IResolvable, "CfnTrigger.ActionProperty"]]]:
        """``AWS::Glue::Trigger.Actions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-actions
        """
        return self._values.get('actions')

    @property
    def type(self) -> str:
        """``AWS::Glue::Trigger.Type``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-type
        """
        return self._values.get('type')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-description
        """
        return self._values.get('description')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-name
        """
        return self._values.get('name')

    @property
    def predicate(self) -> typing.Optional[typing.Union[typing.Optional[aws_cdk.core.IResolvable], typing.Optional["CfnTrigger.PredicateProperty"]]]:
        """``AWS::Glue::Trigger.Predicate``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-predicate
        """
        return self._values.get('predicate')

    @property
    def schedule(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-schedule
        """
        return self._values.get('schedule')

    @property
    def start_on_creation(self) -> typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.core.IResolvable]]]:
        """``AWS::Glue::Trigger.StartOnCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-startoncreation
        """
        return self._values.get('start_on_creation')

    @property
    def tags(self) -> typing.Any:
        """``AWS::Glue::Trigger.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-tags
        """
        return self._values.get('tags')

    @property
    def workflow_name(self) -> typing.Optional[str]:
        """``AWS::Glue::Trigger.WorkflowName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-trigger.html#cfn-glue-trigger-workflowname
        """
        return self._values.get('workflow_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnTriggerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.implements(aws_cdk.core.IInspectable)
class CfnWorkflow(aws_cdk.core.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.CfnWorkflow"):
    """A CloudFormation ``AWS::Glue::Workflow``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html
    cloudformationResource:
    :cloudformationResource:: AWS::Glue::Workflow
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, default_run_properties: typing.Any=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None) -> None:
        """Create a new ``AWS::Glue::Workflow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param props: - resource properties.
        :param default_run_properties: ``AWS::Glue::Workflow.DefaultRunProperties``.
        :param description: ``AWS::Glue::Workflow.Description``.
        :param name: ``AWS::Glue::Workflow.Name``.
        :param tags: ``AWS::Glue::Workflow.Tags``.
        """
        props = CfnWorkflowProps(default_run_properties=default_run_properties, description=description, name=name, tags=tags)

        jsii.create(CfnWorkflow, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str,typing.Any]:
        return jsii.get(self, "cfnProperties")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """``AWS::Glue::Workflow.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-tags
        """
        return jsii.get(self, "tags")

    @property
    @jsii.member(jsii_name="defaultRunProperties")
    def default_run_properties(self) -> typing.Any:
        """``AWS::Glue::Workflow.DefaultRunProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-defaultrunproperties
        """
        return jsii.get(self, "defaultRunProperties")

    @default_run_properties.setter
    def default_run_properties(self, value: typing.Any):
        return jsii.set(self, "defaultRunProperties", value)

    @property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Workflow.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]):
        return jsii.set(self, "description", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Workflow.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]):
        return jsii.set(self, "name", value)


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.CfnWorkflowProps", jsii_struct_bases=[], name_mapping={'default_run_properties': 'defaultRunProperties', 'description': 'description', 'name': 'name', 'tags': 'tags'})
class CfnWorkflowProps():
    def __init__(self, *, default_run_properties: typing.Any=None, description: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Any=None):
        """Properties for defining a ``AWS::Glue::Workflow``.

        :param default_run_properties: ``AWS::Glue::Workflow.DefaultRunProperties``.
        :param description: ``AWS::Glue::Workflow.Description``.
        :param name: ``AWS::Glue::Workflow.Name``.
        :param tags: ``AWS::Glue::Workflow.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html
        """
        self._values = {
        }
        if default_run_properties is not None: self._values["default_run_properties"] = default_run_properties
        if description is not None: self._values["description"] = description
        if name is not None: self._values["name"] = name
        if tags is not None: self._values["tags"] = tags

    @property
    def default_run_properties(self) -> typing.Any:
        """``AWS::Glue::Workflow.DefaultRunProperties``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-defaultrunproperties
        """
        return self._values.get('default_run_properties')

    @property
    def description(self) -> typing.Optional[str]:
        """``AWS::Glue::Workflow.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-description
        """
        return self._values.get('description')

    @property
    def name(self) -> typing.Optional[str]:
        """``AWS::Glue::Workflow.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-name
        """
        return self._values.get('name')

    @property
    def tags(self) -> typing.Any:
        """``AWS::Glue::Workflow.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-glue-workflow.html#cfn-glue-workflow-tags
        """
        return self._values.get('tags')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CfnWorkflowProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.Column", jsii_struct_bases=[], name_mapping={'name': 'name', 'type': 'type', 'comment': 'comment'})
class Column():
    def __init__(self, *, name: str, type: "Type", comment: typing.Optional[str]=None):
        """A column of a table.

        :param name: Name of the column.
        :param type: Type of the column.
        :param comment: Coment describing the column. Default: none

        stability
        :stability: experimental
        """
        if isinstance(type, dict): type = Type(**type)
        self._values = {
            'name': name,
            'type': type,
        }
        if comment is not None: self._values["comment"] = comment

    @property
    def name(self) -> str:
        """Name of the column.

        stability
        :stability: experimental
        """
        return self._values.get('name')

    @property
    def type(self) -> "Type":
        """Type of the column.

        stability
        :stability: experimental
        """
        return self._values.get('type')

    @property
    def comment(self) -> typing.Optional[str]:
        """Coment describing the column.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get('comment')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Column(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.DataFormat", jsii_struct_bases=[], name_mapping={'input_format': 'inputFormat', 'output_format': 'outputFormat', 'serialization_library': 'serializationLibrary'})
class DataFormat():
    def __init__(self, *, input_format: "InputFormat", output_format: "OutputFormat", serialization_library: "SerializationLibrary"):
        """Defines the input/output formats and ser/de for a single DataFormat.

        :param input_format: ``InputFormat`` for this data format.
        :param output_format: ``OutputFormat`` for this data format.
        :param serialization_library: Serialization library for this data format.

        stability
        :stability: experimental
        """
        self._values = {
            'input_format': input_format,
            'output_format': output_format,
            'serialization_library': serialization_library,
        }

    @property
    def input_format(self) -> "InputFormat":
        """``InputFormat`` for this data format.

        stability
        :stability: experimental
        """
        return self._values.get('input_format')

    @property
    def output_format(self) -> "OutputFormat":
        """``OutputFormat`` for this data format.

        stability
        :stability: experimental
        """
        return self._values.get('output_format')

    @property
    def serialization_library(self) -> "SerializationLibrary":
        """Serialization library for this data format.

        stability
        :stability: experimental
        """
        return self._values.get('serialization_library')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DataFormat(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.DatabaseProps", jsii_struct_bases=[], name_mapping={'database_name': 'databaseName', 'location_uri': 'locationUri'})
class DatabaseProps():
    def __init__(self, *, database_name: str, location_uri: typing.Optional[str]=None):
        """
        :param database_name: The name of the database.
        :param location_uri: The location of the database (for example, an HDFS path). Default: a bucket is created and the database is stored under s3:///

        stability
        :stability: experimental
        """
        self._values = {
            'database_name': database_name,
        }
        if location_uri is not None: self._values["location_uri"] = location_uri

    @property
    def database_name(self) -> str:
        """The name of the database.

        stability
        :stability: experimental
        """
        return self._values.get('database_name')

    @property
    def location_uri(self) -> typing.Optional[str]:
        """The location of the database (for example, an HDFS path).

        default
        :default: a bucket is created and the database is stored under s3:///

        stability
        :stability: experimental
        """
        return self._values.get('location_uri')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DatabaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.interface(jsii_type="@aws-cdk/aws-glue.IDatabase")
class IDatabase(aws_cdk.core.IResource, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseProxy

    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        """The ARN of the catalog.

        stability
        :stability: experimental
        """
        ...

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """The catalog id of the database (usually, the AWS account id).

        stability
        :stability: experimental
        """
        ...

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        """The ARN of the database.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        """The name of the database.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IDatabaseProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-glue.IDatabase"
    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        """The ARN of the catalog.

        stability
        :stability: experimental
        """
        return jsii.get(self, "catalogArn")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """The catalog id of the database (usually, the AWS account id).

        stability
        :stability: experimental
        """
        return jsii.get(self, "catalogId")

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        """The ARN of the database.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "databaseArn")

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        """The name of the database.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "databaseName")


@jsii.implements(IDatabase)
class Database(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Database"):
    """A Glue database.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, database_name: str, location_uri: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param database_name: The name of the database.
        :param location_uri: The location of the database (for example, an HDFS path). Default: a bucket is created and the database is stored under s3:///

        stability
        :stability: experimental
        """
        props = DatabaseProps(database_name=database_name, location_uri=location_uri)

        jsii.create(Database, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseArn")
    @classmethod
    def from_database_arn(cls, scope: aws_cdk.core.Construct, id: str, database_arn: str) -> "IDatabase":
        """
        :param scope: -
        :param id: -
        :param database_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromDatabaseArn", [scope, id, database_arn])

    @property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> str:
        """ARN of the Glue catalog in which this database is stored.

        stability
        :stability: experimental
        """
        return jsii.get(self, "catalogArn")

    @property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> str:
        """ID of the Glue catalog in which this database is stored.

        stability
        :stability: experimental
        """
        return jsii.get(self, "catalogId")

    @property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> str:
        """ARN of this database.

        stability
        :stability: experimental
        """
        return jsii.get(self, "databaseArn")

    @property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> str:
        """Name of this database.

        stability
        :stability: experimental
        """
        return jsii.get(self, "databaseName")

    @property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> str:
        """Location URI of this database.

        stability
        :stability: experimental
        """
        return jsii.get(self, "locationUri")


@jsii.interface(jsii_type="@aws-cdk/aws-glue.ITable")
class ITable(aws_cdk.core.IResource, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ITableProxy

    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _ITableProxy(jsii.proxy_for(aws_cdk.core.IResource)):
    """
    stability
    :stability: experimental
    """
    __jsii_type__ = "@aws-cdk/aws-glue.ITable"
    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """
        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "tableName")


class InputFormat(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.InputFormat"):
    """Absolute class name of the Hadoop ``InputFormat`` to use when reading table files.

    stability
    :stability: experimental
    """
    def __init__(self, class_name: str) -> None:
        """
        :param class_name: -

        stability
        :stability: experimental
        """
        jsii.create(InputFormat, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="TEXT_INPUT_FORMAT")
    def TEXT_INPUT_FORMAT(cls) -> "InputFormat":
        """An InputFormat for plain text files.

        Files are broken into lines. Either linefeed or
        carriage-return are used to signal end of line. Keys are the position in the file, and
        values are the line of text.

        see
        :see: https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/mapred/TextInputFormat.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TEXT_INPUT_FORMAT")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "className")


class OutputFormat(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.OutputFormat"):
    """Absolute class name of the Hadoop ``OutputFormat`` to use when writing table files.

    stability
    :stability: experimental
    """
    def __init__(self, class_name: str) -> None:
        """
        :param class_name: -

        stability
        :stability: experimental
        """
        jsii.create(OutputFormat, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="HIVE_IGNORE_KEY_TEXT_OUTPUT_FORMAT")
    def HIVE_IGNORE_KEY_TEXT_OUTPUT_FORMAT(cls) -> "OutputFormat":
        """Writes text data with a null key (value only).

        see
        :see: https://hive.apache.org/javadocs/r2.2.0/api/org/apache/hadoop/hive/ql/io/HiveIgnoreKeyTextOutputFormat.html
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "HIVE_IGNORE_KEY_TEXT_OUTPUT_FORMAT")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "className")


class Schema(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Schema"):
    """
    see
    :see: https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    stability
    :stability: experimental
    """
    def __init__(self) -> None:
        jsii.create(Schema, self, [])

    @jsii.member(jsii_name="array")
    @classmethod
    def array(cls, *, input_string: str, is_primitive: bool) -> "Type":
        """Creates an array of some other type.

        :param item_type: type contained by the array.
        :param input_string: Glue InputString for this type.
        :param is_primitive: Indicates whether this type is a primitive data type.

        stability
        :stability: experimental
        """
        item_type = Type(input_string=input_string, is_primitive=is_primitive)

        return jsii.sinvoke(cls, "array", [item_type])

    @jsii.member(jsii_name="char")
    @classmethod
    def char(cls, length: jsii.Number) -> "Type":
        """Fixed length character data, with a specified length between 1 and 255.

        :param length: length between 1 and 255.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "char", [length])

    @jsii.member(jsii_name="decimal")
    @classmethod
    def decimal(cls, precision: jsii.Number, scale: typing.Optional[jsii.Number]=None) -> "Type":
        """Creates a decimal type.

        TODO: Bounds

        :param precision: the total number of digits.
        :param scale: the number of digits in fractional part, the default is 0.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "decimal", [precision, scale])

    @jsii.member(jsii_name="map")
    @classmethod
    def map(cls, key_type: "Type", *, input_string: str, is_primitive: bool) -> "Type":
        """Creates a map of some primitive key type to some value type.

        :param key_type: type of key, must be a primitive.
        :param value_type: type fo the value indexed by the key.
        :param input_string: Glue InputString for this type.
        :param is_primitive: Indicates whether this type is a primitive data type.

        stability
        :stability: experimental
        """
        value_type = Type(input_string=input_string, is_primitive=is_primitive)

        return jsii.sinvoke(cls, "map", [key_type, value_type])

    @jsii.member(jsii_name="struct")
    @classmethod
    def struct(cls, columns: typing.List["Column"]) -> "Type":
        """Creates a nested structure containing individually named and typed columns.

        :param columns: the columns of the structure.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "struct", [columns])

    @jsii.member(jsii_name="varchar")
    @classmethod
    def varchar(cls, length: jsii.Number) -> "Type":
        """Variable length character data, with a specified length between 1 and 65535.

        :param length: length between 1 and 65535.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "varchar", [length])

    @classproperty
    @jsii.member(jsii_name="BIG_INT")
    def BIG_INT(cls) -> "Type":
        """A 64-bit signed INTEGER in two’s complement format, with a minimum value of -2^63 and a maximum value of 2^63-1.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BIG_INT")

    @classproperty
    @jsii.member(jsii_name="BINARY")
    def BINARY(cls) -> "Type":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BINARY")

    @classproperty
    @jsii.member(jsii_name="BOOLEAN")
    def BOOLEAN(cls) -> "Type":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "BOOLEAN")

    @classproperty
    @jsii.member(jsii_name="DATE")
    def DATE(cls) -> "Type":
        """Date type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DATE")

    @classproperty
    @jsii.member(jsii_name="DOUBLE")
    def DOUBLE(cls) -> "Type":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "DOUBLE")

    @classproperty
    @jsii.member(jsii_name="FLOAT")
    def FLOAT(cls) -> "Type":
        """
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "FLOAT")

    @classproperty
    @jsii.member(jsii_name="INTEGER")
    def INTEGER(cls) -> "Type":
        """A 32-bit signed INTEGER in two’s complement format, with a minimum value of -2^31 and a maximum value of 2^31-1.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "INTEGER")

    @classproperty
    @jsii.member(jsii_name="SMALL_INT")
    def SMALL_INT(cls) -> "Type":
        """A 16-bit signed INTEGER in two’s complement format, with a minimum value of -2^15 and a maximum value of 2^15-1.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "SMALL_INT")

    @classproperty
    @jsii.member(jsii_name="STRING")
    def STRING(cls) -> "Type":
        """Arbitrary-length string type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "STRING")

    @classproperty
    @jsii.member(jsii_name="TIMESTAMP")
    def TIMESTAMP(cls) -> "Type":
        """Timestamp type (date and time).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TIMESTAMP")

    @classproperty
    @jsii.member(jsii_name="TINY_INT")
    def TINY_INT(cls) -> "Type":
        """A 8-bit signed INTEGER in two’s complement format, with a minimum value of -2^7 and a maximum value of 2^7-1.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "TINY_INT")


class SerializationLibrary(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.SerializationLibrary"):
    """Serialization library to use when serializing/deserializing (SerDe) table records.

    see
    :see: https://cwiki.apache.org/confluence/display/Hive/SerDe
    stability
    :stability: experimental
    """
    def __init__(self, class_name: str) -> None:
        """
        :param class_name: -

        stability
        :stability: experimental
        """
        jsii.create(SerializationLibrary, self, [class_name])

    @classproperty
    @jsii.member(jsii_name="HIVE_JSON")
    def HIVE_JSON(cls) -> "SerializationLibrary":
        """
        see
        :see: https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL#LanguageManualDDL-JSON
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "HIVE_JSON")

    @classproperty
    @jsii.member(jsii_name="OPENX_JSON")
    def OPENX_JSON(cls) -> "SerializationLibrary":
        """
        see
        :see: https://github.com/rcongiu/Hive-JSON-Serde
        stability
        :stability: experimental
        """
        return jsii.sget(cls, "OPENX_JSON")

    @property
    @jsii.member(jsii_name="className")
    def class_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "className")


@jsii.implements(ITable)
class Table(aws_cdk.core.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue.Table"):
    """A Glue table.

    stability
    :stability: experimental
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, columns: typing.List["Column"], database: "IDatabase", data_format: "DataFormat", table_name: str, bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, compressed: typing.Optional[bool]=None, description: typing.Optional[str]=None, encryption: typing.Optional["TableEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, partition_keys: typing.Optional[typing.List["Column"]]=None, s3_prefix: typing.Optional[str]=None, stored_as_sub_directories: typing.Optional[bool]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param columns: Columns of the table.
        :param database: Database in which to store the table.
        :param data_format: Storage type of the table's data.
        :param table_name: Name of the table.
        :param bucket: S3 bucket in which to store data. Default: one is created for you
        :param compressed: Indicates whether the table's data is compressed or not. Default: false
        :param description: Description of the table. Default: generated
        :param encryption: The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: Unencrypted
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param partition_keys: Partition columns of the table. Default: table is not partitioned
        :param s3_prefix: S3 prefix under which table objects are stored. Default: data/
        :param stored_as_sub_directories: Indicates whether the table data is stored in subdirectories. Default: false

        stability
        :stability: experimental
        """
        props = TableProps(columns=columns, database=database, data_format=data_format, table_name=table_name, bucket=bucket, compressed=compressed, description=description, encryption=encryption, encryption_key=encryption_key, partition_keys=partition_keys, s3_prefix=s3_prefix, stored_as_sub_directories=stored_as_sub_directories)

        jsii.create(Table, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableArn")
    @classmethod
    def from_table_arn(cls, scope: aws_cdk.core.Construct, id: str, table_arn: str) -> "ITable":
        """
        :param scope: -
        :param id: -
        :param table_arn: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromTableArn", [scope, id, table_arn])

    @jsii.member(jsii_name="fromTableAttributes")
    @classmethod
    def from_table_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, table_arn: str, table_name: str) -> "ITable":
        """Creates a Table construct that represents an external table.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param attrs: Import attributes.
        :param table_arn: 
        :param table_name: 

        stability
        :stability: experimental
        """
        attrs = TableAttributes(table_arn=table_arn, table_name=table_name)

        return jsii.sinvoke(cls, "fromTableAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant read and write permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantReadWrite", [grantee])

    @jsii.member(jsii_name="grantWrite")
    def grant_write(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant write permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantWrite", [grantee])

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """S3 bucket in which the table's data resides.

        stability
        :stability: experimental
        """
        return jsii.get(self, "bucket")

    @property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List["Column"]:
        """This table's columns.

        stability
        :stability: experimental
        """
        return jsii.get(self, "columns")

    @property
    @jsii.member(jsii_name="compressed")
    def compressed(self) -> bool:
        """Indicates whether the table's data is compressed or not.

        stability
        :stability: experimental
        """
        return jsii.get(self, "compressed")

    @property
    @jsii.member(jsii_name="database")
    def database(self) -> "IDatabase":
        """Database this table belongs to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "database")

    @property
    @jsii.member(jsii_name="dataFormat")
    def data_format(self) -> "DataFormat":
        """Format of this table's data files.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dataFormat")

    @property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> "TableEncryption":
        """The type of encryption enabled for the table.

        stability
        :stability: experimental
        """
        return jsii.get(self, "encryption")

    @property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> str:
        """S3 Key Prefix under which this table's files are stored in S3.

        stability
        :stability: experimental
        """
        return jsii.get(self, "s3Prefix")

    @property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> str:
        """ARN of this table.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tableArn")

    @property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> str:
        """Name of this table.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tableName")

    @property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """The KMS key used to secure the data if ``encryption`` is set to ``CSE-KMS`` or ``SSE-KMS``.

        Otherwise, ``undefined``.

        stability
        :stability: experimental
        """
        return jsii.get(self, "encryptionKey")

    @property
    @jsii.member(jsii_name="partitionKeys")
    def partition_keys(self) -> typing.Optional[typing.List["Column"]]:
        """This table's partition keys if the table is partitioned.

        stability
        :stability: experimental
        """
        return jsii.get(self, "partitionKeys")


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.TableAttributes", jsii_struct_bases=[], name_mapping={'table_arn': 'tableArn', 'table_name': 'tableName'})
class TableAttributes():
    def __init__(self, *, table_arn: str, table_name: str):
        """
        :param table_arn: 
        :param table_name: 

        stability
        :stability: experimental
        """
        self._values = {
            'table_arn': table_arn,
            'table_name': table_name,
        }

    @property
    def table_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('table_arn')

    @property
    def table_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TableAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-glue.TableEncryption")
class TableEncryption(enum.Enum):
    """Encryption options for a Table.

    see
    :see: https://docs.aws.amazon.com/athena/latest/ug/encryption.html
    stability
    :stability: experimental
    """
    UNENCRYPTED = "UNENCRYPTED"
    """
    stability
    :stability: experimental
    """
    S3_MANAGED = "S3_MANAGED"
    """Server side encryption (SSE) with an Amazon S3-managed key.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
    stability
    :stability: experimental
    """
    KMS = "KMS"
    """Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    stability
    :stability: experimental
    """
    KMS_MANAGED = "KMS_MANAGED"
    """Server-side encryption (SSE) with an AWS KMS key managed by the KMS service.

    stability
    :stability: experimental
    """
    CLIENT_SIDE_KMS = "CLIENT_SIDE_KMS"
    """Client-side encryption (CSE) with an AWS KMS key managed by the account owner.

    see
    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html
    stability
    :stability: experimental
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-glue.TableProps", jsii_struct_bases=[], name_mapping={'columns': 'columns', 'database': 'database', 'data_format': 'dataFormat', 'table_name': 'tableName', 'bucket': 'bucket', 'compressed': 'compressed', 'description': 'description', 'encryption': 'encryption', 'encryption_key': 'encryptionKey', 'partition_keys': 'partitionKeys', 's3_prefix': 's3Prefix', 'stored_as_sub_directories': 'storedAsSubDirectories'})
class TableProps():
    def __init__(self, *, columns: typing.List["Column"], database: "IDatabase", data_format: "DataFormat", table_name: str, bucket: typing.Optional[aws_cdk.aws_s3.IBucket]=None, compressed: typing.Optional[bool]=None, description: typing.Optional[str]=None, encryption: typing.Optional["TableEncryption"]=None, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, partition_keys: typing.Optional[typing.List["Column"]]=None, s3_prefix: typing.Optional[str]=None, stored_as_sub_directories: typing.Optional[bool]=None):
        """
        :param columns: Columns of the table.
        :param database: Database in which to store the table.
        :param data_format: Storage type of the table's data.
        :param table_name: Name of the table.
        :param bucket: S3 bucket in which to store data. Default: one is created for you
        :param compressed: Indicates whether the table's data is compressed or not. Default: false
        :param description: Description of the table. Default: generated
        :param encryption: The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: Unencrypted
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param partition_keys: Partition columns of the table. Default: table is not partitioned
        :param s3_prefix: S3 prefix under which table objects are stored. Default: data/
        :param stored_as_sub_directories: Indicates whether the table data is stored in subdirectories. Default: false

        stability
        :stability: experimental
        """
        if isinstance(data_format, dict): data_format = DataFormat(**data_format)
        self._values = {
            'columns': columns,
            'database': database,
            'data_format': data_format,
            'table_name': table_name,
        }
        if bucket is not None: self._values["bucket"] = bucket
        if compressed is not None: self._values["compressed"] = compressed
        if description is not None: self._values["description"] = description
        if encryption is not None: self._values["encryption"] = encryption
        if encryption_key is not None: self._values["encryption_key"] = encryption_key
        if partition_keys is not None: self._values["partition_keys"] = partition_keys
        if s3_prefix is not None: self._values["s3_prefix"] = s3_prefix
        if stored_as_sub_directories is not None: self._values["stored_as_sub_directories"] = stored_as_sub_directories

    @property
    def columns(self) -> typing.List["Column"]:
        """Columns of the table.

        stability
        :stability: experimental
        """
        return self._values.get('columns')

    @property
    def database(self) -> "IDatabase":
        """Database in which to store the table.

        stability
        :stability: experimental
        """
        return self._values.get('database')

    @property
    def data_format(self) -> "DataFormat":
        """Storage type of the table's data.

        stability
        :stability: experimental
        """
        return self._values.get('data_format')

    @property
    def table_name(self) -> str:
        """Name of the table.

        stability
        :stability: experimental
        """
        return self._values.get('table_name')

    @property
    def bucket(self) -> typing.Optional[aws_cdk.aws_s3.IBucket]:
        """S3 bucket in which to store data.

        default
        :default: one is created for you

        stability
        :stability: experimental
        """
        return self._values.get('bucket')

    @property
    def compressed(self) -> typing.Optional[bool]:
        """Indicates whether the table's data is compressed or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('compressed')

    @property
    def description(self) -> typing.Optional[str]:
        """Description of the table.

        default
        :default: generated

        stability
        :stability: experimental
        """
        return self._values.get('description')

    @property
    def encryption(self) -> typing.Optional["TableEncryption"]:
        """The kind of encryption to secure the data with.

        You can only provide this option if you are not explicitly passing in a bucket.

        If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``.
        If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``.

        default
        :default: Unencrypted

        stability
        :stability: experimental
        """
        return self._values.get('encryption')

    @property
    def encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        """External KMS key to use for bucket encryption.

        The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``.

        default
        :default: key is managed by KMS.

        stability
        :stability: experimental
        """
        return self._values.get('encryption_key')

    @property
    def partition_keys(self) -> typing.Optional[typing.List["Column"]]:
        """Partition columns of the table.

        default
        :default: table is not partitioned

        stability
        :stability: experimental
        """
        return self._values.get('partition_keys')

    @property
    def s3_prefix(self) -> typing.Optional[str]:
        """S3 prefix under which table objects are stored.

        default
        :default: data/

        stability
        :stability: experimental
        """
        return self._values.get('s3_prefix')

    @property
    def stored_as_sub_directories(self) -> typing.Optional[bool]:
        """Indicates whether the table data is stored in subdirectories.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get('stored_as_sub_directories')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'TableProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-glue.Type", jsii_struct_bases=[], name_mapping={'input_string': 'inputString', 'is_primitive': 'isPrimitive'})
class Type():
    def __init__(self, *, input_string: str, is_primitive: bool):
        """Represents a type of a column in a table schema.

        :param input_string: Glue InputString for this type.
        :param is_primitive: Indicates whether this type is a primitive data type.

        stability
        :stability: experimental
        """
        self._values = {
            'input_string': input_string,
            'is_primitive': is_primitive,
        }

    @property
    def input_string(self) -> str:
        """Glue InputString for this type.

        stability
        :stability: experimental
        """
        return self._values.get('input_string')

    @property
    def is_primitive(self) -> bool:
        """Indicates whether this type is a primitive data type.

        stability
        :stability: experimental
        """
        return self._values.get('is_primitive')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'Type(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["CfnClassifier", "CfnClassifierProps", "CfnConnection", "CfnConnectionProps", "CfnCrawler", "CfnCrawlerProps", "CfnDataCatalogEncryptionSettings", "CfnDataCatalogEncryptionSettingsProps", "CfnDatabase", "CfnDatabaseProps", "CfnDevEndpoint", "CfnDevEndpointProps", "CfnJob", "CfnJobProps", "CfnMLTransform", "CfnMLTransformProps", "CfnPartition", "CfnPartitionProps", "CfnSecurityConfiguration", "CfnSecurityConfigurationProps", "CfnTable", "CfnTableProps", "CfnTrigger", "CfnTriggerProps", "CfnWorkflow", "CfnWorkflowProps", "Column", "DataFormat", "Database", "DatabaseProps", "IDatabase", "ITable", "InputFormat", "OutputFormat", "Schema", "SerializationLibrary", "Table", "TableAttributes", "TableEncryption", "TableProps", "Type", "__jsii_assembly__"]

publication.publish()
