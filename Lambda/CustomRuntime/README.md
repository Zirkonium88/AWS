https://docs.aws.amazon.com/lambda/latest/dg/runtimes-walkthrough.html

aws iam create-role --role-name CustomRuntimeRole --assume-role-policy-document file://trust-pol.json

aws iam attach-role-policy --role-name CustomRuntimeRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

http://www.milanor.net/blog/bashr-howto-pass-parameters-from-bash-script-to-r/

aws lambda create-function --function-name R-runtime \
--zip-file fileb://function.zip --handler function.handler --runtime provided \
--role arn:aws:iam::037732949416:role/CustomRuntimeRole

aws lambda invoke --function-name R-runtime --payload '{"text":"Hello"}' response.json

wget https://cran.rstudio.com/src/base/R-3/R-3.4.1.tar.gz
tar xvf R-3.4.1.tar.gz
cd R-3.4.1
./configure --prefix=$HOME/R
make && make install

https://cran.r-project.org/bin/macosx/tools/