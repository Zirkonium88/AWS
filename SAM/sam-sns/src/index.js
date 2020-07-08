// const axios = require('axios')
// const url = 'http://checkip.amazonaws.com/';

const aws = require('aws-sdk');
let response;
const sns = new aws.SNS()

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */
exports.lambdaHandler = async (event, context) => {
    try {
        // const ret = await axios(url);
        response = {
            'statusCode': 200,
            'body': JSON.stringify({
                message: 'Send SNS Notification ...',
            })
        }
        const params = {
          Message: 'Hello World!',
          Subject: 'SNS Notification from Lambda',
          TopicArn: process.env.SNS_TOPIC_ARN
        };
        console.log(params);
        await sns.publish(params).promise()
    } catch (err) {
        console.log(err);
        return err;
    }
    return response
};
