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
