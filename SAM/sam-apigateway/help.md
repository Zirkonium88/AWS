# Steps

sam package \
  --template-file template.yml \
  --output-template-file api_package.yml \
  --s3-bucket mw-800524020870-example

sam deploy \
  --template-file api_package.yml \
  --stack-name sam-demo-api \
  --capabilities CAPABILITY_IAM

sam local invoke HelloWorldFunction
