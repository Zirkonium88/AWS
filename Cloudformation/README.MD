# Cloudformation and Parameters

I like to use `Troposphere`- a Python library - for my Cloudformation workloads. In this case, I want to create two Buckets. One with a default naming and one with defined one yor my apllication. If you are ready for testing you just need to run `python CreateBucket.py > CreateBucket.yml` to print out the template.

Aftwards you can validate your template with: 

```bash
aws cloudformation validate-template --template-body file://./CreateBucket.yml
```

If everything went fine, you can deploy it with you desried Parameters:

```bash
aws cloudformation deploy --template-file ./CreateBucket.yml --stack-name deployBuckets --parameter-overrides DefaultBucket="Test1234567890" # --capabilities CAPABILITY_NAMED_IAM
```
