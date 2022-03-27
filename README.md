# GoldWatch
# by Obijah(ohbster@protonmail.com)

This is my first serverless application. It's purpose is to monitor the current price of gold,keep track of the daily high and low prices, and send alerts if price reaches above or below a certain amount

*Update this readme to include list of files and there purpose*

*Notes*
- The purprose of this app is primarily a learning exercise. I should be pretty useful during in the meantime with current market volitilty

- The RDS DBInstance will default to whatever the vpc is the default on the aws account. This is only done
to avoid incurring charges by using a subnetgroup and multi-az instances running as free tier only allow a single-az instance and I am unaware of any way to deploy the instance to another VPC without subnetgroup. If you know of one, do email me as I am still learning AWS deployment. ohbster@protonmail.com


- Currently broken so wait before deploying
To deploy, clone this repo and do:
./install.sh

or optionally

sam build
sam depoy --guided

