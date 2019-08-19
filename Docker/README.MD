# Docker on AWS

The following two exmaples show how to integrate in a dockerized way with AWS.

## Use Docker for a static website

This [example](Docker/DockerStaticWebsite/README.MD) shows you how to launch a dockerized static website on AWS Fargate. Using Fragate enables you to use EC2 instances without manageing them in a cluster. Going further, the application loadbablancer enbales you to use path based routing to spin up seperated and specific containers as microservices in a decoupled architecture.

## Docker within a CICD pipeline

CICD with Docker come sp with a lot of advantages. One very important: `docker build`runs within AWS. This [example](Docker/DockerCICD/README.MD) shows you how to launch and use this static website Docker image within a CICD pipeline.

## Docker with AWS Batch

If you want to run high resource intensive jobs on AWS with Docker, AWS Batch is the way to go. This [example](Docker/BatchWorkloads/README.MD) shows how to estimate pi 10k times. I wrote an detailed article, which can be found [here](https://aws-blog.de/2019/06/sound-of-silence-lift-your-heavy-workloads-to-aws-batch-with-docker.html).