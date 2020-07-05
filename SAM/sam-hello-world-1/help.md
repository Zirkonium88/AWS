# Steps

sam package \
  --template-file template.yml \
  --output-template-file package.yml \
  --s3-bucket mw-800524020870-example

sam deploy \
  --template-file package.yml \
  --stack-name sam-demo \
  --capabilities CAPABILITY_IAM

sam local invoke HelloWorldFunction
