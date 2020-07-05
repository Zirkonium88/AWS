# Use S3 events and Lambda to change BucketPolicies

This [Lambda](https://github.com/Zirkonium88/AWS/tree/master/Lambda/Bucketpolicy/handler.py) evaluates a Bucketname. If the name matches a key word, a Bucketpolicy is changed. In this case, the Bucketpolicy sets a Deny `DeleteBucket` and `DeleteObject`.
