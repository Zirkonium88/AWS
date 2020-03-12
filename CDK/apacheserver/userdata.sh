#!/bin/bash
sudo yum update -y
sudo yum -y install httpd php
sudo chkconfig httpd on
sudo service httpd start
aws s3 cp s3://my-deployment-bucket-20201203/index.html /var/www/index.html