# Docker demo: Static web page with AWS ECS

This demos shows how to build a [Docker container](https://www.docker.com/resources/what-container) serving as a webserver. The webserver hosts a [static webpage](index.html). Afterwards, we will push the Docker container to AWS. Finally, the Docker container used to launch an [Amazon ECS cluster](https://aws.amazon.com/ecs/?nc1=h_ls). But we can used [Amazon SQS](https://aws.amazon.com/sqs/?nc1=h_ls) and [Amazon EC2](https://aws.amazon.com/ec2/?nc1=h_ls) to create a pipline. 

1. First, [(install and) activate Docker](https://runnable.com/docker/getting-started/).

2. Generate the `Dockerfile`.

    ```bash
    touch Dockerfile
    ```

    Edit the file, e.g. with `nano Dockerfile`. An example can be found [here](https://github.com/Zirkonium88/AWS/blob/master/Docker/Dockerfile).

3. Build and tag the Docker container: 

    ```bash 
    docker build -t hello-world .
    ```

4. Test your container on localhost: 

    ```bash 
    docker run -p 80:80 hello-world
    ```

5. Stop your running container:
    * `docker ps` to retrieve the contaibner-ID 
    * `docker stop container-ID`

6. Create a AWS ECR repository via the [CLI](https://aws.amazon.com/cli/?nc1=h_ls): 

    ```bash
    aws ecr create-repository --repository-name hello-repository  --region eu-west-1
    ``` 
    Change `repository-name` and `region` accordingly.

7. Copy `uri` to your clipboard.

8. Tag the Docker container for your respository: 
    ``` bash
    docker tag hello-world XXX.dkr.ecr.eu-west-1.amazonaws.com/hello-repository # XXX = your account-ID
    ``` 
    Change the `uri` accordingly.

9. Get temporary credentials for your repository via the CLI: 
    ```bash 
    aws ecr get-login --no-include-email --region eu-west-1
    ``` 
    Copy the output to your clipboard.

10. Push the Docker container to your repository:
    ```bash
    docker push XXX.dkr.ecr.eu-west-1.amazonaws.com/hello-repository # XXX = your account-ID
    ```
11. Go the ECS service. Click on `Get started` and choose `Costum container`. Set the port settings to 80.

12. After ECS deployed your application, get the `DNS-Name` of the deployed `ELB` (e.g. **EC2 console**). Paste it in to your browser tab.