# GoldWatch
# by Obijah(ohbster@protonmail.com)

This is my first SAM / CloudFormation application. Its primary purpose is a learning exercise to help learn the process of deploying on AWS with cloudformation. It's secondary purpose is to monitor the current price of gold, keep track of the daily high and low prices, and send alerts if price reaches above or below a certain threshold

*Update this readme to include list of files and there purpose*

*Notes*
- The purprose of this app is primarily a learning exercise. I should be pretty useful during in the meantime with current market volitilty

- The RDS DBInstance will default to whatever the vpc is the default on the aws account. This is only done
to avoid incurring charges by using a subnetgroup and multi-az instances running as free tier only allow a single-az instance and I am unaware of any way to deploy the instance to another VPC without subnetgroup. If you know of one, do email me as I am still learning AWS deployment. ohbster@protonmail.com

- Currently broken so wait before deploying
To deploy, clone this repo and do:

./install.sh for each stack. The install will be much cleaner in time. Now it is messy.

or optionally

sam build
sam depoy --guided

*Purpose*
This is my first project using AWS. On the surface, it displays daily spot prices for an ounce of Gold in USD. Underneath, it was meant to develop my understanding of many services including:
- Creating CloudFormation /SAM stacks (created in yaml and deployed from AWS CLI using simple bash scripts)
- ![diagram here](/GoldWatch%20VPC.jpg "VPN Diagram")
- VPC  
- EC2 instances in multiple availability zones behind an application load balancer
- Apache webserver's with PHP running on Amazon Linux
- Lambda functions written in python and triggered via an EventBridge rule
- Parameter store with secret strings for storing database connection info
- RDS MySQL instance
- Route 53 managed domain pointing to ALB
- ACM public SSL certificate
- CodeBuild, CodeDeploy and CodePipeline using GitHub for automated deployment

This is an on going hobby project. Next plans are to integrate SES and contact lists to allow automated email alerts when price reaches set targets, and to display charts using historical data from the database.
I am very open to hearing any critique / suggestions that can help me to improve.
Obijah
ohbster@protonmail.com

Repositories:
https://github.com/ohbster/GoldWatch
https://github.com/ohbster/GoldWatch_WWW


*Services / Resources Used by GoldWatch*
- CloudFormation
- CodeBuild / CodeDeploy / CodePipeline
- GitHub
- SAM
- CodeDeploy
- EC2
- S3
- RDS
- SSM
- Lambda
- Route53
- ACM
- SES
- EventBridge

*Languages Used*
- Python
- PHP
- HTML
- Bash Scripting

*TODO*
- Allow people to create and receive price alerts by email
- Create function to mail contacts when a price exeeds a target limit
- Complete CodeBuild stack
- Complete CodeDeploy stack
- Complete CodePipeline stack
- Clean up install


*Sources*
Tutorials that helped me learn CloudFormation and extremely helpful in helping me create this app.
AOS Notes https://www.youtube.com/channel/UCxm6ZcNMXMrckKRJPXlDu_w
