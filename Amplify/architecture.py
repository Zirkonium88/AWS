from diagrams import Cluster,Diagram
from diagrams.custom import Custom
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.network import APIGateway as API
from diagrams.aws.network import Cloudfront as CF
from diagrams.aws.network import Route53 as R53
from diagrams.aws.integration import Appsync
from diagrams.aws.database import Dynamodb

with Diagram("React App", show=False, direction="LR"):

    user = Custom("App User", "./img/users.png")

    with Cluster("Frontend: DNS & SSL"):
        dns = R53("api.example.com")
        cf = CF("CF Distribution")

    with Cluster("Frontend: App & Auth."):
        bucket = S3("Bucket")
        cognito = Cognito("User Pool")
    
    with Cluster("Backend: API & DB"):
        app = Appsync("GraphQL")
        dynamodb = Dynamodb("NoSQL DB")     

    user - dns >> cf >> bucket >> cf >> dns
    bucket >> cognito >> bucket
    bucket >> app >> bucket
    app >> dynamodb >> app
