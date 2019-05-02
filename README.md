# Demos for AWS workloads

This repository will provide some demo examples from my daily AWS workloads. It will probably grow day by day. So far, the most examples are written in Python. Therefore, feel free to participate!

## Big Data workloads

* Lambda does not fit? The [SQS example](SQS/README.MD) will show you how to unzip large gzip files via S3 events and EC2.
* Do you want to use Zeppelin on AWS EMR without hard coded credentials? Look up this [example](EMR/README.MD).

## Cloudformation templates

* If your interested in various examples of [CloudFormation](https://github.com/Zirkonium88/aws-cf-templates), look here. It's a repo of one of my colleagues.

## Hosting Docker on AWS

* Do you want to host a Docker container as Apache webserver? The [Docker example](Docker/README.MD) will show you how.

## Deploying an AWS Lambda on AWS via Serverless

* You do not how a deployment to AWS Lambda could work? The example on [Serverless](https://github.com/Zirkonium88/AWS/tree/master/Lambda/ServerlessDemo/README.MD) will show how.
* Do you need a example for simple Lambda processing pipeline? In the tutorial for connecting [Amazon S3 and DynamoDB via AWS Lambda](https://github.com/Zirkonium88/AWS/tree/master/Lambda/GetImagenames/README.MD), you will get your example.

## Deploying my HUGO webpage

* You want to know how to set up a HUGO webpage within a CICD pipeline? Look at this [example](BuildHUGO/README.MD).
* Do you need a Lambda which loads data from a CSV into DynamoDB? Go [forward!](Lambda/LoadData/README.MD)
* After we have loaded our data into a DynamoDB table, we maybe want to call it from a static website. This [example](https://github.com/Zirkonium88/AWS/blob/master/BuildHUGO/CallDynamo.MD) shows how to use the Javascript SDK to do so.

## Machine and DeepLearning on AWS

* Do you want to know how to use a the AWS out-of-the-box convolutional neural network ([CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network))? Try it out with this [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/DetectFaces).
* Do you want to know how Amazon Rekognition and Polly can interact with each other? Try it out with this [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/CompareFaces).
* Got a text-to-speech problem? Look here for an [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/TransScribeMP3) with some additionall exeperinces.
* Are you a data scientist and you love using cheat sheets?. I found this nice repo and [forked](https://github.com/Zirkonium88/Data-Science--Cheat-Sheet). It contains alot of different pdf's.

## Talks on AWS within our AWS UserGroup

* Do you want to know how to make AWS AI/ML services available on IoT? Within our [AWS UserGroup in Hannover](https://www.meetup.com/de-DE/AWS-Usergroup-Hannover/) we talked about [that](https://github.com/Zirkonium88/AWS/tree/master/Presentations/20190319_UserGroup_AI_on_IoT.pdf). 