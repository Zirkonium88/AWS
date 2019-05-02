# Create and deploy a HUGO webpage in a CIDCD manner

 So far, I used pretty ugly tools to deploy my webpages. Now, a [HUGO](https://gohugo.io) webpage came up in a workshop. This is pretty straight forward. You can locally develop you webpage by using a lot of differents themes ([look up here](https://gohugo.io/getting-started/quick-start/)). Aftwards you can push the compiled result to somewhere. For my [web page](trctrainings.com), I'm using the the [Hermit theme](https://themes.gohugo.io/hermit/).

## Presequities

I like automation. I just want to push a markdown-file to a repository. Fire and forget. To do this within AWS, you need the following services.

* Amazon S3
* Amazon CodeCommit 
* Amazon CodePipeline

If you want to have your own URL, you need the folliwng services as well.

* Route53
* CloudFront
* AWS Lambda

## Setting up a CICD pipeline

### Deploying a Hugo website to AWS in 6 steps (CDN+HTTPS)

Don't write things twice. I just followed this [tutorial](https://simpleit.rocks/golang/hugo/deploying-a-hugo-website-to-aws-the-right-way/). Two things I need to mention. First, do not skip the Lambda@Edge step. Otherweise, your webpage will not work! Second, set `draft: false` within your markdown header section. Otherwise the content will not be publsihed.

```

---
title: "EXAMPLE"
date: 2019-04-28T21:48:38+02:00
draft: false
---

```

### Getting the CICD pipeline

I just want to use `git add .`, `git commit -m 'Fancy new cotent` and `git push` for my deployment. For a more detailed tutorial, look up [here](https://digilution.io/posts/ci-cd-pipeline-for-hugo/). The build process of my HUGO webpage shall be done with a pipeline.

* Create a CodeCommit [repository](https://docs.aws.amazon.com/codecommit/latest/userguide/how-to-create-repository.html) and push your HUGO website.
* Next, we need a [Build Project](https://docs.aws.amazon.com/codebuild/latest/userguide/create-project.html).
* Finally, we need a [CodePipeline](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html).

Two important things to mention. First, I used my own `buildspec.yml`. 

````yml

version: 0.2

env:
  variables:
    s3_output: "exmaple.com"
    s3_output_redirect: "www.exmaple.com"
    hugo_version: "0.55.4"
    CLOUDFRONT_ID_A: "FIRST_ID"
    CLOUDFRONT_ID_B: "SECOND_ID"

phases:
  install:
    commands:
      - wget "https://github.com/gohugoio/hugo/releases/download/v${hugo_version}/hugo_${hugo_version}_Linux-64bit.deb"
      - sudo dpkg -i hugo_${hugo_version}_Linux-64bit.deb
    finally:
      - hugo version
  build:
    commands:
      - hugo
      - cd public && aws s3 sync . s3://${s3_output} && aws s3 sync . s3://${s3_output_redirect}
    finally:
      - echo "Script finished running"
  post_build:
    commands:
      - aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_ID_A} --paths "/*"
      - aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_ID_B} --paths "/*"
    finally:
      - echo "CloudFront invalidation successfull"

````
Why? After deploying the HUGO webpage, you need to invalidated every object within your CloudFront distribution. Second, I want to use `www.exmaple.com` and `exmaple.com`. Thats why I need a second `aws sync`. Additionally, you need to edit the execution and it's policy with the permission for CloudFront and S3 for both buckets.

### Delivering the HUGO wegpage with our pipeline

Using the [Hermit theme](https://themes.gohugo.io/hermit/), every post needs to be placed in `content/posts/` and every additional webpage needs to be in `content/`. After finishing my content, `git add .`, `git commit -m 'Fancy new cotent` and `git push` will do the rest. Cheers!

### Speeding things up

If you think this is not fast enough, you can use S3 for `Build Project` as well. In doing so, you can skip the git process.