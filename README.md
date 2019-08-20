# Demos for AWS workloads

This repository will provide some examples from my daily AWS workloads. It will probably grow day by day. So far, the most examples are written in Python. Therefore, feel free to participate!

## Big Data workloads

* Lambda does not fit your workload? The [SQS example](SQS/README.MD) will show you how to unzip large gzip files via S3 events and EC2.
* Do you want to use Zeppelin on [AWS EMR](https://aws.amazon.com/emr/?nc1=h_ls) without hard coded credentials? Look up this [example](EMR/README.MD).

## AWS IoT

* This [AWS IoT example](https://github.com/Zirkonium88/AWS/tree/master/IoT) shows how to publish random data to an AWS IoT topic. The example can be extended to recieve data as well. The script can run on an Raspberry Pi but also on your local machine.

## Cloudformation templates

* If your interested in various examples of CloudFormation, look [here](https://github.com/Zirkonium88/aws-cf-templates). It's a repo of one of my colleagues.
* A small Demo on how to use Parameters and Troposphere in and for Cloudformation can be found [here](https://github.com/Zirkonium88/AWS/tree/master/CloudFormation/README.MD).

## Docker on AWS

* Do you want to host a Docker container as Apache webserver? This [Docker example](Docker/DockerStaticWebsite/README.MD) will show you how.
* Do you want a CICD for a the previous (or any other) Docker workload? Look out [here!](Docker/DockerCICD/README.MD)
* Docker batch workloads? Look [here!](https://github.com/Zirkonium88/AWS/blob/master/Docker/README.MD)

## Deploying an AWS Lambda on AWS via Serverless

* You do not how a deployment to AWS Lambda could work? The example on [Serverless](https://github.com/Zirkonium88/AWS/tree/master/Lambda/ServerlessDemo/README.MD) will show you how.
* Do you need a example for a simple Lambda processing pipeline? In this tutorial for connecting [Amazon S3 and DynamoDB via AWS Lambda](https://github.com/Zirkonium88/AWS/tree/master/Lambda/GetImagenames/README.MD), you will get your example.
* How to prevent unintentional deletion of buckets and their contents? This example shows it with [Lambda and the setting of Bucketpolicies](https://github.com/Zirkonium88/AWS/tree/master/Lambda/BucketPolicy/README.MD).
* Do you want to automize your IAM processes? Have a look [here!](https://github.com/Zirkonium88/AWS/blob/master/Lambda/AddUser/README.MD)
* Do you want to dump Data from  

## Deploying my HUGO webpage

* You want to know how to set up a HUGO webpage within a CICD pipeline? Look at this [example](BuildHUGO/README.MD).
* Do you need a Lambda which loads data from a CSV into DynamoDB? Go [forward!](Lambda/LoadData/README.MD)
* After we have loaded our data into a DynamoDB table, we maybe want to call it from our static website. This [example](https://github.com/Zirkonium88/AWS/blob/master/BuildHUGO/CallDynamo.MD) shows how to use the AWS Javascript SDK to do so.

## Machine and DeepLearning on AWS

* Do you want to know how to use a the AWS out-of-the-box convolutional neural network ([CNN](https://en.wikipedia.org/wiki/Convolutional_neural_network))? Try it out with this [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/DetectFaces).
* Do you want to know how Amazon Rekognition and Polly can interact with each other? Look up this [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/CompareFaces).
* Got a text-to-speech problem? Look here for an [example](https://github.com/Zirkonium88/AWS/tree/master/Lambda/TransScribeMP3). The example describes experiences as well.
* You are a data scientist and you love to use cheat sheets? I found this nice repo and [forked](https://github.com/Zirkonium88/Data-Science--Cheat-Sheet) it. It contains a lot of different pdf's.

## Talks on AWS within our AWS UserGroup

* Do you want to know how to make AWS AI/ML services available on IoT? Within our [AWS UserGroup in Hannover](https://www.meetup.com/de-DE/AWS-Usergroup-Hannover/) we talked about [that](https://github.com/Zirkonium88/AWS/tree/master/Presentations/20190319_UserGroup_AI_on_IoT.pdf).