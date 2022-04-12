#!/bin/bash
sudo yum update
sudo yum install ruby
sudo yum install wget

CODEDEPLOY_BIN="/opt/codedeploy-agent/bin/codedeploy-agent"
$CODEDEPLOY_BIN stop



yum erase codedeploy-agent -y

cd /home/ec2-user

wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install

chmod + x ./install
sudo ./install auto