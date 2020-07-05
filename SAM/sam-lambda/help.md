# Steps

sam package \
  --template-file template.yml \
  --output-template-file lambda_package.yml \
  --s3-bucket mw-800524020870-example

sam deploy \
  --template-file lambda_package.yml \
  --stack-name sam-demo-lambda \
  --capabilities CAPABILITY_IAM

sam local invoke OpenHelloWorldFunction
